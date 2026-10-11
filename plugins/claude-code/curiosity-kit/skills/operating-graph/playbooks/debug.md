# Diagnose a stopped or inconsistent graph

## Select evidence without changing it

Use the exact run directory and reported symptom. Debugging is read-only unless a separate requested repair is authorized. Capture the current graph/version, reported state, failing command and error, last known good observation and the affected invocation/artifact. Do not normalize timestamps, repair hashes or rewrite JSON before understanding the failure.

Read [CLI](../references/cli.md) for `replay`, `resume-check`, `status`, `ready` and `inspect`. These diagnostics must not dispatch or repair. If a command refuses corrupt state, keep that refusal as evidence and inspect the bounded local records as data; do not bypass the guard through another mutation path.

## Trace cause, not just the final error

1. Check committed history and projection agreement. Find the first mismatching operation, missing immutable object, broken hash link or unsupported record version. An internally consistent hash chain alone does not prove the snapshot or receipts agree. Old-format runs need explicit conversion handling, never silent reinterpretation.
2. Reconstruct the affected node's invocation sequence: preparation/reservation, issued or unknown launch, actual response, return, validated outputs, criterion checks and settlement. Include older attempts and uncertain/cancelled work; latest status alone can hide the cause.
3. Follow each required input to its exact producer, epoch, attempt, contract and digest. Look for missing, failed, provisional, superseded, invalidated, wrong-producer or wrong-epoch outputs. Compare the consumer's captured inputs with current eligibility. Same-type data is not interchangeable.
4. Check effective approvals against the action's exact scope and trusted decision order. A later denial, changed content/destination, wrong subject, missing actual provenance or required action-time confirmation can block otherwise ready work. Do not repair permission by inventing a grant.
5. Check monotonic consumed attempts, outstanding reservations, actual host slots, deadline and global/epoch/local limits. Releasing a concurrency slot is not refunding an issued attempt. Capacity failure, rejected launch and unknown launch require different recovery.
6. Inspect topology and rewrite history. Distinguish an unsatisfied ordinary dependency from a true same-epoch deadlock or missing feedback seed. A proposed rewrite is not applied. An applied semantic change should invalidate affected descendants/evaluations while retaining explicit unaffected carry-forward. Never let an old evaluator certify a new output.
7. Check worker scope and records: canonical paths, internal symlinks, unique real launch identity when required, no forbidden controller actions, exact return evidence, and observed termination. File ownership instructions are not an OS sandbox.
8. Inspect the actual disputed output. A structurally valid graph can deliver the wrong answer; a correct-looking report can cite stale or unrelated evidence. Compare against the original criterion and raw source, not a worker self-grade.

## Classify and propose the smallest complete repair

- Node/content failure: repair the bounded task or its inputs; invalidate affected evidence and retry only within current authority/budget.
- Edge/topology failure: propose a concrete rewrite with affected closure and quiescence requirements; do not apply it during diagnosis.
- State/persistence corruption: stop dispatch, preserve the first divergence and use the supported authorized recovery path. Unknown external outcomes stay unresolved until observed or explicitly resolved.
- Policy/approval blockage: report the precise missing decision or forbidden action. A stronger model or more retries cannot grant permission.
- Resource exhaustion: report the consumed bound and unfinished work. Do not expand hard limits or reset counters to make the run appear successful.
- Capability/adapter mismatch: identify the missing tool/model/context/termination evidence. No silent inline downgrade or fabricated native receipt.

For each finding provide a concrete triggering input/situation, expected behavior, observed record/output and the code/contract seam responsible. Separate a defect from optional advice or an untested hypothesis. Propose one causal repair and its affected positive/negative recheck; repeated unexplained repair failures call for replanning rather than another speculative patch.

## Return

Return the primary cause, trustworthy completed work, affected artifacts/children, proposed repair, required authority and exact resume point. Preserve original failures and distinguish static inference from an executed reproduction. Do not issue a new success verdict, edit evidence or silently reopen a terminal run.
