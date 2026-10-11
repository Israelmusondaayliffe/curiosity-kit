# Judge and human calibration audit

Use when the user asks whether judges agree with later human review, where machine passes/failures look suspicious, or whether repeated disagreements deserve investigation. Inputs are immutable run/artifact evidence, machine observations, human/reference observations and the governing rubric. No judge changes, source relabeling or new evaluation campaign are implied.

Read [record contract](../references/record-contract.md), then use the helper's `audit` interface in [cli.md](../references/cli.md). Its counts are a starting point for reviewing actual cases, not a substitute for that review.

## 1. Establish the reference question

State what is being judged: a whole task outcome, one artifact version or one criterion. Identify the exact rubric and version, applicable task conditions and reference-label policy. A human label is not infallible merely because it is human; it is the declared reference observation for this audit.

Preserve each observation's ID, observer/role, value, target artifact/task/criterion, rubric/version, event timestamp and supersession/adjudication links. Retain raw labels alongside any explicit normalized positive/negative mapping. A launch approval, deployment authorization or receipt acknowledgment is not an output-acceptance label.

## 2. Build eligible pairs before rates

The pairing key must bind the same logical run, exact target and criterion under the same rubric/version. Two reviews of different artifact revisions cannot calibrate each other. A broad run-level completion signal and a narrow artifact-quality label answer different questions.

Within each target/rubric stratum, select one eligible machine observation and one eligible reference observation using source-authoritative ordering or an explicit adjudication policy. Examples include a named final judge for that rubric and a named adjudicated human review. Declare the policy before counting. Do not use observation order, file mtime, lexical filename, majority by convenience or whichever label agrees with the machine.

Multiple candidate judges and human labels do not create all possible combinations. An unresolved two-by-three observation set is not six independent pairs. If there is no supported single pair, exclude the stratum as unresolved multiplicity and show the available observation IDs. Conflicting human labels remain conflict, not false or a silently chosen winner.

Apply the knowledge cutoff to both observation availability and source revisions. A label known only later must not appear in an earlier as-of audit. Label timestamp alone may not prove when the observer knew it; disclose this if availability evidence is missing.

Report pair coverage against the relevant eligible target/run population, explaining when one run contains multiple independently defined criteria. Do not call criterion pairs “runs” or add their denominators to run acceptance counts.

## 3. Count exact cells

For P eligible comparable pairs:

- machine positive / reference positive: positive agreement;
- machine negative / reference negative: negative agreement;
- machine positive / reference negative: pass-side disagreement;
- machine negative / reference positive: fail-side disagreement.

Agreement is the two agreement cells divided by P. Disagreement is the two disagreement cells divided by P. Both are null when P = 0. Keep missing-machine, missing-reference, stale-target, wrong-rubric, conflicted and unresolved-multiplicity exclusions separate and source-linked.

“False pass” and “false failure” may be retained as familiar directional labels only when immediately qualified as disagreements against the declared reference. They are not automatic causal findings. If reporting false-positive or false-negative rates conditional on reference classes, use the appropriate class denominators and name them; the overall paired disagreement rate is different.

## 4. Inspect the discrepancy, not just the label

For each material flagged pair, read the actual artifact or outcome, governing criterion, machine rationale and human rationale where supplied. Confirm the hashes/versions match the pair. If that content is unavailable, say diagnosis remains limited to label disagreement.

Test competing explanations with the smallest available evidence:

- The machine missed a real requirement: identify the requirement and artifact location that contradict its judgment.
- The machine evaluated an old/different artifact: inspect bound version/hash and chronology.
- The rubric is ambiguous or changed: identify the exact competing interpretation/version.
- The reference label is mistaken or applies another scope: identify its criterion/target mismatch.
- The task was underspecified or impossible under its constraints: inspect the task contract rather than blaming the judge alone.
- A tool/collection defect omitted evidence: identify the missing operation/receipt and whether the judge could see it.

Do not silently adjudicate on behalf of the human or rewrite evidence to fit the diagnosis. Distinguish observed discrepancy, supported cause and unresolved hypothesis. A direct artifact defect may support a judge false pass; an unexplained pair supports only “needs review.”

## 5. Analyze exhaustion and escalation separately

Use exact producer exhaustion mappings, not arbitrary substring matches. Group stop/escalation reasons with source IDs, eligible count and coverage. Identify repeated signatures as clusters worth inspecting. A common string or correlated time period is not proof of one cause.

Keep exhaustion independent of disagreement cells. An exhausted run may still yield an accepted artifact, a rejected artifact or no compatible human judgment. It remains one logical run, not both an exhaustion trial and a failure trial.

## 6. Deliver the audit and next check

Return JSON plus a readable account with:

- source/cohort/time/knowledge identity and label-selection policy;
- eligible paired denominator and four cells;
- pair/reference coverage and every exclusion class;
- exact flagged run/target/observation IDs;
- representative source-grounded case findings;
- observed versus unresolved causes;
- the smallest owner-bound next check.

Use [handoff](handoff.md) if a correction is warranted. The recommendation stays unresolved until the execution/judge owner supplies a bound repair receipt and new evidence. Do not modify prompts, rubrics, labels, limits or source states during this audit.

## Small calibration controls

When evaluating the audit itself, preserve a known matching pair and a clearly mismatched target as controls. Expected behavior: the matching pair counts once; the mismatched target is excluded even if labels agree. Add a known pass-side and fail-side disagreement when changing pair logic. Check actual IDs and denominators rather than merely matching a report heading.

These are isolated behavior checks for an explicitly authorized skill/evaluation task, not authority to send private artifacts to a new judge or run paid models. If delegating review, pass immutable evidence and the question without planting the preferred explanation; require the worker to return useful cases, alternative causes and limits.
