#!/usr/bin/env python3
"""Thin checkpoint hook. Registration/trust belongs to the host adapter."""
import argparse
import json
import os
import sys
from lk_state import Fault, need, clean_path, locked, load, atomic
from loopkit import checkpoint
from lk_binding import resolve, canonical


def main():
    p = argparse.ArgumentParser()
    p.add_argument("event", choices=["pre-compact", "session-start"])
    p.add_argument("--host", required=True, choices=["codex", "claude-code"])
    p.add_argument("--run", default=None, help="explicit selection written into the host registration; no env fallback")
    p.add_argument("--state-root", default=None)
    args = p.parse_args()
    try:
        raw = sys.stdin.buffer.read(65537)
        need(len(raw) <= 65536, "hook-input", "Hook payload is too large")
        payload = json.loads(raw) if raw.strip() else {}
        need(isinstance(payload, dict) and isinstance(payload.get("cwd"), str), "hook-input", "Host cwd is required")
        if args.event == "session-start" and payload.get("source", "startup") not in {"startup", "resume", "compact"}:
            return 0
        selected = canonical(args.run) if args.run else resolve(payload["cwd"], args.host, args.state_root)
        if selected is None:
            return 0
        with locked(selected) as root:
            s = load(root)
            need(s["contract"]["host"] == args.host, "hook-host", "Run belongs to another host")
            need(str(canonical(payload["cwd"])) == s["workspace"], "hook-workspace", "Run does not match the invoking workspace")
            if s["status"] in {"completed", "cancelled", "failed", "exhausted"}:
                return 0
            text = checkpoint(s)
            atomic(root / "checkpoint.txt", text.encode("utf-8"))
        if args.event == "session-start":
            response = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text}}
            output = json.dumps(response, ensure_ascii=False)
            if len(output.encode("utf-8")) > 4096:
                response["hookSpecificOutput"]["additionalContext"] = "Read LoopKit snapshot.json at " + str(root)
                output = json.dumps(response, ensure_ascii=False)
            need(len(output.encode("utf-8")) <= 4096, "hook-output", "Checkpoint pointer exceeds output budget")
            print(output)
        return 0
    except (Fault, OSError, ValueError, KeyError, TypeError) as exc:
        message = "LoopKit checkpoint unavailable (" + getattr(exc, "code", type(exc).__name__) + "). Inspect the selected run; do not infer restored state."
        print(message, file=sys.stderr)
        if args.event == "session-start":
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": message}}))
        return 0  # Visible diagnostic; never brick an unrelated host session.


if __name__ == "__main__":
    sys.exit(main())
