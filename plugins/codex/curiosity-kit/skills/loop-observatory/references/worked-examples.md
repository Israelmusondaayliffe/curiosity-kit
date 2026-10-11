# Worked analytical cases

These examples explain the contract and independently worked arithmetic. They are not claims that a runtime test or native host qualification has passed. [CLI examples](cli.md) provides a complete executable supplied-record example; use the emitted result for actual field names.

## Four runs and a late label

One comparable cohort has four logical terminal runs. Each machine and human observation below binds the same task, artifact, criterion and rubric for its run.

| Run | Machine | Human | Measured cost |
| --- | --- | --- | --- |
| A | positive | initially unknown, later accepted | USD2 |
| B | positive | rejected | USD3 |
| C | negative | unknown | unknown |
| D | negative | accepted | USD4 |

Each stated complete run cost is backed by a cumulative run total or an explicit complete observation-coverage assertion. A single incremental charge without that scope proves only known partial spend.

A's earlier unlabeled revision remains historical. Its later bound label does not create a fifth trial. A copied export of A does not create a fifth run either.

Current results:

- Eligible current terminal runs: 4; historical A revision: 1.
- Human acceptance among labeled runs: 2/3; label coverage: 3/4.
- Paired calibration observations: 3. A agrees positive; B is a pass-side disagreement; D is a fail-side disagreement. Disagreement: 2/3. C is unpaired.
- Mean measured cost of accepted runs: (2 + 4)/2 = USD3, with accepted-cost coverage 2/2.
- Known measured spend: 2 + 3 + 4 = USD9, with cost coverage 3/4.
- Cohort spend per currently evidenced accepted outcome: unknown because C's cost is missing.
- Fully adjudicated cohort cost per acceptance: unknown because C's cost and human outcome are missing.

Now add a valid measured USD1 observation for C, without creating a new trial. Total measured spend is USD10 with cost coverage 4/4. Spend per currently evidenced accepted outcome is 10/2 = USD5, still based on only 3/4 human labels. Fully adjudicated cost per acceptance remains unknown. If C is later rejected, it becomes USD5; if C is accepted, it becomes USD10/3. Saying “USD5 cost per acceptance” without its current-label qualification hides a consequential uncertainty.

A conflicting same-ID A revision without a supported order cannot silently replace A. Preserve both candidates and exclude the unresolved logical run from a single-current claim until authoritative order or a bound correction is supplied.

## Attempts and cumulative spend

A task has two charged operations:

| Measurement | Attempt / operation | Basis | Aggregation | Value | Covers |
| --- | --- | --- | --- | --- | --- |
| charge-1 | attempt-1 / call-1 | measured | incremental | USD7 | none |
| charge-2 | attempt-2 / call-2 | measured | incremental | USD2 | none |
| final-bill | run / bill | measured | cumulative | USD9 | charge-1, charge-2 |

Before `final-bill`, known non-overlapping spend is USD9. Complete run-cost coverage additionally requires a source-backed coverage assertion naming both charges; without it, USD9 is known partial spend. After the supported cumulative bill arrives, it replaces its two covered components and spend remains USD9. The failed first attempt is not free, the accepted second attempt does not cost only USD2 at the task level, and the bill is not an extra USD9 charge.

If a later authoritative revision changes `final-bill` to USD9.50 for the same scope, it replaces USD9. It does not add USD9.50. If the later observation has no supported identity/revision relationship, preserve the ambiguity instead of assuming an order.

A measured USD0 with explicit billing evidence is different from a missing measurement. An estimated USD9 belongs to an estimated series, not the measured total. A reserved USD20 budget is not a charge. USD9 and EUR4 cannot be added into “13” of an unnamed currency.

An inclusive token total of 1,000 with 200 cached tokens is 1,000 tokens, not 1,200. Without an explicit subset/coverage relationship, report the observations separately and withhold a combined total. Tokens alone do not establish a monetary amount.

## Current state, history and knowledge

Run R has source-authoritative revisions 4 and 5. Revision 4 ended at 10:00 with no human label. At 12:00 a review becomes available against the same artifact, represented in revision 5. A report “as known at 11:00” uses the evidence known then; a current report may use revision 5. Both reports count one logical run. The current report does not rewrite the historical result.

Suppose another producer permits a valid recovered/nonterminal revision 6. Its current eligible terminal cohort no longer contains R, while revisions 4 and 5 remain historical. This is not a second failure trial. Accepted LoopKit forbids terminal reopening, so the same terminal-to-active transition there is rejected rather than treated as an authorized recovery.

File mtime and ingestion order do not establish this order. If revisions are opaque strings with no source-supported comparison, require bound supersession or retain conflict.

## Pair only the same question

Machine observation M1 evaluates artifact `sha256:aaa`, criterion `completeness`, rubric `review@2`. Human observation H1 evaluates artifact `sha256:bbb`, even if it is from the same named run. They are not a calibration pair.

If H2 evaluates `sha256:aaa` but criterion `visual-quality`, it still does not pair with M1. If H3 shares artifact and criterion but uses `review@3`, it also does not pair without an explicit evidence-backed equivalence mapping. Equality of the run ID or both labels saying “pass” does not repair these mismatches.

Two valid machine reviews and three conflicting human reviews are not six observations. Declare the reference/adjudication policy. If one source-authoritative final machine and one adjudicated human observation are identified for the same target/rubric, use that single pair. Otherwise record unresolved multiplicity and exclude it from the paired rate.

## Task mix can reverse the story

Two engines were run on different mixes of easy and hard tasks:

| Engine | Easy | Hard | Pooled |
| --- | --- | --- | --- |
| X | 9/10 accepted | 1/2 accepted | 10/12 = 83.3% |
| Y | 1/1 accepted | 2/3 accepted | 3/4 = 75% |

The pooled fraction favors X, while the within-stratum fractions are 90% versus 100% on easy tasks and 50% versus 66.7% on hard tasks. Tiny denominators and different task mixtures prevent a defensible engine-superiority claim. Report the strata and ask for a matched comparison only if the user's decision needs it. Do not execute new runs as a side effect of this report.

## No-new-result is about evidence and the question

First run: a complete selected source set yields report Q with a fixed cohort, parser/metric version and cutoff. Second run: all the same sources are successfully captured and all context is unchanged. A scheduled conditional request may return no new result, referencing Q.

Third run: A receives a late target-bound label. The run count is unchanged, but Q's analytical result changed; emit a new report. Fourth run: one selected source becomes corrupt. Even if the last valid current rows would be identical, report partial/error and the failed source. Do not reuse Q as healthy silence.

A different grouping or a new cutoff is also a different analytical request. Two concurrent reports need distinct output identities even if their timestamps share the same second.

## A plain-language answer with limits

“Two of the three reviewed runs were accepted; the fourth has no human label. Two of three comparable machine/human pairs disagree, one in each direction. Known measured spend is USD9 across three of four runs. Accepted runs average USD3 each, but total spend per accepted outcome is unknown because C's cost is missing. B and D need artifact-level review before deciding whether the judge or the reference label is wrong.”

This answer preserves completion versus acceptance, exact denominators, missing cost and unresolved diagnosis without requiring the reader to understand the observer's implementation.
