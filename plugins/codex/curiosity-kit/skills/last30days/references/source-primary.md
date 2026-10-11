# Primary, developer and market evidence

Use [the evidence contract](evidence-contract.md) for record, date and claim semantics. These methods use available native tools, supported connected reads, permitted public pages or supplied evidence. They do not enable APIs, credentials, paid collectors or trading. Load only the relevant section.

## Official pages and original factual records

Resolve the official organization/domain before reading releases, documentation, changelogs, product pages, public filings, standards or original datasets. Follow secondary reports back to the cited owner. Record version, publication/update/event dates and what the source actually establishes. An official announcement proves the announcement; claimed performance, adoption or independent impact may need external evidence. A current documentation page without history cannot prove when a capability launched.

For a changing product, inspect its release/changelog and matching documentation together. Resolve a discrepancy by version and rollout status before concluding a contradiction. Keep announced, preview/beta, generally available and future plans distinct when the source makes those distinctions. Read methods/definitions behind quantitative claims and carry units, denominators and caveats into the answer. Use older material as labeled context; do not apply a blanket recency exception for an authoritative source.

## Research papers and arXiv

Search the specific research question and relevant authors/terms through available scholarly or general search. Open the abstract page and original paper when accessible. Record paper identifier, authors, original submission date, version date and exact version read. An in-window revision may be recent research activity while the original result is older; say which changed. Read the methods, evaluation setup, results and limitations relevant to a material claim, not just a promotional abstract. Identify preprint versus published status when supported. A paper author's finding is an attributed result under its stated setup, not automatic consensus. Follow substantial contrary or replication evidence when it could change the answer. Missing full text limits the claim to what was actually read.

## GitHub topic, person and project modes

Use the connected GitHub read tool or verified public pages. Explicitly constrain public-research results to public repositories even if an authenticated tool can see private ones. Do not read raw tokens. Resolve owner/repository, account type and canonical project links; stripping a suffix such as -sdk or -docs does not prove another repository is its parent. Remove only an exact .git URL suffix when normalizing, never arbitrary trailing characters.

For topic research:

1. Search relevant public issues, pull requests, discussions and releases using aliases and the task's exact date basis. Creation, update, merge and release dates answer different questions. Check both interval bounds after retrieval.
2. Read the issue/PR body, labels/state and relevant comments, including maintainer responses and resolution. Preserve comment links, authors and dates. Inspect linked code/docs only when needed to establish the claim. A highly commented open issue is not automatically a complaint or a confirmed defect.
3. Distinguish reported, reproduced, acknowledged, fixed in a commit, merged and released. A merged fix alone does not establish that users received a release. Keep remaining reproduction/version uncertainty visible.

For a person:

1. Verify the account belongs to the intended person, rather than a similarly named organization.
2. Inspect authored PRs and relevant contribution records in the interval. Keep created-in-window, merged-in-window and current-state questions separate. Record pagination and search caps before presenting totals.
3. Group contributions by repository. Verify ownership independently for each repository before labeling own versus external work. A repository absent from a short profile list is not thereby external.
4. Count open, merged and closed-unmerged PRs from their actual states. Total minus merged is not open. Distinguish observed sample counts from API/search totals, and identify any uninspected pages.

For a project:

1. Verify the repository and related package/product. Read README positioning and current release/changelog records; keep undated README context out of newly published evidence.
2. Inspect relevant releases, issue/feature-request patterns, maintainer responses and contribution activity. Choose issues by relevance and substantive evidence, using activity only to prioritize reading.
3. Capture stars/forks as timestamped popularity snapshots, not adoption or quality. Recheck the exact repository when a current metric matters. Retain falling as well as rising counts and never substitute a previous maximum.
4. Cite separate release, issue and PR dates. Do not stamp the repository with the interval end just because no release date is available.

## Careers and company boards

For vacancies or hiring signals, load [hiring.md](../playbooks/hiring.md). Follow the verified company's careers page to its actual board. Supported public pages or already available ATS reads can supply evidence, but a guessed slug or nonempty board cannot prove ownership. Current vacancy snapshots, original posting dates, modification dates and actual hires are different claims. Preserve source tier, pagination and unique posting identity before making any count or strategic inference.

## StockTwits and sampled market discussion

Use only when the question actually concerns a financial instrument or market discussion. Resolve a ticker/cashtag to its issuer, exchange or asset identity before searching; short common-word aliases alone are ambiguous. If several symbols are requested, collect and report each separately rather than implying that one symbol's stream covers all of them.

Inspect accessible messages with original timestamps and deduplicate by message identity. Record the actual interval and collection method, such as latest accessible messages or date-bounded search, plus any failures/partial pages. A latest-N stream is not a complete monthly population. Keep bullish, bearish and untagged counts separate. If calculating a bullish share among tagged messages, use bullish divided by bullish plus bearish, state that denominator, and leave it undefined when no messages are tagged. Do not silently put untagged messages in that denominator or treat them as neutral votes.

Retain author/message links and observed likes/reshares as available. Compare sentiment snapshots only with sampling differences visible; a ratio can change because different messages entered the sample. Self-declared sentiment is not investment performance, representative investor opinion or a factual forecast. Research remains read-only.

## Prediction markets and Polymarket

1. Resolve the exact event, child market/contract, outcome identity and resolution rules. Similar short titles can concern different dates or conditions. Retain stable event/market/outcome IDs when available along with the verified page link. Search active or closed markets according to the question, never assume an active-only search answers a historical one.
2. Inspect the actual question, outcomes, close/resolution date and current status. Record price/quoted probability, retrieval timestamp, volume and liquidity only where observed. An event's updated timestamp is snapshot metadata, not its original announcement date or evidence the underlying event occurred recently.
3. Attach each movement to the same contract/outcome and stated interval. A move from 0.42 to 0.47 is 5 percentage points, about 11.9% relative to 0.42; do not label the two measures interchangeably. Do not attach the most active child's movement to a different displayed outcome.
4. Check whether outcomes are mutually exclusive and exhaustive before summing their prices. Separate binary markets often overlap. Prices are market observations with liquidity and resolution constraints, not verified probabilities of truth.
5. For a freshness check, retrieve the same event/market/outcome and verify returned identity before comparing. Renamed or reordered labels do not reliably identify the same outcome. If identity, units or observation basis cannot be matched, report unverifiable rather than changed.

These observations can supplement a researched answer when relevant. They cannot override contradictory primary evidence, establish a trade recommendation, or authorize a transaction. Preserve private-source dependencies if the research also uses a selected private corpus.
