# Local graph command reference

Python 3.9+; standard library only. Mutation currently requires a POSIX local filesystem with `fcntl` locking (including the tested cloud Linux surface and intended macOS surface). An unsupported lock surface fails closed. No installation, network client, account or model call is performed by this CLI. Choose the actual canonical local run root: the engine rejects symlink components, including convenient path aliases. Resolve the selected root explicitly before initializing, and never use that resolution to widen the authorized location.

From the skill root, invoke `python3 scripts/graphctl.py <command> ...`. From elsewhere, use the actual absolute path to that script; do not assume the user's current directory is the skill directory. Each subcommand accepts `--json`. Output is JSON in either mode, compact with that flag and indented otherwise. Use `python3 scripts/graphctl.py <command> --help` for the actual argument contract.

## Format and compatibility

Graph definitions retain schema `1.0`. Runs and task/launch/return records use protocol **2**, with a separately supplied run contract. V1 live records are not silently migrated. Unsupported/unsafe old operations return conversion-needed; retain originals and create an isolated v2 run after mapping the intended work. No command edits an old installed plugin or transfers its acceptance claims.

Read-only `verify` no longer closes a run. Explicit `finalize` performs terminal mutation only when the verdict and closure conditions permit it. Raw `transition` and `register-artifact` names remain discoverable but reject unsafe direct mutation; use the guarded invocation/return lifecycle for every lane. This deliberately closes the old bypass rather than preserving its unsafe behavior.

## Common mutation controls

Use `--operation-id <safe-id>` to identify one intended mutation, and `--expected-generation <integer>` to reject a stale controller view where accepted. Repeating the same committed operation ID and intent returns its stored result; changing intent under the same ID rejects. Do not reuse an ID for a new action. `init` rejects expected-generation because no prior generation exists. `recover` is a dedicated projection repair, not a new dispatch.

A failed command is not permission to edit state manually. Inspect whether the intent committed before retrying. External issuance and local recording are not one atomic transaction: an unknown outcome requires observation/settlement, not a new operation ID and blind relaunch.

## Definition and initialization

- `validate <graph.json>`: read-only definition parsing and invariants. Reports graph identity and supported formats; does not prove a semantic outcome.
- `init <graph.json> --run-root <owned-directory> --contract <run-contract.json>`: creates a new `run-<graphId>` directory. Existing run directory rejects. Captures the original graph and frozen contract; starts no workers.

The run contract is documented in [graph-contract.md](graph-contract.md). Explicitly set a suitable deadline, criterion bindings, authority scopes and any feedback seeds; defaults are not a substitute for the user's actual bounds. The initialization response supplies the exact run directory and a unique actual runId. Keep both for every subsequent operation; the directory basename is not an interchangeable approval or receipt identity.

## Read-only observations

All take `<run-directory>`:

- `status`: current committed state and unresolved obligations.
- `ready [--lane subagent|inline|human|tool] [--available-slots N]`: eligible frontier and blockers without reservation.
- `dispatch-preview [--lane ...] [--available-slots N]`: subagent frontier by default, still read-only.
- `inspect --format text|mermaid`: record-backed view. Mermaid summarizes topology; it is not the full approval/evidence contract.
- `replay`: reconstructs and checks committed/projection agreement; does not rerun workers.
- `resume-check`: integrity/readiness for resumption plus obligations. It does not resume by itself.
- `verify`: criterion-specific current verdict without finalization. A failed semantic/evidence check is not a corrupt-store repair request.

## Guarded invocation lifecycle

1. `prepare-dispatch <run> [--node <id>] [--lane <mode>] [--available-slots N]`: default lane is subagent. Commits invocation/packet identity and reserves capacity. Returns task paths, hashes and normalized launch specifications. Select a different lane explicitly for inline, human or tool work.
2. `begin-launch <run> <invocation-id>`: commits issuance intent and rechecks current eligibility immediately before the controller's actual host call. An issued intent without an observed response remains an obligation.
3. Controller makes the actual permitted call or performs the selected inline/human work. The CLI does not do this step. Capture the actual response; do not fabricate one to unblock the graph.
4. `record-launch <run> <record.json>`: binds the normalized observed/declared outcome to the prepared invocation and packet. Rejected and unknown launches remain distinct from successful execution.
5. Worker/controller writes the complete return at the packet's `canonicalReturnPath`, within the selected run. `ingest-return <run> <return-packet.json>` validates scope, exact receipts, output types, evidence and criteria before eligibility changes.

Use [node-packet.md](node-packet.md) for exact JSON fields. Neither `transition <run> <node> <status>` nor `register-artifact <run> <node> <type> <path>` can manufacture success or active artifacts; both return the migration guidance above.

## Approval and unresolved outcomes

- `record-approval <run> <record.json>`: record a scoped decision and provenance. The engine checks binding/order; the controller is responsible for actual authenticated permission. Sample decisions are simulated, never user consent.
- `settle <run> <record.json>`: reconcile an issued/unknown/cancelled obligation using the supported observed outcome. An uncertain effect remains uncertain when the host cannot establish what happened. Settlement cannot create new work or silently activate late output.
- `signal <run> <name> <value>`: records bounded diagnostic/feedback data. JSON values are parsed as data; a signal is not executable code or an approval.

## Topology and epochs

- `propose-rewrite <run> <proposal.json>`: persist a fully validated proposal bound to current version. Drafting a file outside the run is a separate non-submission action.
- `apply-rewrite <run> <proposal-id>`: apply within policy/approval/budget only at quiescence; affected evidence is invalidated, old history retained.
- `withdraw-rewrite <run> <proposal-id> --reason <text>`: withdraw a pending proposal and its dispatch-drain intent when appropriate.
- `advance-epoch <run>`: cross the declared barrier with current exact feedback, fresh invocation identities and global limits preserved. It cannot advance by editing a counter.

The six primitives and nine compiled patterns are explained in [rewrite-policy.md](rewrite-policy.md). A rollback is a new permitted version, never deletion of history.

## Stop, omit, recover and finalize

- `cancel-node <run> <node-id> --reason <text>` / `cancel-run <run> --reason <text>`: request stop and account for unissued reservations. Issued/live work requires actual terminal observation; request alone is not proof of termination.
- `omit-node <run> <node-id> --reason <text>`: explicitly omit only eligible optional inactive and fully accounted work permitted by the frozen contract; not a shortcut around a failed required task.
- `recover <run>`: under the writer lock, restore disposable projections from trustworthy committed authority. Reject broken committed chains/objects; never infer an external outcome from a local snapshot.
- `finalize <run>`: verify required results and closed obligations, then commit the terminal result. It does not send/publish deliverables or grant project acceptance. Terminal state prevents new work; narrow late accounting remains possible without reopening.

## Errors and interpreting results

Success exit 0 means the requested command succeeded, not that the entire user job is accepted. `verify` returns nonzero for a non-passing verdict. Current expected failure classes: exit 2 invalid input/policy/packet or failing verification; exit 3 corrupt committed/evidence state; exit 4 missing/inapplicable approval; exit 5 unsupported legacy/conversion-needed. Argument parsing can also exit 2. Read the result's error/verdict and evidence fields; do not grade solely on exit status.

Keep the command, actual result, exact run/candidate identity and relevant artifact evidence in a bounded development receipt when qualifying the skill. The engine's own JSON is not an independent content oracle or native tool attestation.
