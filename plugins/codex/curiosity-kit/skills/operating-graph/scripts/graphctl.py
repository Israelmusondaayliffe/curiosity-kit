#!/usr/bin/env python3
"""Public Operating Graph CLI. Graph schema 1.0; committed run/packet protocol 2.

All 17 original command names remain discoverable. Unsafe raw transition and
artifact-registration mutations explicitly require the guarded lifecycle instead.
verify is now read-only; successful terminal mutation is explicit finalize.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

from graph_engine.runtime import Runtime
from graph_engine.storage import RuntimeErrorBase, CorruptionError, ConversionNeeded
from graph_engine.validation import require_valid_graph, GraphValidationError
from graph_engine.models import Graph
from graph_engine.rewrites import RewriteError
from graph_engine.reporting import render_mermaid, render_runtime_text


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError,ValueError) as exc:
        raise RuntimeErrorBase("cannot read JSON: " + str(exc)) from exc


def parser():
    root = argparse.ArgumentParser(prog="graphctl",description=__doc__)
    subs = root.add_subparsers(dest="command",required=True)
    def add(name, *, run=True, mutate=False):
        p = subs.add_parser(name)
        p.add_argument("--json",action="store_true",dest="json_output")
        if run:
            p.add_argument("run_directory")
        if mutate:
            p.add_argument("--operation-id")
            p.add_argument("--expected-generation",type=int)
        return p
    p = add("validate",run=False); p.add_argument("graph")
    p = add("init",run=False,mutate=True); p.add_argument("graph"); p.add_argument("--run-root",required=True); p.add_argument("--contract")
    for name in ("status","ready","dispatch-preview","replay","resume-check","recover","verify","finalize","advance-epoch"):
        p = add(name,mutate=name in {"finalize","advance-epoch"})
        if name in {"ready","dispatch-preview"}:
            p.add_argument("--available-slots",type=int)
            p.add_argument("--lane",choices=("subagent","inline","human","tool"))
    p = add("prepare-dispatch",mutate=True); p.add_argument("--node",dest="node_id"); p.add_argument("--lane",choices=("subagent","inline","human","tool"),default="subagent"); p.add_argument("--available-slots",type=int)
    p = add("begin-launch",mutate=True); p.add_argument("invocation_id")
    for name,arg in (("record-launch","record"),("ingest-return","packet"),("record-approval","record"),("settle","record"),("propose-rewrite","proposal")):
        p = add(name,mutate=True); p.add_argument(arg)
    p = add("apply-rewrite",mutate=True); p.add_argument("proposal_id")
    p = add("withdraw-rewrite",mutate=True); p.add_argument("proposal_id"); p.add_argument("--reason",required=True)
    for name in ("cancel-run","cancel-node","omit-node"):
        p = add(name,mutate=True)
        if name != "cancel-run": p.add_argument("node_id")
        p.add_argument("--reason",required=True)
    p = add("transition",mutate=True); p.add_argument("node_id"); p.add_argument("status")
    p = add("register-artifact",mutate=True); p.add_argument("node_id"); p.add_argument("artifact_type"); p.add_argument("path")
    p = add("signal",mutate=True); p.add_argument("name"); p.add_argument("value")
    p = add("inspect"); p.add_argument("--format",choices=("text","mermaid"),default="text")
    return root


def execute(args):
    cmd = args.command
    if cmd == "validate":
        graph = require_valid_graph(read_json(args.graph))
        return {"valid":True,"graphId":graph.graph_id,"graphSchemaVersion":"1.0","runtimeRecordVersion":2}
    options = {}
    if hasattr(args,"operation_id") and args.operation_id:
        options["operation_id"] = args.operation_id
    if hasattr(args,"expected_generation") and args.expected_generation is not None:
        options["expected_generation"] = args.expected_generation
    if cmd == "init":
        if "expected_generation" in options:
            raise RuntimeErrorBase("init does not accept expected generation")
        rt = Runtime.create(read_json(args.graph),args.run_root,contract=read_json(args.contract) if args.contract else None,**options)
        return {"runId":rt.load()["runId"],"runDirectory":str(rt.root),"recordVersion":2,"state":rt.load()}
    rt = Runtime(args.run_directory)
    if cmd == "status": return rt.status()
    if cmd in {"ready","dispatch-preview"}:
        return rt.ready(lane=args.lane or ("subagent" if cmd == "dispatch-preview" else None),available_slots=args.available_slots)
    if cmd == "prepare-dispatch": return rt.prepare(node_id=args.node_id,lane=args.lane,available_slots=args.available_slots,**options)
    if cmd == "begin-launch": return rt.begin_launch(args.invocation_id,**options)
    if cmd == "record-launch": return rt.record_launch(read_json(args.record),**options)
    if cmd == "record-approval": return rt.record_approval(read_json(args.record),**options)
    if cmd == "ingest-return": return rt.ingest(read_json(args.packet),return_path=args.packet,**options)
    if cmd == "settle": return rt.settle(read_json(args.record),**options)
    if cmd == "propose-rewrite": return rt.propose(read_json(args.proposal),**options)
    if cmd == "apply-rewrite": return rt.apply_rewrite(args.proposal_id,**options)
    if cmd == "withdraw-rewrite": return rt.withdraw_rewrite(args.proposal_id,reason=args.reason,**options)
    if cmd in {"cancel-run","cancel-node"}: return rt.cancel(node_id=getattr(args,"node_id",None),reason=args.reason,**options)
    if cmd == "omit-node": return rt.omit(args.node_id,reason=args.reason,**options)
    if cmd == "signal":
        try: value = json.loads(args.value)
        except ValueError: value = args.value
        return rt.signal(args.name,value,**options)
    if cmd == "advance-epoch": return rt.advance_epoch(**options)
    if cmd == "verify": return rt.verify()
    if cmd == "finalize": return rt.finalize(**options)
    if cmd == "recover": return rt.recover()
    if cmd == "replay": return rt.replay()
    if cmd == "resume-check":
        status = rt.status()
        return {"resumable":status["state"]["status"] == "running","state":status["state"],"obligations":status["obligations"],"readOnly":True}
    if cmd == "inspect":
        status = rt.status()
        if args.format == "mermaid":
            report = render_mermaid(Graph.from_dict(status["state"]["graph"]),status["state"],status["state"].get("verification"))
            return {"format":"mermaid","content":report,"report":report,"readOnly":True}
        return {**status,"format":"text","report":render_runtime_text(status),"readOnly":True}
    if cmd in {"transition","register-artifact"}:
        rt.load()
        raise ConversionNeeded("superseded unsafe mutation: use prepare-dispatch, begin-launch, record-launch and ingest-return for every lane; cancel/omit have dedicated guarded commands")
    raise RuntimeErrorBase("unknown command")


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        result = execute(args)
        code = 2 if (args.command == "verify" and result["status"] != "pass") or (args.command == "begin-launch" and result.get("authorized") is False) else 0
    except (RuntimeErrorBase,RewriteError,GraphValidationError,ValueError,KeyError,TypeError,OSError) as exc:
        result = {"error":str(exc),"errorType":type(exc).__name__}
        code = getattr(exc,"code",2)
    print(json.dumps(result,indent=None if args.json_output else 2,sort_keys=True,ensure_ascii=False,allow_nan=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
