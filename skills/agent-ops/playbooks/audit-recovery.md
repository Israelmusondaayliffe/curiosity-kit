# Audit, rescue and handoff

## Read-only system audit

Collect the actual instructions, tools, state/receipts, observed failure and current source artifacts. An audit request authorizes inspection and the requested report, not executing the system or applying fixes. Classify each control as supported, failed or unknown, with evidence and the smallest remedy:

1. Outcome: bounded end state, not activity alone.
2. Evidence: inspectable proof of required results.
3. Authority: explicit allowed tools, systems, writes and external actions.
4. Stops: success, failure, blocked, exhaustion and escalation.
5. State: sufficient continuity for the work's interruption risk.
6. Tool contracts: usable inputs, outputs, errors and permissions.
7. Recovery: bounded retry or alternate path that preserves prior work.
8. Cost: appropriate finite execution/resource boundaries and honest observations.
9. Observability: inspectable progress, failures and child accounting.
10. Verification: required checks independent of the worker's assertion.

Cover all ten, including controls with no finding. Unknown evidence never passes silently. Give each finding a unique ID, affected control, severity (blocker/high/medium/low), source location and remedy. Missing essential authority, stop conditions or a defensible verification path blocks execution. Distinguish a well-formed report from a safe working system.

Map common symptoms carefully: wrong done may mean missing checks; endless retries may mean no stopping rule; flaky tool use may mean ambiguous parameters; cost without progress may mean an overbuilt pattern. Trace actual callers and evidence before assigning cause. Preserve legitimate dissent and explain dismissed findings. Do not infer a recurrent defect from one run.

## Bounded rescue

Identify what failed: task framing, tool/environment, worker execution, coordination, verification or stale context. Keep successful artifacts and their evidence. Do not silently loosen the scope, bypass permissions, change the requested model or transfer unrelated private context.

Before continuation, inspect the real host child/session identity, its terminal/running state, current artifact hashes, remaining budget and permission. A trusted resumable session may continue only with the same or narrower assignment. When lineage is uncertain or the host cannot resume safely, close or quarantine that attempt and prepare a fresh bounded assignment. Do not fabricate a successful resume or duplicate integration of a previous return.

Record contradictory evidence as quarantined and identify what resolves it. Emergency transfer requires the user's applicable authority for that target and data. A fresh diagnostic or adversarial reviewer advises; it does not accept the repaired work. On cancellation or revocation, stop further launches, use supported cancellation for owned active children and report any unconfirmed stop. Never alter unrelated sessions.

## Context continuity

Use observed context usage only when exposed by the host. Unknown is not zero, and a guessed percentage cannot establish remaining capacity. Choose a task-appropriate checkpoint or handoff before loss of useful context; a historical fixed 150,000-token threshold is not a portable limit. Keep bulk logs at their original authorized locations and pass concise evidence pointers. Do not remove required scope, failures or unresolved work merely to shorten the brief.

## Self-contained handoff

Prepare these seven parts for a recipient that cannot see this conversation:
1. Objective and current outcome status.
2. Accepted decisions and source authority.
3. Available inputs with exact paths/revisions and access limits.
4. The recipient's bounded next task and unresolved work.
5. Read/write/action limits inherited from the current actual authority, approvals and expected output destination. A proposed change the user has not authorized, such as a code fix during a no-change request, is marked as needing the user's explicit approval; the handoff never grants it.
6. Verification criteria, known failures and actual evidence.
7. Return format, stop conditions and who integrates.

Link existing artifacts rather than reproducing whole specs. Remove secrets and unnecessary personal context. Suggested skills must exist and remain optional unless explicitly declared as a real prerequisite. A prepared Cowork or other-host prompt does not transmit, launch or qualify that host. Use a verified supported surface only after the relevant authority is established.

Read returned artifacts and check the requested work before integration. If essential inputs or evidence are unavailable, return an honest incomplete handoff with the exact missing item; do not fill gaps from guesses.
