# Assumption Challenger

Use for evidence-grounded scrutiny of a plan, prompt, strategy, idea, business case or technical decision: assumptions, blind spots, contradictions and what could go wrong. Do not impose it on a quick factual question, divergent brainstorming or an emotional-support request. Produce a calibrated review, including a sound-plan result when warranted. Read the [common evidence/choice contract](../references/evidence-and-choice.md).

## Choose scope and execution mode

Identify the actual input, decision/stakes, evidence base, as-of cutoff, user constraints and requested output. Ask one focused question if the target is materially ambiguous. Default standard depth; choose light for a bounded quick review, deep for requested rigor or consequential stakes. Effort changes breadth and depth, never permission to invent research or omit verification of material delivered claims. There is no compulsory search/finding count or time promise.

Routes:
- **Full review**: research → plan → challenge → verify → synthesize.
- **Research only**: return the dossier and its limits, without invented later phases.
- **Supplied research / skip web**: inspect supplied evidence as the dossier, then plan onward. Do not claim fresh web research. Missing private material remains a named limitation.
- **Reverify**: use prior findings and their actual evidence; verify, then synthesize a changed/retained/removed record. Do not silently rewrite the original as if it had always been correct.

Default execution is complete serial phases in this context. Preserve role-specific artifacts and handoff checks; do not pretend that changing a role label creates independent review. If the user requests supported native phase workers, use the [phase contracts](../references/assumption-challenger/phase-contracts.md): launch dependent roles sequentially only after inputs exist, pass the actual scoped artifact/evidence and return requirements, and inspect actual returns. No mandatory five-agent launch. Unavailable required host/model/tools are a stated blocker or accepted fallback, never simulated native execution. Serial and worker adapters have distinct qualification evidence.

## 1. Research: build a bounded dossier

Read [research protocol](../references/assumption-challenger/research_protocol.md) and use the [dossier template](../assets/assumption-challenger/research_dossier_template.md). Identify material claims and needed evidence types. Inspect supplied sources first, then relevant current primary/reliable sources only when within scope. Preserve origin, access and distinct dates; conflicting accounts and unavailable bodies matter. Group evidence by relevant dimensions such as technical, market, user, regulatory, ethical or historical; skip inapplicable dimensions with reasons rather than padding them.

Return a subject summary, sources with locators, findings by dimension, bounded disagreement/consensus/unassessed state, open questions, sufficiency assessment and limitations. Treat source quantity/diversity/recency as diagnostics, not proof. A private supplied-only dossier can be useful; it is not a failed web search or a claim of public validation.

For a saved dossier, run the shipped structural checker with the actual skill path, for example `python3 -I -B scripts/dossier_check.py DOSSIER.md --effort standard --pace slow --json`. See [exact contract](../assets/contracts/README.md). Repair structural errors before presenting it as a valid dossier. Then separately judge whether the evidence supports the requested review. A valid incomplete dossier can support an explicitly limited missing-input report, not a silently complete analysis. If the central question cannot be assessed, name the exact missing source/evidence and stop or narrow with the user.

## 2. Plan: target the critique

Read [analysis frameworks](../references/assumption-challenger/analysis_frameworks.md) and use the [analysis plan](../assets/assumption-challenger/analysis_plan_template.md). Tie the user's actual objective and dossier claims to testable hypotheses, not generic criticism. Standard/deep consider all five lenses; light prioritizes the material subset and names exclusions:
1. Hidden assumptions: criticality, fragility and observability.
2. Blind spots and uncertainties: reducible versus irreducible uncertainty.
3. Alternate viewpoints: stakeholders, constraints and alternative mechanisms.
4. Contradictions and tensions: productive tradeoffs versus fatal incompatibility.
5. Meta-analysis: framing, bias, evidence dependence and how the critique itself could be wrong.

For each applicable lens name the hypothesis, source IDs, supporting/contradicting observations needed, consequence and test. A sound dimension can yield no material finding. Do not manufacture a quota. Check that every planned challenge could matter to the decision and that dependent claims are linked.

For AI prompt review, additionally examine task clarity, appropriate examples, output contract, constraints, edge cases, tool/model capability assumptions and context efficiency. Use current official model facts only when relevant, date them, and do not assume one provider's controls apply to another. Request concise evidence/rationale rather than private reasoning disclosure. Full prompt engineering remains an optional Model Prompt Lab handoff, not a required dependency.

## 3. Challenge: make claims inspectable

Apply the plan and [bias reference](../references/assumption-challenger/cognitive_biases.md), recording the [raw findings](../assets/assumption-challenger/challenge_findings_template.md). Each finding needs a stable ID, precise claim, affected input/assumption, evidence/source IDs, concise reasoning, impact, counterevidence, draft confidence and what would falsify it. Distinguish a fact from an interpretation, prediction or unresolved question.

Challenge both the proposal and the critic. Look for selection bias, circular support, repeated origins, alternative explanations, hidden constraints and disproportionate remedies. Deep work can inspect second-order effects and low-likelihood/high-impact cases when decision-relevant, labelled with their uncertainty. Do not present several lenses repeating one source as corroboration. Keep a supported premise standing.

## 4. Verify every material delivered finding

Read [verification protocol](../references/assumption-challenger/verification_protocol.md), then produce [verified findings](../assets/assumption-challenger/verified_findings_template.md). Check evidence support, reasoning validity and counterevidence/alternatives for each material finding. Passing two does not excuse a failure in the third. Use actual source passages and context; body inaccessible means unverified, not confirmed.

Retain the original finding alongside its verification disposition: confirmed within scope, partially confirmed/narrowed, not confirmed, or speculative. Correct overbroad wording, downgrade unsupported certainty and remove an unsupported finding from recommendations. A useful speculative possibility can remain explicitly hypothetical with a test; it cannot masquerade as an established reason to act. Record what changed and why. All material light-mode output is verified too; reduce scope instead of spot-checking and presenting the remainder as confirmed.

## 5. Synthesize for a decision

Use the [final report template](../assets/assumption-challenger/final_report_template.md); consult [examples](../references/assumption-challenger/example_reports.md) only if helpful for shape. Lead with the bounded bottom line and highest-impact verified findings. Preserve the seven areas: assumptions, blind spots, alternate views, tensions, open questions, refinements and meta-reflections/limitations. Light may combine them compactly or mark nonapplicable areas; standard/deep give their material detail. Do not pad empty sections with invented risks.

Prioritize by consequence, evidence and reversibility. Each recommendation targets a verified weakness or a clearly labelled uncertainty and names a useful next check/change. “If overwhelmed, start here” identifies the smallest decision-changing step. Preserve positive evidence and unresolved disagreement. Deep output can include relevant dossier excerpts and a verification log, without exposing unrelated private data or dumping all resources.

## Failure and completion

A broken phase is not fixed by fluent synthesis. Repair the precise artifact, narrow the claim/scope transparently, or return the exact blocker; if the choice changes the user's intended outcome, ask whether to retry, narrow or stop. Preserve original failure and later correction separately. Do not silently downgrade effort or mark unperformed research complete.

Check final claims against verified findings and source locators, priorities against stakes, requested route completion and working links. Return the requested dossier/reverification/report, material evidence limits and next action. Keep intermediate substantive artifacts available when saved, or provide the relevant evidence summary on request; never invent a past artifact or worker trace. A critique and recommended remedy authorize no execution.
