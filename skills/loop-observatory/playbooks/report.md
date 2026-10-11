# Portfolio report

Use for a bounded outcome summary or a comparison across evidenced engines, models, versions, task strata or periods. The input is a validated observer snapshot or an explicit source selection to ingest first. Produce JSON and Markdown from the same selected cohort. A prose-only answer may summarize those artifacts, but must not invent unavailable telemetry.

Read [record contract](../references/record-contract.md) for fields and [worked examples](../references/worked-examples.md) for arithmetic.

## 1. Define what the numbers answer

State the user's question, source selection, report operation, current/historical basis, event window and knowledge cutoff. Use timezone-aware timestamps and explicit interval boundaries. “Runs that ended in September, judged using labels known on 1 October” is different from “September runs using all labels known today.” Do not substitute ingestion time for a missing run event time.

Default to one defensibly current revision per logical run. Keep history for traceability, not as extra observations. A historical report must explicitly select revisions as of its event and knowledge cutoffs; a later acceptance must not leak backwards. Count changed-cost and label revisions separately from new trials.

Declare a cohort using evidenced task family/dataset, producer/model/version, conditions, rubric and time filters. Missing group dimensions remain an unknown group. Do not hide rows to make a comparison look clean. When the helper cannot apply a requested semantic filter, derive a documented subset with exact IDs and disclose the limit rather than pretending that a text search is a validated cohort.

## 2. Reconcile the denominator

Show intake status and source coverage before performance claims. Reconcile selected sources and records with current terminal runs, current nonterminal runs, historical revisions, duplicates, conflicts, filtered rows and unavailable/corrupt sources. Give source-linked reasons for exclusions.

For eligible current terminal runs, let:

- N = eligible logical runs;
- A = runs with trustworthy human acceptance;
- R = runs with trustworthy human rejection;
- L = A + R;
- U = N - L, including missing/conflicting/stale acceptance evidence as separately described.

Acceptance among labeled runs is A/L; it is null when L is zero. Human-label coverage is L/N; it is null when N is zero. Do not use A/N as “acceptance rate” without explicitly naming it “currently evidenced acceptance share of all eligible runs.” Rejected, unlabeled and conflicted are different categories. A machine pass is not a human accept.

Label coverage can be selective: successful or disputed runs may be reviewed more often. State this before generalizing to all runs. A report with one accepted label in one reviewed run is “1/1 among labeled runs; 1/N coverage,” not proof of perfect performance.

## 3. Compute only evidenced measurements

Keep machine completion and machine verdict counts separate from human outcomes. Summarize iteration and duration only where valid numeric evidence exists; show observed count/eligible count, units, mean/median/range where useful, and unknown count. Duration derived from start/end must use the same documented run scope, valid timezone-aware times and nonnegative interval. Missing finish time is not zero seconds. Runtime, wall time and human waiting time are different measures.

Use exact producer mappings for exhausted runs. Retain raw stop/escalation reasons and display their frequencies with denominators. A note containing “iteration” is not an exhaustion code. Repeated text is a frequency cluster; it does not establish a common failure cause.

Group by engine, model, version and time only where those values are evidenced. Include unknown groups and the same metric/coverage fields for every group. Use the helper's supported group flags; avoid invented provider/model aliases. Time buckets must state which timestamp and timezone define them.

## 4. Name cost metrics precisely

Retain currencies and measured versus estimated series separately. Never convert missing telemetry to zero or infer a bill from model names, subscription meters or token counts. Mixed currencies have separate totals unless the user supplied an explicit dated conversion basis; the helper does not fabricate FX rates.

For one currency and a compatible cost scope:

1. **Known measured spend** is the non-overlapping sum of known measured charges. Always show measured cost coverage, unknown/invalid costs and whether the spend is only partial.
2. **Mean measured cost of accepted runs** is measured spend attributable to accepted runs divided by accepted runs. The complete-cohort version requires known compatible costs for all A accepted runs and A > 0. A subset mean can be reported only with an explicit observed-subset name and its own coverage.
3. **Cohort spend per currently evidenced accepted outcome** is total compatible cohort spend/A. It requires complete cost coverage for the entire relevant cohort and A > 0. Its denominator is currently known accepts; human-label coverage must remain visible.
4. **Fully adjudicated cohort cost per acceptance** additionally requires all eligible human outcomes resolved. It remains unknown while an eligible outcome lacks an adjudicated label.

Do not retain the old ambiguous “cost per accepted result” label for an accepted-only mean. Rejected/failed attempts may have real spend. A USD7 failed attempt plus a USD2 accepted attempt is USD9 of spend. A later authoritative cumulative USD9 covering both replaces those components; it is not USD18. [Measurement examples](../references/worked-examples.md#attempts-and-cumulative-spend) cover this precisely.

Current record selection alone does not establish the spend total. Incremental observations require an explicit complete-scope coverage assertion before they support full-run cost; an authoritative cumulative run total carries that scope. A valid single charged operation otherwise supports known partial spend only. The selected cost observations must cover every relevant distinct charged attempt and exclude duplicates/overlaps. If the coverage scope is unclear, show known observations and withhold an all-cohort total.

## 5. Decide whether a comparison is defensible

Before a “better,” “cheaper” or “regressed” claim, compare task mix, conditions, model/judge/rubric versions, attempt policy, observation windows and label coverage. Display compatible strata and descriptive fractions. A pooled difference may reflect different work rather than different capability.

If conditions are incompatible, say no defensible performance ranking is available and name the smallest missing control. Do not invent a rerun campaign or execute new trials. For tiny or handpicked samples, say the observations are descriptive. Correlated retries of one task are not independent tasks.

Do not add confidence intervals mechanically. An interval requires a stated estimand and sampling assumptions. If those are unsupported, exact counts/coverage are more honest. A formal interval cannot remove confounding, repair a bad rubric or make missing labels random.

A causal explanation needs source-level evidence: inspect the actual target, criterion and failure trace before attributing a cluster to the model, judge or tool. Keep competing explanations available and use [handoff](handoff.md) for the unresolved next check.

## 6. Write and check both artifacts

Lead the readable report with the answer and the evidence boundary. Include:

- source/cohort/time/cutoff identity and complete/partial/error status;
- intake and current/history counts with exclusions;
- acceptance numerator/denominator and label coverage;
- cost names, currency/basis and cost coverage;
- useful engine/model/version/time or task strata;
- iteration/duration and stop/escalation summaries where available;
- important disagreements or unresolved comparisons, exact source IDs and next evidence requests.

JSON is the raw structured evidence contract. Markdown is a display-safe presentation: escape source-controlled Markdown/HTML/link syntax without rewriting the raw JSON values. Do not expose irrelevant sensitive payloads or private paths in a report for another audience. JSON and Markdown must agree on metrics, counts, flagged IDs and uncertainty.

Use unique immutable output names. Two reports in one second must not overwrite each other. Preserve earlier reports so an unchanged conclusion and a changed knowledge state can be distinguished.

## 7. Handle incremental/no-new-result requests

No-new-result is valid only when all selected inputs were read successfully, the current source/revision selection is unchanged, and the analytical identity matches the prior result: operation, parser/metric version, cohort/filter, time and knowledge cutoff, label policy and grouping. A new question against identical source bytes still deserves a new analysis.

A late label, newly resolved conflict, changed cumulative charge, different cutoff or new read failure changes the result. Do not suppress it because no new run ID appeared. An unchanged partial/error read is still a visible partial/error condition, not healthy silence. Conditional suppression does not install, verify or authorize a schedule.

## Bounded review before delivery

Check at least one real numerator/denominator and one source-linked exception from the actual generated artifacts. For a riskier comparison, work the core arithmetic independently and inspect one known-good and one known-bad case under the same criteria. Keep this small and targeted; a mandatory review panel or giant telemetry harness is unnecessary. Fix only an observed defect and retain the original result when recording a correction.
