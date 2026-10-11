# Diagnose and repair a bug

Use this method for wrong behavior, crashes, intermittent failures, regressions, or a requested diagnosis. The central result is a supported causal explanation and a check that distinguishes broken behavior from the intended result. A plausible patch and a quiet log are not enough.

Read [the host contract](../references/host-contract.md). Diagnosis alone does not authorize code changes, production instrumentation, external messages, or deployment. If repair is requested, use the local implementation and scope-preservation practices in [implement.md](implement.md).

## Establish the bug and the allowed work

Read the full supplied report and relevant follow-up, including attachments or traces available within scope. Keep its original system as the issue of record. A pasted exception needs no newly created ticket.

Capture the expected behavior, observed behavior, affected user or caller, entry point, known version, environment, and timing. Distinguish what the reporter observed from what you have reproduced. When intended behavior is unclear, consult accepted requirements and tests before asking a focused question. Existing behavior alone cannot establish intent.

Preserve secrets and personal data while collecting evidence. Retain only the relevant redacted lines and safe sample inputs. Do not place credentials in command text, logs, fixtures, or reports. Production captures and instrumentation may require authority beyond local debugging.

Inspect current edits and staged work before touching the checkout. Use isolated sample data. If another process, browser, or service is involved, confirm the actual instance, revision, profile, endpoint, and state you are observing. A stale server can make a correct patch look ineffective; a different instance can make a broken patch look fixed.

## 1. Build a discriminating feedback loop

Choose the nearest available route that exercises the reported failure:

- An existing test or a small regression test at the relevant interface.
- A request through the actual development service.
- A CLI command with a fixed input and independently specified output.
- A browser interaction that checks the visible state and relevant network or stored effect.
- A safe captured request or event replay.
- A small isolated reproduction using the real affected logic.
- A property, differential, or randomized test when concrete inputs are not yet known.

Inspect project run commands before invoking them. Reuse existing test infrastructure. Do not install a new driver, launch a production write, or expose a server merely to obtain a reproduction.

Run the candidate loop and inspect the failure. It must catch this bug. "The process exited nonzero" is inadequate if the reported problem is duplicate reservations and the actual failure is a missing database. State the exact assertion, error, wrong value, ordering, or effect that identifies the symptom.

Make the loop cheap enough to repeat without changing its meaning. Isolate data, pin time and random seeds where relevant, and reset only owned state. Cache expensive setup only if the setup is not part of the defect. Keep the original invocation, inputs, and necessary conditions so the final repair can be checked on the original route.

For an intermittent bug, retain trial count, failure count, seed or scheduling conditions, environment, and duration. Increase reproduction probability with a controlled stressor or barrier when useful. A fixed sleep can help investigate timing, but is usually weaker than synchronizing on the actual event. Do not report that one green trial eliminated a previously intermittent failure.

If the exact environment is unavailable, continue safe source inspection or a translated experiment when useful. Label the result precisely: a source-supported hypothesis, a reproduced mechanism in an isolated fixture, or a translated route. Name the missing access or redacted observation needed to reproduce the original case. Do not collapse these evidence levels into "reproduced and fixed."

## 2. Reduce the case without losing the bug

Keep the original reproduction intact. Remove one input, step, caller, configuration setting, or dependency at a time. Rerun after each removal. Keep a reduction only when the same defining failure remains.

Do not remove load-bearing conditions merely to reach a unit test. A multi-user failure may depend on two actors, distinct permissions, separate processes, a common store, and a particular ordering. A one-caller test with a different error is not a smaller version of that bug.

Stop reducing when further reduction ceases to clarify the mechanism or would remove required conditions. An exhaustive mathematical minimum is unnecessary. The useful result is a small case whose remaining parts have a known role, plus the original case it represents.

Keep data semantics intact during anonymization. Changing a timezone boundary, duplicate identifier, missing field, or byte encoding can erase the defect even when the redacted example looks similar.

## 3. Trace the mechanism and test competing explanations

Trace backward from the wrong output to the first point where valid state becomes invalid. Read actual callers and data transformations. Check runtime, dependencies, configuration, generated assets, and build identity before treating application logic as the only possible cause. Search targeted history for the relevant assumption or an earlier attempted repair.

For a nontrivial cause, list a small number of plausible explanations. Each needs a grounding observation and a prediction that another explanation would not make. Do not pad the list to a fixed count when the evidence already isolates a simple defect.

A useful hypothesis says, for example, "both requests read the available count before either commits; forcing the reads to complete before either write should reproduce two allocations." A restatement such as "the system has a race" does not identify a discriminating experiment.

Choose the cheapest probe that separates the leading explanations. Change one variable at a time. Prefer a debugger or targeted boundary observation to logging everything. Mark temporary instrumentation so it can be found and removed. Record the hypothesis, probe, expected distinguishing observation, actual result, and whether the explanation survived. Preserve refuted explanations when they prevent repeating the same work.

Use the technique appropriate to the failure:

| Failure shape | Useful next observation |
| --- | --- |
| Wrong value appears across layers | Inspect the value at each boundary, including units, parsing, null handling, and identity. |
| Regression between known versions | Compare behavior on the same fixture; bisect only in an isolated or otherwise safe checkout with a trustworthy signal. |
| Order-sensitive failure | Pin or record order, isolate shared state, and test the suspected interaction rather than only individual cases. |
| Race or stale update | Control the interleaving at the real shared boundary and inspect the resulting invariant. |
| Delayed or missing job effect | Correlate the accepted operation with queue, worker, retry, and durable outcome using a stable identity. |
| Browser symptom | Check the actual page, request, response, console, and server state; confirm you are driving the intended instance. |
| Slow path | Establish correct completed work and a comparable baseline, then profile separately. Use [optimize.md](optimize.md) for measurement and repair. |

Consider the observer effect. Verbose logs can alter timing or leak data. Mocked dependencies can suppress the actual bug. A passing experiment with different inputs or dependencies narrows the claim; it does not refute every production explanation.

After repeated failed hypotheses or patches, stop varying the same approach. Name the premise they share, such as "both callers use this cache," and directly check it. If symptoms alternate between opposing invariants, revisit ownership and contract rather than patching one side again. A discovered product decision belongs with the user or accepted plan.

## 4. Explain the cause before broadening the repair

State the causal chain using observed links: triggering condition, incorrect transition or assumption, affected boundary, and visible consequence. Identify any link still inferred. A line that looks suspicious is a candidate explanation until the loop or other evidence supports it.

For diagnosis-only work, return that explanation, the reproduction, remaining uncertainty, and the recommended next check. Do not edit because the repair seems obvious.

For authorized repair, choose the smallest change that corrects the shared cause and preserves accepted intent. Fixing both callers with duplicated guards may hide a defect in their shared state owner. Conversely, moving all code into a new abstraction may be unnecessary when a local boundary check is the real correction. Trace the cause before choosing the size.

A deliberate behavior change needs its actual approval. Never weaken an assertion, drop a denied-action case, or rename a regression as expected behavior to make the build green. If the existing contract is contradictory or impossible, stop the dependent repair and report the exact conflict.

## 5. Prove the repair through the right interface

Place the minimized case in the existing test home when it reaches the actual bug pattern. Prefer the public or established internal interface whose behavior the contract promises. Use an independently chosen expected result.

Run it before the fix and capture the intended failure. Then apply the repair and observe the same case passing. If there is no suitable automated seam, keep the executable reproduction and disclose the missing regression protection. Do not add a production export or test-only mode solely to make an unrealistic unit test possible when the real entry point can exercise the case.

Rerun the original unminimized scenario. Check every materially affected caller, not only the path used to minimize. For shared state, preserve actor count and process boundaries. For durable behavior, read after a fresh process or use another independent effect observation as needed. For a forbidden write, verify the absence of the effect rather than only an error response.

Run broader relevant tests and inspect failures. A failure's location being unchanged does not prove it was pre-existing. Establish that claim with comparable baseline evidence or leave its origin unknown. A setup failure, unavailable service, skipped check, or inconclusive flaky run remains separate from a pass.

For intermittent failures, repeat under the previously failing conditions and report the actual count and outcomes. Choose trials based on the observed rate, experiment cost, and consequence of a missed bug. A finite run supports a bounded observation, not proof that the failure can never recur.

## Example investigation

Illustrative case: two callers sometimes create a reservation for the last available item.

Original route: two authenticated development clients submit against one item in the same database. Before repair, the isolated scenario produces two successful responses and two durable reservations.

Reduced case: preserve two separate connections and the shared store; remove the page rendering. Place a barrier after each availability read. The same duplicate allocation remains.

Competing explanations: duplicate transport submission predicts that one client can cause both writes. A non-atomic availability check predicts that two distinct requests can both pass the read before either writes. Observed request identities and the controlled interleaving distinguish them.

Repair: enforce the agreed invariant at the storage boundary used by both callers. The regression expects one accepted reservation, one defined conflict, and one durable allocation. The original two-client route must also pass. A single mocked service invocation would not establish this repair.

## Cleanup, report, and interrupted work

Remove owned diagnostic instrumentation and temporary overrides. Retain the regression test and enough safe evidence to explain the result. Do not erase unowned files or stop an unrelated process. Recheck affected behavior after cleanup if the removed instrumentation could change timing or control flow.

Return the observed cause, changed files, red and green evidence, original-route result, affected-caller checks, and remaining limits. Use "mechanism reproduced, original environment unverified" when that is what happened. Keep a required blocked observation visible even if the local patch is useful.

On resume, verify the current code, environment, partial experiments, and any still-running work. Do not repeat a consequential effect because its response was lost. Reconcile outcome first. Keep the original reproduction and rejected hypotheses so the next attempt starts from evidence instead of another plausible guess. Use [learn.md](learn.md) for a durable handoff when needed.

A postmortem or additional guard is useful when consequence or a repeated pattern warrants it. Prefer a stronger invariant, type, existing check, or focused regression test before adding standing instructions. Recording that lesson is separate from editing global configuration or publishing an incident report.
