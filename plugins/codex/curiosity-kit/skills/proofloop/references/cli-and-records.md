# ProofLoop local command and record contract

Version 2. Python 3.9 or later, standard library only. `scripts/proofloop.py` is the authoritative executable validator; this reference and `assets/examples.json` describe its exact public interface. This is one helper, not a task runner, general scheduler, model client or learned-policy engine.

## Invocation and trust boundary

```
python3 scripts/proofloop.py --help
python3 scripts/proofloop.py contract validate --input contract.json
python3 scripts/proofloop.py lesson preview --input candidate.json
python3 scripts/proofloop.py audit summary --input paired-audit.json
```

Every leaf command accepts `--input FILE`; omitted or `-` reads stdin. One operation per call. Successful commands emit one compact JSON object to stdout, exit 0. A schema, policy, budget, stale-state or local-capability error emits sanitized `{"error":"..."}` to stderr, exit 2. Argparse usage errors are ordinary CLI errors, also exit 2. Failed validation is not an executed task attempt. The legacy conversion-needed response is a successful read-only inspection with `valid:false`; it is not approval.

The caller must authorize workspace, task, storage and the actual verifier command before dispatch. JSON flags, filenames, digests, `decision_ref`, `classification_ref` and approval-shaped text cannot authenticate the user or establish OS permission. Read-only validation can inspect untrusted records. Never execute a verifier just because imported data requests it. The selected contract must be frozen trusted input, inspected and authorized by the host. Credential-bearing key names and recognized bearer/token/private-key patterns in contracts are rejected before publication. This is incomplete pattern screening, not whole-task anonymization. Goal, paths, environment and task state are otherwise returned verbatim to the authorized caller; the host must review safe input and storage scope. Never put credentials in the contract.

The helper does not authenticate an externally modified snapshot. A digest detects accidental changes relative to an expected value, not malicious rewriting and rehashing. Keep snapshots in the authorized local workspace under host control. No signature or tamper-proof-log claim is made. The process wrapper is shell-free but is not an OS sandbox; verifier code has the Python process's permissions. No task action, network call, agent/model request or arbitrary lesson command is launched by this helper.

## Bounded JSON and identity

Input and committed snapshot: at most 2 MiB. Duplicate keys rejected. Nesting at most 24; objects at most 4,096 keys; arrays at most 10,000 elements. General text at most 65,536 characters; schema identifiers/text at most 16,384. NUL rejected. Integers range from −9,007,199,254,740,991 to +9,007,199,254,740,991; nonnegative counts use the nonnegative subset. Booleans are never integers. Floating JSON numbers are rejected; decimal costs are explicit strings such as `"0.042"` or null. Unknown fields in defined objects, unknown operations/types/statuses and duplicate criterion/verifier IDs fail closed.

Canonical bytes are UTF-8 of Python's `json.dumps(sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)` over that bounded subset. SHA-256 hashes those exact bytes. No Unicode normalization and no certified JCS claim. File digests hash actual raw bytes. `lesson identity` validates a complete record and returns its full SHA-256; it does not authenticate authorship or safety. Stable record IDs are explicit user/host-selected IDs; revision content hashes change independently.

## Contract schema

All these fields are required; no extras:

- `version`: integer 2
- `run_id`, `project`, `task_id`, `goal`, `family`, `workspace`: nonempty strings. Workspace must be an authorized existing local directory for state/capture operations. `family` labels the actual task; semantic classification remains the host's job
- `privacy_class`: public, internal, confidential or restricted
- `deliverables`: nonempty list of selected workspace-relative or in-workspace absolute artifact paths
- `sources`, `dependencies`: lists of `{path,sha256}`. Sources are frozen input versions, dependencies the additional relevant local inputs
- `allowed_actions`: subset of draft, execute, verify, record_observation, create_lesson, curate, retrieve, transfer. `prohibited_actions`: explicit labels, never overlapping allowed actions. Unknown requested actions are denied
- `learning`: none, ephemeral or workspace_ledger
- `learning_eligibility`: `{eligible:boolean,excluded_domains:[strings],classification_ref:string}`. `eligible:true` with excluded domains is contradictory. Ineligible work, any excluded domain, or a recognized high-stakes family requires none. This declaration is not a substitute for host classification
- `storage`: transient or task_local. workspace_ledger requires task_local. Other adapters unsupported
- `criteria`, `verifiers`: lists described below. At least one required criterion
- `budgets`: exact counters drafts, executions, verifiers, tool_calls, minutes, learning_records, candidates, policy_promotions. Each integer 0–100,000; minutes positive; candidates ≤1; promotions exactly 0
- `deadline_ms`: immutable positive UTC Unix milliseconds, in the future at init
- `budget_scope`: adapter_only or global. Global can be inspected but dispatch blocks because unseen host calls cannot be measured
- `verification_plan`: integer counts initial_invocations, repair_invocations, final_invocations. Sum must cover unique required E3 verifiers, including E4 dependencies, and fit verifier/tool-call budgets. Host must separately check the actual schedule and final freshness/repair allowance
- `best_effort`: actual boolean. Does not waive criteria or grant execution authority

Normalized ineligible family names: medical, legal, financial, employment, identity, security-policy and permission. Case, spaces and underscores normalize. Recognized aliases include health/healthcare/medicine, law, finance/investment, hiring/recruitment, identity-management, security, permissions/authorization. This finite list does not detect disguised high-stakes content. The host must set explicit eligibility accurately even for a family named `other`.

Default proposal, not automatically added to missing JSON: 3 drafts, 2 task executions, 2 verifier invocations, 20 tool calls, 30 minutes, 2 learning records, 1 candidate and 0 promotions. Explicit lower user caps win. Larger bounded contracts require separate acceptance before init; no live cap increase. Deadline is the lesser of the external deadline and start + minutes. Persisted start/deadline/counters survive supported resume; transient state is only as durable as the explicitly retained returned JSON. Conversation/tool retention belongs to the host and cannot be erased by this helper.

### Criteria

Every criterion: `{id,description,required:boolean,method,verifier,predicate}`.

- E2: `verifier:null,predicate:null`. A direct human/authenticated external observation is recorded as host_declared. Host must authenticate its source, relevance, currentness and exact candidate; the CLI cannot do that. E3 does not substitute for E2
- E3: verifier ID plus predicate `{exit_code:0..255,stdout_sha256?:hex}`. Exit and optional complete stdout digest must both match. Expected nonzero is a negative-control expectation, not application success. No eval strings, regex evaluation, code predicates or imported evaluator dispatch
- E4: `verifier:null`; predicate `{components:[criterion IDs],held_out:[IDs],provenance_groups:{component_id:group},independence_ref:string}`. At least two distinct E2/E3 components, no E4 recursion; nonempty held_out is a proper subset; at least two provenance groups. Every component must actually pass fresh. Host must verify declared independence and held-out/postcondition validity; inventing group labels does not prove independence

E0/E1 can be recorded as guide-only observations and E3/E4 can be supplied for audit, but imported assertions never become captured proof. Only capture creates local E3 observations. A passing average, empty required set or extra judge votes never produces verified completion.

### Verifier

Each verifier requires:

- `id`; shell-free `argv` nonempty string list with absolute executable as first member
- `executable_sha256`: actual executable hash, independently pinned
- `cwd`: selected in-workspace directory; `env`: complete string-valued environment, not inherited implicitly
- `pins`: nonempty list of `{path,sha256}` for script and relevant dependencies. Host must list every relevant dependency; a script hash does not pin imported libraries/services
- `configuration`, `test_data`: canonical SHA-256 identities of the declared config and test data, bound in the frozen contract. Relevant actual files also belong in pins/sources/dependencies
- `timeout_ms`: 1–1,800,000; `output_cap_bytes`: 1–1,048,576 across stdout and stderr together
- `containment:"process_group"`; `concurrent_mutation:"host_exclusive"`. These specify a required boundary, not a self-authenticating guarantee. The host must actually isolate inputs from concurrent writers. Other stronger containment requirements block rather than silently downgrade

The wrapper checks executable and pinned bytes before launch, sets the explicit environment/cwd, closes stdin and starts a new POSIX session/process group. It streams stdout/stderr into bounded memory; deadline or overflow terminates the owned group. Owned-group cleanup also happens on normal leader exit. It captures actual return code/signal, elapsed milliseconds, hashes of captured stdout/stderr, byte count, timeout/truncation and before/after identities. It does not retain raw output. A truncated prefix hash is labeled incomplete and cannot pass. No uncaptured stdout content or privacy review is claimed from a hash. Descendants deliberately escaping the group are outside this process-group boundary; use an actual host sandbox if such containment is required. Non-POSIX hosts block capture/ledger operations.

## Run envelopes, state and counters

State-changing commands use:

```
{"workspace":"/authorized/workspace","store":"state.json",
 "expected_generation":0,"expected_digest":null,"payload":{}}
```

Init uses generation 0/null and a nonexistent selected store. Other writes use the exact generation/digest returned by the previous committed snapshot. A transient operation omits `store` and instead supplies `state` (except init). The identical schema returns an updated complete snapshot to stdout; no local file is written. `verify` requires task_local storage and will not secretly persist a transient run. Small chat-only methods need no CLI/store at all.

Read-only report/retrieve envelopes need workspace plus store, or workspace plus state, and a payload where applicable. Expected generation/digest fields, if included on a read, are not CAS requirements; reads return the actual current identity. Caller must compare returned identity to the exact reviewed selection.

Snapshot fields: version, generation, digest, immutable contract, contract_digest, started_ms, last_ms, deadline_ms, revision, spent, operations, observations, lessons, history, derivatives. Digest excludes only its own digest field. Every commit increases generation and appends an event within the same snapshot. Failed, superseded, interrupted and pending operation history is retained; recording does not replace old evidence or refund capacity. Revision advances only when a draft is reserved.

Local commit uses an exclusive `.lock` file, expected generation/digest CAS, a mode-0600 temporary file, file fsync, same-directory atomic replace and directory fsync. Parent aliases resolve normally only if still inside the selected resolved workspace; selected leaf symlinks, a selected leaf `..` and escaping paths are rejected. Local POSIX filesystem semantics are required. An I/O error after atomic replacement may leave the new snapshot committed even if directory fsync or response delivery failed. Never assume rollback or retry blindly: reread the exact store and reconcile generation/digest and pending effects. This is one guarded snapshot, not a distributed database or guaranteed behavior on every network filesystem. The helper neither breaks orphan locks nor claims automatic recovery. An operator must reconcile pending effects and explicitly authorize recovery before changing an orphaned lock. A killed process may leave a consumed pending reservation and a lock. The helper cannot guard against hostile concurrent replacement of the workspace itself; host-exclusive local ownership remains required.

Only task-local derived view entries in the snapshot are invalidated on revision/exclusion. No arbitrary path field is followed for derivative rewrites; this version creates no separate derived files. Transfer previews are not automatically registered external copies. Before applying one, check current selected source revisions/exclusions at the host. Outside copies remain unknown; history retains prior record bytes, so exclusion is not erasure. Sensitive cleanup requires separately authorized remediation.

### `contract validate`

Input: contract. Output `{valid:true,contract_digest}`. Schema/plan check only; no executable launch and no guarantee the host authenticated the task. No writes.

### `contract init`

Input: state envelope, payload contract. Validates actual source/verifier pins, storage choice, future deadline and selected workspace. Returns first snapshot, generation 1. Task-local init writes the named store; transient init writes nothing.

### `contract check-action`

Input `{contract,action}`. Output `{eligible:true,human_authorization:"host_must_check_current_request"}` or error. Known action membership, prohibition and learning none are checked; task effects and human permission are not executed/authenticated.

### `step reserve`

Payload `{operation_id,run_id,kind,revision}`; kind draft, execute or observe. Verify reservations belong only to verify. Draft revision must be current+1; other operations use the current positive revision. Run IDs and one-use IDs must match/not recur. Frozen source/dependency/verifier pin drift, clock rollback, elapsed deadline and global budget scope block new dependent dispatch before reservation charges.

Reserve before host task dispatch. Each reserve charges one tool_calls unit and one drafts/executions counter where applicable. Observe charges a host-call reservation only. A task-action dispatch is an execution; submitting a candidate to its review gate is a draft; one verifier invocation can cover multiple criteria. Helper bookkeeping calls do not pretend to count all platform calls. External calls stay unknown. An execute at the draft cap also requires explicit best_effort and a nonempty complete fresh deterministic required gate. If that gate is absent, execution blocks.

Payload is appended as a pending operation with reservation time, charges, source/dependency identities and artifact identities. Receipt IDs are consumed even if the eventual effect is failed, interrupted or unknown.

### `step record`

Payload `{run_id,operation_id,revision,outcome,observations}`. Outcome completed, failed, interrupted or unknown. Must match one pending non-verifier reservation exactly, including the reservation's own revision. A reservation stays settleable after a later draft; its observations keep that older revision and are stale for the current candidate. Each observation is `{criterion,passed:boolean,method,decision_ref,limits:[strings]}`. Known criterion required; method E0–E4. E2 is host_declared; everything else supplied here is imported_unverified. Current artifacts/inputs are captured as identity bindings, but those hashes do not authenticate the statement. Actual E2 decision must cover those exact current bytes. Already-dispatched effects can still be settled if inputs changed or disappeared: the observation retains the declared result, adds an explicit invalidity limit and contract_pins_match:false, and cannot certify the frozen contract. Accounting remains consumed. Failed history is retained. No second charge.

### `verify`

Payload `{operation_id,run_id,revision,verifier}`. Preflight failures (unknown verifier, pin drift, a missing or out-of-workspace `cwd`) consume no verifier reservation. Valid dispatch reserves and commits before launch (one verifier and one tool-call charge), captures actual execution, then appends observations for every bound E3 criterion in one second commit. A launched/capture-failed attempt remains consumed. Crash before completion leaves pending state, not a refund. No task execution counter is charged for the verifier. Missing process-group capability, storage or identity blocks.

### `report`

Input read envelope, optional `terminal` value for explicit blocked, budget_exhausted, policy_denied, capability_missing, security_quarantine, cancelled or completed_unverified. Caller cannot request completed_verified. Without override, every required criterion must have fresh acceptable passing evidence and there must be no pending/unknown operation effects. Later failed evidence supersedes earlier pass for that criterion without deleting history. Current inputs must also match the original frozen contract pins, not merely the observed current hashes. Any changed revision, artifact or tracked input invalidates old evidence conservatively. Input drift/unavailability returns a useful unverified report instead of silently adopting new source versions. No unaffected-evidence optimization is claimed.

Output includes task_outcome, per-criterion passed/fresh/evidence/history_count, spent, unknown external_tool_calls, artifacts, deadline, pending operations, storage and separate learning_status. `ineligible_learning_disabled` is a learning status, not task failure. Host must reconcile pending task effects and verify output completeness before final release. Report itself does not close/mutate the run. Before/after equality does not detect change-and-revert races or untracked libraries/services.

## Lesson schema and lifecycle

All records require version=2, stable `id`, positive `revision`, `type`, `status`, `project`, origin `task_id`, `family`, `privacy_class`, nonempty `scope` string labels, `created_ms`, `expires_ms` (null or later timestamp), `provenance` (local/imported_quarantined), `content`, `dependencies` string list and `privacy_review` (pending/host_reviewed). Scope labels use exact overlap/subset semantics; no wildcard/path-policy language. Dependencies used for retrieval are selected current source/dependency SHA-256 identities. No high-stakes learning record is permitted. Unknown fields, including the formerly unused legacy_preview field, are rejected; legacy conversion uses only its separate command envelope.

Content fields (all nonempty strings):

- observation/experience: result, limits
- candidate_lesson/approved_advisory: trigger, method, applicability, exceptions, disconfirming_evidence, benefit_hypothesis, reuse_check, key, value
- user_preference: quote, selection_ref, key, value. Quote must be the actual scoped user quote/selection checked by host; a synthetic fixture is not real permission

Type/status pairs:

- observation and experience: recorded or locally_excluded
- candidate_lesson: candidate, rejected, expired, superseded or locally_excluded
- approved_advisory: approved_advisory, expired, superseded or locally_excluded
- user_preference: recorded, superseded or locally_excluded

An advisory has `approval:{decision_ref,source_digest}` recording the candidate revision it came from. It remains advisory, never policy. Inactive advisory revisions retain that historical binding only. Reserved policy, revocation and promoted_lesson types are rejected. Expiry is effective at read time; no background mutation is required.

### `lesson validate` and legacy conversion

Input complete record returns valid/digest. Original records with `schema_version:"1.0"` are checked for their required legacy fields, supported type, privacy class, scope/provenance shapes and timezone-aware creation timestamp, then return conversion_preview_required. Legacy candidate lifecycle text does not inherit activation.

For an actual conversion preview supply `{legacy:original_record,proposed:complete_v2_record}`. Both are validated; record ID, origin task ID and privacy class must match. Proposed revision must be 1, imported_quarantined and privacy pending, with no advisory type/approval. It returns exact proposed bytes/digest plus source digest. Host reviews semantic mapping; the CLI does not claim arbitrary legacy content was faithfully translated. Nothing is saved. Conversion is never a silent rewrite or trust upgrade.

### `lesson identity`, `redact-preview`, `conflicts`, `preview`

Identity validates a record then hashes it. Redact-preview validates, traverses content/keys, scrubs recognized secret-key fields, email addresses, common personal local paths, token forms, bearer credentials, AWS access IDs and private-key blocks. It returns safe proposed record/digest, transformation count and residual risk. Changes increase revision, reset privacy pending and remove active approval; an advisory becomes a quarantinable candidate revision. No save or erasure. Patterns are deliberately incomplete; host privacy review is mandatory before display/use.

Conflicts takes `{records:[...]}` and returns ID pairs for active, same-project overlapping scope records with identical structured key but different value. Expired/excluded records do not conflict. Semantic contradiction, authority and broad applicability still require manual review. Conflict lists return IDs, not raw content.

Preview takes one safe record with no recognized redaction needed and privacy host_reviewed; returns that exact record, safe_digest and effective status. A hash or privacy string cannot replace actual host review. Review this exact revision before making a decision.

### `lesson transition`

Stateful payload `{record,decision,action,predecessor_digest?}`. Only workspace_ledger persists lessons. none blocks every learning operation; ephemeral lessons are session-only host material, never persisted by this command. A new observation/experience/candidate/preference is one learning record; atomic snapshot updates are not additional records. At most one candidate can be created/imported within the contract.

Decision required fields: action, record_id, revision, safe_digest, project, task_id, decision_ref. It binds the exact displayed safe input record and current task/project. `decision_ref` is a pointer to host-checked permission, not authentication or future consent.

- add: new ID, revision1, current origin task, eligible scope and current budget/deadline; no advisory injection
- approve: exact current active local candidate becomes next-revision approved_advisory after structured conflict check
- reject/expire/supersede/exclude: next revision with the corresponding allowed status. All types can be excluded. No arbitrary cleanup
- revise: provide next-revision safe record plus exact predecessor_digest. Only same type, or advisory→candidate, allowed; never inherit approval. Revising an `imported_quarantined` record to `local` provenance is the only route from an import to a curatable local candidate; it needs its own exact host-reviewed decision, and `approve` then needs another. Preference scope can only narrow. Prior revision is retained, old derivative markers invalidated. Changing scope/content/dependencies requires a new exact review decision

The helper returns the committed complete snapshot. Reread/preview the new exact record before retrieval; curation is separate from retrieval permission and task-action authority.

### `lesson retrieve-check`

Read envelope payload `{record_id,decision,scope,dependencies}`. Requires a current local active advisory/preference, matching project/family, privacy reviewed, permitted subset scope, exactly matching dependency list, actual fresh frozen source pins and dependencies present in the current contract. Imported, expired, excluded, conflicting, changed or cross-project material does not pass. Decision action must be retrieve and bind the exact record/current task. Output is record/digest/generation/state_digest plus consistency_only and host_must_authenticate_current_permission. Retrieval defaults off: no command runs unless explicitly selected and actually authorized.

## Transfer

`transfer preview` input `{records:[complete records],destination_project}`. Validates records, removes approvals, neutralizes advisory→candidate, resets revision1/privacy pending, labels imported_quarantined and destination project, redacts recognized sensitive/path content, and returns `{bundle,bundle_digest,conflicts,authority}`. Bundle is `{version:2,destination_project,records}`. A neutral preview is neither external transmission nor activation. Host checks source currentness/exclusion, full privacy and destination authority.

`transfer apply` uses state envelope payload `{bundle,bundle_digest,decision_ref,destination_project}`. Requires actual local workspace_ledger destination authority at host, exact bundle identity, destination/family agreement, new distinct IDs, imported quarantine/no approval, clean recognized patterns and remaining record/candidate budgets. It appends quarantined records only. No network adapter, external write, automatic retrieval or cross-project inherited trust. Outside exports/copies remain unknown.

## Audit

`audit compare-cases` input `{cases:[{id,actual,expected}]}`. Nonempty, unique IDs, both values mandatory. Typed canonical-byte equality means true differs from 1. Output kind explicitly says supplied_comparison_not_executed_tests, with matched and all_matched. This preserves the original comparison operation without misrepresenting it as executed regressions.

`audit summary` input:

- selection: `{ids,start_ms,end_ms,family,metric:"errors"|"errors_then_latency",missingness:"indeterminate"}`; nonempty unique IDs, bounded window, eligible family
- pairs: exactly selected `{id,at_ms,family,without,with,independence,provenance}`. Provenance supplied or imported; independence is a declared explanation, not authenticated fact
- each side: `{identities,required_pass:boolean|null,errors:integer|null,latency_ms:integer|null,cost_decimal:string|null}`
- identities: exact SHA-256 fields contract, artifact_spec, verifier, configuration, test_data, environment, budget, criteria, source, work. artifact_spec means the same target specification, not identical output bytes across conditions
- controls, incidents, reviewer_disagreement: supplied annotation arrays retained without manufacturing calibration/probe evidence

Different identities are incomparable. Missing quality/errors is indeterminate. Mandatory-quality change takes priority over errors; faster failed mandatory quality cannot be helpful. Error improvement helps only when required quality passes; more errors harms. Both failed with same errors are neutral on this selected metric, never success. With metric errors, equal passing quality/errors is neutral; latency and cost can remain unknown and imply no speedup claim. With errors_then_latency, equal passing quality/errors compares latency; missing latency is indeterminate. Select the metric before inspecting outcomes. Costs are disclosed as supplied decimal strings or unknown, not used to override quality. Output includes per-pair categories, helpful/neutral/harmful/indeterminate/incomparable counts and separate selected/comparable/determinate denominators, selected metric, missing-cost and missing-latency counts, raw controls/incidents/disagreement and limits. Under20 comparable pairs is exploratory;20 alone proves nothing. Zero supplied incidents means only none in the selected supplied cases. No new runs, probes, edits or learning writes occur.

## Development verification and portability

Run `python3 -m unittest discover -s evals/proofloop -v` from the candidate root. Tests exercise public subprocess CLI calls with newly authored tiny local scripts and isolated temporary files; no donor runtime, models, accounts or private history. Runtime `audit compare-cases` is not this test suite.

POSIX capture/ledger paths are tested on the drafting cloud interpreter; Python3.9 compatibility is a syntax/library target, not evidence that every Python/OS/filesystem was executed. Native Codex/Claude activation, human-authentication judgment, actual cross-host parity, tamper resistance, adversarial escaped descendants, genuine paired learning benefit and distributed durability remain separate qualification work.
