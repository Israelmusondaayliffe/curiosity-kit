# Local research records and CLI

This is the exact mechanical contract for `scripts/research_store.py`. Python 3.9+ and its standard library are the only runtime requirements. No network, subprocess, credentials, home-directory defaults, provider dispatch, automatic folder scan, installation, browser, schedule, or delivery. The model performs research and semantic review using [the evidence contract](evidence-contract.md); the helper preserves and compares supplied observations. A structurally valid claim is not thereby true. Source visibility and review flags are declarations to audit, not authenticated proof.

## Minimal operation

From this skill directory, with an explicit new temporary or user-selected store:

```
python scripts/research_store.py validate assets/research-record.example.json
python scripts/research_store.py ingest assets/research-record.example.json --root /tmp/example-research
python scripts/research_store.py list --root /tmp/example-research
python scripts/research_store.py show sample-20261009 --root /tmp/example-research
python scripts/research_store.py search export --entity 'Example Project' --source official --start 2026-10-01 --end 2026-10-09 --root /tmp/example-research
python scripts/research_store.py export sample-20261009 --format html --visibility public --out /tmp/example-report-1.html --root /tmp/example-research
```

The example is synthetic, not a real researched fact. Use `--help` or command `--help` for argument help. All commands print UTF-8 JSON to stdout. Expected failures exit 2 with stderr JSON `{"error":{"code":"…","message":"…"}}`; argument syntax errors use argparse help. Errors are explicit, not empty results. Empty matches return `{"status":"empty","results":[]}`. Missing roots are `missing_store`; corrupt/unreadable state fails rather than being deleted or silently skipped. Commands do not automatically repair state.

## Canonical run schema

`assets/research-record.example.json` is a complete valid instance. Root required keys:

- `schema`: exactly `last30days.run/v1`
- `id`: stable ASCII identifier matching `[A-Za-z0-9][A-Za-z0-9._-]{0,99}`
- `created_at`: RFC3339 timestamp with timezone, e.g. `2026-10-09T16:00:00Z`. Fractional seconds are compared at microsecond precision (pad shorter fractions, truncate beyond six digits consistently on Python 3.9+); saved source strings retain their original precision.
- `scope`, `sources`, `claims`, `findings` as below
- Optional `public_metadata` and `derivation` only

All object fields are explicitly enumerated. Unknown fields, duplicate JSON keys/IDs, nonfinite numbers, wrong types, impossible dates, invalid versions, unsafe IDs/links and dangling evidence references are errors. Convert useful donor fields into the supported provenance structures or retain the original as a clearly private legacy artifact; never silently discard useful evidence. This is a new versioned normalized record, not compatibility with the old donor dataclass/agent JSON.

### Scope

`scope = {entity, queries, window, lanes, selection}`. Entity is a nonempty string, queries a nonempty unique string array. `window = {start,end,timezone,boundary}` supports:

- `boundary:"inclusive"`: start/end are valid YYYY-MM-DD; the entire end date is included in the named IANA timezone.
- `boundary:"half-open"`: start/end are full RFC3339 timestamps, start inclusive and end exclusive. Offset precision is retained. `timezone` still names the interpretation/context; do not silently convert a requested half-open interval into dates.

`lanes` is an array `{id,status,detail}` with unique IDs. Status is `ok`, `partial`, `no_results`, `failed`, `unavailable`, `not_attempted`, or `excluded`. A lane with collected sources must be `ok` or `partial`. A no-results lane means an actual search found none; unavailable is not a zero result. `selection = {cap,method}`: cap is null or a nonnegative integer (zero requires zero sources); method describes the actual selection policy. Stored descriptions are observations/configuration, not instructions to execute.

### Sources

Required source fields:

`{id,lane,url,title,body,visibility,origin_id,published_at,retrieved_at,read_status,date_basis,engagement,locators}`.

- `lane` references a scope lane. `url` accepts absolute HTTP/HTTPS, or private `corpus:`/`urn:` locators. Userinfo/credentials and unsafe schemes are rejected. No link is fetched.
- `body` is supplied text or null. Full/partial read requires supplied body; body absence remains explicit. `content_hash` is optional SHA256 of the UTF-8 supplied body and must match exactly; no content hash is invented for a locator-only record.
- `visibility`: public/private/unknown, applying to the entire source including title, body, locators, origin metadata, author, metrics and optional fields. Mixed-provenance text must use separate source records, or private/unknown classification. Do not relabel a private-derived summary as a public body.
- `origin_id` identifies the substantive original/event lineage, not a count of independent URLs. Distinct observations may share it. It is declared, not automatically established.
- `published_at`: RFC3339 or null. `retrieved_at`: RFC3339, no later than run creation. Source future publication is allowed only when labelled `date_basis:"future_publication"`; it is not eligible completed recent evidence. Future event announcement can have recent real publication and separate `event_at`.
- `read_status`: full/partial/metadata_only/unreadable. `date_basis`: publication/event/updated/unknown/historical_context/future_publication. Date semantics and eligibility require human/model review; parser success does not admit a source to recent findings.
- `engagement`: array `{metric,value,unit,denominator,observed_at}`. Value finite; denominator null or string. Observation time explicit. Preserve falling counts exactly. Do not compare incompatible metrics/denominators.
- `locators`: array `{kind,url,label,author,text}`. Author/text nullable. Preserve exact commenter identity, thread/section/chapter URL, excerpt, auto-transcript label and supplied context here. Locator text inherits source visibility.

Optional source fields: `author`, `community` (string/null); `event_at`, `original_published_at` (timestamp/null); `content_hash`; `origin_url` (safe URL); `origin_note` (text); `eligibility` (eligible/historical_context/undated/future_publication/entity_mismatch/out_of_window/unreviewed). Use original publication for reprints, and keep later retrieval/repost observations separate. Unknown publication is null, not mtime/import time. Keep old/context/entity-mismatched observations out of supported recent claims even if retained for explanation.

### Claims, findings and typed data

Claim: `{id,text,source_ids,visibility,review_status}`, optional `datum`. Source IDs are a nonempty unique array. Include supporting, contradicting, quoted and private inputs that materially affected the assertion. `review_status` supported/contradicted/uncertain/unreviewed is the reviewer’s judgment; shape validation cannot authenticate it.

Finding: `{id,text,source_ids,claim_ids,visibility}`. Source IDs nonempty; claim IDs may be empty. A finding/cluster/drill summary must list every contributing dependency, including indirectly through claims. Public projection checks both edges. Free-standing unsupported summary fields are not allowed.

Optional claim datum: `{kind,key,value,unit,denominator,observed_at}`, optional `modality`. Kind number/probability/percentage/status/date. Probability range 0..1; percentage 0..100; date a real YYYY-MM-DD; numeric values finite. Key must fully bind the entity/repository, market event/outcome occurrence, symbol/window or status subject. Unit and denominator must match before comparison. Modality asserted/quoted/hypothetical/question/negated; omitted means asserted by the submitting reviewer. Quoted/question/hypothetical/negated data do not become verified factual status assertions.

### Public metadata and derivation

`public_metadata = {reviewed:true|false,title,entity}`, optional `coverage` (array of reviewed public-safe caveats) and `window` (must exactly match scope window). Public generation requires reviewed true. Review these fields for private names and inferences; they are not automatically made safe by labelling them public. Include material date/coverage limitations in the reviewed fields. Anonymous lane outcome enums are additionally preserved without private lane names/details.

`derivation = {parent_run_id,source_ids,claim_ids,finding_ids,operation}` optionally identifies an exact saved parent and selected parent members. Ingest checks parent existence and every selected member. Empty member arrays are allowed only where no such member informed the operation; the reviewer remains responsible for complete dependencies. A private/unknown selected parent dependency blocks public export of the derived run, including transitive dependencies. Rebuild from public evidence rather than deleting the private row or laundering its conclusion. Validation alone cannot check a parent store; ingest does.

## State and recovery

`ingest INPUT --root STORE` validates before creating the store. `runs/ID.json` is canonical and immutable. Exact repeated ID/content returns unchanged; changed content under an existing ID returns conflict. Canonical JSON serialization makes key order irrelevant. Files are created mode 0600 and newly owned directories 0700; existing unrelated permissions are not changed. All selected path components reject symlinks except verified macOS system aliases `/tmp → /private/tmp` and `/var → /private/var`, canonicalized before checks; arbitrary links and internal store links remain rejected.

Commits write a same-directory restrictive temporary, flush/fsync it, and atomically link it to a previously nonexistent final name. Existing output is never replaced. Interrupted `.pending-*` files are ignored and never promoted. Their presence does not invalidate intact committed records; safe retry creates a fresh temporary. The helper does not delete orphan files or foreign files. Canonical corrupt records cause explicit failure; use a verified earlier copy or immutable source artifact in a separately selected recovery store. No silent destructive repair. Watch snapshots retain all prior revisions.

`list` lists run/legacy IDs, kind, creation time and entity with deterministic ordering. `show ID` returns exact saved run, legacy or corpus record. `search QUERY` is deterministic case-insensitive AND substring search over saved source titles/bodies or legacy content. Filters `--entity`, `--start`, `--end`, `--source` apply to run evidence; dated filters omit unknown publication. Dates filter publication, not retrieval/mtime; inspect returned `date_basis`, then use `show RUN_ID` to review original publication and eligibility before treating a match as recent. Results include stable run/item locators, URLs, visibility and bounded excerpts. It is historical local recall, not new search or an embedding relevance claim. Corrupt state does not become no matches.

## Import and corpus

`import FILE --id OPTIONAL_ID --root STORE` accepts an explicit UTF-8 .md/.txt/.json file. Both the input and its complete serialized JSON record (escaping, metadata and trailing newline included) must fit within 8 MiB; oversized records fail with `size_limit` before creating the store or record. It does not treat arbitrary JSON as a validated run. Original UTF-8 bytes are preserved losslessly as the private immutable record’s content string: re-encoding it as UTF-8 reproduces the exact input, including whitespace/newlines. The record stores original path, import time and a SHA256 checked against those bytes; no redundant raw blob/base64 copy is needed. Publication/entity/window remain null and freshness unknown; filename/import time do not fill research facts. Reimport of identical path+bytes is idempotent. Explicit same ID with changed bytes/path conflicts.

`corpus index FILE... --root STORE` uses the same bounded mechanism, only explicitly enumerated files, at most 100 per command and the same 8 MiB input/serialized-record limits per file. No directory recursion, glob discovery, home/account scan, PDF extraction, media download, external embedding or external query. Other formats require separately supported extraction into an explicit allowed text file. Each path+content version has a distinct immutable ID and shared document_id; changed bytes create another version even if mtime/size are reused. `modified_at` is filesystem observation metadata only. `corpus search QUERY --root STORE` searches all retained versions with exact original path/record locator and private visibility. Convert selected content into a separate private source record only with its exact provenance.

## Watch state, deltas and briefs

```
python scripts/research_store.py watch add releases --scope scope.json --root STORE
python scripts/research_store.py watch list --root STORE
python scripts/research_store.py watch record releases RUN_ID --expected-revision 1 --root STORE
python scripts/research_store.py watch update releases --scope new-scope.json --expected-revision 2 --root STORE
python scripts/research_store.py watch pause releases --expected-revision 3 --root STORE
python scripts/research_store.py watch archive releases --expected-revision 4 --root STORE
python scripts/research_store.py watch list --archived --root STORE
python scripts/research_store.py watch restore releases --expected-revision 5 --root STORE
```

Scope file is exactly the run scope object. Add optionally accepts `--schedule TEXT`; update also accepts it. This records an unactivated request; scheduler_status always unconfigured. No budget is measured/enforced. Add name collision requires update; exact repeated initial configuration returns unchanged. IDs are stable names, not arbitrary user labels.

Revisions are global for this store’s watch configuration. Every mutation except new add requires `--expected-revision`; add can also supply it. Atomic creation of the next numbered full snapshot is a compare-and-swap commit: concurrent writers for the same revision cannot both succeed. Stale revision fails and prior snapshots remain. Reload state before retrying. No lock stealing or stale-PID guess. Ordinary removal archives, never deletes runs/history; restore is reversible.

`watch record NAME RUN_ID` binds an existing validated run without collecting anything. Query/entity/selection/lane outcomes/window mismatch requires `--relationship 'Describe changed scope and limits'`; exact absolute window differences also require it. Recording already-bound run is unchanged. Saving a schedule is not a registered automation; use actual supported host tools only when authorized.

`delta BEFORE AFTER --root STORE` compares exact run IDs. Entity, query, selection/cap, source lane health, timezone/boundary and window duration must be comparable. Failed/partial/incompatible comparisons return comparable false/status unverifiable. Comparable results have categories added/continuing/changed/not_observed/aged_out/unverifiable with source IDs and URL. Identity is lane+URL+origin, not mutable title. Body/title/metric/date differences are mechanical changed. Missing body is unverifiable. Aged-out requires publication in the before interval and before the after interval; a source already old in both cannot age out. Not-observed is not removal/disappearance. No change of factual truth or quality is inferred.

`brief RUN_ID... --root STORE [--format json|md] [--out NEW_FILE]` creates a dated digest from selected saved runs (default JSON). It includes per-run/entity relevance, findings, exact source citations and coverage. Same-origin exact duplicate findings within one run may collapse; separate runs/topics remain represented. This does not infer independence or representative trends. Optional output is no-clobber. Inspect claim/source dependencies and review the digest before delivery. To retrieve a saved digest, read that explicit artifact without rerunning collection.

## Freshness and export

`freshness BASE UPDATED --root STORE [--claim-id ID] [--source-id ID]` matches typed datum kind/key/unit/denominator, entity, source URL/origin, asserted modality and supported review status. Updated observed_at must be later. Missing, ambiguous or incomparable data returns unverifiable; bad explicit selections error. Exact numeric/status/date equality returns unchanged, inequality changed, with original/updated claim/source IDs, values and observation basis. It does not refetch, perform approximate odds tolerances, interpret arbitrary prose or attest truth. Privacy follows both observations. Use semantic review for factual reversals or unsupported new types.

`export RUN_ID --format json|md|html --visibility private|public --out NEW_FILE --root STORE` and `library-export RUN_IDS... --format html|atom --visibility private|public --out NEW_FILE --root STORE` generate only local new files. Parent output directory must exist. Repeated names conflict, including the third attempt; choose a new filename. No cache-miss research, opening, upload, publishing or subscription happens.

Public projection retains only explicitly public sources and derived claims/findings whose complete dependency closure remains public. It omits raw scope, queries, private titles, lane details and unknown fields. Identifiers are remapped and run identity opaque; public metadata supplies reviewed title/entity, optional exact window and caveats. Unknown source/claim/finding classifications are excluded. URLs and locator URLs are revalidated as HTTP/HTTPS. Derived parent private context blocks projection. Public projection is a syntactic privacy boundary dependent on complete truthful classification; inspect the whole generated artifact before sharing.

Markdown evidence is placed in a dynamically lengthened plain-text fence to prevent supplied markup from becoming instructions/HTML. HTML escapes all source text, uses safe links and a restrictive no-network CSP, and emits no scripts/remote assets. Library HTML contains every selected report and a linked index, searchable via browser Find. Atom is real XML with escaped text, content-derived stable selected-set feed identity and immutable entry identity (distinct stores with reused run IDs cannot collide merely because of their IDs), saved creation/update timestamp and safe related source links. These timestamps describe saved content updates, never fresh live truth. No linked private download is generated. Generating a local public projection is not permission to distribute it.
