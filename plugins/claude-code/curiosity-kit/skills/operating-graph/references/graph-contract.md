# Graph and run contracts

Graph definitions describe work; the run contract binds execution and evidence. Neither grants external authority by itself. Read [Design](../playbooks/design.md) for the method and [CLI](cli.md) for operations.

## Definition: schema 1.0

Top-level fields are `schemaVersion`, `graphId`, `name`, `goal`, `limits`, `nodes`, `edges`, `rewritePolicy` and `metadata`. Use the complete [minimal definition](../assets/templates/graph.json) or [diamond definition](../assets/templates/diamond-graph.json), then adapt the actual job. IDs use lowercase letters, digits and hyphens and must be unique. Metadata includes `createdBy` and canonical UTC `createdAt`; additional metadata values are strings. Conditions are declarative data, never executable expressions.

### Original goal

`goal` contains a statement, typed deliverables (`id`, `artifactType`, `description`), `completionCriteria` and `authorityNodeId`. Criterion identities in this schema are their exact strings: preserve those strings rather than substituting new labels during evaluation. A meaningful criterion identifies an observable requirement, not a general promise of quality. Required deliverables need an enabled producer and independent evaluator path.

After initialization, the original goal, criterion meanings, deliverables, authority, existing permission boundary and hard limits cannot be weakened through a rewrite. A different goal is a new authorized run.

### Nodes

Each node specifies:

- Identity and purpose: `id`, `kind`, `label`, `purpose`, `enabled`, `critical`, `priority`.
- Execution: `execution.mode`, optional `execution.skill` and optional exact `execution.modelHint`.
- Scope and data: `capabilities`, typed `inputs` and `outputs` using `artifactType` and `required`.
- Quality: exact `successCriteria` strings.
- Bounds: `budget.maxAttempts`, `budget.workUnits`; `localLoop.enabled`, `maxIterations`, ordered `sequence` and `stopCondition`.

Kinds are authority, controller, worker, state, evaluator, distributor and signal. Modes are inline, subagent, tool and human. Exactly one enabled authority and one enabled controller own the run; every enabled node must be reachable from authority. A node cannot evaluate or approve its own output.

An optional skill reference is a public, available capability selected for this task, not a hidden sibling dependency. A model hint is a real requested model; lack of support blocks that mode. Local loops stay inside one node's bounded work and cannot rewrite topology or controller records. Runtime counters enforce invocation/launch/global bounds; work-unit/local-iteration reports remain declared measurements whose actual host enforcement must not be overstated.

### Edges

An edge has `id`, `source`, `target`, `kind`, `enabled`, `required`, `temporal`, `artifactTypes` and `activation`. Kinds are goal, assign, read, write, verify, approve, publish, measure, escalate and learn. Temporal values are same_epoch and next_epoch.

Activation declares `mode` (all/any), exact node-state requirements, artifact types and approval IDs. Required edge data must come from that exact source and epoch, with an eligible successful invocation and matching digest. Node required input types must be supplied by routed edges. A same-type artifact from another branch cannot satisfy a missing producer. Optional edges can relay available context but do not turn into mandatory ordinary dependencies.

Approval is an independent mandatory predicate. A required approve edge or required approval-bearing activation cannot be bypassed by source success or ANY activation. Record actual scoped permission through the controller; never use topology as consent.

The enabled same-epoch projection must be acyclic. Every feedback cycle needs a next_epoch edge and finite epoch bounds. Execution requires a declared bootstrap seed for required epoch-one feedback, exact prior-epoch lineage thereafter and a quiescent barrier. A predicate saying an epoch could advance is not an executed epoch transition.

### Limits and policy

Positive integer limits include `maxConcurrentWorkers`, `maxNodeRuns`, `maxGraphVersions`, `maxEpochs`, `maxAutoRewrites` and `defaultMaxAttempts`. Booleans are not integers. Define smaller job-appropriate bounds rather than treating template values as a target. Outstanding reservations and unknown/live calls consume capacity; issued attempts are not refunded when a slot is released.

`rewritePolicy` contains `automaticRiskLevels`, `approvalRiskLevels` and `prohibitedMutations`. Use [policy guidance](rewrite-policy.md) and [machine-policy example](../assets/templates/policies.json). Original trigger heuristics now live in prose; unsupported `triggerPolicies` are not a functioning scheduler configuration. The runtime validates policy rather than silently dropping those keys.

## Run contract: execution record protocol 2

Pass a JSON object to `init --contract`. Supported keys:

- `deadline`: canonical UTC absolute deadline. Set it to the actual authorized bound. If omitted, the runtime supplies a finite 24-hour default; this does not override a shorter user deadline.
- `maxLaunchAttempts`: positive monotonic launch allowance, subordinate to graph/global limits.
- `criteria`: one mapping per original criterion: exact `criterion`, required `deliverableId`, `evaluatorNodeId`. Missing mappings cannot pass final verification. The evaluator must consume and judge that exact current deliverable.
- `approvalBindings`: object keyed by approve-edge ID or activation approval ID. Each value contains `subjectType`, `subjectId` and an action `scope` object. Types are external-action, artifact or resume; rewrite bindings are derived from the exact persisted proposal. The runtime adds current run, node/epoch/contract and input-digest scope. When an edge and an activation name separate gates, bind both explicitly; no implicit aliasing.
- `seeds`: list of `{edgeId, artifactType, path, sha256}`. A seed binds one next-epoch edge and declared type, is read from the selected actual local file, and is copied into immutable owned content. A hash mismatch blocks initialization.
- `optionalNodeIds`: unique noncritical nodes eligible for explicit omission. A node feeding required work cannot be made optional merely to bypass it. Live/uncertain work still requires settlement.
- `evidenceTier`: `simulated` for sample adapters, `controller-declared` for ordinary controller-mediated CLI records, or `controller-observed` only with an actual observation-verifying adapter. Imported JSON cannot establish observed provenance. Target-host qualification remains external evidence in every case.

See the complete [minimal run contract](../assets/templates/run-contract.json), [diamond run contract](../assets/templates/diamond-run-contract.json) and [research run contract](examples/research-run-contract.json). These bind the example definitions; change the definition and bindings together before initialization. They do not contain real user consent.

## Evidence, state and success

Every invocation captures run/node/epoch/attempt/graph contract, exact consumed inputs, immutable packet/launch/return bindings and owned output paths. Artifacts become eligible only after successful committed ingestion. Failed or quarantined outputs remain historical/provisional. A semantic rewrite invalidates affected evidence and evaluations; unchanged completed work needs an explicit carry-forward relation.

An evaluator's goal judgment names the original criterion, exact artifact ID/digest, result and reason, with actual inspected evidence. The engine checks bindings; it does not understand arbitrary business truth. The controller and independent evaluator must inspect the content. Machine pass, actual native execution and user acceptance remain distinct.

## Examples and their use

- [Minimal graph](../assets/templates/graph.json): authority/controller, one producer and independent evaluator. Replace generic deliverable criteria with the user's observable outcome.
- [Diamond](../assets/templates/diamond-graph.json): independent specialists, skeptic, synthesis, final content evaluation and human decision. A separate small decision audit checks the later decision record so it is not falsely certified before the human step occurs.
- [Research/build/review](examples/research-build-review.json): exact research relay to a report and independent claim review.
- [Adaptive publishing](examples/adaptive-publishing-org.json): design example with optional distribution channels, shared state and feedback. Supply actual action scopes, current approvals, criterion bindings and a deliberate executable feedback contract before running; the definition alone is not permission to publish. Optional feedback does not automatically schedule a new epoch. Do not treat its illustrative metadata or policy as a captured run.

Validate any adapted definition, then exercise the actual job and its important failure behavior. Schema validity cannot certify the audience, claim quality, source truth or benefit of a proposed graph.
