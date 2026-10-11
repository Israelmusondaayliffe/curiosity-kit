# Local runtime protocol 2

Load before mutating a run or interpreting its recovery evidence. [CLI](cli.md) is the supported command interface; `graph_engine.runtime.Runtime` is the supported Python control interface. Original pure graph/model/invariant/rewrite helpers remain useful; superseded v1 persistence/mutation entry points cannot bypass v2 guards.

## One authoritative history

Each initialization receives a unique run identity, even when another copy uses the same graph and directory basename. Each local run has immutable numbered records under `commits/`. A committed operation records its identity, intent digest, prior commit hash, sequence, timestamp, complete resulting run data and result. This is the source of truth. Readable projections include `state.json`, `graph.json`, `contract.json`, `policies.json`, `events.jsonl`, `artifacts.jsonl`, `approvals.jsonl`, graph-version views, packet/receipt views, rewrite views and any finalized verification. They are derived views, not alternate controllers.

Content-addressed objects under `objects/` retain exact artifact/seed bytes. Invocation history binds those objects to original source paths, declared producers, exact inputs and outcomes. Immutable graph versions and prior attempts remain identifiable through later changes.

The controller alone writes canonical records and receipts. Workers write only their invocation's declared worker/artifact roots. All parsed data remains data; graph conditions or worker recommendations are never executed as code.

## Commit, retry and recovery

A bounded per-run POSIX lock serializes local controllers. Only initialization creates the run and lock; read-only operations on a missing run must fail without creating files. Lock acquisition has a finite timeout and never steals a live lock. No lock remains held across a real worker/effect call.

A mutation loads trusted committed history, verifies projections and bindings, checks operation-specific preconditions, stages immutable content, commits one operation and publishes its derived projections. Atomic file replacement is used within that protocol; it is not described as a magically atomic multi-file transaction.

A stable operation ID means the same intended mutation. Same ID and intent returns its committed result; changed intent under that ID is rejected. Use the current expected generation to reject stale control decisions. Stop, revoke, record failure, quarantine, cancel and settle have appropriate narrower guards than new execution, so exhausted/revoked work can still be made safe.

If a process stops before commit, staged content is not eligible state. If it stops after commit but before all projections publish, ordinary reads detect the mismatch. Authorized `recover` reconstructs projections from the intact committed chain and objects. It does not repair a broken committed chain, authenticate altered history or invent a missing external outcome. Historical replay explicitly distinguishes reconstructed records from checking mutable external evidence; recovery reports remaining evidence issues rather than pretending changed worker files were healed. Preserve the original error and exact recovery result.

The bounded guarantee is tested local process-interruption recovery. It is not distributed consensus, arbitrary power-loss durability, hostile same-user protection, cryptographic human authentication or exactly-once behavior for an unqueryable connector. Hashes detect tested divergence within the controller trust boundary.

## Readiness and reservation

Readiness is computed from enabled/current nodes, exact required producer/epoch artifacts, declared ALL/ANY data activation, independently mandatory approval gates, lifecycle/deadline and remaining bounds. Optional input is used only through its declared edge when available. A worker's succeeded label alone cannot supply another node's required artifact.

Ordering preserves higher priority, critical before optional, more incomplete immediate required successors, then lexical ID. Filter by the selected execution lane before applying capacity. The host controller supplies currently available capacity after accounting for itself and other work; the graph cannot discover every external host task from a JSON limit.

Preparation creates one immutable invocation identity and reserves space. Prepared, issued-unknown, running, cancellation-pending and effect-unknown obligations consume capacity. Actual/uncertain launch attempts consume monotonic allowance; a released concurrency slot does not refund them. Proven never-issued reservations can be released without claiming a worker ran.

`begin-launch` is the final local eligibility/intention boundary immediately before the actual host action. Losing the response leaves an unknown obligation. The next step is observation/settlement, not a new blindly issued launch. A different attempt uses a fresh identity and current inputs, permissions and remaining budget.

## Packets, outputs and evaluation

The generated task captures run/graph/epoch/node/invocation/attempt, semantic contract hash, exact inputs, expected outputs/criteria, launch intent, deadline, allowed roots and controller-authority denials. The launch record binds observed or declared response to that packet. Return ingestion checks the canonical path, receipt bindings, identities, owned paths, output types, hashes, all exact criteria and evidence references. See [node-packet.md](node-packet.md).

The engine can reject unsafe paths and symlink aliases in the tested local scope. It cannot physically prevent every write by a process sharing its user/filesystem; actual containment requires a separately supported sandbox. A reported write list is not a comprehensive forensic audit.

Successful committed output is eligible only under its exact producer/invocation/epoch/contract. Failed/blocked, late or guard-quarantined output stays provisional. Current source bytes and immutable object/receipt identities are checked; changing a reviewed output makes its old evidence stale or corrupt rather than silently preserving a pass.

Goal-level evaluations belong to evaluator invocations and bind exact consumed deliverable IDs/digests to the original criterion strings. A criterion needs a specific judgment and inspected evidence, not a generic no-errors flag. Runtime checks establish binding and declared independence; semantic truth and actual native context separation still require competent inspection of real artifacts/tool evidence.

## Approval ordering

The frozen run contract describes exact gate/action scopes. Runtime scope also binds run, node, epoch, semantic contract and captured input digests. The controller records an actual permitted decision and its provenance, or labels a sample decision simulated. Resolve effective grants/denials/revocations by trusted controller record order, not arbitrary imported timestamps or a collision of subject strings.

Revalidate before issuing work and before accepting eligible outcomes. Changed content/destination/input scope needs a current applicable decision. Approval for a rewrite cannot remove the original action approval boundary. Revocation stops future authorized action but cannot undo an already issued effect; retain the actual or unknown outcome.

## Rewrites and feedback

A persisted proposal establishes a drain boundary; new dispatch pauses while current obligations settle. Applying requires confirmed quiescence, current base/policy/approval and remaining limits. No in-flight cross-version compatibility is silently inferred.

A committed rewrite preserves original goal/authority/history, computes semantic affected closure, invalidates changed eligibility/evaluations and records explicit unaffected carry-forward. Historical records keep their actual old versions. Rollback is another permitted version, not history erasure. Read [rewrite-policy.md](rewrite-policy.md).

Epoch advancement is explicit. Required current-epoch work reaches its barrier, live/reserved/unknown work is settled, and exact declared feedback is available. Epoch one has its declared seed; later invocations consume previous-epoch artifacts. Advance creates fresh invocation opportunities without resetting global counters/history. If the goal is already satisfied, finish rather than add an unnecessary epoch. Exhaustion remains an unfinished bounded outcome.

## Stop, late data and terminal closure

Cancellation records a request and accounts for proven unissued reservations. Actual live/unknown work remains unresolved until observed stopped/rejected/completed as appropriate. An interrupt or missing response is not proof of termination. Optional inactive and fully accounted work can be explicitly omitted only under its frozen contract.

Late results can be appended as non-activating settlement without reopening a terminal run. They cannot revive cancelled success, activate artifacts, advance dependents or upgrade a verdict. This narrow accounting exception does not permit new work after closure.

Read-only `verify` returns the current criterion/evidence verdict. `finalize` commits completion only when the original requirements and all relevant obligations are resolved. A command exit 0, structurally valid artifact or machine pass is not independent project/user acceptance. Preserve exact evidence tier, failures, optional limitations and required unrun host checks in the handoff.
