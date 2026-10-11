# Read hiring signals

Use for current vacancies, recent role postings or company-direction hypotheses based on jobs. Apply [the evidence contract](../references/evidence-contract.md) and the collection method in [research.md](research.md). A posting is evidence of advertised recruiting intent; it does not prove a hire, headcount increase, funded budget, revenue or a delivered roadmap.

## Verify the company and board

1. Resolve the actual company, country and official domain. Follow its careers link or an official link to the hiring board. Greenhouse, Ashby, Lever, Workable and SmartRecruiters are possible public board hosts, not guaranteed integrations. Verify the board's company name, linked domain and job content against the requested organization. An inferred slug, guessed URL or first nonempty board is only a lead.
2. Prefer readable first-party careers/board listings through available native or permitted browser tools. Follow pagination or record the unvisited pages and displayed total. If a supported read tool exposes a public ATS response, use its actual returned fields and continuation. Do not install a CLI or probe credentials to enable collection.
3. If board content is unavailable, inspect the careers page's visible jobs or accessible JobPosting structured data. Handle a single object, arrays and nested @graph entries; resolve relative job URLs against the verified source page. If neither works, use indexed job pages as a web-search sample. Record the actual source tier and outcome. A failed board with ten indexed hits is a partial search sample, not ten total vacancies.
4. Match mirror/aggregator entries back to canonical postings where possible. Deduplicate by employer plus stable posting ID/canonical URL, using location and role details to resolve ambiguity. The same title in different locations or distinct requisitions can represent separate vacancies; title-only deduplication loses evidence. Conversely, one role mirrored on five sites remains one advertised role.

## Establish what the dates prove

Capture title, posting identifier/URL, department, location/remote scope, seniority, substantive responsibilities and source dates. Distinguish original posting, modification, expiry/validThrough and retrieval times. Check whether the role is still listed and whether an expiry date contradicts a "currently open" claim.

For "posted in the last 30 days," include only roles with a supported original posting date in the selected interval. A recently edited old posting or fresh mirror does not establish a new vacancy. For "currently hiring," a readable current board can establish a vacancy snapshot even when original date is unknown; keep it out of the verified new-posting count. A newly observed role is only new to this collection unless a comparable earlier board snapshot establishes an addition.

Compare role populations only across named snapshots with compatible company, filters, board coverage and date semantics. Separate additions, revised descriptions, reposts, expired roles and not-observed items. Missing roles during an outage are not confirmed filled or removed. If a pagination cap or access failure changed coverage, do not report a hiring acceleration or decline from raw totals.

## Interpret the actual responsibilities

Group related roles after reading their descriptions. Use tokens and phrases with word boundaries: "AI research" and "machine learning" can support an AI/ML theme; "retail," "email" and "supply chain" cannot because they contain the letters ai. A role can support more than one theme, but report unique-role totals separately from overlapping theme counts.

Useful themes and the evidence to look for:

- Enterprise readiness: enterprise security, compliance, solutions architecture or procurement responsibilities tied to business customers.
- Go-to-market: sales segments, new territories, customer success or marketing mandates with specific audience/product context.
- AI/ML: explicit modeling, ML infrastructure, evaluation or deployed AI responsibilities, rather than a generic company slogan.
- Infrastructure: reliability, platform, developer operations or scaling work described in the role.
- Product expansion: a named product, market or function and concrete development responsibilities.
- Data/analytics: data engineering, analysis, measurement or experimentation responsibilities.

Keep unmatched postings as ordinary department/general hiring. Company size must come from a dated reliable company/source statement when needed; five sampled roles do not make the company a startup. Do not derive a numerical confidence score from counts or undocumented size thresholds. Explain confidence through directness, posting identity, date quality, coverage and agreement with other evidence.

Review strategic roles separately from bulk themes. A first/founding role, new executive mandate, specialized function or unusual location may matter even as a single posting. Read the exact wording and check available baseline/context before calling it the first role or a new expansion. A title such as "Founding Engineer" supports that advertised title; it does not establish the company's full history. A senior title alone does not prove a new department. Keep credible isolated signals visible rather than hiding them under a volume threshold.

## Report a bounded finding

For each material signal, give the observed role(s), canonical links, relevant responsibility excerpt/paraphrase, date basis, unique-role count and interpretation. State competing explanations when consequential: replacement hire, evergreen listing, remote location option, board repost or ordinary scaling. Corroborate a proposed business expansion with official plans or other independent evidence before upgrading it beyond a hypothesis.

If hiring is incidental to general research, include only findings that help answer the question and explain omissions when asked. If hiring was explicitly requested, report sparse evidence and strategic singletons with their limits instead of suppressing the section. Distinguish "no qualifying new postings found in this accessible sample" from "the company is not hiring."

Before delivery, reconcile counts to unique posting identities, check mirrors and old reposts, verify the board/company match, and ensure no inference became a claimed hire, budget or revenue figure. Preserve private-source dependencies in any derived hiring interpretation or export.
