# Assumption Register

Use to make load-bearing beliefs in a plan, forecast or decision inspectable over time. Produce or revise a compact register, not a monitoring service. Read the [common evidence/choice contract](../references/evidence-and-choice.md) and, for saved JSON, [contracts](../assets/contracts/README.md).

## Extract and frame

Read the actual decision and available evidence. Ask “what must be true for this to work?” Keep assumptions whose failure could change the choice, scope, timing or test; do not turn every sentence into a record. Separate factual, behavioral, capability and timing claims. A user preference is a governing value rather than an empirical belief to falsify.

Give each assumption a stable ID, precise claim and affected decision. Record:
- Why it is load-bearing and consequence of being wrong.
- Supporting and contradicting evidence, including source/origin/date/context; evidence gaps are explicit.
- Status and confidence with rationale, not an unexplained probability.
- Reversibility: `reversible`, `partly-reversible` or `irreversible`.
- Actual owner or unknown; concrete test or unknown; expected observable result and timing where known.
- Kill condition: a measurable threshold or observable event that would require stopping/changing the dependent plan, with the responsible decision owner.
- Dated revision history and what evidence changed the assessment.

## Maintain honest status

Use `untested`, `supported`, `weakened`, `falsified` or `expired`.
- Untested includes material owner/test gaps. Do not invent an assignment or test to remove the gap.
- Supported requires evidence of the right type in the relevant context; one interview may support a stated preference but not independent adoption.
- Weakened records contrary evidence that reduces support without conclusively disproving the claim.
- Falsified needs an actual result meeting the claim's failure criterion, not just a missed deadline or criticism.
- Expired identifies evidence whose freshness/context no longer supports the decision; preserve its historical status and revisit trigger.

An inconclusive test stays inconclusive. Keep both support and contradiction. On new evidence, retain the ID, previous status/confidence, date, source and reason for transition. A renamed claim retains identity if its meaning is unchanged; a materially different claim gets a new linked ID. Do not overwrite history or convert a planned test into a completed one.

## Review and return

Check unique IDs, evidence fit, status consistency, observable kill conditions and unknown owner/test visibility. Tighten “if results are bad” into a concrete event/threshold agreed or explicitly proposed; do not claim agreement for a suggested threshold. Use the existing structured checker when saving JSON: `python3 scripts/validate_artifact.py register ARTIFACT.json`. It validates fields and sequencing, not the truth of the evidence.

Return current load-bearing assumptions, changed items and reasons, unresolved gaps and the smallest next test/decision. Save in the authorized project record if requested; otherwise return it directly. Revisit when actual evidence changes or the user asks, without activating a schedule.
