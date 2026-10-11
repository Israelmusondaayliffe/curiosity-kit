# Source-backed relationships

Use this method to answer a bounded relationship question, inspect a supplied graph, or prepare a graph change. Read [the source contract](../references/source-contract.md) first. For scalable parsing, indexing, graph traversal, incremental processing, media, or exports, also read [the Graphify provider guide](../references/graph-provider.md).

A map can show what the sources connect. It cannot turn repetition into independent evidence, similarity into identity, or a dependency into causation. Keep the supporting claim and its conditions visible.

## Choose the actual result

- A small, selected set of documents can support a local relationship map using ordinary file readers. Produce the map, citations and unresolved questions. No provider is required.
- An existing provider graph can help locate relevant material. Check its corpus and revision before relying on it. Answer from the underlying evidence where accessible.
- A requested scalable build, update, merge, visualization or media operation needs the declared provider and the relevant qualification. A manually written map does not complete those operations.
- An audit or question is read-only. Rebuilding, adding a source, saving an answer, publishing, or installing an integration is a separate effect. Do only the effects covered by the current request and applicable approvals.

Do not make another personal skill a prerequisite. Leave coding implementation work, capture systems and decision interviews with their existing owners. This method owns the general evidence-backed relationship artifact.

## Establish the boundary

Record the question, intended audience, selected source set, corpus identity and source revisions. Name the graph input and requested output, if any. Include the relevant time window and whether the question concerns historical or current state.

For provider work, identify the environment, absolute corpus root, output root, graph filename and allowed effects. Never infer the root from a convenient current directory or an existing graph directory. A saved graph can describe a different project. A supplied manifest is a claim to check against the selected inputs.

Inventory every selected input as read, partially read, unavailable, unsupported, excluded or prohibited. Keep those states separate from a complete read that found no relevant relationship. Follow only authorized links. Do not expand into all repositories, notes or accounts because a source mentions them.

## Build identities before edges

1. Give each corpus a stable identity. For a repository, use its verified repository identity and the selected commit; for a document collection, use its declared collection identity and selected snapshot. A directory basename is not a repository identity.
2. Identify a source by corpus plus its full relative path or provider-native document ID. Store the observed revision or content digest separately. Keep the original locator and its resolvable root; a private absolute path is not a portable citation.
3. Identify a file-owned entity by corpus, full relative path, entity kind and qualified name or stable source anchor. Preserve this tuple even if a provider assigns a short ID. If a compact ID is needed, serialize the tuple unambiguously and hash it with a standard digest, retaining the tuple for inspection. Do not concatenate lossy lowercase stems.
4. Treat occurrences and cross-source concepts separately. Two occurrences can refer to one concept, but that equivalence needs evidence. A shared label alone is insufficient.
5. Keep an alias list with its scope, source and reason. A preferred term or Avoid list can broaden retrieval without proving entity equivalence. Preserve disputed aliases as candidates. Do not merge people, services or symbols merely because their names match.

For example, `service-a/src/auth/session.py::ValidateToken` and `service-b/src/auth/session.py::ValidateToken` remain distinct within one corpus. A second repository containing either path remains distinct too. Line numbers locate an occurrence at a revision; they are not stable entity identity across arbitrary edits.

## Extract claims, then represent relationships

Read the original passage, code location, figure or timestamp. Record the proposition it supports before shortening it to an edge. Preserve quantities, units, negatives, conditions, authority, effective dates and exceptions. A source that says an integration is proposed does not establish an implemented dependency.

Each relationship must retain:

- Source entity, relation and target entity, with direction or an explicit undirected meaning
- Evidence status: `EXTRACTED`, `INFERRED` or `AMBIGUOUS`
- Source identity, revision and a usable locator, or a named evidence gap
- Supporting passage or a faithful short paraphrase, plus rationale for an inference
- Applicability conditions, observation date when known, and current, historical, disputed or superseded status

`EXTRACTED` means the source explicitly states or structurally exhibits the relation. It does not mean the source is true or authoritative. `INFERRED` means a stated reasoning step joins evidence that does not itself state the relation. Include plausible alternatives and the check that would distinguish them. `AMBIGUOUS` means identity, direction, relation or support remains unresolved. Say which part is uncertain. Do not hide an unsupported link behind a high score.

Use categorical status as the local default. If a provider supplies a numeric confidence, preserve it as that provider's estimate with its rubric and provenance. It is not a calibrated probability, proof of truth or a substitute for status and evidence. Do not invent missing scores or force several incompatible scoring scales into one.

Choose a small vocabulary suited to the question. Define direction in words: caller `calls` callee; document `cites` source; decision `supersedes` earlier decision; claim `depends_on` prerequisite. Shared authorship, topical similarity, dependency, chronology and causation are different relations. Add a new type only when an existing one loses relevant meaning.

Preserve parallel edges when their relation, evidence, time or conditions differ. Reciprocal relationships need two directed records. A legitimate recursive call or self-reference is not a dangling endpoint. A grouped relation involving several participants may use a group record with all members and supporting evidence; do not imply every pair is linked.

## Assemble and inspect

For small maps, a short prose list or table is enough. Use stable entity and relation IDs when later updates will refer to them. Keep the source list beside the map. No universal JSON wrapper is required.

For larger reading work, split only the selected material into bounded chunks suited to its size and modality. Assign each source once unless overlap is deliberate and recorded. Give readers the same identity rule and relation definitions. Choose one result channel for the run, such as structured returned records that the coordinator collects. Do not require disk chunk files after choosing returned records. If the host returns files instead, inspect exactly those named files, not a broad glob that can include prior runs.

Reconcile returned records against the expected source list. Record every completed, empty, failed and unread chunk. A successful empty extraction is a result; a missing return is not. Count independently observed incidents rather than echoed summaries. Resolve identity collisions by returning to source evidence, never by keeping whichever duplicate arrived first.

Before presenting a usable graph or map:

1. Check that every edge endpoint exists and every cited locator resolves within the selected source set. A missing endpoint blocks publication of that graph. Keep a separate partial diagnostic if useful.
2. Inspect same-label entities and aliases for false merges. Check the question's load-bearing directions against their original evidence.
3. Separate explicit facts, proposed relationships and contested interpretations. Trace summaries to their underlying origin rather than counting derivative copies as corroboration.
4. Check observation dates and applicability. A fresh summary of an old result does not refresh the result. A later contributor using an older revision cannot supersede current evidence by arrival order.
5. List material missing sources, unsupported formats, failed reads and truncation. A graph can be useful and partial; report both. Do not call it complete because some fragments parsed successfully.

Community clusters, high-degree entities and surprising connections are navigation aids. They may suggest a useful question or source to reopen. Centrality does not establish importance to the user, trustworthiness or a causal role. Give labels that describe inspected members; do not turn an inferred cluster theme into a source-authored decision.

## Answer query, path and explain requests

First identify candidate entities using exact labels, known aliases and source-owned terms. If several candidates fit, show their full identities. Resolve from context where the evidence distinguishes them; otherwise ask the smallest necessary question or answer separately. Do not silently choose the first tied result.

For a query, retrieve a small connected evidence set around the candidates, then reopen load-bearing sources. Say whether the answer describes an explicit relation or an inference. Include contradictory or superseding evidence that changes the answer.

For a path, state whether the user needs directed reachability, an undirected connection, or a specific relation type. Walk the selected relation types in the required direction. Show each hop's evidence status and locator. A shortest connection is not necessarily an execution sequence, a causal explanation or the strongest-supported path. If the provider searches an undirected graph, label that limit and verify arrows separately. Never answer a directed question with an undirected path as though they were equivalent.

For an explanation, identify the exact entity and its source role, then describe relevant incoming and outgoing relations separately. Preserve parallel relations. Explain why the relations matter for the question without adding undocumented behavior. Expose unknown dependencies as unknown.

Budget complete evidence records. Narrow the graph, lower traversal depth or summarize nonessential branches before dropping a load-bearing locator. Do not cut raw output in the middle of an edge or citation. Disclose the traversed scope, filters and omitted branches where they affect confidence.

Distinguish these outcomes:

- No matching entity in the completely searched bounded set
- Matching entities with no path under the stated relation and direction rules
- Inconclusive because the source set, graph coverage or retrieval is incomplete
- Provider operation unavailable, while a named bounded file analysis may still be possible

Do not save a query answer, add it as a node, run reflections or alter source records by default. If the user asks to retain the answer, create the selected derivative with primary-source links, generation date, uncertainty and correction history. A later answer must not cite that derivative as independent corroboration of its own origins.

## Propose or perform a scoped change

A read-only audit returns proposed changes. An authorized update applies only the selected change in the named destination. Before writing, preserve the previous usable artifact through the host's ordinary collision-safe versioning or backup method. Use a new output location when replacement authority is unclear.

For each changed source, determine its previous and replacement contribution. A source that now yields zero entities must remove its old contribution in the candidate result. A deleted source must not linger as current evidence. An inaccessible source is different: preserve its history with an access gap, rather than pretending it was deleted or false.

Retain unaffected claims and their evidence. Mark a changed claim and its actual dependent claims for review. Do not invalidate every fact in a document because one assertion changed. A supersession edge needs evidence identifying what was replaced and when; preserve historical meaning and authorized history.

For provider updates, follow the provider guide's real command boundaries and failure checks. Do not hand-edit provider caches or manifests to make a failed run appear current. Prepare and inspect a candidate output, including requested exports, before selecting it as the new usable revision. If publication fails, report the exact artifacts that changed and retain the prior usable revision. Do not report a transaction or recovery guarantee the provider has not demonstrated.

## Worked local example

Suppose the selected synthetic collection is `payments-notes` at snapshot `r4`:

- `decisions/retries.md`, lines 8-10: the accepted decision sets two retries for interactive requests and excludes batch imports.
- `proposals/three-retries.md`, lines 3-7: a later draft proposes three retries and calls the service "Gateway".
- `glossary.md`, lines 4-5: "Gateway" is the presentation name for the interactive service, not the batch importer.
- `incidents/timeout.md`, lines 11-16: a workaround succeeded, but the cause remained unknown.

The useful map identifies the accepted retry decision, interactive service, batch importer, proposal and observed incident separately. It includes:

- The accepted decision `applies_to` the interactive service, `EXTRACTED`, with the two-retry condition and batch exclusion intact.
- "Gateway" as a glossary-supported alias for the interactive service. The word alone does not merge the batch importer.
- The draft `proposes_change_to` the accepted decision, `EXTRACTED`. It does not `supersede` it without acceptance evidence.
- The incident `may_inform` retry design, `INFERRED`, with its unknown cause stated. It does not prove that retries fixed the underlying fault.

If the draft cites an unavailable benchmark, record that evidence gap. It limits the proposed change's support, not the existence of the accepted decision. If a later authorized correction changes only the incident's timing, update timing-dependent conclusions while retaining the supported retry decision.

## Deliver and stop

Return the answer or requested artifact first. Give exact source identities and locators, meaningful gaps, and the next evidence needed when unresolved. For file work, identify the actual output and read it back. State whether the result is a local bounded map, a provider candidate, an audited graph, or a completed qualified provider operation. State remaining native or provider checks without implying they ran.

Stop when the requested question or artifact is complete within its boundary, or the next dependent action requires missing evidence, access, provider capability or user authority. Do not add a watcher, persistent store, broad crawl or new runtime to finish a bounded mapping task.
