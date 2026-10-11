# Audit supplied outcomes read-only

Use for an explicit ProofLoop audit. Determine what the selected evidence supports about outcomes, retrieval effects, verifier quality and record health. Do not run new candidates, repair records, launch a benchmark, change exclusions or edit policy to complete an audit.

## Fix the selection before counting

Name the selected runs/records, date window and timezone, task families, comparison question, quality metrics, required criteria, pairing rules, equality/tolerances and missingness policy. Inspect the complete authorized set rather than choosing only successful examples. If selection happened after outcomes were visible, label the analysis descriptive and its selection bias. A broad question does not authorize a private-history sweep.

Validate records and resolve their evidence pointers with the [CLI contract](../references/cli-and-records.md). Check whether a result was actually captured, imported, declared, stale, superseded, incomplete or invalid. An empty list, missing expected value or identical fixture field is not a regression pass. The supplied-comparison command compares typed observations only; it does not execute the subject.

## Establish comparability and evidence quality

For a with/without-retrieval pair, compare the task/criteria, source and candidate-input basis, model/host/effort where observed, tools, permissions, budget, environment, verifier/configuration/data versions and actual amount of completed work. Name material differences. Different tasks or a reduced denominator cannot establish faster equivalent work.

Record evidence independence by generation, verifier implementation/configuration, data/source and trust path. Two model votes or two reruns of the same flawed checker are correlated. E0 reflection and E1 judgment do not become verified improvement through repetition. E4 needs the declared independent and held-out/postcondition evidence; no automatic promotion follows.

Inspect evaluator calibration using supplied known-good and targeted-defect controls. Ask whether the evaluator rejects the failure it claims to catch. Preserve its raw disagreement and false positives/negatives. Report a missing or weak control as a limitation or proposed repair; do not secretly run new tests or modify the evaluator during the audit. A score average cannot overrule failed mandatory criteria.

## Classify all selected pairs

Use the frozen quality rules before time/cost. Separate:

- Helpful: comparable evidence shows the defined practical improvement without a failed required outcome.
- Neutral: comparable, sufficient evidence meets the declared equality/tolerance rule.
- Harmful: comparable evidence shows worse required quality, unsafe behavior or the predeclared material regression. Faster wrong work is not helpful.
- Indeterminate: otherwise comparable evidence is missing, inconclusive or insufficient to classify.
- Incomparable: material condition/work differences prevent the requested comparison.

Keep selected, comparable and determinate denominators explicit. Do not drop missing records or turn unknown into neutral. Report observed latency, attempts, tokens or monetary cost only with units and coverage. Missing counters remain unknown; a shared account-meter movement is not isolated run cost. Sum only compatible measurements and state exclusions.

For small samples, report exact counts and case-level reasons. The original source's fewer-than20-pairs rule marks exploratory evidence; reaching20 is not a causal or statistical guarantee. Do not launch more runs to meet it. Even a matched observed gain can be limited by selection, noise and shared dependencies. Explain that rather than claiming general superiority.

### Literal audit example

Five supplied pairs have error counts without/with retrieval of `(1,0)`, `(0,0)`, `(0,1)`, `(unknown,0)` under comparable conditions, plus `(2,0)` under a different contract. The classification is one helpful, one neutral, one harmful, one indeterminate and one incomparable. Selected5, comparable4, determinate3. These labels describe this supplied fictional fixture, not measured model performance. If timestamps/costs are missing, do not report a speedup or savings.

## Audit record and security health

Review selected records for stale sources, expired applicability, contradictory active guidance, missing provenance, improper approval reuse, unacknowledged exclusions and derivative status. Keep a read-only expiry finding separate from a stored status transition. Imported records and exact hashes can be structurally valid while remaining unauthenticated.

Report unauthorized activation, protected-data disclosure, cross-scope retrieval, forged consent, altered verifier/criteria, stale replay, wrong-target work, prohibited writes and excluded content surviving in derivatives separately from ordinary quality defects. “Zero observed incidents” is scoped to the actual inspected set and exercised checks, not universal safety. The helper's structural pass cannot certify this critical suite.

Preserve failed and invalid runs in the audit. A corrected output does not retroactively change a primary grade. Distinguish source defects, setup/isolation failures, reviewer mistakes and required candidate failures. Inspect actual traces when authorized; a test profile name or app-server listing alone is not the authenticated model's catalog.

## Return proposals without applying them

Return the audit question and selection, comparability decisions, outcome counts/denominators, criterion findings, calibration and independence limits, observed usage with coverage, security incidents and record-health issues. Link each material conclusion to the inspected evidence. Propose the smallest useful next action, such as narrowing an advisory, fixing a verifier or collecting a missing outcome. Do not write a lesson, change a record or begin that next action unless separately requested.

If a required source is unavailable, give the useful bounded findings and exact missing evidence. An honest no-decision is better than a causal story built from incomplete counts.
