# Normalize supplied evidence

Preserve and analyze actual raw results against the exact frozen plan. Normalization checks declared structure, identity, accounting and arithmetic. It cannot authenticate a provider run, a human grade, a freeze timestamp or a source's truth.

## Identify what was supplied

Read the plan and raw files, not their names or readiness flags. Preserve the originals unchanged in the authorized work location. Identify run provenance, whether records are observed or synthetic, model/configuration/case/scorer identities, trial and attempt structure, environment and stopping state. Keep explicit unknowns. A supplied result may be useful even when it cannot support a selection.

Use [the evaluation contract](../references/evaluation-contract.md) for the current local format and [raw.example.json](../assets/raw.example.json) for a synthetic specimen. Legacy source formats lack several identities. An explicit import may preserve their contents and describe the missing information, but must not fill today's plan hashes into old rows and call them verified. If no evidence-preserving mapping exists, return a clear unsupported-import limit and a non-decisional summary.

## Validate identities, attempts and coverage

Run `python3 scripts/lab.py normalize FROZEN.json RAW.json --out NORMALIZED.json` with a fresh output path. Inspect its output rather than treating exit success as a winner.

Check the expected candidate × case × repetition matrix. Total row count is not coverage. Preserve missing combinations, duplicate or unplanned identities and records tied to changed configurations. Verify all recorded attempts within each trial: unique/consecutive attempt identity, eligible retry cause, allowed maximum and no later cherry-picked result after a terminal outcome. All billed or timed attempts remain in resource accounting.

Keep separate statuses for campaign stop compliance, terminal execution, task correctness and selection eligibility. A budget-stopped run can be valid but incomplete. A correct refusal can satisfy a declared negative case. Campaign safety stops, truncated responses and missing required observations prevent a successful deployment comparison even when outputs parse.

## Check scoring rather than just averaging

For a supported deterministic scorer, recompute from stored output and the frozen expected result. Reject contradictory supplied scores. An output promising to do the work cannot pass exact expected-output checking merely because a record asserts completion. For subjective or model grading, retain grader identity/configuration, rubric identity, assessed-output identity, receipt, explanation and failure/abstention state. Imported assessments are attributed judgments, not independently verified facts.

The helper accepts only its documented closed contract. It does not execute arbitrary scorer code, formulas or imports. Unsupported metrics and analyses need an explicit separate method. Missing grader evidence is not score zero. Preserve original judgments and any later adjudication as distinct evidence; rescoring changes the decision evidence identity.

Review numeric fields for finite values, appropriate bounds, units and population. Booleans are not numeric measurements. Null cost or latency remains unknown. Optional unknown cost can limit cost claims without destroying a quality-only analysis; a cost ceiling or cost-based choice requires the relevant cost evidence. Do not hide fast errors, timeouts or retries from latency denominators.

## Recompute and return

The normalized artifact retains raw evidence. Use `python3 scripts/lab.py verify FROZEN.json NORMALIZED.json` to recheck identities and recomputed results before relying on it. A modified aggregate cannot inherit the original verification. Review the actual outputs, artifact contents and available authorized tool evidence where the task requires them. Hash equality and counters are supporting identity/accounting evidence, not semantic task proof.

Return the checked normalized artifact, explicit invalid or missing records, attempts/trials/coverage accounting, aggregate units, uncertainty and known limitations. Distinguish input invalidity from a valid partial or no-decision result. Do not delete inconvenient records, backfill missing executions, invent zero costs or relabel synthetic data. If a decision was requested, continue to [select](select.md) with these limitations intact.
