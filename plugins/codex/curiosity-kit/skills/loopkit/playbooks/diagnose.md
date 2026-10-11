# Diagnose and improve a loop

Identify the failing layer before changing prompts. Read only the selected run's contract, snapshot, events/results, checkpoint, relevant artifacts and schedule observations. Do not search unrelated transcripts. Run the read-only `doctor` first; supplement its mechanical findings with actual task evidence.

## Fault → recovery

| Fault | Evidence to inspect | Smallest useful recovery |
|---|---|---|
| Contract | Unobservable outcome, absent input, weak check, ambiguous scope | Clarify the specific invariant; revise only with applicable authority |
| Execution | Failed argv, timeout, broad action, repeated equivalent work | Reproduce the exact symptom; narrow the action or fix the missing prerequisite |
| Verification | Invented pass, stale input/output, stub, mutated artifact, missing judgment | Run the real check on current artifacts; keep quality review distinct |
| State | Integrity mismatch, stale generation, pending intent, receipt disagreement | Preserve evidence, establish the last committed snapshot and actual effects; reconcile before resuming |
| Hooks | No activation, wrong host/workspace, duplicate invocation, oversized/noisy output | Inspect actual registration/trust and explicit run binding; exercise the owning event |
| Schedule | Prepared-only record, wrong cadence, unobserved run, no-op masking error | Inspect the real host schedule and execution; repair only within schedule authority |

Return typed finding, evidence, consequence and smallest recovery/check. Do not turn every finding into a framework rewrite.

## Build a red-capable recovery check

For a hard defect, first make the user's actual symptom observable. Prefer the existing test seam, a CLI fixture or captured trace; use a real UI/service path when required. Minimize the reproducer while it still fails. For timing faults, control inputs/time/seeds and record reproduction frequency rather than pretending it is deterministic.

Once the failing signal exists, rank plausible causes with falsifiable predictions. Change one variable at a time. Use targeted instrumentation, with a distinctive label so it can be removed. If a human-only surface is indispensable, provide concise steps and request observations, never credentials. If no safe red-capable route is available, state what was tried and the precise access/artifact needed; do not present an untested theory as the cause.

Repair the diagnosed cause within scope, then rerun the original reproducer and the relevant regression case. Inspect actual output and side effects. Remove only task-owned temporary instrumentation/processes; retain proof. A static fix or successful parser check alone does not establish recovery.

## Requested retrospective

When explicitly asked to reflect/retro, use the selected run or supplied session evidence. Separate one-off friction from recurring patterns. Examine judgment, tooling and overlooked alternatives; separate reviewers are useful when risk warrants and available, not a compulsory fleet.

For each material learning, give the incident, existing mechanism, proposed smallest structural fix and direct regression test. Check for an existing unwired/broken check before proposing a new one. Mechanical failures usually merit an executable guard; judgment failures need a clear criterion/example. Distinguish accepted proposals, unsupported/redundant findings and deferred work.

Do not automatically edit guides, global instructions, skills, permissions or schedules. Present consequential changes for the applicable authorization. Optional collaboration remains bounded, and a missing reviewer is disclosed. Diagnosis and retrospective should make the next run more reliable, not generate another long report in place of the repair.
