# Prepare and observe recurrence

Use the actual supported host scheduler when the user requests recurrence. No cron, daemon or endless shell-loop substitute. No stale product assumptions: inspect the current available surface and official guidance if binding it requires information not already verified. Local LoopKit state is not a scheduler, and writing a record schedules nothing.

## Readiness

Require a successful manual run using the same relevant tools/permissions, an explicit cadence and timezone, a self-contained task prompt, clean no-op behavior, evidence on meaningful changes, and a stop/pause condition. Check UI capability when the task needs browser/computer access. A missing dependency is blocked, not “nothing changed.” Scheduling activation and recurring external actions need their own bounded authority.

Use [schedule schema](../references/schedule.md). Prepare the record only after verifying the manual run against current artifacts. Keep a reusable contract separate from terminal run instances: each recurring invocation needs its own bounded execution record, tied to the schedule id; do not force a completed run back to running or overwrite prior results.

## Lifecycle

1. Prepare the schedule draft locally. State clearly that it is prepared only.
2. With applicable authority, use the host's supported scheduling control. Inspect the returned actual identifier, cadence, timezone, enabled status and task input. Capture the host response. If creation is uncertain, read the host before retrying; never create duplicates blindly.
3. Record activation with the real host id, surface, authorization reference and evidence. A successful local record operation confirms bookkeeping, not that the host was contacted.
4. Observe a real scheduled execution and inspect its result/artifact or valid no-op. Link the real execution id, host evidence and result-verification evidence. An activation response alone is not an execution receipt.
5. Respect explicit manual-run and side-effect counts: test no-op and stop behavior in a disposable copy without rerunning or mutating the user workspace, and preserve supplied tools during prepare-only work; if a tool lacks the requested behavior, name the gap and prepare a minimal wrapper or proposal in authorized task storage without changing the original tool or activating a schedule. Missing inspection or permission remains failed/blocked, never a clean no-op; pause/remove a test schedule through the host only when covered by its test authority, then capture the host confirmation.
6. Report precisely: prepared, active but unobserved, observed, attention required, paused or stopped. A missed/failed run cannot be reported as scheduled success.

For ambiguous results, use read-only host inspection first. Do not weaken permissions or change cadence merely to clear an error. Preserve historical observations and the manual-run evidence. Use native schedule controls for activation/pause/removal; the local CLI deliberately cannot perform those actions.
