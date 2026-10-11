# Keep shared applications owned and recoverable

Load this method when an app has another consumer, meaningful stored data, consequential writes, automation, or operational dependence, or when the user asks for release, change, health, handoff, recovery, or retirement work. It extends the existing plan and implementation. It is not a second lifecycle engine, mandatory registry, or fixed interview.

Use [the host contract](../references/host-contract.md), [verification](verify.md), and [delivery](deliver.md) for actual tools, evidence and authorized effects. Keep one owner for the task. Reuse project records and controls. A sole-consumer disposable tool should stay lightweight while still respecting its real data and exposure risks.

## 1. Establish the real use and responsibility

Read the current brief, repository/runbook, accepted decisions and known users before asking questions. Determine:

- What useful outcome the app produces and which existing process/tool it replaces or supports.
- Who opens, runs, depends on or directly uses it. Reliance on an exported report counts as a second consumer.
- Responsible owner, and a backup for shared or consequential operation. Distinguish a name in a file from someone who has accepted responsibility.
- Data sources, sensitivity, storage, retention, access roles, write destinations, external dependencies, exposure and automation.
- What happens if output is wrong, service is unavailable, an action repeats, or the owner leaves.

Use an existing app identity/catalog if one is relevant. Inspect known tools before proposing another build and state the search scope; no search can prove that no suitable tool exists anywhere. Existing `.citizen` or other governance records can supply context, but must not be reset or treated as current approval by default.

Ask only the unresolved material question that changes the next step. Unknown sensitivity, ownership, access or failure consequence remains unknown. Do not convert missing facts to low risk. Missing ownership can block consequential release while leaving read-only diagnosis and a transfer plan useful.

## 2. Reassess changes before editing or provisioning

Compare the request with the accepted brief. Reassess changed consumers, data, sensitivity, writes, network destinations, authorization, autonomy, infrastructure, dependencies, irreversibility, recovery, or policy. Use the actual semantic change, not a keyword score or a "personal app" label.

For each material changed obligation, add one concrete behavior and proof to the affected implementation slice. Reuse the existing requirement/unit IDs. For example:

- A second report consumer needs the agreed meaning/date, ownership and known limitations preserved. It does not automatically need a new login system.
- Two reservation writers need one durable allocation and a defined conflict for the loser.
- A new write role needs denied-action checks that prove no unauthorized downstream effect.
- A new background consumer needs compatibility and health observations for that consumer, not just the web process.

Keep facts, risk recommendation, accepted decision and evidence distinct. Record the relevant policy version when an actual policy governs the work. A generated risk label or approval-shaped JSON cannot authorize resources, production writes or release.

## 3. Apply the relevant control purposes

These 35 source controls are audit coordinates for retained engineering purposes. Select applicability from the real task. They are not 35 mandatory artifacts or global PASS fields. For an applicable purpose, name the project check or observation that can establish it. For a non-applicable purpose, give a brief reason. If essential evidence is unavailable, block the affected claim rather than the entire unrelated task.

| Source IDs | Purpose and adequate evidence |
| --- | --- |
| CF-A01, CF-A02 | Respect approved read/write roots and unrelated files. Inspect scoped paths and rely on actual host permissions. A safe-looking path or lack of escaping symlinks does not prove operating-system confinement. |
| CF-A03, CF-A04 | Prevent secret disclosure and use supported secret references. Check likely output, logs and configuration paths; a pattern scan has stated limits. Do not copy live credentials into fixtures or reports. |
| CF-A05 | Keep network destinations within authorization. Establish actual enforced limits if isolation is claimed; a config field or source regex is not network enforcement. |
| CF-A06 | Use the project's dependency lock and reproducible dependency procedure. A lock file's presence alone does not establish that the build used it. |
| CF-A07, CF-A08 | Separate local work, production writes and elevated provisioning. Verify the real integration, current action grant and observed result. Local templates are not provisioned services. |
| CF-B09, CF-B10, CF-B11 | Keep source understandable and generated/data material appropriately stored. Judge the project's maintenance cost rather than impose universal line, byte or minification bans. |
| CF-B12, CF-B13, CF-B14 | Keep runtime data from accidentally rewriting source; make persistence, generators and migrations deliberate, scoped and recoverable. Inspect paths and actual effects. |
| CF-B15, CF-B16 | Protect atomicity and shared invariants under interruption and contention. Exercise competing actors against isolated state at the real process/storage boundary. Keywords cannot prove these properties. |
| CF-B17 | Validate real external-input boundaries with meaningful malformed, missing, oversized or adversarial cases appropriate to the application. |
| CF-B18, CF-B19 | Establish authentication and authorization for actual users, data and actions. Exercise allowed and denied paths and inspect denied effects. Single-user status does not waive exposure risk. |
| CF-B20 | Record consequential actions where auditability is needed, with useful actor/action/outcome provenance and privacy limits. A replaceable local hash chain cannot alone prove trusted authorship. |
| CF-B21 | Inspect reachable evaluation, shell-input and deserialization hazards and actual safeguards. Static scans support, but cannot certify, absence. |
| CF-B22 | Preserve compatibility and migration/backout or forward-recovery evidence for actual schema changes. A migration file's existence proves neither execution nor correct data meaning. |
| CF-C23, CF-C24 | Run applicable tests, lint and type checks with the project's real tools. Preserve failures and setup blockers. A missing tool does not pass its check. |
| CF-C25, CF-C26, CF-C27, CF-C28 | Bind secret, dependency vulnerability, lock and license checks to the actual release and applicable project policy. Name tool coverage and unavailable sources. |
| CF-C29 | Establish a reproducible build at the scope the release needs. Record artifact/runtime/dependency identity and limits from unavailable services or differing environments. |
| CF-C30, CF-C31 | Classify the actual change and obtain current authority for consequential effects. Evidence generation and release authorization remain separate. |
| CF-C32 | Prove applicable restore or forward recovery using isolated representative state. A backup existing is not a restore test. |
| CF-C33 | Keep user help, owner, limitations and required project records current. Reuse the existing documentation/catalog instead of imposing another registry. |
| CF-D34, CF-D35 | Observe health/errors/usage and ownership/review needs for the running app. Keep release identity, observation time, missing signals and responsible owner visible. No automatic scheduling or retirement follows. |

Apply PASS, FAIL, BLOCKED, UNAVAILABLE and NOT_APPLICABLE to the specific observed check, with its target and reason. Do not pass behavioral obligations because a static search found expected terminology. Do not require Python templates, a donor CLI, fixed models, another provider or any personal sibling to satisfy these purposes.

## 4. Choose compatibility and recovery deliberately

Before deleting an old interface or schema, identify all supported consumers, including old deployed workers, scheduled jobs, saved inputs, queue messages, exports, browser clients and rollback binaries. Repository symbol search alone is insufficient.

Immediate migration and deletion is suitable when the whole affected set can change together and retained data no longer needs the old interpretation. Otherwise use the smallest compatibility period needed: expand, migrate consumers/data in bounded batches, observe cutover, then contract. Preserve units and field meaning, not just names and row counts.

Before contraction, establish that supported callers use the new form, retained inputs/queued work remain readable or were safely converted, and the agreed backout version can run against the new data. If a required consumer cannot be inspected, defer contraction while completing useful compatible work within scope.

Write recovery instructions for the actual affected state:

| State | What to establish |
| --- | --- |
| Code and configuration | Which prior revision can run with current data and dependencies, and what observation proves it. |
| App data or schema | Valid restore point or forward repair, representative records/relationships and invariants after recovery. |
| Governance records | Consistent brief, decisions and audit context; preserve later valid decisions rather than blindly select the newest snapshot. |
| Accepted external effects | Stable operation identity and authoritative outcome readback before retry. Local restoration does not undo an already accepted effect. |

A snapshot of a governance JSON file does not restore a database, schema, queue or remote action. Name the irreversible boundary, recovery operator, necessary authority and verification. Test restore in isolated representative data when permitted. Do not restore production just to prove a backup, and do not erase evidence of accepted actions during rollback.

## 5. Release with exact evidence

Before release, verify the intended artifact/revision, environment, applicable control outcomes, required independent review, unresolved risks, rollback compatibility, operator and action authority. Refresh evidence whose inputs changed. A green build, risk assessment, successful merge or generated approval record does not authorize deployment.

Use the actual supported deploy route only when authorized. Record the requested release, the service/provider's accepted result, the observed deployed identity and remaining rollout stages. Partial rollout, pending queue or a successful command exit are not complete deployment proof. If only a local artifact exists, call it a local artifact.

After deployment, positively observe the intended revision in the relevant environment. Distinguish staging from production. A healthy old revision does not verify a new release. Check all material runtime consumers; a new web process and old worker can coexist. Use meaningful route/data/job behavior rather than only an HTTP status page when the obligation concerns processing or persistence.

Report deployment and sampled health separately. State the observation time and scope. If no health, usage or review-date data exists, mark it unknown. An empty warning list is not positive health evidence. Retain a first failed sample as a failed sample even when alerting policy requires repeated failures. Compare change against a baseline only after confirming its environment, revision, route set, measurement method and useful age. "No change" from a broken baseline is not healthy.

## 6. Observe operations and product signals

For a requested health check or product pulse, use authorized read-only sources. Confirm read-only database access before querying where database access is needed; analytics/tracing can suffice without it. Do not connect new accounts or persist settings as a hidden setup step.

Define the actual time window and timezone. Account for the source's known ingestion lag, disclosing a chosen buffer when exact lag is unknown. State canonical metric definitions, denominators, filters, environment and missing sources. Compare compatible windows and avoid double-counting overlapping systems. Do not invent good/bad thresholds or causal explanations from correlation.

Produce a compact readout of relevant usage, performance, errors and follow-up, with links to underlying queries or records where safe. Keep raw personal content, account identifiers and sensitive samples out of saved/shared reports unless specifically necessary and authorized. A read-only report may propose a concrete next action; it does not authorize a repair, notification, resource change or schedule.

For a named-scope report-only simplicity or feedback sweep, branch into read-only behavior before ordinary mutation setup. Inspect only the authorized sources/code. Do not write source cursors, leases, acknowledgments, labels, reactions, config, commits or plans as an incidental "probe". Keep recommendations tied to observed duplication, complexity or user feedback. A mutable feedback automation would need a separate explicit contract for sources, effects, contiguous processed frontier, concurrency and retries. It is not required by this skill.

## 7. Maintain, hand off or retire

When health fails, ownership changes, usage drops, or a review date passes, inspect the current facts before recommending action. Missing signals are unknown. An inactive app can merit a discussion about archival; inactivity does not authorize deletion or withdrawal of a dependency someone still uses.

For a transfer, establish the accepting owner, app/revision, current use, data/dependency boundaries, known failures, pending decisions, operational access needed and usable recovery instructions. Access grants are separate authorized operations. Do not transmit secrets in the handoff. Keep deployment and health evidence scoped to what was actually observed.

For a requested retirement, enumerate current consumers, exports, scheduled/background work, endpoints, credentials, retention duties and recovery needs before proposing steps. Preserve necessary data and continuity. Execute only approved shutdown/archive/deletion steps using normal recovery where available, with required confirmation for irreversible actions. Verify the actual retired components and report anything still running or depended on.

A local setup diagnosis stays read-only: inspect the selected repository's config, tools and supported capabilities, separate missing optional tools from required blockers, and report exact repair scope. Apply setup repairs only when authorized. Do not refresh examples, delete old config, install software or connect accounts merely because diagnosis found drift.

## Close the current task

Return the actual state, what changed or was observed, its evidence, material unknowns, the responsible owner and the next decision or action. A few lines in the existing plan/runbook can be enough. No extra registry, universal score, review fleet, background scheduler or standing monitoring service is implied. Keep continued observation active only when the user requested an outcome that still needs it, under the watch contract in [delivery](deliver.md).

## Write a human-run setup or cutover procedure

Use this when a requested operation contains a step only the user can perform, or when the requested deliverable is a reusable operator procedure. Read the actual product instructions and current project setup first. Do not invent screen names, permission choices or recovery commands.

1. Establish the intended final state, operator, exact environment and allowed actions. Separate preparation from the human-only action and from its independent completion check.
2. Order stages by dependency. For each stage give the actual instruction, input needed, exact destination, sensitivity, visible success signal, failure branch and whether repetition is safe. Carry existing decisions forward; ask only for the unresolved input that blocks the next stage.
3. Keep secret values out of the procedure, chat, generated files and logs. Name the approved secure entry surface. If it is unavailable, stop that stage and let the user enter the value through the real service. Never replace a secure handoff with a text box backed by a local credential file.
4. Make progress resumable using the existing task note. Record completed effects and their observed identities, not secrets. Before a retry, inspect the actual destination. A missing local checkmark does not establish that the operation failed.
5. Dry-run the instructions against an isolated sample or inspect the real available interface without committing the action. Mark unavailable screens or untested transitions precisely. The user must be able to tell preparation complete from operation complete.

A useful stage might read: "Select the approved staging database in the existing deployment console. Confirm its environment identifier matches the brief. Run the already-reviewed migration preview and retain its output. Stop if the preview names production or changes objects outside the approved set. The next stage requires the operator's migration approval."

That example is a structure, not a claim that a particular console has those controls. Replace it with verified product-specific instructions. Return the procedure, its current completed stage, known effects, exact remaining human action and recovery limits. Do not turn it into a new web application or scheduler unless the user requested that product.
