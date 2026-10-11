#!/usr/bin/env python3
"""LoopKit CLI: local state, captured execution, verification, and recovery."""
import argparse
import json
import sys
from pathlib import Path
from lk_state import Fault, need, read_json, validate, initialize, load, locked, atomic, encoded, artifacts, nonempty
from lk_run import execute, finish, review, pause, resume, reconcile, reopen, check_unit, TERMINAL
from lk_schedule import prepare, observe
from lk_binding import bind, unbind


def summary(s):
    return {k: s.get(k) for k in ("run_id", "run_path", "generation", "status", "unit_index", "iterations",
                                   "no_progress", "next_action", "pending", "reopened", "rechecks")}


def checkpoint(s):
    lines = ["LoopKit checkpoint (index only; reread the authoritative snapshot)",
             "Run: " + s["run_path"], "Workspace: " + s["workspace"],
             "Generation: " + str(s["generation"]), "Status: " + s["status"],
             "Outcome: " + s["contract"]["outcome"],
             "Verified units: " + ", ".join(x["id"] for x in s["verified_units"]),
             "Next: " + s["next_action"],
             "In-flight work requires reconciliation before replay." if s["pending"] else "No recorded in-flight action."]
    text = "\n".join(lines)
    if len(text.encode("utf-8")) > 3000:
        text = "LoopKit checkpoint is oversized. Read snapshot.json in run: " + s["run_path"]
    need(len(text.encode("utf-8")) <= 3500, "checkpoint-too-large", "Run pointer exceeds hook output limit")
    return text


def diagnose(run):
    findings = []
    def add(code, evidence, recovery):
        findings.append({"code": code, "evidence": evidence, "recovery": recovery})
    try:
        s = load(run)
    except Fault as exc:
        add(exc.code, str(exc), "Preserve corrupt files; compare a known intact snapshot. Do not reconstruct success from narrative")
        return {"findings": findings, "completion_verified": False}
    if s["pending"]:
        add("uncertain-action", s["pending"], "Inspect the exact action's real effects and executor liveness; reconcile before resume")
    if artifacts(s) != s["last_artifacts"]:
        add("workspace-drift", "Current artifact digests differ from last observation", "Inspect changes and rerun the affected checks; preserve user edits")
    if s["status"] == "exhausted" or (s.get("budget_reached") and s["status"] != "completed"):
        add("budget-stop", {"iterations": s["iterations"], "no_progress": s["no_progress"]}, "Report unfinished units; changing the agreed budget needs task authority")
    units = s["contract"]["units"]
    for index, u in enumerate(units[:s["unit_index"] + (s["unit_index"] < len(units))]):
        try:
            check_unit(s, Path(run).resolve(), u)
        except (Fault, OSError) as exc:
            done = index < s["unit_index"]
            add(getattr(exc, "code", "evidence-unavailable"), {"unit": u["id"], "committed": done, "detail": str(exc)},
                ("Committed unit: run check --unit " + u["id"] + " --execute; if it still fails, reopen --unit " + u["id"] +
                 " with the observed cause, redo it, finish it. Other verified units stay valid") if done else
                "Reproduce the named check failure, inspect captured output, make one scoped repair, then rerun the exact symptom check")
    sched = s.get("schedule")
    schedule = None
    if sched:
        observed = [h for h in sched["history"] if h.get("event") in {"execution", "no-op"} and h.get("result") in {"success", "no-op"}]
        schedule = {"status": sched["status"], "host_id": sched.get("host_id"), "observed_executions": len(observed),
                    "last_observed_execution": observed[-1].get("execution_id") if observed else None}
        if sched["status"] == "attention-required":
            add("schedule-attention", schedule, "Inspect the failed or blocked host execution; do not report the schedule as working")
        elif sched["status"] != "observed" and not (sched["status"] in {"paused", "stopped"} and observed):
            add("schedule-unproven", schedule, "Inspect the actual host schedule and first execution; preparation is not activation")
    return {"run_id": s["run_id"], "status": s["status"], "findings": findings, "schedule": schedule,
            "completion_verified": s["status"] == "completed" and all(f["code"].startswith("schedule-") for f in findings)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate"); v.add_argument("contract")
    i = sub.add_parser("init"); i.add_argument("contract"); i.add_argument("--run", required=True); i.add_argument("--workspace", required=True)
    for command in ("bind", "unbind"):
        q = sub.add_parser(command); q.add_argument("run"); q.add_argument("--workspace", required=True)
        q.add_argument("--host", required=True, choices=["codex", "claude-code"]); q.add_argument("--state-root", default=None)
        if command == "bind":
            q.add_argument("--replace-run", default=None)
    for command in ("status", "doctor", "checkpoint"):
        q = sub.add_parser(command); q.add_argument("run")
    for command in ("run-unit", "check", "finish", "review", "stop", "resume", "reconcile", "reopen",
                    "schedule-prepare", "schedule-observe"):
        q = sub.add_parser(command); q.add_argument("run"); q.add_argument("--expected-generation", type=int, required=True)
        if command in ("check", "review", "reopen"):
            q.add_argument("--unit", required=command == "reopen", help="a committed unit (check: recheck only; review: refresh)")
        if command in ("run-unit", "check"):
            q.add_argument("--execute", action="store_true")
        if command in ("review", "reconcile", "schedule-prepare", "schedule-observe"):
            q.add_argument("--note", required=True, help="JSON file (schedule-prepare: draft; schedule-observe: host observation)")
        if command in ("stop", "resume", "reopen"):
            q.add_argument("--reason", required=True)
        if command == "resume":
            q.add_argument("--acknowledge-drift", action="store_true",
                           help="record inspected artifact changes; affected units stay stale until rechecked or reopened")
        if command == "stop":
            q.add_argument("--status", required=True, choices=["paused", "blocked", "waiting_input", "cancelled", "failed", "exhausted"])
    args = p.parse_args()
    try:
        c = args.command
        if c == "bind":
            out = bind(args.run, args.workspace, args.host, args.state_root, args.replace_run)
        elif c == "unbind":
            out = unbind(args.run, args.workspace, args.host, args.state_root)
        elif c == "validate":
            validate(read_json(args.contract)); out = {"valid": True}
        elif c == "init":
            out = summary(initialize(read_json(args.contract), args.run, args.workspace))
        elif c == "status":
            out = summary(load(args.run))
        elif c == "doctor":
            out = diagnose(args.run)
        elif c == "checkpoint":
            with locked(args.run) as root:
                s = load(root)
                text = checkpoint(s)
                atomic(root / "checkpoint.txt", text.encode("utf-8"))
                out = {"generation": s["generation"], "path": str(root / "checkpoint.txt"), "bytes": len(text.encode("utf-8"))}
        elif c in ("run-unit", "check"):
            out = summary(execute(args.run, args.expected_generation, c == "run-unit", args.execute, getattr(args, "unit", None)))
        elif c == "finish":
            out = summary(finish(args.run, args.expected_generation))
        elif c == "review":
            out = summary(review(args.run, args.expected_generation, read_json(args.note), args.unit))
        elif c == "reopen":
            out = summary(reopen(args.run, args.expected_generation, args.unit, args.reason))
        elif c == "stop":
            out = summary(pause(args.run, args.expected_generation, args.status, args.reason))
        elif c == "resume":
            out = summary(resume(args.run, args.expected_generation, args.reason, args.acknowledge_drift))
        elif c in ("schedule-prepare", "schedule-observe"):
            s = (prepare if c == "schedule-prepare" else observe)(args.run, args.expected_generation, read_json(args.note))
            out = summary(s); out["schedule"] = s["schedule"]
        else:
            out = summary(reconcile(args.run, args.expected_generation, read_json(args.note)))
        print(json.dumps(out, sort_keys=True, ensure_ascii=False))
        return 1 if c == "doctor" and out["findings"] else 0
    except (Fault, OSError, KeyError, TypeError, StopIteration) as exc:
        print(json.dumps({"error": getattr(exc, "code", "invalid-state-or-input"), "detail": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
