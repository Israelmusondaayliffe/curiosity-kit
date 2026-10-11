# Evidence, dates and disclosure

This reference owns interpretation rules across research, saved runs and outputs. The exact versioned JSON/CLI contract is in [local-store.md](local-store.md); do not invent fields or mistake a parser result for a factual verdict. For a short unsaved answer, the same distinctions can live in concise working notes rather than a formal ledger.

## Identity and time

Keep the exact subject, product/version, geography and question attached to each observation. Resolve aliases against a primary identity record; same-name companies, people and projects are different subjects. Preserve case-sensitive URL paths and query values. Remove tracking parameters only when doing so demonstrably preserves resource identity. An exact duplicate URL is an item deduplication candidate, not permission to discard distinct observations of it at different times.

Separate publication, substantive update, event, retrieval and local-import times. A page read today did not necessarily publish today. A recent announcement of a future event is recent evidence of that announcement; the event has not happened. A fresh reprint inherits its original event/publication basis for claims of novelty unless it adds genuinely new reporting. Preserve both dates and origin lineage. A generated synthesis, filesystem mtime or importer timestamp cannot supply a missing source date.

Default recent research uses the preceding 30 days ending at the actual as-of time, with the user's timezone when known. Record precise start/end and whether endpoints are inclusive or exclusive. For an explicitly date-only calendar range, state its convention; do not silently substitute a different instant range. Convert offsets before testing eligibility. A timestamp just before midnight locally can fall outside a UTC interval. If only a calendar publication date is known at an instant boundary, preserve that uncertainty rather than invent an hour.

Classify candidates as eligible recent evidence, older context, undated/unverifiable, out-of-window or wrong identity. Future publication dates cannot prove completed past-period publication; retain them only as labelled anomalous leads/context if useful. Do not silently repair impossible dates or widen the window to increase results. Unknown dates remain unknown. Current undated documentation may answer a current capability question while being unable to prove what changed during the window.

## What was actually collected

For each attempted lane retain the source scope, actual query or supplied-input identity, retrieval time, access route, selection/cap and outcome. Distinguish success, successful zero results, partial/truncated retrieval, failed read, authentication/access restriction, unavailable tool and not attempted. Explain an exclusion without contacting that source. A zero cap means collect nothing; optional fallbacks cannot override exclusions, the window or the requested cap. A source can yield search metadata while its body remains unreadable.

Record each material item with its exact locator, author/owner where available, relevant source body or faithful bounded excerpt, read coverage, dates and date basis. Preserve comment authors and reply relationships, transcript timestamps/language and any translation or automated-transcription limits. A body hash represents the captured bytes only; no body means no invented content hash. A partial read supports only what was actually inspected. Search snippets and AI-generated search/app summaries are leads until the underlying source is checked.

Engagement has a platform-specific metric, value and observation time; unknown is not zero. Lower later counts remain lower observations, not a reason to retain historical maxima. Platform search returns a sample affected by query, ranking, access and pagination. Neither an indexed sample nor a fixed result cap establishes exhaustive coverage.

## Claims and independence

For every consequential assertion, identify the supporting source passages, contrary evidence, scope and review status. A direct quote establishes what the quoted person said. An official announcement establishes what was announced; independent performance, adoption and impact claims may need different evidence. Distinguish observation, attributed claim, inference and unresolved hypothesis in the actual answer.

Use the canonical support states: supported, contradicted, uncertain or unreviewed. Explain partial support or unresolved dispute in the claim wording; do not invent extra schema states. A status is the reviewer's declared judgment, not authenticated proof. Check whether the cited body actually entails the assertion, including negation, subject, version, units, denominator and date. Numeric comparisons require compatible measurement conditions. Missing numbers or overlapping words cannot establish semantic support. Contradictions should change confidence or scope, not be hidden by a majority vote.

Deduplicate exact items, then group shared origins: copied press releases, syndicated articles, repeated quotations, cross-posts and summaries of the same study are not independent corroboration. Preserve a derivative source when it adds distinct firsthand evidence or useful analysis, marking what is new. Keep an origin/event identity and its uncertainty; a cluster label alone does not prove shared origin. Do not merge different vacancies or events merely because titles match. One source may support several claims without duplicating its body.

A recommendation or ranking needs grounded fit/tradeoff reasons. Popularity measures observed attention. A market price is a dated market observation with an exact question and resolution scope. Neither is an automatic truth score. If no supported conclusion follows, return that limitation and the smallest useful next verification.

## Privacy follows the whole derivation

Classify supplied sources and derived text as public, private or unknown. Local corpus is private by default. A public URL does not make a claim public when private evidence affected its wording, selection, contradiction, priority or conclusion. Propagate every contributing dependency through findings, summaries, cluster titles, drill-downs and freshness verdicts. Include query/report titles, entity aliases, watch labels, IDs, filenames and diagnostic text in disclosure review.

For public output, build a new projection from explicitly public material and reviewed public metadata. Retain a claim only when all its dependencies are public and sufficient for that wording. Omit private/unknown-supported content, or independently re-derive it from allowed public evidence. Deleting private source rows or marker strings does not sanitize a derived conclusion. Do not include hidden local paths, corpus locators, private queries or a private-dependent verdict under a public citation. Inspect the rendered/text/JSON/feed result, including headings and links, before delivery.

The helper enforces declared dependency/field rules and remaps export identities; it cannot detect an undeclared private influence or prove labels truthful. Human/model semantic review is still required. Public classification is not permission to upload/share. Private-derived terms must not be sent to public search or another service without applicable authority.

## Reuse and verification boundary

An exact saved run is an immutable observation. A later run can supersede its usefulness without rewriting history. A drill identifies its actual parent and members; a freshness comparison identifies its base/current datum, source, units and check time. An unchanged byte/value comparison is narrow evidence, not a claim that the entire external world is unchanged. Incomparable scope, missing source, stale retrieval or mismatched denominators give an unverifiable result.

Before returning an answer or artifact, inspect decisive citations, entity/date eligibility, arithmetic, origin independence and disclosure. Preserve failed lanes and consequential uncertainty alongside the affected conclusion. Structural validation, local persistence, actual collection, native host invocation and production readiness are separate claims; report only the ones established by observed work.
