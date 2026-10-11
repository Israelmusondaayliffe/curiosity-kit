# Long-run task contract

Fill this with observed host capabilities. It is a design/delivery template, not an evaluator JSON contract or a ready-to-run service. Remove inapplicable optional instructions from the final prompt. Follow [the full method](../playbooks/long-run.md).

## Outcome and scope

- Requested outcome and intended reader/use:
- Specification location and version:
- Required deliverables and locations:
- Acceptance criteria and evidence for each:
- Explicit exclusions:
- Authorized actions and confirmation boundaries:
- Supervised/unattended mode and user-interruption route:
- Time/spending/resource bounds:

## Host readiness

For each, name the actual tool/location, observed check, limitation and owner. Use ready, degraded or blocked. Do not fill unavailable capabilities with invented names.

- Specification read and output write/retrieval:
- Execution and returned job identifiers:
- Status, wait and cancellation:
- Independent reviewer or alternative checks:
- Checkpoint persistence:
- Authorized reusable-memory mechanism:
- User-visible mid-run delivery and attachment access:
- Final response visibility:
- Context/state transfer, timeout, streaming and output capacity:

## Complete task prompt

```text
Complete [outcome] for [reader/use] within [scope]. Read the specification at [verified location/version]. Success requires [criteria]. Use only [actual tools] and actions already authorized in [authority boundary]. Pause dependent actions when required permission or input is missing.

Track each required item as not started, active, blocked, failed or verified. Tie progress claims to observed results or artifacts and preserve their provenance. Distinguish created from checked. State failed and skipped checks.

At [milestones], apply [checks]. Use [actual reviewer route] with the specification and artifact version. If that route is unavailable, use [real alternative] and state the lost assurance. Do not call self-review independent or waive a hard review requirement.

Record each started job's identifier, owner, state, output location and next action in [checkpoint location]. Work on independent authorized items while jobs run. Before ending, reconcile every acceptance item and started job. Wait or collect results through [real mechanism]. Do not repeat uncertain side effects. Retry only [eligible categories] within [attempt/resource bounds]. Stop on [completion, cancellation, exhausted bound or exact blocker].

Before context transfer, preserve current requirements, authority, artifact versions, completed action receipts, active job identifiers and unresolved decisions. After transfer, re-read the checkpoint and reconcile actual state before acting. Use only supported opaque-state handling.

Use [existing memory mechanism] only for authorized reusable lessons with evidence and scope. If unavailable, preserve a task checkpoint without creating persistent learning policy.

Deliver ready partial results or direct answers through [verified user channel]. If no such route exists, save permitted partial artifacts and deliver at the next supported response boundary; do not promise immediate notification. End with a standalone outcome summary, evidence, limitations and any decision needed.
```

## Milestones and active-work ledger

Repeat these records as needed. They are conceptual task records, not input to lab.py.

- Acceptance item / dependency / artifact version / check / current status / evidence:
- Started work / owner / host job ID / observed status and time / output / next action / cancellation rule:
- Retry category / allowed recovery / attempt limit / deadline / cost bound / terminal result:
- Context checkpoint / active contract version / next action / unresolved authority:

## Qualification and delivery

- Ordinary completion test, expected/observed:
- Running job at proposed completion, expected/observed:
- Failed review, permission blocker and timeout, expected/observed:
- Missing reviewer, delivery or memory, expected/observed:
- Context transfer and user intervention, expected/observed:
- What was actually exercised, evidence locations and provenance:
- What remains unrun or blocked:
- Persistent configuration changes proposed for the owning system, not applied:
- Exact rollback/resume artifact:

Readiness conclusion: [usable design / partially qualified / blocked execution]. Do not equate prompt completion with runtime qualification.
