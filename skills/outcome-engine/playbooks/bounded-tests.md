# Bounded assumption tests

Use a bounded test when a consequential uncertain assumption should be tested before a larger commitment. The output can be a proposed test, a permitted executed test with observations, or an interpretation of supplied results. Keep those assignments distinct. A request to design an experiment does not recruit participants, spend money or alter production.

## Precommit before seeing results

Name the decision and its owner, the single riskiest assumption, current evidence and the smallest reversible observation that could change the decision. State a falsifiable prediction: what observation would contradict it? An exercise that can only confirm the preferred answer is not a useful test.

Record:

- Method, planned sample/participants, selection criteria and relevant baseline or comparison.
- Measure and independent expected-result source. For a qualitative check, specify the observable distinction rather than inventing a score.
- Separate support, weakening, inconclusive and invalidation rules. Resolve overlap before the run. Record which validity rule takes precedence.
- Time, cost, data, permission and ethical boundaries; actual authorized actions; stop signal and what to do if stopped early.
- Known confounders, sampling/measurement limitations and what the test cannot prove.
- Where raw observations will be retained, the follow-on decision owner and the permitted next action.

Use the [filled planned record](../assets/test-example.json) and [checker contract](../references/checker.md) when a machine-checkable record is useful. Planned records say not-run and contain no fabricated observations. Keep the original precommit unchanged when results arrive.

## Choose the cheapest informative instrument

Prefer a real supported observation at the user's relevant interface. A mock, role-play, supplied dataset or prototype can answer its bounded question; it does not prove demand, reliability, learning or deployment in the real world. A useful test may be source reconciliation or a small read-only simulation rather than a production integration.

For numerical comparisons, ensure both arms perform comparable work, use the same units and denominator, and record relevant configuration. Exclude neither failures nor slow runs merely because they worsen the result. Check for cached/skipped work, different samples, noisy measurements and measuring a trivial inner step instead of the user's end state. Record run count and spread when they affect interpretation. A baseline without the feature cannot support a speedup ratio for that feature; use a declared absolute bound and disclose the missing comparison.

Do not impose a coding red/green loop on a research interview or creative preference test. Preserve its useful principle: the observation can disagree with the prediction, and the expected result is independent of the mechanism under test.

## Execute only the authorized test

Follow [deliver and resume](deliver-and-resume.md) within the precommitted bounds. Observe the actual sample, execution conditions, source/artifact version, deviations, confounders and early stops. Separate what happened from what you think it means. Do not clean away adverse results, adjust the threshold after seeing the score or turn a prototype into a product rollout.

If permission, data boundaries, safety, cost or time requires a stop, stop that operation. Preserve useful evidence, the stop reason and its effect on validity. An exhausted run is not a completed successful experiment.

## Classify without laundering evidence

Compare observations with the unchanged rules. Execution state is planned or completed; completed does not mean successful. Classification is:

- not-run: no completed observation yet, planned state only.
- supports: a valid result meets the precommitted support rule, within its scope.
- weakens: a valid result meets the weakening rule.
- inconclusive: valid evidence cannot distinguish the options under the stated rules.
- invalid: a method, sample, authority or evidence condition broke the precommit sufficiently that it cannot update confidence. Name the exact reason.

Validity comes before a favorable score. For example, a five-independent-attempt test requiring four unassisted completions is invalid when one successful participant was coached and coaching is a precommitted invalidation condition. Do not remove that attempt and use a new denominator to declare success. A separate valid three-of-five result can be inconclusive if that is the original rule. Neither result proves a population-wide completion rate.

State the confidence update in words supported by evidence, remaining uncertainty and what would change the next decision. Avoid invented precision. Choose stop, repeat, revise, scale or return to the decision owner as a recommendation. Scale is not authorization to spend, publish, deploy or enroll more people.

## Retain the record and changes

Give the test a stable ID and each immutable entry a separate record ID, positive version and actual timestamp. Retain the precommitted record and raw observations. A completed or corrected interpretation is a new entry linked to its predecessor, not an in-place rewrite. A material change of method, threshold, sample rule or prediction starts a new planned lineage; it cannot retroactively improve the old result.

For a canonical later record, invoke the bundled experiment check with the explicit predecessor file. It compares the supplied pair's IDs, version, predecessor hash and precommit, and preserves completed raw observations during interpretation-only corrections. It does not find previous files automatically, prove append-only storage, authenticate chronology or guarantee that the rest of history was retained. An unavailable predecessor means continuity remains unverified. Never claim the word append or a recorded hash proves historical integrity.

The script validates structure, not whether qualitative observations satisfy the rules. Inspect the raw evidence and classification yourself. Record corrections clearly and preserve invalid/failed labels. If a user specifically authorizes correcting a transcription error, retain the original observation record and the evidence explaining the correction; do not quietly overwrite it or bypass a checker that correctly flags a changed raw observation.

## Return

Return the complete test plan or result requested, actual evidence and deviations, classification, limits and the bounded next decision. A valid weakens or inconclusive result is useful work, not a reason to retry indefinitely until support appears.
