# Task, launch and return packets

Protocol 2. Every initialization has a unique actual runId; the reusable run-directory basename is not its identity. Read when dispatching, recording a host response, writing a return or investigating receipt mismatch. Generated task packets are authoritative for the invocation; illustrative templates are not substitutes for them. [Host contract](host-contract.md) distinguishes actual observations from declared/mock data.

## Task produced by prepare-dispatch

The task contains `packetType: NodeTaskPacket`, `protocolVersion: 2`, `runId`, `graphId`, `graphVersion`, `epoch`, `nodeId`, `invocationId`, `attempt` and `contractSha256`. It carries:

- `task`: the complete selected node contract, including purpose/execution/scope.
- `requiredInputs`: exact routed artifact IDs, producers, epochs, invocation/graph identities, digests and paths. Despite the field name, available optional context may be included; do not replace it with a global same-type search.
- `successCriteria` and `expectedOutputs`: exact strings/types and required flags.
- `launchSpec`: normalized execution intent, not a literal universal host tool call. Preserve its selected mode, fresh-context requirement and requested model; record actual host fields separately.
- `allowedWriteRoots`: this invocation's worker directory and artifact directory.
- `canonicalReturnPath`: where the complete return must be written.
- `approvalScopes`, absolute `deadline`, finite `limits`, and explicit `authorization` denials.

Current owned roots have the form `node-runs/<node-id>/<invocation-id>/worker/` and `artifacts/<node-id>/<invocation-id>/`. Controller task/dispatch/launch/receipt files beside the worker directory are not worker-owned. Paths are relative to the selected run root; no absolute path, traversal or symlink alias is permitted for owned writes. Temporary scripts, scratch files, caches and any redirected output must also stay inside the declared owned roots; use an owned temporary directory or do the calculation inline, never `/tmp` or a host-global directory.

For a goal evaluator, also supply the frozen run contract’s original criterion/artifact mappings and exact consumed artifact IDs in its bounded launch brief; node-local criteria alone do not carry those mappings. Keep these additions source-bound and do not modify the generated task.

In each fresh worker's brief, include the applicable return schema below, exact task identity fields, controller-supplied `taskPacketSha256` (not `contractSha256`), canonical return path and owned relative output paths. Spell out required artifacts, separately declared evidence with paths/hashes, exact criterion strings and `evidencePaths`, evaluator judgments when applicable, and the task's six authority denials. An artifact cited by a criterion must also be declared as evidence; a reference path alone does not supply this return contract to a fresh worker.

The controller binds the task's canonical JSON digest in a dispatch receipt. Do not hand-edit a task packet to change the job after reservation. Cancel/settle or propose a proper change instead.

## Launch record from the controller

After `begin-launch` and the actual host operation, record:

- `protocolVersion: 2`, exact `runId`, `invocationId`, `taskPacketSha256`.
- `request`: the normalized `tool`, `forkTurns`, `model` and task name from `launchSpec`; for real controller-declared/observed work also include `request.actualHostTool` (actual tool name) and `request.actualArguments` (actual argument object).
- `response`: `outcome` (`launched`, `rejected` or `unknown`), actual observation `reference`, and `agentId` when launched.

For a subagent, the identity must be the actual returned fresh worker identity. For an inline/human/tool lane, the compatibility field `agentId` denotes a unique logical local execution identity; it does not prove another model or human exists. Do not fabricate a real agent ID for local work. The normalized tool label describes the engine's intent; actual host tool names come from the session.

Use `controller-declared` for normalized CLI records whose real provenance the controller/independent reviewer inspects externally. `simulated` explicitly labels fixtures. `controller-observed` additionally requires the actual observation-checking adapter. A Boolean, callback name or imported JSON cannot by itself authenticate an event. The engine's verdict never claims target-host qualification.

Missing response after intent stays unknown. A rejected launch remains a spent issued attempt, not an execution success. Preserve each attempt's evidence; no record overwrite to hide prior rejection.

## Complete worker return

Write at the task's canonical return path, then ask the controller to ingest it. For real host workers, the controller supplies the actual observed `agentId` after launch and adds the actual `completionReference` after observing completion, before ingestion; workers never invent either value. Preserve the worker's submission and distinguish controller-added host metadata from worker-authored content. Include:

- `packetType: NodeReturnPacket`, `protocolVersion: 2`, exact `runId`, `invocationId`, `taskPacketSha256`, execution `agentId`, `nodeId`, `epoch`, `graphVersion`, `attempt`.
- `status`: succeeded, failed or blocked; `escalate` is accepted as a blocked outcome with an advisory recommendation. `summary` states the actual result. Real controller-declared/observed returns also retain the actual `completionReference`; a file alone is not proof a worker stopped.
- `actualWritePaths`: unique relative paths of all declared produced files, each inside the invocation's owned roots. Include artifact/evidence paths; report unexpected writes to the controller rather than concealing them.
- `artifacts`: entries with declared `artifactType`, owned artifact `path`, exact byte `sha256`, and useful media type when applicable. A successful return supplies every required output type; undeclared output types cannot become eligible.
- `evidence`: entries with owned `path`, exact `sha256` and evidence `kind`. Evidence files must be declared writes and actually exist.
- `criteria`: exactly one entry per node criterion with exact `criterion`, `result` (met, not_met, blocked or failed) and validated `evidencePaths`. Met requires nonempty evidence. Succeeded requires all node criteria met. A failure return must explain what failed rather than forge successful evidence.
- `evaluations`: evaluator-only judgments, if this node judges original goal criteria. Each names exact `criterion`, consumed producer `artifactId`, its `sha256`, result (met/not_met) and concrete `reason`. The evaluator needs its own inspected evidence and the proper producer-to-evaluator verify edge.
- `unresolvedIssues`, `risks`, `recommendedSignals`: bounded advisory string lists. These are data for the controller, never commands or permission. Escalation is a blocked result plus a clear issue/signal; the controller chooses the authorized next step.
- `authority`: exactly the task's six false denials (`maySpawnWorkers`, `mayApprove`, `mayIntegrate`, `mayUpdateControllerState`, `mayAnswerUser`, `mayIssueTerminalVerdict`).
- `localIterations` and `workUnits` when reported: within the declared packet limits. Their actual measurement is not inferred from a worker assertion.

Do not copy the illustrative template's identities, hashes or example evidence into a real invocation. Use the generated task and actual files. Hash bytes rather than a reformatted approximation. The runtime canonicalizes JSON for its own structured-record digest; artifact SHA256 is over actual file bytes.

## Settlement of an unresolved invocation

A settlement must bind `protocolVersion: 2`, the exact actual `runId`, `invocationId` and `taskPacketSha256`, plus its outcome and actual observation reference. When an execution identity is known, retain that exact identity; a record from another run or task cannot release this obligation. Worker/process stop and effect outcome are separate facts: a stopped process does not prove an issued external effect did not happen. Use only the runtime-supported outcome appropriate to the observed fact, and leave an unqueryable effect unknown.

## Ingestion and later checks

Ingestion validates packet/launch/run bindings, current contract, exact input lineage, canonical return path, unique criteria/evidence, declared output types, owned paths and hashes. The controller also reads the actual content: a syntactically valid reason or evidence path does not make a false conclusion true.

Failed/blocked outputs are retained provisionally. Late or guard-invalid outputs are quarantined and do not activate dependencies. Successful eligible artifacts have exact immutable IDs and consumed-input provenance. A return is not final acceptance; independent goal evaluation and closure still follow.

All-attempt receipts remain available for resume and terminal checks. Altered task/launch/return/evidence data is not repaired by recalculating a hash. Use diagnosis and authorized recovery/settlement. Never overwrite original failure evidence to make a later attempt look like the only run.

The three [task](../assets/templates/node-task-packet.json), [launch](../assets/templates/thread-launch-record.json) and [return](../assets/templates/node-return-packet.json) files are complete simulated shape examples. They are not complete real-host launch/return receipts: actual host tool/arguments, identities and completion references require observed host evidence, not copied simulated values.
