# Assumption Challenger: research protocol

Load for dossier preparation; consult during verification when evidence quality/currentness is disputed. Use [shared evidence and choice definitions](../evidence-and-choice.md), [researcher responsibilities](phase-contracts.md#phase-1-researcher--research-dossier) and the [dossier template](../../assets/assumption-challenger/research_dossier_template.md). Evidence requirements follow the claim, stakes and decision horizon, not a source quota.

## 1. Frame the evidence question

Identify subject, affected decision, material external claims, jurisdiction/population if relevant, horizon and constraints. Select dimensions from technical, market, audience, regulatory/legal, ethical and historical according to what could change the analysis. A skipped dimension needs a reason when its omission is material; do not invent irrelevant coverage to fill a template.

Choose the actual source mode: **web**, **supplied**, or **mixed**. Supplied-only material can be sufficient for a bounded internal question. It is not public validation or fresh web research. Unknown private facts remain unknown. Read-only access does not authorize sharing private inputs in public search queries; keep queries nonsensitive or obtain the needed authority.

## 2. Search and read deliberately

1. Start with a mapping query to identify domain vocabulary, primary organizations, mechanisms and alternatives.
2. Narrow to the decisive claims using specific entities, scope and definitions. For a business concept, distinguish interest, trial, repeat use and actual payment; for a technical claim, distinguish documentation from tested behavior.
3. Seek contrary evidence: failure cases, criticism, alternatives and the strongest opposing account. Search toward genuine disconfirmation, not a token dissenting quote.
4. For drift-sensitive claims, use relevant date filters/current terminology and verify dates in the source. A year in a query or headline does not make the underlying data current.
5. Read the source body or relevant original record for material claims. Record when only a snippet, abstract, summary or inaccessible body was available. Follow citations to original evidence when available and worthwhile.
6. Stop when additional work is unlikely to change the bounded analysis, or when access/time limits intervene. Record the remaining gap and what would resolve it. Do not keep searching merely to reach a source or dimension count.

Reformulate weak searches with technical terms, proper names or the original publication. Low-quality search results are a limitation, not evidence that no better evidence exists. Do not bypass access denials.

## 3. Source tiers are claim-relative

Record tier and a short basis. Tier labels organize inspection; they neither certify truth nor automatically set confidence.

- **A: direct/original and fit for this claim.** Examples include applicable official documentation, original data with methods, relevant primary research, a directly inspected internal record, statutory/regulatory text for what it says, or a firsthand interview for what that person reported. A source may establish its own policy or observation without proving effectiveness or general applicability. Peer review, official branding and expertise do not remove methodological limits or conflicts.
- **B: accountable secondary synthesis.** Reporting with named sources and transparent sourcing, expert analysis engaging evidence, or a documented review of relevant original work. Check whether it adds independent analysis or merely repeats another source. Access-limited analyst reports cannot support claims whose underlying text was not inspected.
- **C: contextual signal or weakly supported account.** Forum/social posts, promotional material for general outcome claims, summaries, aggregators and anecdotes. These can establish a person's stated experience or a company's positioning, while remaining weak evidence for population prevalence, causality or market size. Follow leads to stronger material where consequential.
- **D: unreliable or unverifiable for the claim.** Untraceable assertions, spam, fabricated-looking evidence or unsupported derivative content. Do not use these to establish a material conclusion; record only when their existence itself matters and is directly observed.

The same source can merit different treatment for different claims. A vendor page is primary for its listed feature and interested testimony for performance claims. A user interview is direct evidence of that interviewee's account, not proof of demand across a market. For high-stakes current law, medicine or finance, use authoritative applicable sources and state the limit of this analysis; do not infer individualized professional advice from generic material.

## 4. Time and provenance

Assess pace at the **claim** level and record the dossier's dominant pace:
- **Fast-moving:** current capabilities, availability, prices, rules, launches or volatile conditions. Prefer current applicable primary evidence and check for superseding updates. Old foundational work may remain useful for a stable mechanism while being inadequate for a current feature or rule.
- **Standard:** established professional/business practices where recent context and transferability still matter. Older evidence is acceptable if its conditions remain relevant; say why.
- **Slow-moving:** established concepts or historical questions where foundational sources can remain appropriate. Do not require an arbitrary recent fraction.

Keep publication/update date, event/data period, external retrieval date and local inspection date separate. A document downloaded today is not evidence generated today. Use `unknown` when a date is unavailable and `n/a` where the date type genuinely does not apply. Do not fill unknown publication dates with retrieval dates. A future publication date is anomalous relative to the stated as-of date, not recent evidence; investigate or mark unusable for a present-tense claim. Preserve raw date anomalies rather than silently correcting them.

Give each source a stable S ID, resolvable URL or authorized document locator, origin group and access extent. Origin records the original evidence-producing source, not only the web domain. Syndicated copies, press-release rewrites and articles citing the same study are one evidence origin for that claim. Keep distinct useful interpretations but never count them as independent observations.

## 5. Write findings the next phase can use

A dossier D finding states a narrow claim and its type (observed/documented, supplied claim, or researcher inference), relevant dimension, supporting S IDs and precise locations, applicability, contradictory evidence, recency and caveats. It should identify what the source establishes and what remains inferred.

Synthetic illustration: a supplied interview says one customer prefers ordering only when supplies run low. The supported claim is that this interviewee expressed that preference. “Remote workers reject subscriptions” exceeds both population and strength. The next useful hypothesis may be whether target customers' replenishment patterns fit a fixed schedule, with evidence still needed.

Separate a source's reported opinion from evidence supporting that opinion. Keep arithmetic inspectable with actual inputs, units and calculation, but do not create an estimate from unsupported multipliers. Empty evidence is not zero demand, zero risk or zero feasibility.

## 6. Map disagreement honestly

For each material disagreement record subject, position, named source/advocate, basis, context/date, shared ground and implications. Check whether different populations, definitions, data periods or objectives explain the difference before treating it as contradiction. Do not give a weak fringe claim equal weight merely to appear balanced.

Use **State: disagreement** when actual conflicting supported positions were found. Use **State: consensus** only for bounded common ground in the reviewed evidence, with Scope and source IDs; this does not mean universal agreement. Use **State: unassessed** if contrary evidence was not adequately examined, with the reason and its consequence. A heading labelled “disagreement” or “N/A” is not the work.

## 7. Sufficiency and structural gate

The dossier's **Assessment: bounded** means its limits and evidence have been documented for a specified scope; it does not mean the claims are independently proven. **Assessment: incomplete** identifies unresolved material coverage, access, date or evidence problems that prevent the intended next-phase conclusions. State in Evidence Sufficiency which claims the available evidence can support, which it cannot, and whether to proceed narrowly, repair research or ask a focused question.

Check relevant dimensions, claim/source traceability, origin diversity where independent corroboration matters, currency of decisive claims, actual contrary-evidence effort and explicit inference labels. A single applicable source may settle a narrow documentation question; many sources may still fail to establish causality or transfer to this case.

The shipped dossier helper is required for saved dossiers and optional for unsaved in-context work; it checks structure and detectable consistency. Record the actual result, or blocked/not run with the reason, without claiming an unperformed check passed. It does not read every cited source, certify credibility, establish semantic sufficiency, prove currentness or authorize any action. Repair genuine structural defects; retain honest incompleteness rather than padding for a PASS. If web access is unavailable, disclose the actual supplied evidence and remaining limits instead of pretending research succeeded.
