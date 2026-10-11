# Decision Synthesizer

Use for a bounded unresolved decision with material interviews, evidence or distinct options already available. Do not conduct a new research campaign, rank unrelated early ideas, or choose who/what performs a job here. Read the [common evidence/choice contract](../references/evidence-and-choice.md); structured saved artifacts use [contracts](../assets/contracts/README.md).

## Assemble the decision

State the question, owner, options with stable IDs, hard constraints, stakes, reversibility and horizon. Separate current/proposed/settled claims. Inventory only evidence bearing on this choice: observations, supplied claims, assumptions, judgment/preferences, disagreements and gaps. Retain strongest support and counterevidence with locators; collapse repeated origins without deleting disagreement.

Use the same decision-specific criteria for each option. Apply hard disqualifiers before preferences. Explain material tradeoffs, including why an apparently attractive alternative fails or remains unproven. Scores are optional; uncertain evidence cannot be disguised by precise weights. If options are semantic duplicates, return the exact variation needed to [Explorer](multi-direction-explorer.md). Do not invent a complete evidence base to make the matrix look balanced.

## Judge sufficiency

Use exactly one state, proportional to consequence and reversibility:
- **recommend**: material criteria and load-bearing claims adequately support a choice. Explain confidence and counterevidence; this is still a recommendation.
- **recommend provisionally**: a reversible bounded choice is useful despite named uncertainty, with conditions, a review trigger and containment of downside.
- **decline pending evidence**: a material gap could change an important choice. Name the smallest evidence needed, not a generic demand for more research.

A declined irreversible public launch can coexist with a separately framed provisional private test, but do not conflate their authority or evidence states. State risks, conditions, confidence and the evidence/change that would reverse the recommendation. Empty risk/condition/missing-evidence lists are acceptable when honestly justified; never fill them with null or invented items to satisfy a schema. “No known material risks within this bounded comparison” does not mean universal safety.

## Cross the actual choice gate

Present the recommendation or evidence gap and stop at the owner's choice unless the request already contains an applicable choice/delegation. Ask for the choice, correction to a governing value, or explicit scoped delegation. Before that, choice stays pending and the final decision record stays null/absent.

After actual choice/delegation, check that the selected ID is a real option and preserve a choice different from your recommendation. A supplied statement of delegation must actually authorize this decision; do not infer it from a placeholder name or JSON field. Record rationale, accepted risks, rejected alternatives, unresolved evidence, review trigger, immediate next action and next owner. The record must match the actual chosen ID. If a choice contradicts a hard constraint, expose the conflict and ask whether the constraint changed; do not silently discard it.

## Check and return

Review evidence sufficiency, alternative distinctness and choice provenance yourself. If saving structured output, follow the contract/template and run `python3 scripts/validate_artifact.py synthesis ARTIFACT.json` from the skill directory using the actual installed path. Inspect both errors and final content; passing structure is not consent or truth. A malformed artifact can be corrected without reopening a valid decision.

Return the decision map, sufficiency state, recommendation/limits, choice status and final record only when authorized, plus a non-executing handoff. Track material ongoing uncertainty with [Register](assumption-register.md) only when needed. If the central question is candidate fit, use [Matcher](candidate-matcher-and-brief-builder.md). Do not start the recommended action.
