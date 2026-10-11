# Supported source profiles

Select a profile explicitly in the manifest. Profile names describe this reader's mapping, not a universal producer API. The reader does not import, execute or refresh producer code. Unknown schema/status values fail visibly; it does not guess from nested keys.

Directory capture fingerprints every regular file under the selected bounded root, then the adapter reads only the profile's semantic fields. Choose the smallest relevant run root, not a project/home directory. Symlinks, nonregular files and exceeded limits are rejected. Content paths/URLs inside JSON are never followed into additional sources.

## supplied-v1

One JSON file with `schema_version: "1.0"` and a `records` array. This is the independent route for supported exported/mapped evidence, including producers without a dedicated reader. See [record contract](record-contract.md) for the full input shape and [CLI example](cli.md#complete-supplied-record-example) for a usable example.

The source's `namespace` applies to its records; each record supplies its producer and native run ID. A nonnegative integer `revision` is an explicit authoritative ordering assertion within that producer/namespace/run. Do not invent those revisions to break conflicts. If the underlying source lacks order, preserve conflicting evidence rather than manufacturing a larger revision.

A single captured file binds the bytes read; `coherence: "frozen-export"` additionally records the owner's assertion that the export represents a coherent capture. Neither establishes the truth of an external artifact or the correctness of a label. Supplied records must explicitly map lifecycle, judgment targets and measurements; producer-like names alone do not establish their meaning.

## loopkit-legacy

Select one legacy run directory containing `state.json` and `contract.json`. The supported schema marker is integer `schema_version: 1` when present. Primary mappings:

- native run ID: `state.run_id`, checked against `contract.run_id` when the contract supplies it;
- revision: `state.generation` when available;
- whole-run lifecycle: `state.status`;
- iteration count: `state.iteration`, never the contract's iteration policy object;
- goal: `contract.goal` or `contract.objective`;
- model/version: the contract's explicit fields;
- event/known time: `state.updated_at`, otherwise `state.completed_at`, with explicit timezone required;
- stop/escalation: explicit state fields.

Supported terminal states are `completed`, `failed`, `cancelled`, `exhausted`. `draft`, `ready`, `running`, `waiting_input`, `scheduled`, `blocked`, `paused` are nonterminal. A blocked run remains resumable even when a prior receipt passed.

Receipts are read from `evidence/receipts/*.json` and matched to the state's run ID and iteration. More than one matching receipt is a conflict. A matching receipt with the same status may supply machine-completion evidence. A differing status is valid only when the current state is reachable through the producer's permitted no-iteration transitions: a running receipt can precede blocked or cancelled state without another iteration. That receipt is retained as historical evidence and its checks are not promoted to current judgment. Entering completed requires a new receipt; a terminal receipt cannot explain a transition back to active state, so completed-to-blocked remains rejected. Raw judgments lacking exact artifact/rubric/human bindings are not calibration pairs.

The original toy fixture path `receipts/receipt.json` is not treated as a current authoritative real-producer receipt. Raw flat labels, costs or token counters without measurement units/basis are not promoted into calibrated labels or billed spend. When valid external evidence exists, map it explicitly through supplied-v1; do not edit the source run to fit this reader.

Coherence is `best-effort-multifile` unless the manifest declares a frozen export, in which case it is `owner-asserted-frozen-export`. File hashes alone do not establish a transactional legacy snapshot.

## loopkit-snapshot-v2

The `v2` suffix is the Observatory reader-profile generation. The accepted LoopKit producer's enclosed state schema remains integer `schema: 1`; this profile does not invent producer schema 2.

Supply its `snapshot.json` envelope, or the single snapshot file. It contains `state` and the SHA-256 of the producer's canonical state encoding. The reader checks the envelope's `sha256`, enclosed `state.schema == 1`, `state.contract_sha256` against the canonical embedded contract, and nonnegative integer `state.generation`.

Mappings:

- native ID/revision/status: `state.run_id`, `state.generation`, `state.status`;
- iteration count: `state.iterations`;
- goal: `state.contract.outcome`;
- event/known time: `state.updated_epoch`, converted from seconds to UTC;
- task identity: `state.contract_sha256`;
- artifact identity when present: digest of `state.last_artifacts`;
- raw judge evidence: `state.reviews`;
- stop reason: `state.stop_reason`; blocked/waiting-input next action may be shown as escalation context.

Terminal/nonterminal states follow the LoopKit mapping above. An accepted terminal revision cannot reopen to active state; reject that unsupported lifecycle transition. The reader preserves embedded checks/reviews and explicitly warns that external logs, workspace files and review artifacts were not independently verified. Hash-valid review text is not automatic human acceptance. Model and costs remain unknown when the snapshot has no supported evidence for them.

Coherence is `verified-single-envelope`, which means the envelope/contract bindings were checked. It does not mean the actual artifact's quality, live workspace, user approval or external review evidence was verified.

## operating-graph-legacy

Select one run directory containing `state.json` and `graph.json`; `events.jsonl` is optional. Supported `state.recordVersion` is integer 1 when present.

Mappings:

- native ID: `state.runId`, with the original flat `run_id` fallback;
- whole-run status: `state.status`; never `nodeStates.*.status`;
- graph version: `state.graphVersion`;
- iteration/work count: `state.totalNodeRuns`, with the flat `iteration` fallback;
- revision: `state.generation`, otherwise the highest matching event `sequence` when present;
- event/known time: matching sequence event `timestamp`, otherwise `state.updated_at`;
- goal/model: explicit `graph.goal` and `graph.model`;
- stop/escalation/raw judge/human label: explicit whole-state fields.

Supported terminal states are `completed`, `failed`, `cancelled`, `exhausted`. `running`, `paused`, `blocked`, `stopped` are nonterminal in this mapping. Unsupported states require a new evidence-backed mapping, not a convenient alias.

CamelCase identities and version fields are native evidence, not errors to coerce away. Node success, critic verification and execution approval remain separate from whole-run human output acceptance. Raw legacy labels without exact target/rubric binding cannot form a calibration pair.

Coherence is best-effort multi-file or owner-asserted frozen export. An event sequence orders supported evidence; it does not independently prove that a mutable state projection and every referenced object were committed together.

## operating-graph-v2

Two input forms are supported:

1. **Immutable run closure:** a run directory containing contiguous `commits/00000001.json`, `commits/00000002.json`, etc., and their referenced `objects/<sha256>` files. Each commit must have `recordVersion: 2`, a valid canonical digest, matching sequence/filename, correct `previousSha256`, unique operation ID, bound state generation/run ID, and complete hash-verified object closure. The reader preserves revisions from the chain. Coherence is `verified-immutable-commit-object-closure`.
2. **Frozen state export:** one JSON file containing the state directly or under `state`, with `coherence: "frozen-export"` in the manifest. The state must still have `recordVersion: 2`, supported status, and a graph definition bound to `versions[str(graphVersion)]`. Optional `exported_at` is the supplied event/known time. Coherence is only `owner-asserted-frozen-export`.

A bare commit file cannot stand in for a missing chain/object closure. A mutable projection directory without its closure is not quietly promoted to verified. Return `missing-closure` and request the needed supplied evidence.

State mappings use `runId`, `generation`, `status`, `totalNodeRuns`, `graphVersion`, `graphId`, `graph.goal`, `graph.model`, `stopReason`, `escalationReason` and raw `verification`. Event time comes from the commit timestamp or supplied export time. Native `recordVersion: 2` is separate from the graph's own version number.

Terminal states match the Graph mapping above. Valid authoritative current revisions retire older terminal views where the producer permits it; current and historical counts stay separate. Graph approvals and verification are producer evidence, not human output acceptance or a matched calibration label. The reader never fetches source-linked object URLs or executes a Graph operation.

## When evidence exceeds these readers

Return the precise unsupported field/profile or missing closure. If the user already supplied an adequate export, create a separate source-linked mapping to supplied-v1 in the observer's output area; retain native identities, values and unknowns. Do not replace the native files. Document the exact fields and meaning used so the mapping can be checked. If the required semantic binding is absent, ask for that evidence rather than filling it in.
