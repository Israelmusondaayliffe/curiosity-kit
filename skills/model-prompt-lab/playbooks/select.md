# Select from evidence or return no decision

Write a complete decision memo with the narrowest claim supported by the frozen comparison. The output may select the baseline, select a named candidate or make no decision. An operational preference to keep the current deployment is not proof that it won.

## Check evidence before ranking

Read the frozen plan, normalized results and preserved raw evidence. Recompute with `python3 scripts/lab.py verify FROZEN.json NORMALIZED.json`. Confirm the actual requested decision, baseline and candidate identities. Do not infer readiness from equal counts, a matching hash, a successful request or the model's completion statement.

Review six separate questions:

1. Identity: do prompt, configuration, tools, parser, cases and scorer match? Does the observed model/version resolve a mutable alias, or is that drift unknown?
2. Coverage: is the fixed trial matrix accounted for, with all attempts and stops retained? Has retry treatment changed what was compared?
3. Scoring: do deterministic grades match outputs? Are subjective grades attributed, calibrated and supported, with judge failures and disagreements visible?
4. Comparability: did both sides perform the same required work under the intended deployable conditions? Were order, cache, effort, tools or permissions confounded?
5. Adequacy: are case diversity, sample size, held-out status, uncertainty and practical difference sufficient for this particular claim? A hundred repetitions of one easy case do not establish broad deployment quality.
6. Authority/provenance: what establishes result origin and the timing of plan freeze relative to exposure? A timestamp and digest alone cannot prove preregistration, consent or authentic human review.

Where review receipts are used by the helper, record the actual review and its evidence. A supplied attestation remains an attestation; it is not authenticated because it parses. Unknown required gates remain unknown. A bounded recommendation can be conditional on identified external evidence, but cannot hide that condition.

## Apply only the declared rule

Apply safety and hard deployment/quality thresholds first, then the preregistered primary metric and meaningful-difference threshold, followed only by declared tie-breakers. Respect direction and units. A cost or speed optimization still needs the declared quality floor. Include every relevant attempt in costs and latency; account-wide usage is not marginal request cost.

The offline helper's supported rule and metric names are defined in [evaluation-contract.md](../references/evaluation-contract.md). Run `python3 scripts/lab.py decide FROZEN.json NORMALIZED.json --out DECISION.json`. It recomputes the evidence instead of trusting edited aggregate fields. The result is a bounded rule application, not a universal statistical judgment or permission to deploy. Synthetic specimens may show a hypothetical rule outcome but never a real recommendation.

Return no-decision when the plan is incomplete or changed, required observations are missing, results are materially incomparable, campaign safety stops fired, grading is unsupported, evidence is inadequate, or the declared rule leaves a tie. A missing required metric is not a favorable zero. Unknown optional cost permits only the quality claim that does not depend on it. A complete comparison below the replacement threshold may retain a qualifying baseline only if that distinct outcome was specified before results; do not turn a tie into a preference after the fact.

For an unsupported statistical/weighting rule, preserve the requested analysis and name the missing method. Do not replace it with the helper's simplest metric merely to produce a verdict. If a new prompt combines strengths of several candidates, assign it a new identity and verify it. The hybrid does not inherit either source's results.

## Write the full memo

Lead with the decision and scope. Then give:

- The actual baseline and selected candidate or the exact reason no choice is justified.
- Measured findings with evidence references, units, number of independent cases/repetitions, failure/retry counts and uncertainty. Separate provider-reported claims and qualitative preference.
- Why the frozen rule produced that outcome, including hard gates and any declared tie-breaker.
- Tradeoffs and limitations: population, tools/interface, unseen cases, source/chronology limits, mutable model resolution, missing costs and unresolved grader disagreement.
- Deployment conditions and rollback criteria. A recommendation does not itself deploy, change accounts or install the candidate.
- The smallest additional evidence that would resolve an inconclusive result, within a separately authorized next run.

A memo can be written here without an optional writing or reporting sibling. Use the user's requested format and keep traceability near the claim. If only a supplied-result review was authorized, finish the review without launching another comparison. Preserve first failures and prior decisions; a later result supersedes them explicitly rather than rewriting history.
