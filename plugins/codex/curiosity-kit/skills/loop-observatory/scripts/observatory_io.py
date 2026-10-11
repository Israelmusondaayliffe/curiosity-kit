"""Bounded captured-byte intake and producer-specific, read-only adapters.

No producer is imported or executed. Content paths are never followed. Integrity
checks describe a captured envelope/closure, not live artifact verification or
human acceptance. See NOTICE for source attribution and distribution limits.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PARSER_VERSION = "observatory-2.0.0"
SCHEMA_VERSION = "2.0"
PROFILES = ("supplied-v1", "loopkit-legacy", "loopkit-snapshot-v2",
            "operating-graph-legacy", "operating-graph-v2")
DEFAULT_LIMITS = {"max_files": 1000, "max_file_bytes": 8 * 1024 * 1024,
                  "max_total_bytes": 64 * 1024 * 1024, "max_depth": 24,
                  "max_json_depth": 64, "max_records": 10000}
LOOPKIT_TERMINAL = {"completed", "failed", "cancelled", "exhausted"}
LOOPKIT_STATES = LOOPKIT_TERMINAL | {"draft", "ready", "running", "waiting_input", "scheduled", "blocked", "paused"}
GRAPH_TERMINAL = {"completed", "failed", "cancelled", "exhausted"}
GRAPH_STATES = GRAPH_TERMINAL | {"running", "paused", "blocked", "stopped"}


class EvidenceError(ValueError):
    def __init__(self, code, detail):
        self.code = code
        super().__init__(detail)


def need(condition, code, detail):
    if not condition:
        raise EvidenceError(code, detail)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def canonical(value, newline=False):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + ("\n" if newline else "")).encode("utf-8")


def digest(value, newline=False):
    return hashlib.sha256(canonical(value, newline)).hexdigest()


def safe_id(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", str(value)).strip("-.")[:100] or "source"


def number_value(value, *, integer=False):
    need(type(value) in (int, float) and math.isfinite(value) and value >= 0,
         "invalid-number", "Expected finite nonnegative numeric value, without string or boolean coercion")
    need(not integer or type(value) is int, "invalid-integer", "Expected nonnegative integer")
    return value


def bool_value(value):
    need(value is None or type(value) is bool, "invalid-label", "Labels must be boolean or null")
    return value


def timestamp(value):
    if value is None:
        return None
    need(isinstance(value, str), "invalid-time", "Expected RFC3339 time with timezone")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        need(parsed.tzinfo is not None and parsed.utcoffset() is not None,
             "ambiguous-time", "Time must include an explicit timezone")
        return parsed.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
    except (ValueError, OverflowError) as exc:
        if isinstance(exc, EvidenceError):
            raise
        raise EvidenceError("invalid-time", "Invalid RFC3339 time: " + str(value)) from exc


def epoch_time(value):
    if value is None:
        return None
    number_value(value)
    try:
        return datetime.fromtimestamp(value, timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
    except (ValueError, OverflowError, OSError) as exc:
        raise EvidenceError("invalid-time", "Invalid epoch time") from exc


def nonempty(value, label):
    need(isinstance(value, str) and bool(value.strip()), "missing-field", label + " must be a nonempty string")
    return value


def object_value(value, label):
    need(isinstance(value, dict), "invalid-object", label + " must be an object")
    return value


def safe_path(path):
    p = Path(os.path.abspath(os.path.expanduser(str(path))))
    for component in [p, *p.parents]:
        need(not component.is_symlink(), "unsafe-symlink", "Symlink path refused: " + str(component))
    return p


def within(path, root):
    return path == root or root in path.parents


def validate_output(output, roots):
    output = safe_path(output)
    for root in roots:
        root = safe_path(root)
        need(not within(output, root) and not within(root, output), "source-output-overlap",
             "Output and source paths must be disjoint: " + str(root))
    need(not output.exists() or output.is_dir(), "invalid-output", "Output must be a directory")
    return output


def atomic_json(path, value):
    atomic_bytes(path, json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode() + b"\n")


def atomic_bytes(path, content):
    path = safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    safe_path(path.parent)
    fd, temporary = tempfile.mkstemp(prefix=".observatory-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_json(content, max_depth=64):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            need(key not in out, "duplicate-json-key", "Duplicate JSON key: " + key)
            out[key] = value
        return out
    def invalid(value):
        raise EvidenceError("nonfinite-json", "Nonfinite JSON constant: " + value)
    try:
        value = json.loads(content, object_pairs_hook=unique, parse_constant=invalid)
    except (ValueError, UnicodeError, RecursionError) as exc:
        if isinstance(exc, EvidenceError):
            raise
        raise EvidenceError("invalid-json", str(exc)) from exc
    stack = [(value, 0)]
    while stack:
        item, depth = stack.pop()
        need(depth <= max_depth, "json-depth-limit", "JSON nesting limit exceeded")
        if isinstance(item, dict):
            stack.extend((v, depth + 1) for v in item.values())
        elif isinstance(item, list):
            stack.extend((v, depth + 1) for v in item)
        elif isinstance(item, float):
            need(math.isfinite(item), "nonfinite-json", "Nonfinite JSON number")
    return value


def fingerprint(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def inventory(root, limits):
    root = safe_path(root)
    need(root.exists(), "missing-source", "Source does not exist: " + str(root))
    if root.is_file():
        return [(root.name, root)]
    need(root.is_dir(), "unsafe-source-type", "Source must be a regular file or directory")
    found, pending, visited = [], [(root, 0)], 0
    while pending:
        directory, depth = pending.pop()
        need(depth <= limits["max_depth"], "traversal-depth-limit", "Directory nesting limit exceeded")
        for entry in sorted(directory.iterdir()):
            visited += 1
            need(visited <= limits["max_files"] * 4, "traversal-entry-limit", "Too many directory entries")
            info = entry.lstat()
            need(not stat.S_ISLNK(info.st_mode), "unsafe-symlink", "Symlink inside source: " + str(entry))
            if stat.S_ISDIR(info.st_mode):
                pending.append((entry, depth + 1))
            else:
                need(stat.S_ISREG(info.st_mode), "unsafe-source-type", "Nonregular source file: " + str(entry))
                found.append((entry.relative_to(root).as_posix(), entry))
                need(len(found) <= limits["max_files"], "file-count-limit", "Too many source files")
    return sorted(found)


def capture(root, limits):
    """Hash and parse the same captured bytes; retain stat/inventory race checks."""
    root = safe_path(root)
    entries = inventory(root, limits)
    data, stats, total = {}, {}, 0
    for relative, path in entries:
        safe_path(path)
        before = path.lstat()
        need(before.st_size <= limits["max_file_bytes"], "file-size-limit", "Source file too large: " + relative)
        need(before.st_mode & 0o444, "unreadable-source", "Source has no read permission: " + relative)
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as stream:
            opened = os.fstat(stream.fileno())
            need(stat.S_ISREG(opened.st_mode) and fingerprint(before) == fingerprint(opened),
                 "concurrent-source-change", "Source changed before capture: " + relative)
            content = stream.read(limits["max_file_bytes"] + 1)
            after = os.fstat(stream.fileno())
        need(len(content) <= limits["max_file_bytes"], "file-size-limit", "Source file too large: " + relative)
        need(fingerprint(before) == fingerprint(after) == fingerprint(path.lstat()),
             "concurrent-source-change", "Source changed during capture: " + relative)
        total += len(content)
        need(total <= limits["max_total_bytes"], "total-byte-limit", "Total source bytes exceeded")
        data[relative], stats[relative] = content, fingerprint(after)
    need([r for r, p in inventory(root, limits)] == [r for r, p in entries],
         "concurrent-source-change", "Source inventory changed during capture")
    for relative, path in entries:
        safe_path(path)
        need(fingerprint(path.lstat()) == stats[relative], "concurrent-source-change", "Source changed after capture: " + relative)
    files = [{"path": r, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)} for r, b in sorted(data.items())]
    return data, {"path": str(root), "files": files, "sha256": digest(files), "bytes": total}


def json_file(files, name, limits):
    need(name in files, "missing-required-file", "Required source file missing: " + name)
    return load_json(files[name], limits["max_json_depth"])


def read_json_files(files, names, limits):
    values = []
    for name in names:
        if name.endswith(".jsonl"):
            for index, line in enumerate(files[name].splitlines(), 1):
                if line.strip():
                    values.append((name + ":" + str(index), load_json(line, limits["max_json_depth"])))
        else:
            values.append((name, json_file(files, name, limits)))
    return values


def roots_config(path):
    path = safe_path(path)
    files, evidence = capture(path, DEFAULT_LIMITS)
    manifest = object_value(load_json(files[path.name]), "manifest")
    need(manifest.get("schema_version") == "1.0", "unsupported-manifest", "Manifest schema_version must be '1.0'")
    sources = manifest.get("sources")
    need(isinstance(sources, list) and sources, "missing-sources", "Manifest requires a nonempty explicit sources list")
    limits = dict(DEFAULT_LIMITS)
    for key, value in object_value(manifest.get("limits", {}), "manifest.limits").items():
        need(key in limits and type(value) is int and 0 < value <= limits[key], "invalid-limit", "Limits may only reduce documented defaults")
        limits[key] = value
    need(len(sources) <= limits["max_files"], "source-count-limit", "Too many registered sources")
    ids, out = set(), []
    for entry in sources:
        s = dict(object_value(entry, "source"))
        nonempty(s.get("id"), "source.id")
        need(s["id"] not in ids, "duplicate-source-id", "Duplicate source id: " + s["id"])
        ids.add(s["id"])
        need(s.get("profile") in PROFILES, "unsupported-profile", "Unsupported producer profile: " + str(s.get("profile")))
        nonempty(s.get("namespace"), "source.namespace")
        nonempty(s.get("path"), "source.path")
        source_path = Path(s["path"]).expanduser()
        s["path"] = str(safe_path(source_path if source_path.is_absolute() else path.parent / source_path))
        need(s.get("coherence", "best-effort") in {"best-effort", "frozen-export"}, "invalid-coherence", "Unknown capture assertion")
        s["coherence"] = s.get("coherence", "best-effort")
        out.append(s)
    return {"schema_version": "1.0", "sources": out, "limits": limits,
            "manifest_path": str(path), "manifest_sha256": evidence["sha256"]}


def base_record(source, run_id, revision, state, raw, pointers):
    nonempty(run_id, "run_id")
    if revision is not None:
        number_value(revision, integer=True)
    return {"producer": source["profile"].split("-legacy")[0].split("-snapshot")[0].split("-v2")[0],
            "namespace": source["namespace"], "run_id": run_id, "revision": revision,
            "profile": source["profile"], "status": state, "raw": raw,
            "field_pointers": pointers, "judgments": [], "measurements": [],
            "warnings": [], "source_ids": [source["id"]]}


def supplied(source, files, limits):
    need(Path(source["path"]).is_file() and len(files) == 1, "supplied-file-required", "supplied-v1 needs one JSON file, not a directory")
    name = next(iter(files))
    envelope = object_value(json_file(files, name, limits), "supplied envelope")
    need(envelope.get("schema_version") == "1.0", "unsupported-schema", "Supplied schema_version must be '1.0'")
    records = envelope.get("records")
    need(isinstance(records, list) and len(records) <= limits["max_records"], "invalid-records", "Expected bounded records list")
    result, errors = [], []
    for i, raw in enumerate(records):
        try:
            object_value(raw, "record")
            r = dict(raw)
            nonempty(r.get("producer"), "record.producer")
            nonempty(r.get("run_id"), "record.run_id")
            number_value(r.get("revision"), integer=True)
            nonempty(r.get("status"), "record.status")
            need(type(r.get("terminal")) is bool, "invalid-terminal", "Supplied terminal must be boolean")
            r.update(namespace=source["namespace"], profile=source["profile"], source_ids=[source["id"]],
                     field_pointers={k: name + "#/records/" + str(i) + "/" + k for k in raw},
                     warnings=[], raw=dict(raw))
            result.append(r)
        except (EvidenceError, TypeError) as exc:
            errors.append({"id": source["id"] + "#/records/" + str(i), "reason": getattr(exc, "code", "invalid-record"), "detail": str(exc)})
    return result, errors, "owner-asserted-frozen-export" if source["coherence"] == "frozen-export" else "single-captured-file"


def descriptive_telemetry(record, state):
    """Retain explicitly scoped legacy fields without inventing monetary units."""
    for field in ("duration_seconds", "tokens", "stop_reason", "escalation_reason", "judge_verdict", "human_label"):
        if field in state:
            record[field] = state[field]
            record["field_pointers"][field] = "state.json#/" + field
    if type(state.get("machine_completion")) is bool:
        record["machine_completion"] = state["machine_completion"]
    if type(state.get("human_acceptance")) is bool:
        record["raw_human_acceptance"] = state["human_acceptance"]
    usage = state.get("usage")
    if isinstance(usage, dict):
        record["raw_usage"] = usage
        if type(usage.get("tokens")) is int and usage["tokens"] >= 0:
            record["tokens"] = usage["tokens"]
            record["field_pointers"]["tokens"] = "state.json#/usage/tokens"
    if any(key in state for key in ("cost", "cost_usd", "total_cost", "usage")):
        record["warnings"].append("Legacy usage/cost retained descriptively; measurement basis, currency, inclusive scope and charge identity are not inferred.")
    return record


def legacy_loopkit(source, files, limits):
    s = object_value(json_file(files, "state.json", limits), "LoopKit state")
    c = object_value(json_file(files, "contract.json", limits), "LoopKit contract")
    need(s.get("schema_version", 1) == 1 and c.get("schema_version", 1) == 1, "unsupported-schema", "Legacy LoopKit schema must be 1")
    need(s.get("status") in LOOPKIT_STATES, "unsupported-status", "Unknown LoopKit state")
    if c.get("run_id") is not None:
        need(s.get("run_id") == c["run_id"], "run-binding-mismatch", "State and contract run_id differ")
    r = base_record(source, s.get("run_id"), s.get("generation"), s["status"], {"state": s, "contract": c},
                    {"run_id": "state.json#/run_id", "revision": "state.json#/generation", "status": "state.json#/status",
                     "iteration": "state.json#/iteration", "goal": "contract.json#/goal"})
    r.update(terminal=s["status"] in LOOPKIT_TERMINAL, process_completion=s["status"] == "completed",
             iteration=s.get("iteration"), goal=c.get("goal", c.get("objective")), model=c.get("model"),
             version=c.get("version", c.get("schema_version")), event_time=s.get("updated_at", s.get("completed_at")),
             known_time=s.get("updated_at", s.get("completed_at")), stop_reason=s.get("stop_reason"), escalation_reason=s.get("escalation_reason"))
    receipts = read_json_files(files, sorted(n for n in files if n.startswith("evidence/receipts/") and n.endswith(".json")), limits)
    matching = [(name, x) for name, x in receipts if isinstance(x, dict) and x.get("run_id") == s.get("run_id") and x.get("iteration") == s.get("iteration")]
    need(len(matching) <= 1, "conflicting-current-receipts", "Multiple current-iteration receipts")
    r["raw"]["receipts"] = [{"path": name, "value": x} for name, x in receipts]
    descriptive_telemetry(r, s)
    if matching:
        name, receipt = matching[0]
        receipt_status = receipt.get("status")
        transitions = {
            "draft": {"ready", "cancelled", "failed"}, "ready": {"running", "scheduled", "cancelled", "failed"},
            "running": {"waiting_input", "scheduled", "blocked", "exhausted", "failed", "cancelled"},
            "waiting_input": {"running", "blocked", "cancelled", "failed"},
            "scheduled": {"running", "blocked", "cancelled", "failed"},
            "blocked": {"running", "cancelled", "failed"}}
        changed_since_receipt = receipt_status != s["status"]
        if changed_since_receipt:
            # transition_run changes state/generation without consuming an iteration.
            # Only a NEW receipt may enter completed; terminal receipts cannot reopen.
            reachable, pending = set(), [receipt_status]
            while pending:
                candidate = pending.pop()
                for target in transitions.get(candidate, set()):
                    if target not in reachable:
                        reachable.add(target)
                        pending.append(target)
            need(s["status"] in reachable, "receipt-state-mismatch", "Receipt/state mismatch cannot be explained by permitted no-iteration transitions")
        checks = receipt.get("checks", [])
        need(isinstance(checks, list) and all(isinstance(x, dict) and type(x.get("passed")) is bool for x in checks),
             "invalid-receipt-checks", "Current receipt checks need objects with boolean passed fields")
        if changed_since_receipt:
            r["judge_verdict"], r["machine_completion"] = None, None
            r["historical_receipt_pointer"] = name + "#"
            r["field_pointers"].pop("machine_completion", None)
            r["field_pointers"].pop("judge_verdict", None)
            r["warnings"].append("Current state has advanced through a supported no-iteration transition; the matching-iteration receipt is historical, so its checks are not promoted to current judgment.")
        else:
            r["judge_verdict"] = receipt.get("judgments")
            r["machine_completion"] = all(x["passed"] for x in checks) if checks else None
            r["field_pointers"]["machine_completion"] = name + "#/checks"
            r["field_pointers"]["judge_verdict"] = name + "#/judgments"
    r["warnings"].append("Legacy receipts lack exact artifact/rubric/human identity bindings; raw judgments are not calibration pairs.")
    return [r], [], "owner-asserted-frozen-export" if source["coherence"] == "frozen-export" else "best-effort-multifile"


def loopkit_snapshot(source, files, limits):
    name = "snapshot.json" if "snapshot.json" in files else next(iter(files), "snapshot.json")
    envelope = object_value(json_file(files, name, limits), "LoopKit snapshot")
    s = object_value(envelope.get("state"), "snapshot.state")
    need(envelope.get("sha256") == digest(s), "snapshot-integrity", "LoopKit snapshot digest mismatch")
    need(s.get("schema") == 1, "unsupported-schema", "Accepted LoopKit state schema must be 1")
    c = object_value(s.get("contract"), "snapshot contract")
    need(s.get("contract_sha256") == digest(c), "contract-integrity", "LoopKit contract digest mismatch")
    need(s.get("status") in LOOPKIT_STATES, "unsupported-status", "Unknown LoopKit state")
    number_value(s.get("generation"), integer=True)
    r = base_record(source, s.get("run_id"), s["generation"], s["status"], {"state": s},
                    {"run_id": name + "#/state/run_id", "revision": name + "#/state/generation", "status": name + "#/state/status",
                     "iteration": name + "#/state/iterations", "goal": name + "#/state/contract/outcome"})
    r.update(terminal=s["status"] in LOOPKIT_TERMINAL, process_completion=s["status"] == "completed",
             iteration=s.get("iterations"), goal=c.get("outcome"), model=None, version="accepted-schema-1",
             event_time=epoch_time(s.get("updated_epoch")), known_time=epoch_time(s.get("updated_epoch")),
             task=s.get("contract_sha256"), artifact=digest(s["last_artifacts"]) if s.get("last_artifacts") else None,
             stop_reason=s.get("stop_reason"), escalation_reason=s.get("next_action") if s["status"] in {"blocked", "waiting_input"} else None)
    r["judge_verdict"] = s.get("reviews", [])
    r["warnings"].append("Snapshot and contract hashes verified. Embedded checks/reviews retained; external logs, workspace artifacts and review evidence were not independently verified or followed.")
    return [r], [], "verified-single-envelope"


def legacy_graph(source, files, limits):
    s = object_value(json_file(files, "state.json", limits), "Graph state")
    g = object_value(json_file(files, "graph.json", limits), "Graph definition")
    need(s.get("recordVersion", 1) == 1, "unsupported-schema", "Use operating-graph-v2 for protocol 2")
    need(s.get("status") in GRAPH_STATES, "unsupported-status", "Unknown Graph status")
    events = read_json_files(files, ["events.jsonl"] if "events.jsonl" in files else [], limits)
    run_id = s.get("runId", s.get("run_id"))
    sequences = [e["sequence"] for n, e in events if isinstance(e, dict) and e.get("runId") == run_id and type(e.get("sequence")) is int]
    revision = s.get("generation", max(sequences) if sequences else None)
    event_times = [e.get("timestamp") for n, e in events if isinstance(e, dict) and e.get("runId") == run_id and e.get("sequence") == revision]
    r = base_record(source, run_id, revision, s["status"], {"state": s, "graph": g, "events": [e for n, e in events]},
                    {"run_id": "state.json#/runId", "status": "state.json#/status", "version": "state.json#/graphVersion",
                     "iteration": "state.json#/totalNodeRuns", "revision": "events.jsonl#/sequence"})
    r.update(terminal=s["status"] in GRAPH_TERMINAL, process_completion=s["status"] == "completed",
             iteration=s.get("totalNodeRuns", s.get("iteration")), goal=g.get("goal"), model=g.get("model"),
             version=s.get("graphVersion"), event_time=event_times[-1] if event_times else s.get("updated_at"),
             known_time=event_times[-1] if event_times else s.get("updated_at"), stop_reason=s.get("stop_reason"),
             escalation_reason=s.get("escalation_reason"), judge_verdict=s.get("judge_verdict"), human_label=s.get("human_label"))
    descriptive_telemetry(r, s)
    r["warnings"].append("Legacy state is a captured projection; nested node success and approval records are never whole-run acceptance.")
    return [r], [], "owner-asserted-frozen-export" if source["coherence"] == "frozen-export" else "best-effort-multifile"


def graph_v2(source, files, limits):
    commits = sorted(n for n in files if re.fullmatch(r"commits/\d{8}\.json", n))
    previous, run_id, operations, snapshots = None, None, set(), []
    if commits:
        for sequence, name in enumerate(commits, 1):
            record = object_value(json_file(files, name, limits), "Graph commit")
            need(record.get("recordVersion") == 2, "unsupported-schema", "Graph committed record version must be 2")
            unsigned = {k: v for k, v in record.items() if k != "sha256"}
            need(record.get("sha256") == digest(unsigned, newline=True), "commit-integrity", "Graph commit digest mismatch: " + name)
            need(record.get("sequence") == sequence and name == f"commits/{sequence:08d}.json" and record.get("previousSha256") == previous,
                 "commit-chain-integrity", "Incomplete or inconsistent Graph commit chain")
            need(record.get("operationId") not in operations, "duplicate-operation", "Repeated Graph operationId")
            operations.add(record.get("operationId"))
            s = object_value(record.get("data"), "Graph commit data")
            need(s.get("generation") == sequence and s.get("recordVersion") == 2, "generation-integrity", "Graph commit generation mismatch")
            need(run_id is None or run_id == s.get("runId"), "run-binding-mismatch", "Graph committed run identity changed")
            run_id, previous = s.get("runId"), record["sha256"]
            need(isinstance(s.get("objects"), list), "missing-closure", "Graph object closure is missing")
            for sha in s["objects"]:
                need(isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha), "invalid-object-id", "Invalid Graph content hash")
                key = "objects/" + sha
                need(key in files, "missing-closure", "Graph committed object missing: " + sha)
                need(hashlib.sha256(files[key]).hexdigest() == sha, "object-integrity", "Graph object content mismatch: " + sha)
            snapshots.append((s, record.get("timestamp"), name + "#/data"))
        coherence = "verified-immutable-commit-object-closure"
    else:
        need(len(files) == 1, "missing-closure", "Graph protocol 2 directory needs complete commits and object closure")
        name = next(iter(files))
        export = object_value(json_file(files, name, limits), "Graph export")
        need("previousSha256" not in export and "data" not in export, "missing-closure", "A bare commit cannot prove its missing chain/object closure")
        need(source["coherence"] == "frozen-export", "missing-closure", "State-only export requires explicit frozen-export assertion")
        s = export.get("state", export)
        snapshots = [(object_value(s, "Graph state"), export.get("exported_at"), name + ("#/state" if "state" in export else "#"))]
        coherence = "owner-asserted-frozen-export"
    out = []
    for s, event, ptr in snapshots:
        need(s.get("recordVersion") == 2, "unsupported-schema", "Graph state recordVersion must be 2")
        need(s.get("status") in GRAPH_STATES, "unsupported-status", "Unknown Graph status")
        g = object_value(s.get("graph"), "Graph definition")
        need(isinstance(s.get("versions"), dict) and s["versions"].get(str(s.get("graphVersion"))) == g,
             "graph-version-integrity", "Current Graph version is not bound to definition")
        r = base_record(source, s.get("runId"), s.get("generation"), s["status"], {"state": s},
                        {"run_id": ptr + "/runId", "revision": ptr + "/generation", "status": ptr + "/status",
                         "version": ptr + "/graphVersion", "iteration": ptr + "/totalNodeRuns"})
        r.update(terminal=s["status"] in GRAPH_TERMINAL, process_completion=s["status"] == "completed",
                 iteration=s.get("totalNodeRuns"), goal=g.get("goal"), model=g.get("model"), version=s.get("graphVersion"),
                 event_time=event, known_time=event, task=s.get("graphId"),
                 stop_reason=s.get("stopReason"), escalation_reason=s.get("escalationReason"), judge_verdict=s.get("verification"))
        r["warnings"].append("Graph verification and approvals are preserved as producer evidence, not human output acceptance or a matched calibration label.")
        out.append(r)
    return out, [], coherence


ADAPTERS = {"supplied-v1": supplied, "loopkit-legacy": legacy_loopkit,
            "loopkit-snapshot-v2": loopkit_snapshot, "operating-graph-legacy": legacy_graph,
            "operating-graph-v2": graph_v2}


def normalize(source, files, limits):
    return ADAPTERS[source["profile"]](source, files, limits)
