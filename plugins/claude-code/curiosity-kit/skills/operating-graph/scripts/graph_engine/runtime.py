"""One controller-owned runtime for Operating Graph record protocol 2.

The original graph schema, invariants and rewrite compiler remain the declarative
engine. This module joins their execution boundaries under one trusted loader and
operation-specific guard. A controller adapter is trusted code, not authentication.
CLI-imported observations remain declared/simulated evidence, never native proof.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional
import uuid

from .models import Graph, RewriteProposal
from .validation import require_valid_graph, parse_and_validate_rewritten_graph
from .rewrites import apply_operations, classify_risk, compile_pattern
from .storage import (Store, RuntimeErrorBase, CorruptionError, ApprovalError,
                      canonical, digest, byte_digest, identifier, safe_path,
                      safe_root, now, fault)

LIVE = {"prepared", "launch-unknown", "running", "cancel-requested", "effect-outcome-unknown"}
TERMINAL = {"completed", "cancelled", "failed", "exhausted"}
TOOLS = {"subagent": "host.fresh_worker", "inline": "controller.inline",
         "human": "controller.human", "tool": "controller.tool"}


def timestamp(value):
    if not isinstance(value, str) or not value.endswith("Z"):
        raise RuntimeErrorBase("deadline must be a canonical UTC timestamp")
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise RuntimeErrorBase("invalid UTC timestamp") from exc


def require_object(value, label):
    if not isinstance(value, dict):
        raise RuntimeErrorBase(label + " must be an object")
    canonical(value)
    return value


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise RuntimeErrorBase(label + " must be a nonempty string")
    return value


def node_contract(graph, node_id):
    node = next(n for n in graph["nodes"] if n["id"] == node_id)
    semantic = {k:v for k,v in node.items() if k not in {"priority", "label"}}
    edges = [e for e in graph["edges"] if e["target"] == node_id and e["enabled"]]
    return digest({"node": semantic, "incomingEdges": sorted(edges, key=lambda e:e["id"])})


class Runtime:
    """Supported public API. All mutations reload, lock, validate, and commit.

    Optional adapter.verify_observation(kind, record) must inspect the actual
    authenticated host channel and return True. A callback's presence alone is
    not evidence. No API calls a network tool, spawns a model, or approves policy.
    Controller-mediated dispatch must call begin_launch immediately before the
    actual tool, then record_launch with the actual response. On missing response,
    preserve unknown state and reconcile, never blindly relaunch.
    """
    def __init__(self, run_directory, *, adapter=None):
        self.store = Store(Path(run_directory))
        self.root = self.store.root
        self.adapter = adapter

    @classmethod
    def create(cls, graph, run_root, *, contract=None, operation_id="initialize", adapter=None):
        graph = require_valid_graph(graph.to_dict() if isinstance(graph, Graph) else graph).to_dict()
        identifier(graph["graphId"], "graphId")
        for node in graph["nodes"]:
            identifier(node["id"], "nodeId")
        for edge in graph["edges"]:
            identifier(edge["id"], "edgeId")
        config = deepcopy(contract or {})
        allowed = {"deadline", "approvalBindings", "seeds", "criteria", "optionalNodeIds", "evidenceTier", "maxLaunchAttempts"}
        if set(config) - allowed:
            raise RuntimeErrorBase("unknown runtime contract fields: " + ", ".join(sorted(set(config)-allowed)))
        config.setdefault("deadline", (datetime.now(timezone.utc)+timedelta(hours=24)).isoformat().replace("+00:00", "Z"))
        timestamp(config["deadline"])
        if timestamp(config["deadline"]) <= datetime.now(timezone.utc):
            raise RuntimeErrorBase("deadline already elapsed")
        config.setdefault("approvalBindings", {})
        config.setdefault("seeds", [])
        config.setdefault("criteria", [])
        config.setdefault("optionalNodeIds", [])
        config.setdefault("evidenceTier", "simulated")
        config.setdefault("maxLaunchAttempts", graph["limits"]["maxNodeRuns"])
        if config["evidenceTier"] not in {"simulated", "controller-declared", "controller-observed"}:
            raise RuntimeErrorBase("evidenceTier must be simulated, controller-declared or controller-observed")
        if not isinstance(config["maxLaunchAttempts"], int) or isinstance(config["maxLaunchAttempts"], bool) or config["maxLaunchAttempts"] < 1:
            raise RuntimeErrorBase("maxLaunchAttempts must be positive")
        nodes = {n["id"]:n for n in graph["nodes"]}
        if not isinstance(config["optionalNodeIds"], list) or len(set(config["optionalNodeIds"])) != len(config["optionalNodeIds"]):
            raise RuntimeErrorBase("optionalNodeIds must be unique")
        for key in config["optionalNodeIds"]:
            if key not in nodes or nodes[key]["critical"]:
                raise RuntimeErrorBase("optional node must exist and be noncritical")
            if any(e["enabled"] and e["required"] and e["source"] == key and e["target"] not in config["optionalNodeIds"] for e in graph["edges"]):
                raise RuntimeErrorBase("optional node feeds required work")
        seen = set()
        for item in config["criteria"]:
            require_object(item, "criterion binding")
            if set(item) != {"criterion", "deliverableId", "evaluatorNodeId"}:
                raise RuntimeErrorBase("criterion binding requires criterion, deliverableId, evaluatorNodeId")
            if item["criterion"] not in graph["goal"]["completionCriteria"] or item["criterion"] in seen:
                raise RuntimeErrorBase("criterion binding is unknown or duplicate")
            if item["deliverableId"] not in {d["id"] for d in graph["goal"]["deliverables"]}:
                raise RuntimeErrorBase("criterion binding names unknown deliverable")
            if item["evaluatorNodeId"] not in nodes or nodes[item["evaluatorNodeId"]]["kind"] != "evaluator":
                raise RuntimeErrorBase("criterion binding requires an evaluator node")
            seen.add(item["criterion"])
        require_object(config["approvalBindings"], "approvalBindings")
        valid_gates = {e["id"] for e in graph["edges"] if e["kind"] == "approve"}
        valid_gates.update(a for e in graph["edges"] for a in e["activation"]["approvals"])
        for gate, binding in config["approvalBindings"].items():
            identifier(gate, "approval gate")
            if gate not in valid_gates or set(binding) != {"subjectType", "subjectId", "scope"}:
                raise RuntimeErrorBase("invalid approval binding")
            if binding["subjectType"] not in {"external-action", "artifact", "resume"}:
                raise RuntimeErrorBase("invalid approval subject type")
            nonempty(binding["subjectId"], "subjectId")
            require_object(binding["scope"], "approval scope")
        root = safe_root(Path(run_root)) / ("run-" + graph["graphId"])
        if root.exists():
            raise RuntimeErrorBase("run directory already exists")
        rt = cls(root, adapter=adapter)
        data = {"recordVersion": 2, "runId": "run-"+graph["graphId"]+"-"+uuid.uuid4().hex, "generation": 0,
                "graphId": graph["graphId"], "graphVersion": 1, "epoch": 1, "status": "running",
                "graph": graph, "versions": {"1": graph}, "contract": config,
                "nodes": {n["id"]:{"status":"pending", "currentInvocation":None,
                          "completedEpoch":None, "attempts":0} for n in graph["nodes"]},
                "invocations": {}, "artifacts": {}, "approvals": [], "proposals": {},
                "rewrites": [], "carryForwards": [], "epochs": [], "signals": [],
                "objects": [], "launchAttempts":0, "totalNodeRuns":0,
                "autoRewritesApplied":0, "rewritePending":False, "verification":None}
        seeds = []
        for i, seed in enumerate(config["seeds"]):
            require_object(seed, "seed")
            if set(seed) != {"edgeId", "artifactType", "path", "sha256"}:
                raise RuntimeErrorBase("seed requires edgeId, artifactType, path, sha256")
            edge = next((e for e in graph["edges"] if e["id"] == seed["edgeId"]), None)
            if not edge or edge["temporal"] != "next_epoch" or seed["artifactType"] not in edge["artifactTypes"]:
                raise RuntimeErrorBase("seed must bind an exact next-epoch edge and declared type")
            source = safe_root(Path(seed["path"]))
            if not source.is_file():
                raise RuntimeErrorBase("seed file missing")
            content = source.read_bytes()
            if byte_digest(content) != seed["sha256"]:
                raise RuntimeErrorBase("seed file/digest mismatch")
            seeds.append((seed, content))
        with rt.store.lock(create=True):
            for index, (seed, content) in enumerate(seeds, 1):
                sha = rt.store.stage_object(content)
                data["objects"].append(sha)
                art_id = "seed-" + str(index)
                data["artifacts"][art_id] = {"artifactId":art_id, "type":seed["artifactType"],
                    "nodeId":"seed", "invocationId":None, "epoch":0, "graphVersion":1,
                    "sha256":sha, "path":"objects/"+sha, "sourcePath":None,
                    "inputs":[], "active":True, "eligibleVersions":[1], "seedForEdge":seed["edgeId"]}
            data["objects"] = sorted(set(data["objects"]))
            result = {"runId":data["runId"], "runDirectory":str(root), "recordVersion":2, "state":data}
            rt.store.commit(data, [], operation_id, "init", {"graph":graph,"contract":config}, result)
        return rt

    def _validate(self, data, *, verify_files=True):
        if data["recordVersion"] != 2:
            raise CorruptionError("unsupported runtime record version")
        if data["graph"] != data["versions"][str(data["graphVersion"])]:
            raise CorruptionError("graph version binding mismatch")
        original = Graph.from_dict(data["versions"]["1"])
        valid = parse_and_validate_rewritten_graph(data["graph"], original_graph=original)
        if valid.violations:
            raise CorruptionError("committed graph invalid: " + "; ".join(str(v) for v in valid.violations))
        agents = set()
        for key, inv in data["invocations"].items():
            if inv["invocationId"] != key or inv["taskPacketSha256"] != digest(inv["task"]):
                raise CorruptionError("invocation/task binding mismatch")
            task = inv["task"]
            historical = data["versions"].get(str(task["graphVersion"]))
            if not historical or task["runId"] != data["runId"] or task["contractSha256"] != node_contract(historical, inv["nodeId"]):
                raise CorruptionError("historical task contract mismatch")
            if inv["dispatchReceipt"]["taskPacketSha256"] != inv["taskPacketSha256"]:
                raise CorruptionError("dispatch receipt mismatch")
            if inv.get("launch"):
                if inv["launchReceipt"]["launchSha256"] != digest(inv["launch"]):
                    raise CorruptionError("launch receipt mismatch")
                agent = inv["launch"]["response"].get("agentId")
                if agent and inv["launch"]["response"]["outcome"] == "launched":
                    if agent in agents:
                        raise CorruptionError("worker identity reused across invocation history")
                    agents.add(agent)
            if inv.get("returned"):
                rr = inv["returned"]
                if rr["returnSha256"] != digest(rr["packet"]) or rr["packet"]["taskPacketSha256"] != inv["taskPacketSha256"]:
                    raise CorruptionError("return receipt mismatch")
                for item in rr["packet"]["evidence"] if verify_files else []:
                    path = self._owned_file(inv,item["path"])
                    if byte_digest(path.read_bytes()) != item["sha256"]:
                        raise CorruptionError("historical return evidence changed")
                if verify_files and rr.get("sourceReturnPath"):
                    import json
                    path = safe_path(self.root,rr["sourceReturnPath"])
                    if not path.is_file():
                        raise CorruptionError("historical return packet missing")
                    try:
                        if json.loads(path.read_text(encoding="utf-8")) != rr["packet"]:
                            raise CorruptionError("historical return packet changed")
                    except ValueError as exc:
                        raise CorruptionError("historical return packet invalid") from exc
            for binding in task["requiredInputs"]:
                art = data["artifacts"].get(binding["artifactId"])
                if not art or any(binding.get(k) != art.get(k) for k in ("sha256", "nodeId", "invocationId", "epoch")):
                    raise CorruptionError("input lineage mismatch")
        return data

    def load(self):
        with self.store.lock():
            data, _ = self.store.load()
            return self._validate(data)

    def _mutation(self, operation, intent, apply, *, operation_id=None, expected_generation=None, allow_terminal=False):
        operation_id = operation_id or "op-" + uuid.uuid4().hex
        identifier(operation_id, "operationId")
        with self.store.lock():
            accounting = operation in {"cancel-run","cancel-node","settle","record-launch","ingest-return"} or (operation == "record-approval" and intent.get("decision") in {"denied","revoked"})
            data, records = self.store.load(check_objects=not accounting)
            self._validate(data,verify_files=not accounting)
            for record in records:
                if record["operationId"] == operation_id:
                    if record["operation"] != operation or record["intentSha256"] != digest(intent):
                        raise RuntimeErrorBase("operation ID reused with changed intent")
                    return deepcopy(record["result"])
            if expected_generation is not None and expected_generation != data["generation"]:
                raise RuntimeErrorBase("expected generation mismatch")
            if data["status"] in TERMINAL and not allow_terminal:
                raise RuntimeErrorBase("terminal run forbids activation or new work")
            result = apply(data)
            data["objects"] = sorted(set(data["objects"]))
            fault("after-stage")
            return self.store.commit(data, records, operation_id, operation, intent, result)

    def _node(self, data, node_id):
        result = next((n for n in data["graph"]["nodes"] if n["id"] == node_id), None)
        if result is None:
            raise RuntimeErrorBase("unknown node: " + str(node_id))
        return result

    def _check_deadline(self, data):
        if timestamp(data["contract"]["deadline"]) <= datetime.now(timezone.utc):
            raise RuntimeErrorBase("absolute run deadline exhausted")

    def _active(self, data, *, producer=None, epoch=None, artifact_type=None, seed_edge=None):
        selected = []
        for art in data["artifacts"].values():
            if not art["active"] or data["graphVersion"] not in art["eligibleVersions"]:
                continue
            if producer is not None and art["nodeId"] != producer:
                continue
            if epoch is not None and art["epoch"] != epoch:
                continue
            if artifact_type is not None and art["type"] != artifact_type:
                continue
            if seed_edge is not None and art.get("seedForEdge") != seed_edge:
                continue
            if art["invocationId"]:
                inv = data["invocations"][art["invocationId"]]
                if inv["status"] != "succeeded":
                    continue
            self._verify_artifact(art)
            selected.append(art)
        return sorted(selected, key=lambda a:a["artifactId"])

    def _verify_artifact(self, art):
        path = safe_path(self.root, art["path"])
        if not path.is_file() or byte_digest(path.read_bytes()) != art["sha256"]:
            raise CorruptionError("artifact content missing or changed: " + art["artifactId"])
        if art.get("sourcePath"):
            source = safe_path(self.root, art["sourcePath"])
            if not source.is_file() or byte_digest(source.read_bytes()) != art["sha256"]:
                raise CorruptionError("artifact source changed: " + art["artifactId"])

    def _inputs(self, data, node):
        inputs = {}
        problems = []
        incoming = [e for e in data["graph"]["edges"] if e["enabled"] and e["target"] == node["id"]]
        for edge in incoming:
            if edge["kind"] == "approve":
                continue
            previous = edge["temporal"] == "next_epoch"
            epoch = data["epoch"] - int(previous)
            seed = previous and data["epoch"] == 1
            get = lambda typ: self._active(data, producer=None if seed else edge["source"], epoch=epoch,
                                            artifact_type=typ, seed_edge=edge["id"] if seed else None)
            types = sorted(set(edge["artifactTypes"] + edge["activation"]["artifacts"]))
            matches = {typ:get(typ) for typ in types}
            if edge["required"] and any(not matches[t] for t in edge["artifactTypes"]):
                problems.append("missing exact edge artifacts: " + edge["id"])
            for artifacts in matches.values():
                for artifact in artifacts:
                    inputs[artifact["artifactId"]] = deepcopy(artifact)
            source = data["nodes"].get(edge["source"], {})
            source_ok = (source.get("status") == "succeeded" and source.get("completedEpoch") == epoch)
            if previous and not seed:
                source_ok = any(inv["nodeId"] == edge["source"] and inv["epoch"] == epoch and inv["status"] == "succeeded" for inv in data["invocations"].values())
            if seed:
                source_ok = bool(types) and all(matches.values())
            conditions = []
            for state_req in edge["activation"]["nodeStates"]:
                st = data["nodes"].get(state_req["nodeId"], {})
                if previous and state_req["status"] == "succeeded":
                    matched = source_ok if state_req["nodeId"] == edge["source"] else any(i["nodeId"] == state_req["nodeId"] and i["epoch"] == epoch and i["status"] == "succeeded" for i in data["invocations"].values())
                else:
                    matched = st.get("status") == state_req["status"] and (state_req["status"] != "succeeded" or st.get("completedEpoch") == epoch)
                conditions.append(matched)
            conditions.extend(bool(matches[t]) for t in edge["activation"]["artifacts"])
            satisfied = (any(conditions) if edge["activation"]["mode"] == "any" else all(conditions)) if conditions else source_ok
            if edge["required"] and not satisfied:
                problems.append("dependency not satisfied: " + edge["id"])
        for requirement in node["inputs"]:
            if requirement["required"] and not any(a["type"] == requirement["artifactType"] for a in inputs.values()):
                problems.append("missing routed required input: " + requirement["artifactType"])
        return sorted(inputs.values(), key=lambda a:a["artifactId"]), problems

    def _approval_scopes(self, data, node, inputs):
        gates = set()
        for edge in data["graph"]["edges"]:
            if edge["enabled"] and edge["required"] and edge["target"] == node["id"]:
                if edge["kind"] == "approve":
                    gates.add(edge["id"])
                gates.update(edge["activation"]["approvals"])
        result = {}
        for gate in sorted(gates):
            binding = data["contract"]["approvalBindings"].get(gate)
            if not binding:
                result[gate] = None
                continue
            result[gate] = {"runId":data["runId"], "subjectType":binding["subjectType"],
                           "subjectId":binding["subjectId"], "authority":data["graph"]["goal"]["authorityNodeId"],
                           "scope":{"nodeId":node["id"], "epoch":data["epoch"],
                                    "contractSha256":node_contract(data["graph"], node["id"]),
                                    "inputs":[{"artifactId":a["artifactId"],"sha256":a["sha256"]} for a in inputs],
                                    "action":deepcopy(binding["scope"])}}
        return result

    def _approved(self, data, binding):
        if binding is None:
            return False
        # Scope forms the approval identity, not approvalId or a bare subject string.
        matching = [a for a in data["approvals"] if all(a.get(k) == binding.get(k) for k in ("runId", "subjectType", "subjectId", "authority", "scope"))]
        return bool(matching and matching[-1]["decision"] == "granted")

    def _eligibility(self, data, node, *, invocation=None):
        problems = []
        if data["status"] != "running":
            problems.append("run is not running")
        if not node["enabled"]:
            problems.append("node disabled")
        if data["rewritePending"] and invocation is None:
            problems.append("rewrite boundary draining")
        if timestamp(data["contract"]["deadline"]) <= datetime.now(timezone.utc):
            problems.append("absolute run deadline exhausted")
        if invocation is None and data["nodes"][node["id"]]["status"] not in {"pending", "failed", "blocked"}:
            problems.append("node is not eligible for a fresh invocation")
        inputs, input_problems = self._inputs(data, node)
        problems.extend(input_problems)
        scopes = self._approval_scopes(data, node, inputs)
        for gate, scope in scopes.items():
            if not self._approved(data, scope):
                problems.append("required scoped approval: " + gate)
        if invocation:
            if invocation["task"]["contractSha256"] != node_contract(data["graph"], node["id"]) or invocation["graphVersion"] != data["graphVersion"]:
                problems.append("invocation contract is stale")
            expected = [{k:a[k] for k in ("artifactId", "sha256", "nodeId", "invocationId", "epoch")} for a in inputs]
            actual = [{k:a[k] for k in ("artifactId", "sha256", "nodeId", "invocationId", "epoch")} for a in invocation["task"]["requiredInputs"]]
            if expected != actual:
                problems.append("input lineage changed")
        return inputs, scopes, problems

    def _capacity(self, data):
        live = [i for i in data["invocations"].values() if i["status"] in LIVE]
        prepared = sum(i["status"] == "prepared" for i in live)
        return min(data["graph"]["limits"]["maxConcurrentWorkers"]-len(live),
                   data["contract"]["maxLaunchAttempts"]-data["launchAttempts"]-prepared,
                   data["graph"]["limits"]["maxNodeRuns"]-data["launchAttempts"]-prepared)

    def _node_budget(self, data, node):
        spent = sum(i["nodeId"] == node["id"] and (i.get("issued") or i["status"] == "prepared") for i in data["invocations"].values())
        return spent < node["budget"]["maxAttempts"]

    def ready(self, *, lane=None, available_slots=None):
        data = self.load()
        return self._ready(data, lane=lane, available_slots=available_slots)

    def _ready(self, data, *, lane=None, available_slots=None):
        ready, blockers, scopes = [], {}, {}
        for node in data["graph"]["nodes"]:
            if lane is not None and node["execution"]["mode"] != lane:
                continue
            _, approval_scopes, issues = self._eligibility(data, node)
            scopes.update(approval_scopes)
            if not self._node_budget(data, node):
                issues.append("node attempt budget exhausted")
            if issues:
                blockers[node["id"]] = issues
            else:
                ready.append(node)
        def order(node):
            downstream = len({e["target"] for e in data["graph"]["edges"] if e["enabled"] and e["required"] and e["source"] == node["id"] and data["nodes"][e["target"]]["status"] not in {"succeeded","skipped","cancelled"}})
            return (-node["priority"], -int(node["critical"]), -downstream, node["id"])
        ready.sort(key=order)
        capacity = max(0,self._capacity(data))
        if available_slots is not None:
            if available_slots < 0:
                raise RuntimeErrorBase("available slots must be nonnegative")
            capacity = min(capacity, available_slots)
        selected = ready[:capacity]
        for node in ready[capacity:]:
            blockers[node["id"]] = ["capacity or global attempt reservation exhausted"]
        return {"readyNodeIds":[n["id"] for n in selected], "blockers":blockers,
                "approvalScopes":scopes, "capacity":capacity, "generation":data["generation"]}

    def status(self):
        data = self.load()
        result = self._ready(data)
        result.update({"state":data, "runId":data["runId"], "obligations":[i["invocationId"] for i in data["invocations"].values() if i["status"] in LIVE],
                       "evidenceTier":data["contract"]["evidenceTier"], "nativeQualification":False})
        return result

    def prepare(self, *, node_id=None, lane="subagent", available_slots=None, **options):
        if lane not in TOOLS:
            raise RuntimeErrorBase("unknown execution lane")
        intent = {"nodeId":node_id,"lane":lane,"availableSlots":available_slots}
        def apply(data):
            self._check_deadline(data)
            frontier = self._ready(data, lane=lane, available_slots=available_slots)
            selected = frontier["readyNodeIds"]
            if node_id is not None:
                if node_id not in selected:
                    raise RuntimeErrorBase("node not ready: " + "; ".join(frontier["blockers"].get(node_id,["lane mismatch or no capacity"])))
                selected = [node_id]
            outputs = []
            for selected_id in selected:
                node = self._node(data, selected_id)
                inputs, scopes, problems = self._eligibility(data,node)
                if problems or self._capacity(data) < 1 or not self._node_budget(data,node):
                    raise RuntimeErrorBase("preparation reservation guard failed")
                attempt = 1+sum(i["nodeId"] == selected_id for i in data["invocations"].values())
                inv_id = f"inv-{selected_id}-{attempt:04d}"
                directory = f"node-runs/{selected_id}/{inv_id}"
                worker = directory + "/worker"
                artifact_root = f"artifacts/{selected_id}/{inv_id}"
                for relative in (worker, artifact_root):
                    safe_path(self.root, relative).mkdir(parents=True, exist_ok=True)
                spec = {"tool":TOOLS[lane], "forkTurns":"none", "model":node["execution"]["modelHint"],
                        "taskName":"og_" + digest({"root":str(self.root),"invocation":inv_id})[:24],
                        "normalizedIntent":True,"identityKind":"host-worker" if lane == "subagent" else "logical-local-invocation"}
                task = {"packetType":"NodeTaskPacket", "protocolVersion":2, "runId":data["runId"],
                        "graphId":data["graphId"], "graphVersion":data["graphVersion"], "epoch":data["epoch"],
                        "nodeId":selected_id, "invocationId":inv_id, "attempt":attempt,
                        "contractSha256":node_contract(data["graph"], selected_id), "task":deepcopy(node),
                        "requiredInputs":inputs, "successCriteria":node["successCriteria"],
                        "expectedOutputs":node["outputs"], "launchSpec":spec,
                        "allowedWriteRoots":[worker,artifact_root], "canonicalReturnPath":worker+"/return-packet.json",
                        "approvalScopes":scopes, "deadline":data["contract"]["deadline"],
                        "authorization":{"maySpawnWorkers":False,"mayApprove":False,"mayIntegrate":False,
                            "mayUpdateControllerState":False,"mayAnswerUser":False,"mayIssueTerminalVerdict":False},
                        "limits":{"workUnits":node["budget"]["workUnits"],"maxLocalIterations":node["localLoop"]["maxIterations"] if node["localLoop"]["enabled"] else 1,
                                  "enforcement":"host work and local iterations are declared; controller enforces invocation limits"}}
                sha = digest(task)
                inv = {"invocationId":inv_id,"nodeId":selected_id,"epoch":data["epoch"], "graphVersion":data["graphVersion"],
                       "attempt":attempt,"directory":directory,"task":task,"taskPacketSha256":sha,"status":"prepared","issued":False,
                       "dispatchReceipt":{"protocolVersion":2,"invocationId":inv_id,"taskPacketSha256":sha,"preparedGeneration":data["generation"]+1},
                       "launch":None,"launchReceipt":None,"returned":None,"lateReturns":[],"settlements":[]}
                data["invocations"][inv_id] = inv
                data["nodes"][selected_id].update(status="ready",currentInvocation=inv_id)
                outputs.append({"invocationId":inv_id,"nodeId":selected_id,"taskPacketPath":directory+"/task-packet.json",
                                "taskPacketSha256":sha,"task":task,"launchSpec":spec})
            fault("after-packet-stage")
            return {"invocations":outputs,"count":len(outputs)}
        return self._mutation("prepare-dispatch",intent,apply,**options)

    def _invocation(self, data, inv_id):
        identifier(inv_id,"invocationId")
        if inv_id not in data["invocations"]:
            raise RuntimeErrorBase("unknown invocation")
        return data["invocations"][inv_id]

    def begin_launch(self, invocation_id, **options):
        def apply(data):
            inv = self._invocation(data,invocation_id)
            if inv["status"] != "prepared":
                raise RuntimeErrorBase("only an unissued prepared reservation may begin launch")
            node = self._node(data,inv["nodeId"])
            _,_,issues = self._eligibility(data,node,invocation=inv)
            if issues:
                inv["status"] = "released"
                inv["releaseReason"] = issues
                data["nodes"][node["id"]]["status"] = "blocked"
                return {"invocationId":invocation_id,"authorized":False,"status":"released","issues":issues}
            # Budget includes every other reservation. This reservation already owns one slot.
            if self._capacity(data) < 0 or not self._node_budget_including_current(data,node):
                raise RuntimeErrorBase("launch boundary capacity/budget changed")
            inv["issued"] = True
            inv["effectPending"] = node["execution"]["mode"] == "tool"
            inv["status"] = "effect-outcome-unknown" if node["execution"]["mode"] == "tool" else "launch-unknown"
            inv["intent"] = {"idempotencyKey":data["runId"]+":"+invocation_id,
                             "authorizedGeneration":data["generation"]+1,"approvalDecisionIds":[a["decisionId"] for a in data["approvals"] if a["decision"] == "granted"],
                             "request":inv["task"]["launchSpec"],"taskPacketSha256":inv["taskPacketSha256"]}
            data["launchAttempts"] += 1
            data["nodes"][node["id"]]["attempts"] += 1
            return {"invocationId":invocation_id,"intent":inv["intent"],"status":inv["status"],
                    "next":"controller may issue exactly this authorized request once; missing response requires reconciliation"}
        return self._mutation("begin-launch",{"invocationId":invocation_id},apply,**options)

    def _node_budget_including_current(self,data,node):
        count = sum(i["nodeId"] == node["id"] and (i.get("issued") or i["status"] == "prepared") for i in data["invocations"].values())
        return count <= node["budget"]["maxAttempts"]

    def _observation(self,data,kind,record):
        if data["contract"]["evidenceTier"] == "controller-observed":
            if self.adapter is None or not self.adapter.verify_observation(kind, deepcopy(record)):
                raise RuntimeErrorBase("actual host observation unavailable; a JSON claim cannot establish controller-observed evidence")
            return "controller-observed"
        return "simulated-controller-declaration" if data["contract"]["evidenceTier"] == "simulated" else "controller-declared-unverified"

    def record_launch(self, record, **options):
        record = deepcopy(require_object(record,"launch record"))
        def apply(data):
            inv = self._invocation(data,record.get("invocationId"))
            if inv["status"] not in {"launch-unknown","effect-outcome-unknown","cancel-requested"} or inv.get("launch") is not None:
                raise RuntimeErrorBase("launch observation requires one outstanding issued intent")
            for key,value in {"protocolVersion":2,"runId":data["runId"],"taskPacketSha256":inv["taskPacketSha256"]}.items():
                if record.get(key) != value:
                    raise RuntimeErrorBase("launch record binding mismatch: " + key)
            request = require_object(record.get("request"),"launch request")
            spec = inv["task"]["launchSpec"]
            for key in ("tool","forkTurns","model"):
                if key not in request or request[key] != spec[key]:
                    raise RuntimeErrorBase("launch request mismatch: " + key)
            if "taskName" in request and request["taskName"] != spec["taskName"]:
                raise RuntimeErrorBase("launch task name mismatch")
            response = require_object(record.get("response"),"launch response")
            outcome = response.get("outcome")
            if outcome not in {"launched","rejected","unknown"}:
                raise RuntimeErrorBase("invalid launch outcome")
            nonempty(response.get("reference"),"launch observation reference")
            if outcome == "launched":
                agent = nonempty(response.get("agentId"),"agentId")
                if any(i.get("launch",{}).get("response",{}).get("agentId") == agent for i in data["invocations"].values() if i.get("launch")):
                    raise RuntimeErrorBase("agent identity reused; every invocation must be fresh")
            if data["contract"]["evidenceTier"] != "simulated":
                nonempty(request.get("actualHostTool"),"actualHostTool")
                require_object(request.get("actualArguments"),"actualArguments")
            classification = self._observation(data,"launch",record)
            inv["launch"] = record
            inv["launchReceipt"] = {"invocationId":inv["invocationId"],"launchSha256":digest(record),
                                     "evidenceClass":classification,"identityKind":inv["task"]["launchSpec"]["identityKind"],"observedGeneration":data["generation"]+1}
            cancelled = inv["status"] == "cancel-requested" or data["status"] != "running"
            if outcome == "launched":
                data["totalNodeRuns"] += 1
                inv["status"] = "cancel-requested" if cancelled else "running"
                data["nodes"][inv["nodeId"]]["status"] = "cancel-requested" if cancelled else "running"
            elif outcome == "rejected":
                inv["effectPending"] = False
                inv["status"] = "cancelled" if cancelled else "launch-rejected"
                data["nodes"][inv["nodeId"]]["status"] = "cancelled" if cancelled else "blocked"
            self._close_cancel(data)
            return {"invocationId":inv["invocationId"],"status":inv["status"],"evidenceClass":classification}
        return self._mutation("record-launch",record,apply,allow_terminal=True,**options)

    def record_approval(self, record, **options):
        record = deepcopy(require_object(record,"approval"))
        def apply(data):
            required = {"approvalId","runId","subjectType","subjectId","scope","decision","authority","provenance"}
            if set(record) != required:
                raise ApprovalError("approval fields must exactly match v2 decision schema")
            identifier(record["approvalId"],"approvalId")
            if record["runId"] != data["runId"] or record["authority"] != data["graph"]["goal"]["authorityNodeId"]:
                raise ApprovalError("approval run/authority mismatch")
            if record["subjectType"] not in {"external-action","artifact","resume","rewrite"} or record["decision"] not in {"granted","denied","revoked"}:
                raise ApprovalError("invalid approval decision or subject type")
            require_object(record["scope"],"approval scope")
            provenance = require_object(record["provenance"],"approval provenance")
            nonempty(provenance.get("reference"),"approval provenance reference")
            nonempty(provenance.get("kind"),"approval provenance kind")
            if data["status"] in TERMINAL and record["decision"] == "granted":
                raise ApprovalError("terminal run cannot gain authority")
            bindings = []
            for node in data["graph"]["nodes"]:
                try:
                    inputs,_ = self._inputs(data,node)
                    bindings.extend(s for s in self._approval_scopes(data,node,inputs).values() if s)
                except RuntimeErrorBase:
                    if record["decision"] == "granted":
                        raise
            if record["decision"] in {"denied","revoked"}:
                bindings.extend({k:a[k] for k in ("runId","subjectType","subjectId","scope","authority")} for a in data["approvals"])
            for proposal in data["proposals"].values():
                bindings.append(self._rewrite_scope(data,proposal))
            binding = {k:record[k] for k in ("runId","subjectType","subjectId","scope","authority")}
            if binding not in bindings:
                raise ApprovalError("approval does not bind a current exact action/proposal scope")
            for earlier in data["approvals"]:
                if earlier["approvalId"] == record["approvalId"] and any(earlier[k] != record[k] for k in ("runId","subjectType","subjectId","scope","authority")):
                    raise ApprovalError("approval ID collision across different scopes")
            evidence = self._observation(data,"approval",record)
            decision = {**record,"decisionId":"decision-"+str(len(data["approvals"])+1),
                        "sequence":data["generation"]+1,"evidenceClass":evidence}
            data["approvals"].append(decision)
            return decision
        return self._mutation("record-approval",record,apply,allow_terminal=True,**options)

    def _owned_file(self, inv, relative, *, artifact=False):
        path = safe_path(self.root,relative)
        roots = inv["task"]["allowedWriteRoots"]
        allowed = roots[1:] if artifact else roots
        if not any(relative.startswith(root+"/") for root in allowed):
            raise RuntimeErrorBase("write path outside exact invocation ownership")
        if not path.is_file():
            raise RuntimeErrorBase("declared file missing: " + relative)
        return path

    def _agent(self, inv):
        for settlement in reversed(inv["settlements"]):
            if settlement["outcome"] == "launched":
                return settlement["agentId"]
        if inv.get("launch") and inv["launch"]["response"]["outcome"] == "launched":
            return inv["launch"]["response"]["agentId"]
        return None

    def ingest(self, packet, *, return_path=None, **options):
        packet = deepcopy(require_object(packet,"return packet"))
        def apply(data):
            inv = self._invocation(data,packet.get("invocationId"))
            if inv["status"] not in {"running","cancel-requested","cancelled"}:
                raise RuntimeErrorBase("return requires observed launched invocation or cancelled late settlement")
            for key,value in {"packetType":"NodeReturnPacket","protocolVersion":2,"runId":data["runId"],"taskPacketSha256":inv["taskPacketSha256"],"agentId":self._agent(inv)}.items():
                if value is None or packet.get(key) != value:
                    raise RuntimeErrorBase("return binding mismatch: " + key)
            for key in ("nodeId","epoch","graphVersion","attempt"):
                if key in packet and packet[key] != inv[key]:
                    raise RuntimeErrorBase("return binding mismatch: " + key)
            if return_path is not None:
                expected = safe_path(self.root,inv["task"]["canonicalReturnPath"])
                supplied = safe_root(Path(return_path))
                if supplied != expected or not supplied.is_file() or supplied.read_bytes() != canonical(packet):
                    # JSON whitespace is not semantically significant, but its content is.
                    import json
                    if supplied != expected or not supplied.is_file() or json.loads(supplied.read_text()) != packet:
                        raise RuntimeErrorBase("return must use canonical invocation worker path")
            status = packet.get("status")
            if status not in {"succeeded","failed","blocked","escalate"}:
                raise RuntimeErrorBase("invalid return status")
            nonempty(packet.get("summary"),"return summary")
            if data["contract"]["evidenceTier"] != "simulated":
                nonempty(packet.get("completionReference"),"actual host completionReference")
            return_evidence_class = self._observation(data,"return",packet)
            authority = packet.get("authority")
            if authority != inv["task"]["authorization"]:
                raise RuntimeErrorBase("worker return cannot claim controller authority")
            for field in ("unresolvedIssues","risks","recommendedSignals"):
                values = packet.get(field,[])
                if not isinstance(values,list) or len(values) > 100 or any(not isinstance(v,str) or not v.strip() or len(v) > 4000 for v in values):
                    raise RuntimeErrorBase(field + " must be a bounded list of nonempty advisory strings")
            writes = packet.get("actualWritePaths")
            if not isinstance(writes,list) or len(writes) != len(set(writes)):
                raise RuntimeErrorBase("actualWritePaths must be a unique list")
            for relative in writes:
                self._owned_file(inv,relative)
            evidence = packet.get("evidence")
            criteria = packet.get("criteria")
            artifacts = packet.get("artifacts")
            evaluations = packet.get("evaluations",[])
            if not all(isinstance(v,list) for v in (evidence,criteria,artifacts,evaluations)):
                raise RuntimeErrorBase("return evidence, criteria, artifacts and evaluations must be lists")
            evidence_paths = set()
            for item in evidence:
                require_object(item,"evidence")
                nonempty(item.get("kind"),"evidence kind")
                path = self._owned_file(inv,item.get("path"))
                if item["path"] not in writes or byte_digest(path.read_bytes()) != item.get("sha256"):
                    raise RuntimeErrorBase("evidence write/digest mismatch")
                if item["path"] in evidence_paths:
                    raise RuntimeErrorBase("duplicate evidence path")
                evidence_paths.add(item["path"])
            expected = inv["task"]["successCriteria"]
            if len(criteria) != len(expected) or {c.get("criterion") for c in criteria} != set(expected):
                raise RuntimeErrorBase("return must cover every exact node criterion once")
            for criterion in criteria:
                if criterion.get("result") not in {"met","not_met","blocked","failed"}:
                    raise RuntimeErrorBase("invalid node criterion result")
                cited = criterion.get("evidencePaths")
                if not isinstance(cited,list) or any(p not in evidence_paths for p in cited):
                    raise RuntimeErrorBase("criterion cites unvalidated evidence")
                if criterion["result"] == "met" and not cited:
                    raise RuntimeErrorBase("met criterion requires actual evidence")
                if status == "succeeded" and criterion["result"] != "met":
                    raise RuntimeErrorBase("successful return has unmet node criterion")
            local_iterations = packet.get("localIterations",1)
            if not isinstance(local_iterations,int) or isinstance(local_iterations,bool) or not 1 <= local_iterations <= inv["task"]["limits"]["maxLocalIterations"]:
                raise RuntimeErrorBase("declared local loop bound exceeded")
            work_units = packet.get("workUnits",0)
            if not isinstance(work_units,int) or isinstance(work_units,bool) or not 0 <= work_units <= inv["task"]["limits"]["workUnits"]:
                raise RuntimeErrorBase("declared work-unit budget exceeded")
            declared = {o["artifactType"] for o in inv["task"]["expectedOutputs"]}
            required = {o["artifactType"] for o in inv["task"]["expectedOutputs"] if o["required"]}
            types = set()
            artifact_sources = []
            seen_paths = set()
            for item in artifacts:
                require_object(item,"artifact")
                typ = item.get("artifactType")
                if typ not in declared:
                    raise RuntimeErrorBase("undeclared output type")
                path = self._owned_file(inv,item.get("path"),artifact=True)
                content = path.read_bytes()
                if item["path"] in seen_paths or item["path"] not in writes or byte_digest(content) != item.get("sha256"):
                    raise RuntimeErrorBase("artifact path/digest/write declaration mismatch")
                seen_paths.add(item["path"])
                artifact_sources.append((item,content))
                types.add(typ)
            if status == "succeeded" and not required <= types:
                raise RuntimeErrorBase("successful return missing required declared outputs")
            node = self._node(data,inv["nodeId"])
            effect_unknown = False
            if node["execution"]["mode"] == "tool":
                effect = packet.get("effectOutcome", "unknown")
                if effect not in {"observed-complete", "not-performed", "unknown"}:
                    raise RuntimeErrorBase("invalid effect outcome")
                if status == "succeeded" and effect != "observed-complete":
                    raise RuntimeErrorBase("successful tool return needs observed-complete effect evidence")
                effect_unknown = effect == "unknown"
                if not effect_unknown:
                    self._observation(data,"effect-outcome",packet)
                    inv["effectPending"] = False
            input_ids = {a["artifactId"] for a in inv["task"]["requiredInputs"]}
            seen_evals = set()
            for ev in evaluations:
                require_object(ev,"evaluation")
                if node["kind"] != "evaluator":
                    raise RuntimeErrorBase("only evaluator nodes return goal criterion judgments")
                key = (ev.get("criterion"),ev.get("artifactId"))
                if key in seen_evals or ev.get("criterion") not in data["versions"]["1"]["goal"]["completionCriteria"]:
                    raise RuntimeErrorBase("duplicate or unknown goal criterion evaluation")
                art = data["artifacts"].get(ev.get("artifactId"))
                if not art or art["artifactId"] not in input_ids or art["sha256"] != ev.get("sha256") or art["nodeId"] == node["id"]:
                    raise RuntimeErrorBase("evaluation must bind exact consumed independent producer artifact")
                if not any(e["enabled"] and e["kind"] == "verify" and e["source"] == art["nodeId"] and e["target"] == node["id"] and art["type"] in e["artifactTypes"] for e in data["graph"]["edges"]):
                    raise RuntimeErrorBase("evaluation lacks declared producer-to-evaluator verify edge")
                producer = data["invocations"].get(art["invocationId"])
                if producer and self._agent(producer) == self._agent(inv):
                    raise RuntimeErrorBase("producer and evaluator worker identity must differ")
                if ev.get("result") not in {"met","not_met"}:
                    raise RuntimeErrorBase("invalid evaluation result")
                nonempty(ev.get("reason"),"evaluation reason")
                if not evidence_paths:
                    raise RuntimeErrorBase("goal judgment requires inspected evidence")
                seen_evals.add(key)
            try:
                _,_,problems = self._eligibility(data,node,invocation=inv)
            except RuntimeErrorBase as exc:
                problems = ["input/authority integrity blocks activation: " + str(exc)]
            late = inv["status"] in {"cancel-requested","cancelled"} or data["status"] != "running"
            quarantine = late or bool(problems) or effect_unknown
            receipt = {"packet":packet,"returnSha256":digest(packet),"ingestedGeneration":data["generation"]+1,
                       "disposition":"effect-unknown-quarantine" if effect_unknown else "late-quarantine" if late else "guard-quarantine" if problems else "accepted",
                       "guardIssues":problems,"artifactIds":[],"evidenceClass":return_evidence_class,"sourceReturnPath":inv["task"]["canonicalReturnPath"] if return_path is not None else None}
            for index,(item,content) in enumerate(artifact_sources,1):
                sha = self.store.stage_object(content)
                data["objects"].append(sha)
                art_id = f"art-{inv['invocationId']}-{index:03d}"
                if art_id in data["artifacts"]:
                    if quarantine:
                        art_id += "-late-" + str(len(inv["lateReturns"])+1)
                    else:
                        raise RuntimeErrorBase("artifact identity already committed")
                artifact = {"artifactId":art_id,"type":item["artifactType"],"nodeId":inv["nodeId"],
                            "invocationId":inv["invocationId"],"epoch":inv["epoch"],"graphVersion":inv["graphVersion"],
                            "sha256":sha,"path":"objects/"+sha,"sourcePath":item["path"],
                            "inputs":[{"artifactId":a["artifactId"],"sha256":a["sha256"]} for a in inv["task"]["requiredInputs"]],
                            "active":status == "succeeded" and not quarantine,"eligibleVersions":[inv["graphVersion"]],
                            "provisional":status != "succeeded" or quarantine}
                data["artifacts"][art_id] = artifact
                receipt["artifactIds"].append(art_id)
                fault("after-artifact-stage")
                if index == 1:
                    fault("after-first-artifact-stage")
            if quarantine:
                inv["lateReturns"].append(receipt)
                inv["status"] = "effect-outcome-unknown" if effect_unknown else "cancelled" if late else "quarantined"
                if data["nodes"][inv["nodeId"]]["currentInvocation"] == inv["invocationId"]:
                    data["nodes"][inv["nodeId"]]["status"] = "effect-outcome-unknown" if effect_unknown else "cancelled" if late else "blocked"
            else:
                inv["returned"] = receipt
                inv["status"] = "blocked" if status == "escalate" else status
                data["nodes"][inv["nodeId"]].update(status=inv["status"],completedEpoch=inv["epoch"] if status == "succeeded" else None)
            self._close_cancel(data)
            fault("after-return-validation")
            return {"invocationId":inv["invocationId"],"nodeId":inv["nodeId"],"status":inv["status"],
                    "disposition":receipt["disposition"],"artifactIds":receipt["artifactIds"],
                    "artifacts":[data["artifacts"][a] for a in receipt["artifactIds"]]}
        return self._mutation("ingest-return",{"packet":packet,"returnPath":str(return_path) if return_path else None},apply,allow_terminal=True,**options)

    def cancel(self, *, node_id=None, reason, **options):
        nonempty(reason,"cancellation reason")
        def apply(data):
            targets = [node_id] if node_id is not None else list(data["nodes"])
            if node_id is None:
                data["status"] = "stopping"
                data["stopReason"] = reason
            for target in targets:
                self._node(data,target)
                runtime = data["nodes"][target]
                inv = data["invocations"].get(runtime["currentInvocation"])
                if inv and inv["status"] in LIVE:
                    inv["cancelReason"] = reason
                    if inv["status"] == "prepared":
                        inv["status"] = "cancelled"
                        runtime["status"] = "cancelled"
                        inv["settlements"].append({"outcome":"never-issued","reason":reason,"generation":data["generation"]+1})
                    else:
                        inv["status"] = "cancel-requested"
                        runtime["status"] = "cancel-requested"
                elif runtime["status"] not in {"succeeded","skipped","cancelled"}:
                    runtime["status"] = "cancelled"
            self._close_cancel(data)
            return {"runStatus":data["status"],"nodeId":node_id,"obligations":[i["invocationId"] for i in data["invocations"].values() if i["status"] in LIVE]}
        return self._mutation("cancel-node" if node_id else "cancel-run",{"nodeId":node_id,"reason":reason},apply,**options)

    def _close_cancel(self,data):
        if data["status"] == "stopping" and not any(i["status"] in LIVE for i in data["invocations"].values()):
            data["status"] = "cancelled"

    def settle(self, record, **options):
        record = deepcopy(require_object(record,"settlement"))
        def apply(data):
            inv = self._invocation(data,record.get("invocationId"))
            for key,value in {"protocolVersion":2,"runId":data["runId"],"taskPacketSha256":inv["taskPacketSha256"]}.items():
                if record.get(key) != value:
                    raise RuntimeErrorBase("settlement binding mismatch: " + key)
            known_agent = self._agent(inv)
            if known_agent is not None and record.get("outcome") in {"stopped","effect-completed","not-performed"} and record.get("agentId") != known_agent:
                raise RuntimeErrorBase("settlement agentId does not match the exact observed invocation")
            outcome = record.get("outcome")
            if outcome not in {"stopped","rejected","launched","effect-completed","not-performed"}:
                raise RuntimeErrorBase("invalid settlement outcome")
            if inv["status"] not in {"cancel-requested","launch-unknown","effect-outcome-unknown"}:
                if outcome == "stopped" and inv.get("issued") and inv["status"] in {"cancelled","succeeded","failed","blocked"}:
                    nonempty(record.get("reference"),"late settlement observation reference")
                    evidence = self._observation(data,"settlement",record)
                    inv["settlements"].append({**record,"evidenceClass":evidence,"lateAccounting":True,"generation":data["generation"]+1})
                    return {"invocationId":inv["invocationId"],"status":inv["status"],"runStatus":data["status"],"lateAccounting":True}
                raise RuntimeErrorBase("settlement requires an unresolved obligation or non-activating late stop acknowledgment")
            nonempty(record.get("reference"),"settlement observation reference")
            evidence = self._observation(data,"settlement",record)
            was_cancelled = inv["status"] == "cancel-requested" or bool(inv.get("cancelReason")) or data["status"] != "running"
            if outcome in {"effect-completed","not-performed"}:
                if not inv.get("effectPending"):
                    raise RuntimeErrorBase("invocation has no unresolved effect")
                inv["effectPending"] = False
                inv["effectResolved"] = outcome
                if outcome == "not-performed":
                    inv["status"] = "cancelled" if was_cancelled else "effect-not-performed"
                    data["nodes"][inv["nodeId"]]["status"] = "cancelled" if was_cancelled else "blocked"
                else:
                    inv["status"] = "cancelled" if was_cancelled else "running"
                    data["nodes"][inv["nodeId"]]["status"] = inv["status"]
            elif outcome == "launched":
                agent = nonempty(record.get("agentId"),"settled agentId")
                if any(self._agent(other) == agent for other in data["invocations"].values() if other is not inv):
                    raise RuntimeErrorBase("settlement reuses another worker identity")
                if self._agent(inv) is not None and self._agent(inv) != agent:
                    raise RuntimeErrorBase("settlement changes known agent identity")
                if self._agent(inv) is None:
                    data["totalNodeRuns"] += 1
                inv["status"] = "cancel-requested" if was_cancelled else "running"
                data["nodes"][inv["nodeId"]]["status"] = inv["status"]
            else:
                if outcome == "rejected" and self._agent(inv) is not None:
                    raise RuntimeErrorBase("observed worker cannot be reclassified as never launched")
                if outcome == "rejected":
                    inv["effectPending"] = False
                inv["status"] = "effect-outcome-unknown" if inv.get("effectPending") else "cancelled" if was_cancelled or outcome == "stopped" else "launch-rejected"
                data["nodes"][inv["nodeId"]]["status"] = "effect-outcome-unknown" if inv.get("effectPending") else "cancelled" if was_cancelled or outcome == "stopped" else "blocked"
            inv["settlements"].append({**record,"evidenceClass":evidence,"generation":data["generation"]+1})
            self._close_cancel(data)
            return {"invocationId":inv["invocationId"],"status":inv["status"],"runStatus":data["status"],"evidenceClass":evidence}
        return self._mutation("settle",record,apply,allow_terminal=True,**options)

    def omit(self,node_id,*,reason,**options):
        nonempty(reason,"omission reason")
        def apply(data):
            if node_id not in data["contract"]["optionalNodeIds"] or data["nodes"][node_id]["status"] not in {"pending","failed","blocked","cancelled"}:
                raise RuntimeErrorBase("only explicitly optional, inactive work may be omitted")
            if any(i["nodeId"] == node_id and i["status"] in LIVE for i in data["invocations"].values()):
                raise RuntimeErrorBase("live optional work cannot be omitted")
            data["nodes"][node_id].update(status="skipped",omissionReason=reason)
            return {"nodeId":node_id,"status":"skipped"}
        return self._mutation("omit-node",{"nodeId":node_id,"reason":reason},apply,**options)

    def signal(self,name,value,**options):
        nonempty(name,"signal name")
        def apply(data):
            record = {"name":name,"value":value,"epoch":data["epoch"],"generation":data["generation"]+1}
            data["signals"].append(record)
            return record
        return self._mutation("signal",{"name":name,"value":value},apply,**options)

    def _rewrite_scope(self,data,proposal):
        return {"runId":data["runId"],"subjectType":"rewrite","subjectId":proposal["proposalId"],
                "authority":data["graph"]["goal"]["authorityNodeId"],
                "scope":{"proposalSha256":digest(proposal),"baseGraphVersion":proposal["baseGraphVersion"]}}

    def _rewrite_checked(self,data,proposal):
        original = Graph.from_dict(data["versions"]["1"])
        current = Graph.from_dict(data["graph"])
        expected_fields = {"proposalId","runId","baseGraphVersion","trigger","evidenceEventIds","riskLevel","reason","predictedEffect","operations","approvalRequired","rollbackVersion"}
        if set(proposal) != expected_fields:
            raise RuntimeErrorBase("rewrite proposal fields must exactly match the declared schema")
        parsed = RewriteProposal.from_dict(proposal)
        identifier(parsed.proposal_id,"proposalId")
        if parsed.run_id != data["runId"] or parsed.base_graph_version != data["graphVersion"]:
            raise RuntimeErrorBase("rewrite run/base graph version mismatch")
        if str(parsed.rollback_version) not in data["versions"]:
            raise RuntimeErrorBase("rewrite rollback version does not exist")
        if not parsed.operations:
            raise RuntimeErrorBase("rewrite must contain an operation")
        ranks = {"low":0,"medium":1,"high":2}
        classified = classify_risk(current,parsed.operations).value
        if any(op.kind.value == "disable_node" and data["nodes"].get(op.params.get("nodeId"),{}).get("attempts",0) > 0 for op in parsed.operations):
            if ranks[classified] < ranks["medium"]:
                classified = "medium"
        if ranks[parsed.risk_level.value] < ranks[classified]:
            raise RuntimeErrorBase("rewrite understates classified risk")
        policy = data["graph"]["rewritePolicy"]
        for op in parsed.operations:
            if op.kind.value in policy["prohibitedMutations"]:
                raise RuntimeErrorBase("rewrite primitive prohibited by declared policy")
        candidate = apply_operations(current,parsed.operations)
        valid = parse_and_validate_rewritten_graph(candidate.to_dict(),original_graph=original)
        if valid.violations:
            raise RuntimeErrorBase("invalid rewritten graph: " + "; ".join(str(v) for v in valid.violations))
        # All effective approval-carrying edges are non-weakenable, including
        # ordinary edges whose activation separately requires approval.
        proposed_edges = {e.id:e for e in candidate.edges}
        for edge in current.edges:
            if edge.enabled and edge.required and (edge.kind.value == "approve" or edge.activation.approvals):
                if edge.id not in proposed_edges or proposed_edges[edge.id].to_dict() != edge.to_dict():
                    raise RuntimeErrorBase("rewrite weakens an effective approval boundary")
        effective_risk = parsed.risk_level.value
        needs = parsed.approval_required or effective_risk in policy["approvalRiskLevels"] or effective_risk in {"medium","high"}
        if effective_risk not in policy["automaticRiskLevels"] and effective_risk not in policy["approvalRiskLevels"]:
            raise RuntimeErrorBase("rewrite risk is not permitted by declared policy")
        if needs and not parsed.approval_required:
            raise RuntimeErrorBase("declared rewrite policy requires approvalRequired")
        return candidate.to_dict(), classified, needs

    def propose(self,proposal,**options):
        proposal = deepcopy(require_object(proposal,"rewrite proposal"))
        def apply(data):
            self._check_deadline(data)
            self._rewrite_checked(data,proposal)
            key = identifier(proposal["proposalId"],"proposalId")
            if key in data["proposals"]:
                raise RuntimeErrorBase("immutable proposal ID already exists")
            data["proposals"][key] = proposal
            data["rewritePending"] = True
            return {"proposalId":key,"proposalSha256":digest(proposal),"approvalScope":self._rewrite_scope(data,proposal),
                    "deferred":any(i["status"] in LIVE for i in data["invocations"].values())}
        return self._mutation("propose-rewrite",proposal,apply,**options)

    def apply_rewrite(self,proposal_id,**options):
        identifier(proposal_id,"proposalId")
        def apply(data):
            self._check_deadline(data)
            if proposal_id not in data["proposals"]:
                raise RuntimeErrorBase("unknown proposal")
            if any(i["status"] in LIVE for i in data["invocations"].values()):
                raise RuntimeErrorBase("rewrite deferred: prepared, running, unknown or cancellation obligation remains")
            if any(w["proposalId"] == proposal_id for w in data.get("withdrawnProposals",[])):
                raise RuntimeErrorBase("proposal was withdrawn")
            proposal = data["proposals"][proposal_id]
            candidate,classified,needs = self._rewrite_checked(data,proposal)
            if needs and not self._approved(data,self._rewrite_scope(data,proposal)):
                raise ApprovalError("rewrite requires latest exact scoped approval")
            if not needs and data["autoRewritesApplied"] >= data["graph"]["limits"]["maxAutoRewrites"]:
                raise RuntimeErrorBase("automatic rewrite budget exhausted")
            version = data["graphVersion"]+1
            if version > data["graph"]["limits"]["maxGraphVersions"]:
                raise RuntimeErrorBase("graph version budget exhausted")
            old_nodes = {n["id"]:n for n in data["graph"]["nodes"]}
            new_nodes = {n["id"]:n for n in candidate["nodes"]}
            affected = {key for key in new_nodes if key not in old_nodes or node_contract(data["graph"],key) != node_contract(candidate,key)}
            changed = True
            while changed:
                before = len(affected)
                for edge in data["graph"]["edges"]+candidate["edges"]:
                    if edge["enabled"] and edge["source"] in affected:
                        affected.add(edge["target"])
                changed = before != len(affected)
            for key,node in new_nodes.items():
                if key not in data["nodes"]:
                    data["nodes"][key] = {"status":"pending","currentInvocation":None,"completedEpoch":None,"attempts":0}
                elif key in affected:
                    old = deepcopy(data["nodes"][key])
                    data["nodes"][key].update(status="pending" if node["enabled"] else "skipped",currentInvocation=None,completedEpoch=None)
                    data["nodes"][key]["invalidatedPrevious"] = old
                elif data["nodes"][key]["status"] == "succeeded":
                    data["carryForwards"].append({"nodeId":key,"invocationId":data["nodes"][key]["currentInvocation"],
                        "fromGraphVersion":data["graphVersion"],"toGraphVersion":version,"reason":"unchanged node/incoming contract and unaffected dependency closure"})
            for artifact in data["artifacts"].values():
                if artifact["nodeId"] in affected:
                    artifact["active"] = False
                    artifact["invalidatedBy"] = proposal_id
                elif artifact["active"]:
                    artifact["eligibleVersions"].append(version)
            rewrite = {"proposalId":proposal_id,"proposalSha256":digest(proposal),"baseGraphVersion":data["graphVersion"],
                       "appliedGraphVersion":version,"classifiedRiskLevel":classified,"affectedNodeIds":sorted(affected),
                       "approvalRequired":needs,"approvalScope":self._rewrite_scope(data,proposal),"generation":data["generation"]+1}
            data["rewrites"].append(rewrite)
            data["graph"] = candidate
            data["graphVersion"] = version
            data["versions"][str(version)] = candidate
            data["autoRewritesApplied"] += int(not needs)
            data["rewritePending"] = False
            data["verification"] = None
            fault("after-rewrite-stage")
            return rewrite
        return self._mutation("apply-rewrite",{"proposalId":proposal_id},apply,**options)

    def withdraw_rewrite(self,proposal_id,*,reason,**options):
        identifier(proposal_id,"proposalId")
        nonempty(reason,"withdraw reason")
        def apply(data):
            if proposal_id not in data["proposals"]:
                raise RuntimeErrorBase("unknown proposal")
            data.setdefault("withdrawnProposals",[]).append({"proposalId":proposal_id,"reason":reason})
            withdrawn = {w["proposalId"] for w in data["withdrawnProposals"]}
            applied = {w["proposalId"] for w in data["rewrites"]}
            data["rewritePending"] = any(key not in withdrawn|applied and p["baseGraphVersion"] == data["graphVersion"] for key,p in data["proposals"].items())
            return {"proposalId":proposal_id,"withdrawn":True}
        return self._mutation("withdraw-rewrite",{"proposalId":proposal_id,"reason":reason},apply,**options)

    def advance_epoch(self,**options):
        def apply(data):
            self._check_deadline(data)
            if data["status"] != "running" or data["rewritePending"] or any(i["status"] in LIVE for i in data["invocations"].values()):
                raise RuntimeErrorBase("epoch barrier has outstanding obligations")
            required = [n for n in data["graph"]["nodes"] if n["enabled"] and n["id"] not in data["contract"]["optionalNodeIds"]]
            if any(data["nodes"][n["id"]]["status"] != "succeeded" or data["nodes"][n["id"]]["completedEpoch"] != data["epoch"] for n in required):
                raise RuntimeErrorBase("all required same-epoch work must finish before epoch advancement")
            if self._verification(data)["status"] == "pass":
                raise RuntimeErrorBase("goal already satisfied; finalize without an unnecessary epoch")
            next_edges = [e for e in data["graph"]["edges"] if e["enabled"] and e["required"] and e["temporal"] == "next_epoch"]
            if not next_edges:
                raise RuntimeErrorBase("graph has no required bounded feedback edge")
            feedback = []
            for edge in next_edges:
                for typ in edge["artifactTypes"]:
                    artifacts = self._active(data,producer=edge["source"],epoch=data["epoch"],artifact_type=typ)
                    if not artifacts:
                        raise RuntimeErrorBase("missing exact current-epoch feedback for " + edge["id"])
                    feedback.extend(a["artifactId"] for a in artifacts)
            if data["epoch"] >= data["graph"]["limits"]["maxEpochs"] or data["launchAttempts"] >= min(data["contract"]["maxLaunchAttempts"],data["graph"]["limits"]["maxNodeRuns"]):
                data["status"] = "exhausted"
                return {"advanced":False,"status":"exhausted","epoch":data["epoch"]}
            old = data["epoch"]
            data["epoch"] += 1
            for node in data["graph"]["nodes"]:
                runtime = data["nodes"][node["id"]]
                if node["enabled"] and runtime["status"] != "skipped":
                    runtime.update(status="pending",currentInvocation=None,completedEpoch=None)
            record = {"fromEpoch":old,"toEpoch":data["epoch"],"feedbackArtifactIds":sorted(set(feedback)),"generation":data["generation"]+1}
            data["epochs"].append(record)
            data["verification"] = None
            return {"advanced":True,"epoch":data["epoch"],"feedbackArtifactIds":record["feedbackArtifactIds"]}
        return self._mutation("advance-epoch",{},apply,**options)

    def _verification(self,data):
        issues = []
        criteria_results = []
        goal = data["versions"]["1"]["goal"]
        current_artifacts = self._active(data,epoch=data["epoch"])
        deliverables = {}
        for deliverable in goal["deliverables"]:
            candidates = [a for a in current_artifacts if a["type"] == deliverable["artifactType"] and a["invocationId"]]
            if len(candidates) != 1:
                issues.append("deliverable must have one exact active current artifact: " + deliverable["id"])
            else:
                deliverables[deliverable["id"]] = candidates[0]
        bindings = {c["criterion"]:c for c in data["contract"]["criteria"]}
        for criterion in goal["completionCriteria"]:
            binding = bindings.get(criterion)
            matches = []
            target = None
            if binding:
                target = deliverables.get(binding["deliverableId"])
                state = data["nodes"].get(binding["evaluatorNodeId"],{})
                inv = data["invocations"].get(state.get("currentInvocation"))
                if target and inv and inv["status"] == "succeeded" and inv["epoch"] == data["epoch"] and inv.get("returned"):
                    for ev in inv["returned"]["packet"].get("evaluations",[]):
                        if ev.get("criterion") == criterion and ev.get("artifactId") == target["artifactId"] and ev.get("sha256") == target["sha256"]:
                            matches.append({**ev,"evaluatorInvocationId":inv["invocationId"]})
            met = len(matches) == 1 and matches[0]["result"] == "met"
            result = {"criterion":criterion,"satisfied":met,"artifactId":target["artifactId"] if target else None,
                      "sha256":target["sha256"] if target else None,"judgments":matches,
                      "basis":"exact independent evaluator judgment" if matches else "missing exact criterion-specific judgment"}
            criteria_results.append(result)
            if not met:
                issues.append("unmet original goal criterion: " + criterion)
        if not goal["completionCriteria"]:
            issues.append("original goal has no explicit completion criteria")
        if data["status"] not in {"running","completed"}:
            issues.append("run is " + data["status"])
        if data["rewritePending"]:
            issues.append("rewrite proposal remains pending")
        for node in data["graph"]["nodes"]:
            if not node["enabled"]:
                continue
            status = data["nodes"][node["id"]]["status"]
            if status != "succeeded" and not (node["id"] in data["contract"]["optionalNodeIds"] and status == "skipped"):
                issues.append("unfinished node: " + node["id"] + " ("+status+")")
        if any(inv["status"] in LIVE for inv in data["invocations"].values()):
            issues.append("unaccounted live/prepared/unknown child obligation")
        omitted = [{"nodeId":key,"reason":node.get("omissionReason","No reason recorded"),
                    "priorOutcomes":[inv["status"] for inv in data["invocations"].values() if inv["nodeId"] == key]}
                   for key,node in sorted(data["nodes"].items()) if node["status"] == "skipped" and key in data["contract"]["optionalNodeIds"]]
        return {"status":"fail" if issues else "pass","checkedAt":now(),"criteria":criteria_results,"omittedNodes":omitted,
                "issues":sorted(set(issues)),"evidenceArtifactIds":sorted(a["artifactId"] for a in deliverables.values()),
                "evidenceTier":data["contract"]["evidenceTier"],"nativeQualification":False,
                "limits":["Logical execution identities do not establish independent native model contexts or human identities.",
                          "Controller records and hashes do not authenticate actors or enforce an OS sandbox.",
                          "Simulated evidence is not a native worker run; actual host observations require independent inspection."]}

    def verify(self):
        return self._verification(self.load())

    def finalize(self,**options):
        def apply(data):
            result = self._verification(data)
            fault("after-verification-computation")
            if result["status"] != "pass":
                raise RuntimeErrorBase("finalization rejected: " + "; ".join(result["issues"]))
            data["verification"] = result
            data["status"] = "completed"
            return {"status":"completed","verification":result}
        return self._mutation("finalize",{},apply,**options)

    def recover(self):
        result = self.store.recover()
        try:
            data = self.load()
            result["evidenceIssues"] = []
        except RuntimeErrorBase as exc:
            data,_ = self.store.load(check_objects=False)
            self._validate(data,verify_files=False)
            result["evidenceIssues"] = [str(exc)]
        result["obligations"] = [i["invocationId"] for i in data["invocations"].values() if i["status"] in LIVE]
        result["state"] = data
        return result

    def replay(self):
        data,records = self.store.load(check_projections=False,check_objects=False)
        self._validate(data,verify_files=False)
        return {"state":data,"operationCount":len(records),"readOnly":True,"externalEvidenceChecked":False}
