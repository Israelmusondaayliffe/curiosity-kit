# Graphify provider operations

This guide retains Graphify's scalable functions through its public command interface. Continuity Vault does not ship, fork or emulate the Graphify engine. Its local [relationship method](../playbooks/relationships.md) supplies source discipline and an honest bounded fallback, not equivalent indexing or media processing.

## Declared provider and evidence level

The donor declares Graphify `0.8.47`, distribution `graphifyy`, command `graphify`, at commit `f87011b38e31251a818d28c228979081bad1d33e` in [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify/tree/f87011b38e31251a818d28c228979081bad1d33e). [Package metadata](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/pyproject.toml) declares Python 3.10 or later and optional backend, media, visualization, watch, MCP and database dependencies.

The recipes below were checked by reading that pinned CLI implementation and relevant supporting functions on 2026-10-07. No provider installation, command, model call or integration was executed during candidate authoring. The user's installed version is unknown. These are source-checked candidate recipes, not native-host acceptance or observed provider passes. Inspect the actual installed implementation and qualify the selected operation before relying on its behavior.

Important implementation differences from broad README claims:

- `extract` builds graph JSON and analysis; report and HTML generation are separate.
- `extract` detects incremental work when its output contains both a manifest and graph. `update` is the code-only route.
- `add` saves fetched content and tells the user to update. It does not update the graph itself.
- `path` searches undirected connectivity and displays stored edge arrows. It does not establish directed reachability.
- `merge-graphs` uses simple undirected graph composition and directory-derived repository tags. It is not a lossless directed-multigraph merge.
- This pinned `extract` branch does not invoke media transcription or parse a `--directed` option. Do not pass unrecognized options and infer success from exit status; some CLI branches ignore unknown arguments.

## Preflight without installation

Check the selected host and environment, source access and output scope. A supported remote task must run in the requested environment. A provider installed elsewhere is not proof it is available there.

Use the host's executable inventory or `command -v graphify` on a compatible shell. Inspect the executable's resolved location and package metadata without importing arbitrary modules. The [pinned CLI startup](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/__main__.py#L2165-L2189) checks global skill destinations before dispatching even `--version` or `--help`; its [version check](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/__main__.py#L96-L124) can read installed skill bodies and version stamps. Under a no-production-read boundary, inspect the actual startup code and establish isolation before the first provider call, including help/version. Use an already qualified task-local process guard if available; otherwise stop if the requested boundary cannot be met. Do not repurpose `HOME`. Once execution is authorized and this boundary is met, inspect `graphify --version` and `graphify --help`. Record the actual executable, package version, environment and relevant help. At the pinned version, most subcommand `--help` calls merely point to global help; `query`, `path` and `explain` treat free text specially. Do not assume they provide conventional help.

Never use `uv tool run`, `uvx`, package imports, an installer, an upgrade, or `graphify install` as a presence probe. The last command registers assistant files and can alter instructions. Missing availability blocks only the requested provider work. An installation or integration change needs its own scope and applicable approval; do not silently substitute another package or host.

Before a build, bind these facts in a short run note outside the scanned corpus:

- Corpus identity, selected root, source revisions and actual included file list, with exclusions and unreadable formats
- Absolute output root and graph filename, permitted writes, collision policy and prior usable revision
- Selected backend, endpoint, model and available features for semantic work; explicit data recipient, purpose and approved cost/resource limits where needed
- Which operations and exports are requested, and which will remain unrun

Honor an explicitly selected model. If it is unsupported, report the gap before substituting. A configured key, logged-in CLI, local server or subscription is not consent to send this corpus or incur charges. Do not select a backend from ambient credentials. Inspect nonsecret endpoint configuration without printing credentials. Use approved secure credential facilities; never put passwords or keys in command arguments, prompts, source files, logs or ordinary chat.

Do not guess that "local" means private: verify the endpoint. Community naming and optional LLM deduplication can also call models. They need the same routing and authority as extraction. Do not enable deduplication, live database introspection, Google Workspace export or a global graph as unrelated additions.

## One operation, one output root

Use an empty, authorized working output for a first candidate. Keep the corpus root fixed across build, add and update. Store the source inventory outside the scan so reports and generated artifacts cannot become new source evidence. Exclude outputs and caches deliberately if they sit below the selected root.

Inspect source-discovery behavior before passing a live directory. At this pin, detection can auto-follow a direct-child symlink, deliberately includes `graphify-out/memory`, and creates Office conversion sidecars under the corpus root even when `extract --out` names another output root. Existing include/ignore files also affect coverage. A separate output flag does not make the whole operation read-only against its corpus.

When these behaviors would exceed the source or write boundary, materialize only the approved selected files in an authorized staging corpus, preserving their full relative paths. Do not use symlink staging. Keep a staging-to-original identity/revision map outside the scan and disclose converted-source mappings. Exclude generated answers and prior output unless the user explicitly selected them as labeled derivatives. Use the same staging root for related operations and check original source drift before accepting the result. If authorized staging is unavailable, stop the affected build rather than scanning a broader live directory.

In the examples, `CORPUS` is the verified absolute source root, `RUN` is the authorized absolute candidate output root and `GRAPH` is `RUN/graphify-out/graph.json`. `BACKEND`, `MODEL` and other capitalized values are selected data, not literal defaults. Set arguments with the host's argument-array mechanism where available. Shell examples require correctly assigned quoted variables; never interpolate source text into code or use `eval`. Paths, questions and labels can contain spaces, quotes and metacharacters.

Process-local `GRAPHIFY_OUT=graphify-out` makes the output convention explicit. Do not inherit an unrelated absolute `GRAPHIFY_OUT` from another task. Process-local `GRAPHIFY_QUERY_LOG_DISABLE=1` prevents the pinned provider's default query-log write. Neither setting changes global shell configuration.

Use a controlled process environment. Remove unapproved acquisition switches such as `GRAPHIFY_GOOGLE_WORKSPACE` from that process instead of inheriting automatic connected-document export. Do not modify the user's persistent environment or print its secrets. Verify the actual included set and writes after the operation, since command syntax alone does not establish scope preservation.

## Build AST and semantic results

Choose the semantic route the user actually wants. Assistant-native extraction uses the active host and its selected model, then public Graphify commands for graph assembly, clustering and export. The optional headless route uses an explicitly selected provider backend. An API key is not required for assistant-native extraction. Do not replace native/subscription work with a paid API call merely because it is easier to script.

### Assistant-native semantic extraction

The pinned public `cluster-only` command accepts raw extraction JSON containing `nodes` and `edges`, as well as its usual graph JSON. Its implementation reads the input's `directed` field, builds the graph, clusters it and writes graph/report/HTML. This provides a real route for source-backed host extraction without importing engine functions. The native reading and extraction must actually occur; hand-authoring a tiny fixture proves only a fixture path, not corpus extraction or scale.

1. Freeze the selected corpus and source inventory using the boundaries above. Use the host's real document/image readers. Media needs a separately produced authorized transcript. Unsupported or unreadable material remains a coverage gap.
2. Use the active assistant or available native readers for bounded source chunks. Honor an explicit model choice. If a requested model or native reader is unavailable, report that gap rather than selecting an API backend. Give each reader exact sources, identity rules, edge-status definitions, audience restrictions and expected output. No fixed worker count or invented host API is required.
3. Choose returned structured fragments as the single collection channel. Each fragment carries its completed/empty/failed source coverage separately from its graph data. The coordinator reads and validates those returns, then writes one named fragment file per actual successful result with ordinary file tools. A return is not required to have also written a disk file. Missing or malformed returns stay failed; do not fill them with invented nodes.
4. Require the provider fields listed below plus CV's usable evidence locators. Reconcile source-owned identities and aliases before assembly. Within the final assembled input, each node ID appears once. Preserve its full corpus/path/entity identity in the accompanying source record. Retain all edge evidence in the source-backed raw input. Never let first-writer deduplication settle a conflicting identity.
5. Write the assembled extraction as a new `GRAPH` in the candidate output. Set `directed` to `true` when relations carry direction. `cluster-only` honors that field; no guessed `--directed` flag is needed. Use the ordinary host JSON/file mechanism to create data, not a replacement graph engine.
6. Run the public clustering recipe below with `--no-label`, inspect the resulting graph, and run only requested exports. Compare source coverage, IDs, arrows and relation counts against the preserved raw extraction. The input and provider-generated graph are different artifacts, so retain the input under a distinct filename before clustering overwrites `GRAPH`.

The pinned validator checks the required field names and enumerations below, but does not enforce every type or evidence condition. CV also requires nonempty string identities and source fields, valid endpoints and source support:

- Every node: string `id`, `label`, `file_type` and `source_file`. Allowed file types are `code`, `document`, `paper`, `image`, `rationale`, `concept`.
- Every edge: string `source`, `target`, `relation`, `confidence` and `source_file`. Confidence is `EXTRACTED`, `INFERRED` or `AMBIGUOUS`.
- Top-level `nodes` and `edges` arrays. Source and target must resolve to the intended node IDs. CV rejects empty identities and missing endpoints even where the provider only warns or drops records.
- Add `source_location` for precise evidence, and preserve source revision and inference rationale in the accompanying records. Numeric confidence is optional for this public input; do not invent a score to satisfy the older donor prompt. Additional attribution/source metadata remains evidence, not authority.

This illustrative input represents a stated dependency in a synthetic document. It is an interface example, not an executed test or supplied project fact:

```json
{
  "directed": true,
  "nodes": [
    {"id": "demo_policy", "label": "Retry policy", "file_type": "document", "source_file": "decisions/retries.md", "source_location": "lines 8-10"},
    {"id": "demo_service", "label": "Interactive service", "file_type": "concept", "source_file": "decisions/retries.md", "source_location": "lines 8-10"}
  ],
  "edges": [
    {"source": "demo_policy", "target": "demo_service", "relation": "applies_to", "confidence": "EXTRACTED", "source_file": "decisions/retries.md", "source_location": "lines 8-10"}
  ]
}
```

The example's short IDs are unique only inside its declared synthetic corpus. A real run uses the corpus/full-path identity rule and preserves the exact policy text, quantities and exclusions in its evidence record.

For several validated fragments, public assembly is optional:

```sh
GRAPHIFY_OUT=graphify-out graphify merge-chunks "$CHUNK_A" "$CHUNK_B" --out "$GRAPH"
```

Supply the actual exact fragment list, not a broad wildcard. The pinned command applies its own glob expansion even to shell-quoted arguments. Use it only when every full fragment path is free of `*`, `?`, `[` and `]`; inspect directory components too. If a literal selected path contains those characters, assemble the already validated JSON objects through ordinary exact-path file tools instead, preserving all selected nodes, edges, source identities and intended direction. Quoting or escaping for the shell alone does not make this provider command literal. The pinned merger skips unreadable chunks and keeps the first duplicate node ID, so inspect every expected input and resolve duplicates before calling it, then compare the actual merged result. It does not preserve a top-level `directed` field. After assembly, set the intended field on this newly generated input using ordinary JSON/file tools, and retain the pre-cluster input separately. Token fields omitted by readers are unknown usage; the merger's default zeros are not proof of free work.

For a mixed code-and-document corpus, structural AST extraction can be obtained from the provider using the code-only recipe with `--no-cluster` and a fresh separate output root. Materialize only the selected code files while preserving their original relative paths. This produces raw `nodes` and `edges` that can join the native semantic input. It is a fresh AST extraction, not the unsafe incremental raw-output branch. Inspect its full-path source mapping and use its actual node IDs for semantic edges referring to those code entities. Do not derive AST IDs by guessing the donor's stem rule, re-extract structural imports in the semantic pass, or join unrelated same-label symbols. Source-root differences between staged code and the full corpus must be reconciled in the input evidence before merging.

This route preserves native semantic extraction and real provider assembly/clustering/export. It does not automatically populate the provider's semantic cache or incremental manifest. The pinned CLI exposes cache-read and fragment-merge helpers but no checked command that saves host-returned semantic results with a complete source manifest. Do not imitate that private cache API or claim an all-cache-hit/incremental pass. Keep an authorized prior raw extraction as a versioned artifact if useful; after source changes, re-extract the selected corpus and assemble a fresh candidate, or qualify an actual supported provider cache/update route. Native-host availability, large-corpus throughput and source-complete output still need observed qualification.

The directed input produces a simple directed graph, not a multigraph. Reciprocal edges can be represented, but multiple distinct relations on the same ordered pair may collapse. Keep the source-backed raw records and block claims of lossless parallel-edge output until a suitable provider route is qualified. Provider path search remains undirected even for a directed input.

### Headless AST or explicitly selected backend

For a verified code-only selected corpus, the public build route is:

```sh
GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 graphify extract "$CORPUS" --out "$RUN"
```

Inspect the included files first. A document or image in that directory can trigger semantic extraction. Do not call a mixed directory "code-only" because the user's main interest is code. Do not run source code, repository setup hooks or package scripts while parsing it.

For an authorized mixed corpus, select the backend and model explicitly:

```sh
GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 graphify extract "$CORPUS" --out "$RUN" --backend "$BACKEND" --model "$MODEL" --token-budget "$CHUNK_TOKENS" --max-concurrency "$CONCURRENCY" --api-timeout "$TIMEOUT_SECONDS"
```

The chunk-token option is not a total spending cap. Estimate the actual corpus and enforce the authorized overall limit through available host controls. Record observed usage when supplied, otherwise unknown. An image's work is not safely estimated by dividing all files by a fixed text-file batch size. Deep extraction is opt-in through supported `--mode deep`; inferred edges still require evidence labels and review.

The pin also recognizes the `claude-cli` backend, using an existing authenticated CLI rather than an API key. Select it only when the user wants that available subscription route and its model/options are compatible. It is distinct from the current assistant-native route and still needs the corpus, endpoint/model and resource boundary checked. Do not assume another host's subscription is available or transfer authority between accounts.

In this headless route the pinned CLI owns AST and semantic extraction, caches, merged in-memory results and output production. Do not splice donor Python snippets into this flow, import private helpers, or reconstruct its hidden intermediates from guessed chunk filenames. This avoids the donor's contradictory return-vs-disk result channels. It does not establish that all provider branches are correct.

Inspect stdout and stderr, expected source coverage and resulting artifacts. A zero exit status alone is insufficient: the CLI catches some AST failures and can retain only successful semantic output. Missing fragments mean partial coverage. If the provider does not expose enough per-file evidence to distinguish an empty extraction from failure, report coverage as unverified for those files. Do not certify an all-source build from a node count.

To generate the local report and HTML without an extra model call:

```sh
GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 graphify cluster-only "$RUN" --graph "$GRAPH" --no-label
```

This is a write operation. It rewrites graph JSON and creates labels/report/HTML in `RUN/graphify-out`. Its report identifies the output root and lacks full original file statistics, so retain the source inventory separately. Existing labels may be reused. Inspect their correspondence with current communities. For authorized model-generated labels, use the supported `label` route with explicit `--backend` and `--model`, then inspect actual labels and provider errors. A model failure may leave placeholders. Do not claim useful labels merely because a label file exists.

Use `--no-viz` only when omitting HTML is intended. In the pinned clustering branch it may remove an existing HTML output. Do not use it as a harmless read option. `--no-cluster` produces a raw extraction rather than the normal graph/report result; see the update warning below before selecting it.

### Identity, direction and graph integrity

Retain corpus plus full-path entity identity in the evidence inventory even if the provider uses another ID. The pinned AST extractor includes a source-based collision-disambiguation pass. That is a useful implementation fact, not proof that cross-file, cached, semantic and merged identities all pass. Test identical symbols in nested same-named paths and separate repositories. Inspect every affected endpoint and provenance before accepting the graph.

The pinned headless build invokes the graph builder without a directed argument. Its builder defaults to an undirected graph while carrying some stored endpoint direction. Do not claim full reciprocal-edge or directed traversal preservation. `--directed` belongs to donor orchestration instructions, not a verified flag for this CLI. If lossless direction or parallel-edge fidelity is required, qualify a provider interface/version that actually supports it; otherwise report that operation blocked or deliver a clearly limited connectivity artifact only when acceptable to the request.

Inspect duplicate IDs, distinct sources sharing an ID, missing endpoints, relation multiplicity, evidence locators and source revisions. `graphify diagnose multigraph --graph "$GRAPH" --json` is a public diagnostic at the pin; it does not prove that already-collapsed edges can be recovered. Dangling endpoints block graph publication. Legitimate self-loops do not.

## Cache and incremental update

Keep cache status separate from source coverage and graph correctness. The pinned semantic cache is content-based, unversioned and strips Markdown frontmatter when hashing. A hit does not qualify a new model, changed extraction policy, permission, author, source URL or other frontmatter-only change. Do not reuse a result across those changes without checking its provenance. Prefer a fresh candidate output root for a required fresh extraction; do not destroy a live cache as a workaround.

For a mixed corpus with semantic changes, prefer a scoped full rebuild into a new empty `RUN` until the installed incremental route passes the cases below. Preserve the selected semantic route. For native extraction, repeat the bounded source reading and assemble fresh raw input; for an authorized headless backend, use the mixed-corpus `extract` recipe with the original `CORPUS`, backend and model. Then cluster and produce requested exports. This is a supported candidate-replacement workflow, not a claim of incremental processing. Check any added model work against the approved resource limit before starting. Keep the previous output untouched and compare the rebuilt candidate against all selected sources, including changed-to-empty and deleted sources.

The pinned `extract` enters incremental mode if the output root already contains both graph and manifest. A qualified incremental run therefore uses the same corpus identity and an authorized candidate copy of that output, not an empty output root. Copying must retain source identity and satisfy its data boundary. Do not choose this optimization until its actual installed behavior is suitable for the requested update. Merely copying a flawed manifest does not make incremental processing safe.

For code-only rebuilding in a project whose graph lives under its corpus root, the public route is:

```sh
GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 graphify update "$CORPUS"
```

`update` has no `--out` option at the pin. It is not interchangeable with the external-output `extract` recipe. Do not run it against a real corpus just to test a staged graph. Test in an authorized disposable corpus or use the explicit-output extraction route. The pinned update can preserve prior semantic content, but document/image changes still need semantic work. A `needs_update` marker is a pending request, not proof that such work ran.

The following cases must be observed before accepting the selected incremental route:

1. All inputs unchanged or all semantic results cached. The result remains complete without requiring a deleted intermediate or new model work.
2. A code-only change within a mixed graph. Unchanged semantic contributions remain, and updated code does not depend on a missing semantic file.
3. A changed source now produces zero entities. Its prior contribution disappears; unchanged sources survive.
4. Deletion-only work. The exact deleted source's nodes and supported edges are removed, without reusing an old extraction fragment.
5. An interrupted or failed graph/export write. The prior usable graph remains identifiable, and any advanced manifest is reported and reconciled before retry.

There are concrete static limits at this pin. The clustered extraction merge determines replaced sources from newly emitted nodes, so changed-to-empty replacement needs runtime qualification and must not be presumed safe. Its `--no-cluster` incremental branch writes the new extraction directly rather than merging the existing graph for changed input. Do not use that branch as a preservation-safe incremental update. The code-update implementation has different pruning and publication logic; it needs its own evidence.

An explicit force option is not a general repair. The pinned `update` parses `--force`, but the headless `extract` parser does not wire that flag into the build; its clustered export already requests force internally. Do not repeat README `extract --force` guidance as proof of a fresh rebuild, correct pruning or safe recovery.

For a confirmed empty-source or update gap, retain the prior revision and prepare a fresh full candidate through supported public commands if that fits the approved scope and cost. Verify the actual result. Report that incremental behavior remains unqualified. Do not manufacture tombstone nodes or edit the manifest to hide the gap.

### Candidate publication and recovery

The provider does not offer a proved atomic transaction for graph, analysis, labels, report, exports and manifest together. The headless build writes graph and analysis before saving its manifest; reports and requested exports happen later. Code update may save its manifest before HTML generation. A successful graph write plus a failed export is therefore partial completion, not a complete bundle.

Keep the previous usable output separate. Run the requested build/update and exports in the authorized candidate location. Read back each required artifact, compare its source set and graph revision, and inspect diagnostic failures before selecting the candidate as usable. Use ordinary versioned directories or the host's supported replacement mechanism, not a new continuity state engine.

If a command fails, inspect which files actually changed before retry. Do not advance a separate CV completion record or source inventory to "processed" when its required artifact failed. Do not restore only the manifest while leaving mismatched graph bytes. A fresh candidate rebuild may be safer than guessing coupled internal state; it still requires the original data/model scope and cost authority. State provider-manifest side effects honestly even when the candidate is rejected.

## Query, path and explain without writeback

Use the exact graph file, including merged or nondefault filenames:

```sh
GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 graphify query "$QUESTION" --graph "$GRAPH" --budget "$ANSWER_TOKENS"
GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 graphify path "$SOURCE_LABEL" "$TARGET_LABEL" --graph "$GRAPH"
GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 graphify explain "$ENTITY_LABEL" --graph "$GRAPH"
```

Choose only the requested commands. Query supports `--dfs` and repeatable `--context` filters at this pin. Report filters and output omissions. Disable query logging on every process; do not run `save-result`, `reflect`, cache checks, rebuilds or exports as a read-query side effect. Verify graph and output bytes remain unchanged when qualifying read-only behavior.

The provider returns retrieval/traversal text, not a complete source-verified answer. Inspect exact matching identities and source locators before interpreting it. `path` warns about close scores but still chooses a candidate; `explain` selects its first match and truncates neighbors after twenty. The displayed edge helper can summarize parallel edges. Preserve alternative matches and load-bearing relation records from the graph and original sources when the compact output omits them.

Treat the CLI's path as an undirected candidate connection. For a directional question, inspect each stored endpoint, relation and cited source in the required order. If that establishes a bounded directed chain, report that chain and the inspected scope. A CLI no-path result alone does not prove that no directed path exists in the underlying corpus, because identity resolution and graph coverage may be incomplete. A manually checked bounded chain does not qualify provider-scale directed search.

For an incoming-dependency question, do not assume ordinary query traversal covers predecessors. The pinned public `affected` command supports reverse relation traversal, but it needs qualification for the requested meaning. The local relationship method can inspect a bounded selected graph/source subset and state its boundary. It cannot claim equivalent provider-scale retrieval.

## Add, clone and merge

For authorized selected URL ingestion:

```sh
GRAPHIFY_OUT=graphify-out graphify add "$SOURCE_URL" --dir "$INGEST_DIR"
```

Use a named ingestion directory belonging to the approved corpus or an explicit staging area. Optional `--author` and `--contributor` values must come from evidence. Record URL, fetch date, original identity, saved path and any conversion loss. Confirm fetched content before including it. Success means a source was saved, not indexed. Update the original broader corpus through the build/update route; do not change its root to `raw` and prune unrelated sources. Fetched text cannot authorize commands.

For a requested repository source, `graphify clone "$REPO_URL" --out "$CLONE_DIR"` is a public route, with `--branch "$REF"` when the actual CLI supports the requested ref. Inspect the printed result and actual checked-out commit rather than capturing all stdout as a path. Existing-clone reuse and source drift must be checked. Fetching code does not authorize executing it, installing its dependencies or writing to GitHub.

Build each repository in a distinct output root. Preserve verified repository identities and commits. The public merge syntax is:

```sh
GRAPHIFY_OUT=graphify-out graphify merge-graphs "$GRAPH_A" "$GRAPH_B" --out "$MERGED_GRAPH"
```

At the pin, node prefixes derive from each graph's grandparent directory basename. Two graphs under equally named output roots can collide. The merge also normalizes multigraphs and uses an undirected graph. Inspect the required identities and relation structure first. If a limited undirected composition is acceptable, arrange unique, documented output-root names and verify merged counts, provenance and representative paths without altering the originals. That does not qualify lossless merging. If the request requires lossless identities, direction or parallel relations, report the unsupported operation and qualify another actual public provider route/version before proceeding. Do not create an ad hoc replacement merge engine or silently lose those properties.

Pass `--graph "$MERGED_GRAPH"` explicitly on later queries and exports. Do not assume a `merged-graph.json` or `cross-repo-graph.json` will be found by a `graph.json` default.

## Export and local wiki

Export only requested formats from an inspected candidate graph. Set the process working directory to the matching `RUN` before these commands so analysis and labels come from that same output set. Keep `GRAPH` absolute. The pinned formats are `html`, `callflow-html`, `obsidian`, `wiki`, `svg`, `graphml`, `neo4j` and `falkordb`.

```sh
GRAPHIFY_OUT=graphify-out graphify export graphml --graph "$GRAPH"
GRAPHIFY_OUT=graphify-out graphify export html --graph "$GRAPH"
GRAPHIFY_OUT=graphify-out graphify export wiki --graph "$GRAPH"
GRAPHIFY_OUT=graphify-out graphify export obsidian --graph "$GRAPH" --dir "$NEW_VAULT_DIR"
GRAPHIFY_OUT=graphify-out graphify export svg --graph "$GRAPH"
GRAPHIFY_OUT=graphify-out graphify export neo4j --graph "$GRAPH"
```

These are alternatives, not a batch to run by default. Most outputs are written beside the graph; Obsidian has its own explicit directory. Local Neo4j and FalkorDB export both write `cypher.txt`, so do not treat them as two independently named artifacts. Use separate candidate directories if both need preservation. `callflow-html` also supports an explicit `--output` file. Inspect all destinations and collision behavior before writing into an existing vault or output set.

Wiki needs community data and should contain a usable index, correctly matched labels and source links. The CLI falls back from analysis to graph community attributes, but its analysis-path handling can use the current working output directory even with an explicit graph. Run exports from the matching `RUN` directory with the declared environment, or otherwise qualify the actual path resolution; never pair another project's analysis with this graph. Read the index and representative pages. A wiki is local output; publishing it needs separate authority.

Verify each requested file opens or parses, contains the intended graph revision and retains the information needed for its use. Rendering success cannot establish source truth. Diagnose unsupported dependencies, size limits, missing community data and partial exports separately. No source or manifest claim should call a failed required export complete.

## Transcription and media intake

Retain media work as a provider-dependent capability with an explicit current gap. The pinned package contains transcription support, but its public `extract` branch selects code, documents, papers and images without transcribing detected media. There is no checked standalone `graphify transcribe` command in this CLI. `add` can download supported media URLs; that is not transcription.

The inspected transcription implementation saves plain text from segment text and omits timestamp fields. It caches by output stem and file existence, so equal stems or changed media can reuse the wrong transcript. Do not promise timestamped, identity-safe media evidence from this route or silently call private engine functions to manufacture it.

For a selected media task, inspect the installed provider's supported public media interface. If it supplies a suitable route, first verify media identity, installed dependencies, chosen transcription model, model-download effects, output location and timestamp preservation. Honor the user's model selection. A first run uses the supplied domain context or a neutral transcription hint; it cannot depend on central graph nodes that do not yet exist.

If the installed public provider still lacks that route, report transcription blocked for this provider version and request or use an already authorized transcript-producing tool where available. Do not call that alternate tool a Graphify transcription pass. Preserve original media identity and time range, transcript version, speaker uncertainty and failed segments. Include the actual transcript in the approved source inventory before semantic extraction. A missing segment is a coverage gap, not silence in the meeting. Additional media/model downloads or external transmission need their own authority.

## Optional ongoing work and integrations

These capabilities remain available through their actual public provider routes, but none activates because a graph, key or configuration exists.

### Watch

For an explicit ongoing request, freeze the corpus, write scope, lifetime, stop condition and handling of non-code changes. Qualify first in a disposable corpus. `graphify watch "$CORPUS"` watches the folder and rebuilds code; non-code changes can create `needs_update` rather than run semantic extraction. `graphify check-update "$CORPUS"` reports the pending marker. Observe process identity, a representative file change, actual outputs and stop through the owning terminal/process tool. Confirm the process stopped. Do not create a service or schedule as part of a temporary watch.

### Hooks and host instructions

`graphify hook status`, `graphify hook install` and `graphify hook uninstall` are public commands. Installation can change Git hooks and merge-driver configuration. Host commands such as `graphify codex install --project` or `graphify claude install --project` can change standing instruction and hook files. They are not required for CV's ordinary graph commands.

Before authorized installation, inspect the actual installed implementation, exact target files and existing hooks/instructions. Preview the scoped change and recovery, preserve unrelated content, and test install/uninstall in a disposable repository without real commits or account effects. Confirm the user's exact requested host and scope. Preserve existing skill identities; do not replace CV with the provider's assistant skill. Do not presume an uninstall is lossless or an existing hook grants future execution consent. `hook-check` is a no-op at this pin, so its presence does not prove graph consultation occurs.

### MCP

The package declares a public `graphify-mcp` executable. Its supported stdio form is:

```sh
GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 graphify-mcp "$GRAPH" --transport stdio
```

Start it only for an authorized temporary service task with the MCP extra available. Inspect advertised tools, graph scope and their actual behavior; make one permitted read request and confirm clean shutdown. Client registration or persistent access is a separate configuration/permission change. HTTP/network exposure and credential generation are outside this stdio recipe and require their applicable security approval. Do not bind a public listener as a convenience.

### Database push

Local `neo4j` or `falkordb` Cypher export is distinct from a push. Before an authorized push, identify the exact server, database/graph namespace, affected records, transmitted data, secure authentication and recovery. Inspect the installed writer's actual merge/delete semantics. `MERGE` does not by itself prove a push is harmless, lossless or safe to retry.

The public shape is `graphify export neo4j --graph "$GRAPH" --push "$APPROVED_URI" --user "$APPROVED_USER"`, or the corresponding `falkordb` format. The pinned CLI reads `NEO4J_PASSWORD` or `FALKORDB_PASSWORD`; do not supply a password flag, embed a credential in a URI or manually configure persistent credentials. Use an approved secure handoff/facility, and stop if none fits the authentication boundary. Verify the exact remote write result without broadening access. An uncertain outcome requires read-only reconciliation before retry.

### Saved answers and reflections

`save-result` and `reflect` are optional persistence commands. Use them only for an explicit request naming the retained answer or bounded set and destination. Inspect their public arguments and actual output paths, keep generated answers as derivatives, preserve correction history and do not treat repeated answers as independent incidents. They never belong in a read-only query recipe.

## Qualification and final report

Qualify only selected operations, using a tiny disposable corpus and genuinely observed artifacts. Record executable/version, source identities, exact arguments without secrets, working directory, output paths, relevant logs, before/after bytes and the specific assertion checked. No donor code execution, model use, installation, persistent integration or external write is authorized by this document itself.

The minimum provider campaign covers build, query/path/explain, selected export, source-ID collision, all-cache-hit, code-only update, changed-to-empty, deletion-only, partial extraction, output-root behavior and failed publication when those routes are used. Directional/multiedge queries and merge must test their actual requirements. Media, wiki, watch, hooks, MCP and database push need their own prerequisites and checks when selected. A fixture hand-authored to match an answer is not a provider build test.

Report each capability as source-checked only, available but unqualified, passed within a named observed case, failed, or blocked. A missing provider never becomes a full provider pass. A successful manual map never becomes a scalable build pass. Native Codex/Claude loading and installed-provider qualification remain separate from this candidate's local method review.

## Pinned implementation references

These are the inspected public routes and selected supporting code, not an end-to-end engine audit:

- [CLI commands and help](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/__main__.py#L2165-L2380), [query/path/explain](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/__main__.py#L2772-L3142), [add and clustering](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/__main__.py#L3238-L3452)
- [Code update](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/__main__.py#L3454-L3508), [merge and exports](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/__main__.py#L3634-L4023), [headless extraction and publication](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/__main__.py#L4098-L4760)
- [Graph replacement and prefixing](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/build.py#L467-L614), [AST identity disambiguation](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/extract.py#L7636-L7707), [its extraction call site](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/extract.py#L12842-L12925)
- [Native fragment assembly](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/__main__.py#L4795-L4840), [cluster-only raw JSON and direction handling](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/__main__.py#L3336-L3376), [input validation fields](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/validate.py), [raw graph construction](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/build.py#L137-L372)
- [Cache behavior](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/cache.py), [query-log opt-out](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/querylog.py), [code-update publication](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/watch.py#L680-L865)
- [Detection scope, symlinks, generated answers and conversion sidecars](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/detect.py#L993-L1135)
- [Media implementation](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/transcribe.py), [URL intake](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/ingest.py#L218-L271), [MCP command arguments](https://github.com/Graphify-Labs/graphify/blob/f87011b38e31251a818d28c228979081bad1d33e/graphify/serve.py#L1385-L1451)
