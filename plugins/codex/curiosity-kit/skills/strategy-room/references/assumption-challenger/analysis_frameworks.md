# Assumption Challenger: analysis frameworks

Load for planning/challenge; consult only the applicable specialized portions. Apply [shared evidence and choice definitions](../evidence-and-choice.md) for evidence labels, confidence and authority. The five lenses organize tests, not mandatory objections. Record no material finding when appropriate. Use [phase contracts](phase-contracts.md) for artifact and gate responsibilities.

## 1. Hidden assumptions detector

An assumption is load-bearing when changing it changes whether the plan works or which option is preferable. Distinguish a stated premise, an implicit dependency and a guess about the user's beliefs. Quote or locate the passage that makes the assumption necessary.

Probe these categories where relevant:
- **Context:** environment stability, time, budget, skills, infrastructure, vendor/API reliability and dependencies outside the owner's control.
- **Audience:** behavior, incentives, motivation, literacy, device/internet access, ability to participate, willingness to pay or switch, and meaningful cultural variation. Do not infer private traits from demographics.
- **Technical:** capability, compatibility, data quality/access/rights, scale, latency, reliability, failure handling and support. A tool being available does not prove the task-specific behavior works.
- **Market/domain:** alternatives, competitive response, timing/urgency, buying process and applicable rules. Verify current claims when they matter; do not insert a generic legal warning as evidence.
- **Process:** approval chains, communication, ownership, team availability, iteration speed and feedback. “We have a team” does not establish capacity during the necessary period.

For each material assumption record:
1. What must hold, and the decision/outcome depending on it.
2. Evidence for and against; whether the dossier actually tests this case.
3. **Criticality:** high/medium/low impact if false, with concrete consequence.
4. **Fragility:** high/medium/low vulnerability given evidence, or unknown when likelihood cannot be assessed.
5. **Observability:** easy/moderate/hard to notice failure early enough to respond.
6. Cheapest useful check or adaptive response, and a visible condition for revisiting the plan.

High criticality, high fragility and hard observability warrant special attention. Do not multiply ordinal labels into fake risk precision. A very consequential unknown may deserve checking even without a high estimated probability. An assumption supported by the dossier can remain a strength, with a change condition rather than a manufactured criticism.

## 2. Blind spot illuminator

Distinguish missing from disproven. Absence in a short brief may mean omitted documentation rather than absent practice; phrase the gap accordingly.

- **Information gaps:** unavailable inputs, missing metrics or denominator, no baseline, unknown source quality, untested demand/capacity and missing validation.
- **Structural blind spots:** incentives, power, organizational constraints, distribution of benefits and burdens, selection effects, and people absent from the decision process.
- **Temporal/scale effects:** adoption versus repeat use, short versus long horizon, maintenance, compounding costs, downstream responses and behavior at materially different scale. Use relevant scenarios; arbitrary tenfold growth is not evidence of likely demand.
- **Boundary conditions:** outliers, edge cases, degraded service, delayed dependencies, withdrawal of a vendor, crisis conditions, recovery and rollback.
- **Cognitive blind spots:** possible framing/selection patterns from [cognitive_biases.md](cognitive_biases.md), tested against the actual material.

Classify along separate axes:
- **Recognized gap:** a known unknown, with the question stated precisely.
- **Reducibility:** reducible by a specified observation/test, irreducible within the decision horizon, or mixed. Reducible does not mean cheap enough to resolve.
- **Response:** research/test for reducible uncertainty; bounded exposure, contingency, feedback and reversible choices for irreducible uncertainty.

Do not label an enumerated scenario a discovered “unknown unknown.” Scenario diversity may help expose unanticipated failure classes, but genuine unrecognized risks cannot be inventoried exhaustively. State which perspectives/boundaries remain unexamined. Prioritize gaps by whether resolving them could change a decision, not by the number of questions generated.

## 3. Alternate viewpoint generator

A useful viewpoint exposes an overlooked constraint, incentive, alternative explanation or opportunity. It is an analytic perspective, not a quotation or a claim that a real expert was consulted.

Consider selectively:
- **Adversarial:** what a competitor could exploit, a critic could refute, or misuse could reveal about the design. Stay within safe analysis.
- **Optimistic:** what unusually favorable conditions would unlock value, which assets the critique undervalues, and what a small success could demonstrate.
- **Domain expert:** actual disagreements in the dossier; operational, usability, security, methodological or compliance concerns grounded in relevant expertise. Do not turn imagined expertise into authority.
- **Stakeholder:** end-user needs, an internal champion's adoption burden, skeptical colleagues, partners, maintainers and adversely affected people.
- **Temporal:** commitments that looked sensible before new evidence, what a future owner may wish had been considered, and long-run consequences missed by short-term metrics.
- **Unconventional:** invert a core premise, compare a meaningfully different delivery method, change a binding constraint or import an analogy whose limits are stated.

For each selected perspective give: its interest/criterion; what the current frame misses; supporting/contrary evidence or explicit hypothetical status; the implication; and a discriminating question/test. Optional depth prompts are surface observation, structural mechanism, and underlying value/worldview. Stop when further personas merely repeat the same objection.

Steelman both support and opposition. A skeptical voice must not use theatrical certainty or invented statistics, and an optimistic voice must not invent growth, efficiency or demand. If a values disagreement cannot be settled by research, identify whose choice it is.

## 4. Contradiction mapper

Name both commitments, show the mechanism of conflict and test whether they truly cannot coexist under the same conditions.

- **Goal–method:** proposed actions undermine the stated outcome; local optimization harms the broader objective.
- **Value:** speed versus assurance, access versus exclusivity, individual incentives versus collective goals, or competing ethical commitments.
- **Theory–practice:** formal process versus observed behavior, declared user need versus actual use, documented strategy versus execution evidence.
- **Structure–culture:** organization, incentives or approval rules demand behavior that stated culture discourages.
- **Resource–ambition:** scope, quality, money, capacity and timeline cannot all be satisfied under the evidenced constraints.

Classify carefully:
- **Productive tension:** both values remain achievable through a tradeoff, sequencing, segmentation, feedback or a design adjustment. Describe that mechanism and its costs; “balance both” is not enough.
- **Fatal inconsistency under stated constraints:** two necessary commitments cannot both hold, or the method defeats a necessary condition for the goal. Identify the deciding evidence and the smallest choice/redesign needed.
- **Unresolved possible tension:** a missing premise determines whether there is a real conflict. Keep it conditional until checked.

A difficult scope is not automatically impossible. An unconventional design is not inconsistent merely because a familiar practice differs. Distinguish fixed constraints from preferences and avoid changing a user-owned value to make the analysis convenient.

## 5. Meta-analysis lens

Evaluate the frame and the scrutiny itself:
1. What was treated as given? Which alternatives, beneficiaries, baselines or definitions were excluded?
2. Which claims were easiest to research, and did this distort attention away from consequential private or tacit factors?
3. Does the input show an observable bias pattern? What non-bias explanation could account for it? Use the taxonomy without diagnosing character or intent.
4. What does the dossier fail to establish: current conditions, specific population, internal politics/capacity, causality or actual tool behavior?
5. What assumptions does this analysis introduce? Does it privilege formal/English-language/public/technology-sector evidence at the expense of relevant lived practice?
6. Where does user or domain judgment govern: values, cultural context, relationships, risk appetite, tradeoffs, feasibility based on tacit experience or strategic taste?
7. How could the critique be wrong, and what evidence would change it?

Confidence tracks the bounded claim and available evidence, not eloquence or a universal percentage. Do not assert a fixed model knowledge cutoff or current capability catalog. Actual available tools, supplied material and verified current documentation govern relevant capability claims. Role separation does not eliminate shared blind spots.

## Anti-paralysis safeguards

More unanswered questions are not automatically progress. Watch for diminishing decision value, repeated restatement and a critique that never identifies a next step. Separate the cost of being wrong from the cost of waiting.

- Identify the minimum evidence needed for a defensible choice; do not pursue completeness for its own sake.
- Use an agreed decision horizon or timebox where relevant. A deadline does not erase a critical evidence gap.
- Favor a reversible informative step when uncertainty remains and stakes permit; state its exposure and what it can actually teach.
- Name the highest-value missing evidence, a concrete next action, and a stop/revisit condition grounded in the user's objective.
- If asked what to do today, give a bounded recommendation when support permits or explain the decisive blocker. Do not force an irreversible choice or imply authority to act.

## Specialized application: prompts and AI-assisted workflows

Use this section only for a prompt/workflow input. It supplements the five lenses; it is not a model catalog or a substitute for executing authorized tests.

**Anatomy checks:** task and audience; success/acceptance criteria; scope and exclusions; input sources and provenance; relevant context and terminology; examples for nonstandard output; format/length/style; tool/capability assumptions; failure/edge handling; privacy/safety/authority boundaries; and what to do when evidence is absent.

**Typical weaknesses:** ambiguous goals; quality words without criteria; overconstraint that prevents useful variation; underconstraint that changes the target; conflicting rules; missing input path; assumed access to private or live data; unavailable modalities/tools; unjustified arithmetic or perfect-recall assumptions; examples that smuggle in fictional facts; and output that appears published/approved when it is only a draft.

**Improve selectively:** clarify the ambiguous decision; remove repetitive instructions; add only examples that resolve a real failure class; permit relevant variation; and define observable evaluation cases. Request concise rationale, assumptions, citations and checks, never private chain-of-thought. A more elaborate prompt is not inherently better. Check current official documentation for consequential product-specific claims and test actual task behavior when separately authorized; say when neither happened.
