# Local CLI contract

Python 3.9+ on a POSIX host is required (standard library, including file locking). Invoke the actual skill path. JSON is input data, never authorization. Commands print JSON: exit 0 means the requested operation/check succeeded; 1 means refused or failed; 2 means invalid input. A valid audit ledger can contain failed controls: inspect `all_pass` and findings, not just exit 0.

```sh
python3 "$SKILL/scripts/agent_ops.py" --help
python3 "$SKILL/scripts/agent_ops.py" check-audit --workspace "$WORKSPACE" --input audit.json
python3 "$SKILL/scripts/agent_ops.py" init --manifest manifest.json --state "$STATE"
python3 "$SKILL/scripts/agent_ops.py" approve --state "$STATE" --contract-sha "$DIGEST" --input approval.json
python3 "$SKILL/scripts/agent_ops.py" launch --state "$STATE" --input launch.json
python3 "$SKILL/scripts/agent_ops.py" observe --state "$STATE" --input observation.json
python3 "$SKILL/scripts/agent_ops.py" complete --state "$STATE" --input return.json
python3 "$SKILL/scripts/agent_ops.py" integrate --state "$STATE" --input integration.json
python3 "$SKILL/scripts/agent_ops.py" review --state "$STATE" --input review.json
python3 "$SKILL/scripts/agent_ops.py" repair --state "$STATE" --input repair.json
python3 "$SKILL/scripts/agent_ops.py" finalize --state "$STATE" --input final.json
python3 "$SKILL/scripts/agent_ops.py" status --state "$STATE"
```

These are stages, not an unattended shell recipe. Start from the supported user imperative "Use bounded delegation for this." Obtain approval between init and approve; create the actual native worker between launch and observe; inspect its actual completion before complete. After all required worker results, the parent integrates, then reserves/observes a fresh critic before review. `$STATE` must be `$WORKSPACE/.fable-advisor/runs/<run_id>/run-manifest.json`. `$DIGEST` is the returned `contract_sha256`, not a guessed file hash.

## Common values

A file reference is exactly `{ "path": "relative/file.txt", "sha256": "actual lowercase SHA256 of those bytes" }`. Compute the hash from the actual file. Paths are workspace-relative, exact, with no traversal or symlinks. Evidence references must live below the declared `evidence_dir`. Create parent-owned observation/command/approval receipts from actual evidence; synthetic receipts are for isolated tests only.

An identity object is `{ "model": null, "reasoning_effort": null }`, replacing null only with the requested or observed value, as appropriate. Null means unknown/unselected, never observed. Every receipt containing `contract_sha256` binds the exact initialized manifest.

## Manifest and approval

Manifest fields, all required:
- `version`: 1; `owner`: `agent-ops`; `mode`: `advisor`; `run_id`: safe unique identifier; `workspace`: existing absolute resolved directory; `parent_id`: actual parent identifier.
- `activation_request`: verbatim activating imperative; `peer_active` and `gauntlet_requested`: actual booleans; `peer_state_paths`: actual disclosed workspace-relative Gauntlet state paths; `peer_controllers`: empty array for this standalone run. Check current disclosed ownership first; unknown blocks initialization rather than becoming false. No conventional peer path is inferred or recursively scanned.
- `plan`: file reference; `inputs`: array of file references; `evidence_dir`: separate relative directory.
- `tasks`: array of `{id, depends_on, reads, outputs, required, criteria, checks}`. Dependencies are task IDs; reads/outputs are exact relative paths; required is boolean; criteria are unique IDs; checks are approved argv arrays such as `["python3", "-m", "unittest", "discover", "-s", "tests"]`. Empty checks are allowed only when no command check is required; criteria still need evidence.
- `integration_outputs`: exact parent-owned paths; `integration_criteria`: IDs; `integration_checks`: argv arrays.
- `budget`: positive integer `launches`, positive integer `concurrency`, nonnegative integer `repairs`. Critic launches count too. Reserve enough for required work and independent review.

Outputs must be disjoint and cannot overwrite plan, inputs, state, manifest or evidence directories. Task reads may name plan/inputs and direct dependency outputs. Generic scheduling and arbitrary nested controllers are unsupported.

Approval JSON contains `contract_sha256` and `evidence` (a file reference to the actual verified approval). Pass the same digest to `--contract-sha`. Approval records do not prove who approved: the parent must verify the real user message.

## Launch and observations

Launch: `contract_sha256`, `launch_id`, `role` (`worker` or `critic`), `task_id` (task ID or null for critic), `read_only` (false for worker, true for critic), `requested_identity`, `runtime_available` (observed boolean). A reservation consumes capacity before native dispatch. Reusing an identical launch ID is idempotent; it does not authorize launching another child.

Observe: `contract_sha256`, `launch_id`, `worker_id`, `host` (`native`), `observed_identity`, `evidence`. Bind only the actual host-returned ID. A critic must be a different fresh child, not the parent or a previous worker. A worker ID may be reused only to continue the same current task after that child's terminal failed return, after the parent has verified real host resume support: add `continuation_evidence` (`{path, sha256}` in the evidence directory) for the inspected native lineage. The relaunch still consumes launch and repair budget. Without verified resume support, use a fresh native retry. Unavailable required capability blocks; contradiction of an explicitly requested identity blocks.

## Returns, integration and review

A command result is `{argv, exit_code, evidence}`. The CLI reads it but never executes argv. A criterion result is `{name, status, evidence}`, where status is `pass` or `fail`. Task and integration results must exactly cover the approved criterion IDs and command argv arrays.

Complete: `contract_sha256`, `task_id`, `launch_id`, `worker_id`, `status` (`success` or `failed`), `artifacts` (file references), `reported_writes` (exact artifact paths), `criteria`, `commands`, `evidence`. Successful completion requires every task output, passing criteria and zero command exits. Failed returns remain evidence, not accepted work. Duplicate completion/review receipts are explicitly refused without changing recorded state or counters; read status after an uncertain submission. They are not a new worker retry.

Integrate: `contract_sha256`, `parent_id`, `integrated_artifacts`, `reported_writes`, `criteria`, `commands`, `evidence`. This records the parent's actual integrated outputs after required predecessors succeed. The returned `subject_sha256` binds worker results and integration.

Review: `contract_sha256`, `launch_id`, `worker_id`, `subject_sha256`, `verdict` (`accepted` or `rejected`), `read_only`: true, `reported_writes`: [], `findings` (strings), `commands`, `evidence`. Accepted reviews have no unresolved findings and must cover the approved integration checks with successful exits. Rejected reviews preserve genuine failed reproduction commands and evidence unchanged, including through later repair. Candidate files must still match the frozen subject. Receipt writing is parent-owned; the critic may return its report through the host without artifact writes.

Finalize: `contract_sha256`, `parent_id`, `subject_sha256`, `review_sha256` from the recorded review result. All launched children must be accounted for, required tasks complete and the exact integration accepted by the fresh critic.

## Stop and recovery

`resume`, `status` and `validate` take only `--state`, read existing state and recheck drift without launching anything. `stop` and `revoke` take `--input` containing `{reason}`. They prohibit further dispatch and never overwrite a completed result. Budget exhaustion also stops dispatch. Unconfirmed children keep the peer log open and ownership held.

If a child was dispatched before interruption but its observation was not recorded, recover its actual native ID/evidence with `observe` for that already-reserved launch, even after stop. This is accounting only: it neither reactivates the run nor permits dispatch. After actual host cancellation/completion, use `settle --state ... --input ...`: `contract_sha256`, `launch_id`, `worker_id`, `status` (`cancelled`, `failed` or `completed`), `evidence`. Null worker ID and `not_started` are only for a reservation with actual evidence it was never launched. Settlement does not accept unfinished artifacts. Ownership remains held until all children are accounted for; then one Gauntlet-compatible terminal line is written.

State and peer log are separate atomic files. A crash between writes can conservatively leave the peer log open; repeat stop/revoke to reconcile it after inspection. Never delete the ownership file to bypass a running or uncertain child.

After a fresh critic rejects the integrated candidate, `repair` explicitly reopens only approved same-scope work. Input: `contract_sha256`, unique `repair_id`, the rejected `review_sha256`, `task_ids` (affected task IDs, or empty for parent-integration-only repair), `reason` and `evidence`. The CLI invalidates those task results and dependent descendants, archives the prior integration and preserves earlier launches, receipts, reviews and usage. Do not overwrite outputs before this transition succeeds. A new integration and fresh critic are required; old acceptance cannot qualify changed bytes.

One repair transition consumes one repair unit. Its first replacement task launches and fresh critic consume the remaining launch budget, without charging that repair twice. A further failed-task retry consumes another repair unit. Exhausted repair or launch capacity refuses further work. Plan, inputs, criteria, scope or authority changes still require new approval; do not use repair to widen a frozen contract. Hash consistency is not authenticated provenance, and this ledger is not an OS sandbox.

## Ten-control audit ledger

Input is `{controls: [...]}` with exactly these IDs: outcome, evidence, authority, stops, state, tool_contracts, recovery, cost, observability, verification. Each entry has `id`, `status` (`pass`, `fail`, `unknown`), `evidence` (nonempty file-reference array) and `findings` (array of `{severity, detail}`). Severity is blocker/high/medium/low. Failed controls need findings; passing controls have none. Unknown may cite the inspected material and its missing evidence. The checker validates coverage and sorts findings; it does not judge whether the evidence supports the claims.

Deterministic checks with temporary files and synthetic host receipts can verify local consistency; they do not establish native host qualification.
