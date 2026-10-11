# Optional Codex advisor composition

Use this route only when the user explicitly names both Gauntlet and the advisor. Gauntlet owns state, budget, approval, integration, final answer and terminal verdict. The advisor supplies bounded work packets. It cannot become another coordinator. The Claude peer workflow remains mutually exclusive and uses the entry gate, not this protocol.

Check plan approval before composing or compiling packets. If approval is absent, stop and ask for approval of the identified plan. If the advisor capability is unavailable, say so and do not fabricate an advisor, host evidence or execution packet. Ask whether to continue with standalone Gauntlet. Standalone Gauntlet does not import this module during ordinary work and requires no installed advisor.

Local packet validation is available without an installed advisor. It checks supplied data and grants no dispatch permission. A valid static fixture is not a live host qualification.

## Commands and API

The Gauntlet CLI exposes:

```sh
python3 scripts/gauntlet.py advisor-validate --context context.json --packet composition.json
```

Exit 0 means the supplied composition packet matches the approved context. Exit 1 means invalid packet data or missing authority. Argument parsing errors exit 2. This command reads JSON and prints validation data; it does not write state or launch anything.

The standard-library module `scripts/advisor.py` exposes:

- `build_composition_packet(context)`: validate the snapshot and return a static CompositionPacket.
- `validate_composition(packet, context)`: validate bindings and return a neutral receipt with `dispatch_authorized: false`.
- `build_task_packet(context, task_id)`: require available advisor capability, accepted dependencies, remaining capacity and recorded worker creation. Return a bounded TaskPacket.
- `validate_return_packet(context, task_packet, returned, blobs, review=None)`: verify result bytes and optional independent review; return data for Gauntlet to register.
- `digest(value)`: SHA-256 of sorted compact JSON, UTF-8, without a trailing newline. Non-finite numbers are invalid.

Every invalid request raises `AdvisorError`, a `ValueError` subclass. Functions do not read or write files, change the input dictionaries, call a model, dispatch a task or construct host proof. No third-party Python package is required.

## Trusted context

Gauntlet supplies this snapshot from its canonical records under its state lock. Do not accept a worker's context as authority. Recheck the live plan, approval, remaining budget and registration eligibility before committing any result.

Required fields:

- `host`: `codex`.
- `invocations`: exactly `{"gauntlet": true, "advisor": true}`, derived from the user's explicit request.
- `run_id`: nonempty canonical run identifier.
- `plan`: approved `version`, a positive integer, and lowercase `sha256`.
- `approval`: `approved: true`, the same `run_id` and exactly the same `plan` object. Preserve additional genuine approval metadata in this object so its hash binds it too.
- `owners`: `state`, `budget`, `approval`, `integration`, `final_answer` and `terminal_verdict`, each exactly `gauntlet`.
- `perspectives`: unique names including `acceptance/scope`, `evidence/correctness` and `integration/adversarial`. Advisor review cannot replace this panel.
- `remaining`: finite nonnegative `launches`, `concurrency`, `minutes`, `cost` and `rounds`. Launches, concurrency and rounds must be integers. Use the same cost unit as the run budget. No unlimited sentinel is allowed.
- `tasks`: the approved task list described below.

A task contains `task_id`, `objective`, recorded selected `model`, `dependencies`, `write_roots`, `outputs`, `criteria`, `evidence_commands` and `limits`. Lists contain unique nonempty strings; dependencies, roots, outputs and commands may be empty. Criteria cannot be empty. Limits have the same five fields as remaining capacity and cannot exceed it. The protocol accepts any nonempty model identifier. Model and effort selection remains the host's responsibility, with the actual choice and any selection limitation recorded honestly.

Paths are normalized project-relative POSIX paths. Absolute paths, parent traversal, backslashes, `.` and writes below `.gauntlet` are refused. Outputs must fall under authorized roots. Cycles, unknown dependencies and duplicate task IDs fail. Overlapping roots are allowed only when the dependency graph serializes those tasks. The caller must additionally resolve real filesystem paths and reject symlink escapes before granting write authority; a pure packet validator cannot inspect filesystem aliases.

The CompositionPacket carries version 1, packet type `CompositionPacket`, the exact run, plan, owners, perspectives and tasks, plus `approval_sha256` and `context_sha256`. Build it with `build_composition_packet`; do not hand-copy hashes. Unknown top-level packet fields fail.

## Host records and execution packets

Only task compilation and return validation require these additional context fields:

- `advisor_available: true`, from an actual capability check.
- `task_status`: canonical task IDs mapped to statuses. The selected task must be `authorized`; each dependency must be `accepted`.
- `host_records`: records indexed by IDs supplied as a task's `worker_record` and, for an optional review, `reviewer_record`.

Each host record contains the same `run_id`, `task_id` and `plan`, its `role` of `worker` or `reviewer`, `fresh: true`, `forked: false`, `successful: true`, nonempty `host_id`, `session_id` and `request_id`, and SHA-256 values `request_sha256` and `response_sha256`. Worker `model` must equal the authorized choice. A reviewer must have `read_only: true` and a different session and creation request from the builder.

These records must come from real host creation requests and responses retained by Gauntlet. The caller verifies their provenance and bytes before supplying them. This module verifies bindings and consistency, not the authenticity of arbitrary JSON. Never manufacture records to satisfy the schema. Missing host evidence blocks execution qualification. No unsupported host adapter is implied by these field names.

The task packet binds the approval hash and copies only the selected task, recorded worker identity, run, plan and ownership. Deliver this bounded packet without the coordinator or builder's conversation history. A reviewer's prompt must not expose sealed builder provenance, builder arguments or another reviewer's verdict.

## Returns and reviews

A ReturnPacket contains:

- `packet_type: ReturnPacket`, `run_id`, `plan`, `task_id`, `task_packet_sha256`.
- `status`: `succeeded`, `blocked`, `failed` or `escalate`.
- `actual_write_paths`: all written project-relative paths, within the authorized roots.
- `artifacts` and `evidence`: lists of `{path, sha256}`. The caller supplies actual file bytes in `blobs`, indexed by those paths. Duplicate paths and byte/hash mismatches fail. Artifacts must be authorized outputs and appear in the actual write set. Successful tasks must return every expected output.
- `usage`: the five finite counters, within task limits. Gauntlet accounts for actual usage using its own monotonic ledger; a return never refunds or resets usage.
- `commands`: the exact authorized command sequence, each with integer `exit_code` and an `evidence_path` referencing hashed evidence. Successful tasks require zero exit codes. Validation does not execute those commands or prove their logs genuine.
- `criterion_to_evidence`: an object containing every criterion exactly once, each mapped to a nonempty list of verified artifact or evidence paths.

An optional ReviewPacket binds `run_id`, `plan`, `task_id`, both packet hashes, the exact artifact records and the trusted `reviewer` record. Its `packet_type` is `ReviewPacket`; its verdict is `accepted`, `revise`, `blocked` or `cannot-verify`. This verdict is a subordinate workstream assessment. It neither approves integration nor certifies the final run.

Keep the original approved task context for immutable packet validation. Before registration, Gauntlet separately checks the current canonical run and task under its lock, rejects stale approval or a superseded task, validates current budget and duplicate receipts, and records the actual result atomically. The module's receipt contains hashes, artifacts, evidence, usage and status, with `requires_gauntlet_registration: true` and `terminal_verdict: null`. No canonical files are changed by this module.

## D5 controls

Run the CLI above with each fixture's separate canonical context and packet. Valid unpinned model data exits 0. Competing ownership, stale packet plan hash, missing context approval, a missing required perspective, cyclic dependencies and unordered overlapping roots each exit 1. Rebuild packet hashes after intentionally mutating canonical context in graph tests, so those tests reach the graph check rather than merely failing a stale hash.

Also test missing explicit invocation, malformed limits, missing advisor capability at task compilation, fabricated or reused reviewer identity, altered result bytes, missing output/evidence coverage and attempted `.gauntlet` writes. Hash equality proves consistency only; live provenance and permission tests need the real host and remain separate.
