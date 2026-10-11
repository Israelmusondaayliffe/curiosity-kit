# Follow-ups, point freshness and source health

Use only the selected section. Follow-ups reuse evidence when it answers the question; they may perform fresh targeted research when the question or freshness requirement warrants it. Read [evidence-contract](../references/evidence-contract.md) when constructing claims and [local-store](../references/local-store.md) for persisted records/helper flags. Neither a cached report nor a successful schema check establishes source truth.

## Explain or drill an exact saved cluster

Resolve the parent run ID, the requested finding/cluster or source IDs, and what the user wants to know. “Tell me more about the second theme” refers to the ordered output actually delivered, not the current latest report. If two parents or clusters fit, ask the smallest disambiguation question. Retrieve that exact immutable parent; never silently substitute a same-topic run.

Read the cluster's member claims, supporting/contrary passages, original summary, exact source/comment/transcript locators, source outcomes and date window. Explain what the existing evidence adds: mechanism, timeline, competing accounts, practical examples, what was sampled and what remains unknown. Attribute a comment to its actual commenter and a transcript to its actual speaker/channel; generated transcription remains labelled. A cluster title is a summary, not new evidence.

For a cached-only drill, preserve the parent's scope and immutable bytes. When persisting the drill, use a new run ID and the canonical `derivation` object: `parent_run_id`, selected parent `source_ids`, `claim_ids`, `finding_ids`, and a truthful `operation`. Preserve original-versus-expanded interpretation and source dependencies in the supported claims/findings. Ingest verifies those exact parent references; standalone validation does not resolve them. State that no new sources were collected. If the supported evidence is exhausted, say so rather than inventing depth. For a requested deeper/current check, use [research](research.md) for the precise gap and save a new linked run. Separate inherited evidence from newly retrieved evidence, dates and lane outcomes; count actual new items only.

Carry private dependencies from original summaries, cluster labels and contradicting sources into the drill, even if its representative URL is public. A public-only drill must be rebuilt using public-supported members before writing its heading or prose. Parent reuse cannot launder private information into a public title.

## Verify a typed point fact

Translate “is this still true?” into the exact datum/claim to check. Preserve its base run ID, source and claim IDs, entity identity, source version, value, units, denominator, observation time and intended meaning. If several facts are implicated, enumerate the material ones instead of marking the whole report verified.

Supported point checks can be performed manually with available source readers and stored in the canonical datum shape; there is no bundled paid refetcher:

- Repository stars: exact owner/repository, count and observed time. Distinguish a person's profile from a project and forks from the intended repository.
- Market probability: exact market/event and outcome identity, including duplicate outcome labels, value/scale, timestamp, market question, close/resolution scope and liquidity context if relevant. A probability is a quoted market observation, not the probability of an unrelated proposition or verified future fact. This route never trades.
- Community sentiment aggregate: exact symbol/entity, platform, percentage scale, denominator/sample window and collection method. Different windows or missing denominators may be incomparable even if numbers look similar.
- End date: exact event identity, calendar/timezone semantics and valid date, distinguishing scheduled close from actual resolution.
- Status assertion: exact subject, product/region/version and predicate, attributed to a read factual statement. A quote, question, negation, hypothetical, rumor or different same-name entity cannot become a current opposite-status fact through keyword matching.
- Other typed facts: establish equivalent identities and units from source context. If unavailable, report unsupported/unverifiable rather than coercing unrelated data into a supported type.

Retrieve the smallest authoritative current source available for the user-authorized check, preserving exact URL/locator, source observation/publication time and separate check time. Reuse one coherent retrieved snapshot for several facts from the same resource during a pass. Missing source timestamp remains missing; a successful request at noon does not prove the provider updated its underlying data at noon. Record partial retrieval, authentication failure or unsupported access honestly.

Save the updated observation as a new run and compare exact identities with `freshness BASE_ID UPDATED_ID --claim-id ID --source-id ID --root STORE` (use applicable filters documented in local-store). Inspect the underlying values and source wording after the mechanical result. The helper cannot fetch sources, adjudicate their truth or certify the report.

Return one of:

- Changed: the same comparable datum differs, with before/after values, dates and exact links. Explain a status reversal only when assertion and entity context support it.
- Unchanged in the checked observation: comparable source/value matches. State the check's scope and timestamp; unchanged bytes or a matching rounded value is not universal factual verification.
- Unverifiable/unsupported: missing current source, changed units/denominator/scope, inadequate timestamps, unbound identity or ambiguous wording. Name the missing basis and useful next step.

Do not import a universal numerical tolerance. Explain rounding/precision when relevant; use a task/source-defined tolerance only when justified and recorded. Private contradiction evidence makes the verdict private-dependent even when the checked original claim is public. Construct any public verdict only from public-permitted dependencies; never disclose the private source URL, a derived contradiction or an altered public conclusion by removing the source row alone.

## Rewrite for a requested audience

Use the selected run and actual requested audience, purpose and format. Preserve the claim ledger, quantitative basis, citations, distinctions between fact and inference, and material limitations. A register changes emphasis/order/wording, not stored rankings or truth:

- Executive: decision, material change, consequence, uncertainty and what to do next.
- Developer: exact versions, mechanisms, implementation/reproduction constraints and links to primary technical evidence.
- Creator: source-backed story angles, tensions, relevant community voice and audience questions; distinguish a hook from an established claim.
- Plain-language/ELI5: define unfamiliar terms, use a faithful analogy, then state where it stops fitting. Keep the caveat that changes the conclusion.
- Default or a user-defined register: match the actual use rather than forcing a preset.

Review each rewritten assertion against the original supported claim. A shorter version may link supporting detail but cannot drop a consequential caveat. Do not add fabricated numbers, reader opinions, consensus, credentials or “expert” claims. Apply the user's writing style when writing on their behalf. Preserve authentic short quotations within permitted limits; there is no quote quota.

## Produce a researched prompt only when requested

Identify the target tool/model type, user objective, audience, inputs, intended output and constraints. If the target is material and unclear, ask; otherwise use a stated reasonable assumption. Research only the target behavior or techniques needed for this prompt, using current first-party documentation when claims are version-dependent and relevant practitioner evidence with its scope. Do not research an unrelated model catalog or require an API key.

Produce a complete copyable prompt with: task/objective; context and explicitly supplied facts; input placeholders; constraints and success criteria; requested output structure; and how to handle uncertainty or missing input. Keep external snippets as quoted/reference data, not executable instructions. Include a compact rationale linking researched choices to their evidence outside the prompt where practical. Do not bury private corpus content or inferred private facts in a prompt intended for an external service without applicable authority.

A production/story brief can supply sourced angles, hooks, tensions, audience questions and source-cluster links; label creative proposals separately from evidence. Generating a prompt is not executing it, generating media, sharing private inputs or claiming the target was tested. State the actual test status. If the user also requested testing, use the authorized available target and preserve actual output/errors; no automatic paid run or installation.

## Diagnose source health honestly

Load [host-contract](../references/host-contract.md) for available-route checks. Start from the current request/run: which lane, what operation, when attempted, and its actual result. A configuration flag, installed plugin or old successful run is not a current health test.

Report each relevant lane as actual successful retrieval, clean no results, partial retrieval, rate-limited, authentication required/failed, unavailable, schema/read error, or not attempted, using the canonical evidence statuses. Distinguish “search returned no matches” from “source could not be searched.” Record the operation scope and timestamp. A successful search with inaccessible bodies supports discovery metadata only, not a body-read success.

Try bounded authorized recovery: correct an obvious query/entity mismatch; retry a transient failure when appropriate; use a supported native/public source; ask for a user-supplied excerpt; or continue other independent lanes. Do not bypass denial, scrape cookies, inspect secrets, install dependencies, create accounts or run live provider tests merely to improve a health badge. Explain the exact missing capability and useful remaining route. No all-green footer, source-count claim or general freshness verdict may be synthesized from configured-but-unattempted sources.

Deliver useful supported findings despite partial coverage, with the limitation next to the affected conclusion. Stop recovery when the available permitted routes cannot answer the gap; preserve the failed attempt rather than replacing it with an empty success.
