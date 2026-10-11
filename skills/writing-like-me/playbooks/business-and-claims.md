# Business intent and claim boundaries

Two functions share this method: reader-purpose craft and factual-support checking. Neither starts a separate writing lifecycle. Preserve diagnose/propose/revise/readiness scope. Read [channel guidance](../references/channels.md) and actual sources.

## Business intent

Determine the actual reader, purpose, available evidence and intended use. Organize around what they need to understand, decide or do:
- Decision memo: decision, options, supported tradeoffs, recommendation if requested, uncertainty and consequence.
- Proposal: the reader's concrete need, relevant approach, evidence-backed value, scope and actual next decision. No invented results, prices, urgency or commitment.
- Operating document: usable sequence, ownership where established, dependencies, exceptions and completion conditions.
- Status/update: what changed, why it matters and what remains unresolved; do not add an ask when none is needed.
- Article or social post: preserve the writer's position and useful context; do not impose business memo headings or a sales ending.

Check substance before polish: can the reader follow the mechanism? Is unfamiliar language explained without losing precision? Does evidence support the stated result? Does the format serve this purpose? A short next step belongs only when the piece actually calls for action.

`wlm.py business FILE` returns cue counts only. The presence of “recommendation,” “risk” or “next” is not proof of a useful business document; their absence is not automatic failure. Use [business checklist](../assets/business-checklist.md) proportionally.

## Claim boundary workflow

1. Define the evidence set: supplied documents, verified tool results, named sources available for inspection, or prose alone. Do not treat absence of contradiction as support.
2. Extract material factual claims, including added numbers, causal links, outcomes, personal experiences, quotations, comparisons and current platform facts. Separate pure opinion, framing and stylistic expression.
3. Classify each as supported, unsupported, uncertain or non-factual. Supported means the evidence establishes this exact scope. Unsupported means no sufficient support in the selected evidence, not proof of falsehood. Uncertain means partial, conflicting, ambiguous or unavailable evidence. Non-factual covers opinion, value judgment or explicitly hypothetical/fictional framing.
4. For substantial claim work use [claim-ledger.json](../assets/claim-ledger.json), with stable ids, text, status, evidence locator and remedy. A simple correction can be a concise source-backed finding; no ledger is compulsory for every sentence.
5. Inspect actual source support and dates. For current, consequential, medical, legal, financial, security or platform-behavior claims, use the available authoritative source when required. A study, expert or example is not automatically proof of generalization. Keep limitations attached to claims.
6. In diagnose mode report the gap and useful remedy. In authorized revision, narrow, qualify, remove or verify the claim. Never smooth unsupported material into authoritative prose or make up a citation. When verification cannot run, disclose the limit and avoid claiming current confirmation.
7. Run `wlm.py claims LEDGER.json` if producing a ledger. Repair invalid fields, ids, status or remedy, then inspect content. Schema success does not certify truth or source quality.

Allowed remedies are keep, remove, qualify, verify and source. A supported claim can still need context; an uncertain claim may remain with honest qualification. Preserve the writer's actual opinion without presenting it as external evidence. Deliver the requested text or findings, not an unsolicited research project.
