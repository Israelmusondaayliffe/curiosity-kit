# Contract and state fields

See [CLI](cli.md) for actual commands and [example](../assets/contract-example.json) for a valid synthetic contract. JSON objects reject duplicate keys. Contract schema 1 belongs to this rebuilt runtime; it is not an automatic import of the originals' schema-1 files.

## Contract

- `schema`: 1
- `host`: actual `codex` or `claude-code`
- `title`, `outcome`: nonempty label and observable finished state
- `authority`: reference to the actual task authorization; this string grants nothing
- `allowed_paths`, `forbidden_paths`: workspace-relative scope, with `.` allowed only when the whole workspace is authorized
- `external_actions`: explicit descriptions of separate approval boundaries or prohibitions; no implied external authorization
- `artifacts`: exact observable workspace-relative files, not directories
- `limits`: positive integer `max_iterations`, `no_progress_limit`, `max_seconds`, `max_output_bytes`
- `stops`: nonempty `success`, `failure`, `blocked`, `exhausted` conditions
- `actions`, `checks`: lists of distinct id-bearing command records
- `judgments`: separate id-bearing qualitative criteria
- `units`: ordered serial units, each with its own observable outcome and required evidence

A command record contains `id`, nonempty `argv` string array, workspace-relative `cwd`, positive `timeout` bounded by the run's time limit, `authority`, and `inputs` listing local scripts/data whose contents determine the result. Optional `artifacts` selects relevant files from the declared artifact list; omission binds the whole list. Declare the smallest complete relevant set, not an artificially narrow set that hides a regression. The resolved executable and literal argv are captured separately. Do not put secrets in argv.

A judgment contains `id`, `criterion` and explicit `independent` boolean. Optional `artifacts` selects its relevant subset of the contract's declared artifact files, parallel to command artifact scope. Omission binds the whole artifact map, so creating or changing a later unit's artifact can stale an earlier judgment. Declare the smallest complete relevant subset without hiding a dependency. The review operation binds actual review evidence and honest reviewer identity to that current scope. To refresh an affected earlier unit, use `review RUN --unit ID --expected-generation N --note FILE` through the integrated CLI, supplying a fresh actual review. This does not waive other checks or reopen a terminal run. Machine pass and judgment pass remain distinct. Review note fields are in the CLI contract; mark missing/failed review `unavailable` or `fail` as appropriate.

A unit contains `id`, `outcome`, and lists `actions`, `checks`, `judgments` referencing defined ids. Every unit has at least one real check. No branch scheduler or generic graph is implied. Coverage must account for all declared checks/judgments; additional domain cases belong in the work packet, not an ever-growing runtime framework.

## Authoritative snapshot

`snapshot.json` is one envelope containing `sha256` of canonical JSON and `state`. State carries run path/id, workspace, frozen contract/hash, monotonic generation, status, unit index, consumed limits, pending intent, captured results, reviews, verified-unit history, events, next action and optional schedule record.

Only the runtime's generation-checked operations write it. All logically committed state is published atomically under a local advisory lock; derived checkpoints and output files cannot independently advance the run. A captured log without a committed result is uncommitted evidence. A missing log, hash mismatch or pending intent must be investigated.

The lock coordinates cooperating runtime writers. It is not an OS security boundary; same-user malicious edits or programs ignoring the lock are outside that guarantee. Local POSIX filesystem assumptions must be checked on the target environment.

## Stops and revisions

Normal operation begins ready, executes bounded iterations, commits verified units and ends completed. Paused, waiting-input and blocked work resumes only when its specific prerequisite is resolved. If artifacts changed meanwhile, an acknowledged resume appends a `drift-acknowledged` event (`reason`, `previous` and `current` artifact maps, `changed`, `stale_committed_units`) and moves only the drift baseline; results and reviews keep their hashes, so affected units stay stale until rechecked or reopened. Exhausted, failed, cancelled and completed states are terminal unless a separately supported, authorized recovery explicitly records a new disposition. Never reset counters or replace evidence to simulate an uninterrupted success.

The rebuilt package does not mutate original live runs or automatically translate their receipts into stronger captured evidence. Inspect a named legacy run read-only, retain its provenance, and initialize a new approved contract if continuation is requested. Original boolean claims do not become captured results through import.
