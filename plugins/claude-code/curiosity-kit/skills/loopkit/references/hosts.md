# Host binding and hooks

The domain method is shared. Registration, trust, invocation payloads and scheduler/Goal controls belong to the actual host. Both Codex and Claude Code qualification must exercise the relevant surface; no Cowork parity is inferred.

## Selected run

Use the durable [workspace binding](binding.md) after initialization or explicit selection. The hook uses an explicit `--run` in its registration if present; otherwise it reads that workspace's exact owned pointer. No environment variable selects a run. No scans or newest-run selection. No pointer means inactivity. It validates the payload's canonical `cwd`, host and snapshot identity, with visible errors for invalid bindings. Intentional root aliases are canonicalized; pointer symlink substitution is rejected.

## Adapter interface

```text
python3 "/absolute/package/skills/loopkit/scripts/loopkit_hook.py" pre-compact --host codex
python3 "/absolute/package/skills/loopkit/scripts/loopkit_hook.py" session-start --host codex
```

Use `claude-code` for that host. Bind actual package paths through the supported host variable at integration and quote the complete path, including spaces. The coordinator emits the exact host registration; this skill supplies no duplicate default-plus-manifest hook registrations. Register each owning event once.

PreCompact refreshes a derived checkpoint. SessionStart restores on startup, resume and compact, and on Claude Code also on fork (forked sessions report source `fork` there); Codex sources are unchanged. The checkpoint is an index with the authoritative run pointer, workspace, generation, outcome, committed units, next action and pending-work warning. Oversized content becomes a short pointer; actual emitted JSON is capped at 4096 bytes. Hooks do not read transcripts, invoke model/provider calls, create schedules, execute the loop or modify artifacts.

Terminal runs are inactive. Missing selection is silent; malformed input, corruption, lock conflict or wrong binding emits a concise visible error. A visible hook error means state was not restored. Read the named run directly before continuing. A failure must not be silently treated as successful restoration.

## Qualification

In an authorized disposable environment, prove native registration/trust and actual event delivery. Check active run, inactive/unselected run, wrong workspace/host, startup/resume/compact, bounded output, interruption and cleanup. Direct script invocation tests only the adapter logic. Preserve evidence after removing only test-owned settings/processes; keep the live harness unchanged. Never bypass trust to make a test green.

### Native hook recipe

A repeatable native check that touches no real state:

1. Create a disposable workspace and run, and bind them with `LOOPKIT_STATE_ROOT` pointing at a disposable directory.
2. Start a fresh headless host session in that workspace with the same `LOOPKIT_STATE_ROOT` exported to the host process. The SessionStart event should write `checkpoint.txt`; confirm it from the host's own hook-response records.
3. Compact that same session through the host (for Claude Code, resume it and send `/compact`). Confirm the PreCompact event from the host's transcript line naming the hook, not from a manual call.
4. Unbind the fixture and confirm the real state root holds no new binding.

Running `loopkit_hook.py` directly is a script check only. Label it that way and never count it as native event delivery.

## Goals and schedules

Create a native Goal only on an explicit user request and an available supported surface. It is a view of the task, not the source of LoopKit state. Scheduling is separately authorized and uses current supported host controls. Availability, activation and observed execution are separate facts. See [schedule](schedule.md). Do not bake product names, old slash commands or speculative cloud behavior into permanent runtime assumptions.
