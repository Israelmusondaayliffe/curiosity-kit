# Saved library and selected local corpus

Use this route for “find my earlier research,” importing an old brief, retrieving an exact saved run, or researching explicitly selected local documents. It does not collect fresh web evidence. Read [local-store](../references/local-store.md) for the actual helper/schema and [evidence-contract](../references/evidence-contract.md) when interpreting or creating records. Resolve the packaged script relative to this skill, not the current working directory; store operations below require the user-selected `--root STORE`; `validate INPUT` only reads its explicit input.

## Retrieve before researching

1. Establish the selected store or supplied artifact, topic/entity, requested date meaning and output. Reuse a store already selected for this task; do not guess a home directory or search every connected account. “What did we find last week?” normally means saved research/run dates, whereas “what happened last week?” asks about source/event dates. Keep the distinction visible.
2. Use `list --root STORE`, `search QUERY --root STORE` and `show RUN_ID --root STORE`. Apply the entity/date/source filters documented in local-store when requested. Search literal topic terms and relevant aliases, then read the exact matching record and relevant source body, not just its search snippet. Preserve run/item IDs in working notes and links/locators in the answer. A missing store, empty store, unreadable/corrupt record and successful search with no match have different outcomes.
3. Answer from the selected record with its original window, collection time and coverage. Say “In the saved September 8 run…” rather than “currently.” A run timestamp is not source publication. Imported legacy text may be useful historical context while lacking a trustworthy window or source ledger. Do not recursively treat a saved synthesis as independent primary corroboration.
4. If the user wants current information, use the saved answer as background and perform the targeted [research](research.md) or [freshness](followup-health.md) route. Library lookup alone never refreshes it. For a conversion/retrieval-only request, stop after returning the selected existing evidence; cache miss is a blocker or an invitation to select another artifact, not permission for silent live research.

## Save normalized research or import legacy work

For a new normalized record, first inspect its claim/source/date/visibility ledger, run `validate INPUT`, then `ingest INPUT --root STORE`. Read back with `show RUN_ID --root STORE`. Validation proves bounded shape/identity properties, not truth. Exact same identity/content is an idempotent repeat; different bytes under that run ID are a conflict. Create a new observation/run identity for changed evidence and retain the original.

For explicitly supplied legacy Markdown/JSON, use `import FILE --root STORE` (optionally `--id` as documented in local-store). Preserve any supplied contextual metadata in a separate clearly labelled companion note; do not invent unsupported import flags. Preserve the original bytes and provenance. An import is a legacy artifact, not a completed recent research run. A date in a filename, filesystem modification time, or today's import timestamp cannot supply missing publication, event, query, entity or coverage facts. Read the original text when interpreting a match. If useful source links are present, distinguish links merely mentioned from source bodies actually read.

One URL may occur in several topics and at several dates. Keep each run's observation, source body and measured engagement, including decreases. Never migrate all sightings into the first topic or replace earlier observations with the latest text/maximal metrics.

## Explicit corpus selection and preparation

- Confirm which supplied files or named directory scope the user selected. A request to use those files permits reading that bounded corpus; it does not permit unrelated account/home discovery or sending their contents to external services.
- The helper accepts explicit `.txt`, `.md`, `.json` files, at most 100 per invocation, through `corpus index FILE... --root STORE`. If a directory was selected, prepare a bounded exact-file manifest first, excluding hidden/system folders and symlinks; do not silently broaden recursively or hide omitted files. For more than the bound, choose a disclosed task-relevant subset or process separately within the approved scope.
- PDF, image, audio, proprietary documents and other formats require an available supported reader/extractor first. Retain original filename/locator, extraction method and page/section/timestamp anchors alongside extracted text. Explain missing access or extraction errors; do not install a parser or upload the file merely to make this lane work.
- Index only selected extracted/plaintext files. Retain content identity, original locator, extraction provenance, index/retrieval time and visibility. Modification time describes local file observation, never publication or high-confidence event date. Reindex changed bytes as a new version; preserve earlier evidence used in saved runs.
- Use `corpus search QUERY --root STORE`, inspect matched passages in context, and check entity/date relevance. Literal search is bounded retrieval, not a claim of exhaustive semantic search. Record a real no-match separately from unreadable input or failed indexing.

## Synthesize private evidence correctly

Treat local evidence as a separate private lane by default. Cite a usable document/page/section locator to the authorized user, and say “From the files you selected.” An internal note is evidence that the note says something; assess who wrote it, when, whether it is firsthand, and what it establishes. Its newer modification time does not outrank a public source's verified event date.

Carry all contributing source dependencies into every derived claim, title, snippet, contradiction, cluster, drill summary and freshness result. A privately learned entity name or inferred sensitive query must not be sent to web search without applicable authority. Public-only research can proceed using independently public terms. When private and public evidence conflict, explain the conflict privately with both bases; a public export must independently rebuild its conclusion from retained public evidence, or omit it. Removing a corpus source row or marker block is insufficient.

## Failure and recovery

Read-only lookup never initializes or “repairs” a missing store. On invalid schema/hash/conflicting identity, preserve both supplied input and prior valid state and report the exact bounded error. Do not turn an unreadable archive into an empty successful library or delete source artifacts to rebuild it. For an interrupted mutation, follow local-store's documented recovery, inspect final committed bytes, and retry only an idempotent operation with the same known input. A stale watch revision belongs to [watch-brief](watch-brief.md), not a force-overwrite library repair.

Deliver the found answer or an honest no-match, exact saved identity/date, useful evidence links/locators, and any limitation that changes how the result should be used. For saved files use [export](export.md) to produce and deliver an accessible artifact; a private executor path alone is not a user handoff.
