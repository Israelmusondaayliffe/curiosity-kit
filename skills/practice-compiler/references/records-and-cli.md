# Records and CLI

This is the implemented contract for `scripts/practice_compiler.py`. It is a standalone Python 3.9+ standard-library program. It needs filesystem access to the explicitly selected exports and system IANA timezone data. It does not call models, APIs, a browser, other skills, a subprocess, or a history collector. Do not install anything to satisfy a missing prerequisite without the separate authority that installation requires. If Python or timezone data is unavailable, use the manual playbook and label the CLI checks unrun.

The program compiles evidence into review candidates, stores substantive reviewed proposals, records declared decisions and emits a checked handoff. It never edits a proposed destination. Hashes establish record consistency, not the identity or consent of a human.

## Ordinary commands

Run from any directory. Relative paths inside a manifest resolve beside that manifest. Other CLI paths resolve against the working directory. Replace `SCRIPT` below with the skill's `scripts/practice_compiler.py` path. `DIGEST` means the exact `casebook_digest` returned by the preceding successful mutation or report.

```sh
python3 SCRIPT scan --manifest selected.json
python3 SCRIPT scan --manifest selected.json --stage --casebook casebook.json --expected-digest absent
python3 SCRIPT scan --manifest next-window.json --stage --retain-other-sources --casebook casebook.json --expected-digest DIGEST
python3 SCRIPT report --manifest selected.json --casebook casebook.json --scope current
python3 SCRIPT report --manifest selected.json --casebook casebook.json --scope cumulative
python3 SCRIPT revise --manifest selected.json --casebook casebook.json --record reviewed.json --expected-digest DIGEST
python3 SCRIPT decide --manifest selected.json --casebook casebook.json --record decision.json --expected-digest DIGEST
python3 SCRIPT handoff --manifest selected.json --casebook casebook.json --proposal-id csv-check-investigation --expected-digest DIGEST
```

`scan` previews on stdout unless `--stage` is present. Preview rejects `--casebook` and `--expected-digest` and creates no files, directories, locks, cache or decisions. Staging requires both state arguments. The destination parent directory must already exist. `absent` is valid only for an absent casebook; existing state requires its exact SHA-256 file digest. A stale digest blocks the mutation.

All commands return JSON on stdout. `--help` returns ordinary help text. `report` and `handoff` are read-only. `revise` does not record a decision. `decide` does not emit a handoff or apply a change. A separately requested output file can receive stdout through ordinary shell redirection; it is a derived snapshot, never another writable approval authority.

Exit codes:

- `0`: the operation completed, or help was shown
- `2`: blocked by invalid arguments, malformed control/state records, privacy policy mismatch, missing authority data, stale evidence, changed destination, writer conflict or I/O failure
- `3`: scan returned partial source or dated coverage. Its counters, diagnostics and any admitted events remain useful. With `--stage`, it may have atomically invalidated old evidence and retained the good sources
- `130`: an ordinary keyboard interruption was handled

Errors use bounded codes and never echo raw arguments, source lines, exception text or private paths. Common codes include `restricted_source`, `source_unavailable`, `symlink_target_not_declared`, `file_budget_exceeded`, `line_budget_exceeded`, `event_budget_exceeded`, `duplicate_json_key`, `cross_source_id_conflict`, `invalid_json_or_encoding`, `unsupported_scalar_record`, `unsupported_codex_event`, `unsupported_claude_record`, `casebook_digest_conflict`, `writer_locked`, `casebook_privacy_policy_mismatch`, `missing_evidence_member`, `unlocated_repair_forbidden`, `decision_revision_mismatch`, `latest_revision_not_approved`, `source_snapshots_changed`, `destination_snapshot_changed`, `context_artifact_snapshot_changed` and `handoff_member_scope_mismatch`. Follow the failing source alias back to the private manifest. Do not guess another source location.

## Selected-source manifest

The manifest is a private, caller-selected mapping from safe aliases to exact files. It is never copied into a handoff. This complete example uses the first two October days in New York:

```json
{
  "schema_version": 1,
  "corpus_id": "csv-review",
  "access": {"basis": "user-selected-export", "reference": "user-request-2026-10-08"},
  "window": {"start": "2026-10-01", "end": "2026-10-02", "timezone": "America/New_York"},
  "included_classes": ["user-session", "neutral-export"],
  "budgets": {"max_files": 8, "max_file_bytes": 1048576, "max_total_bytes": 4194304, "max_line_bytes": 65536, "max_events": 5000},
  "sources": [
    {"alias": "codex-a", "path": "codex-a.jsonl", "adapter": "codex", "source_class": "user-session", "lineage_id": "origin-a", "session_id": "session-a", "mirrors": []},
    {"alias": "neutral-a", "path": "neutral-a.json", "adapter": "neutral", "source_class": "neutral-export", "lineage_id": "copy-a", "session_id": "copy-session", "mirrors": [{"event_id": "copy-a1", "source_alias": "codex-a", "target_event_id": "a1"}]}
  ],
  "destinations": [{"alias": "delivery-rule", "path": "delivery.md"}],
  "private_terms": ["fictional-private-canary"]
}
```

Required fields are shown above. `destinations` and `private_terms` may be omitted. Each source requires `alias`, `path`, `adapter`, `source_class`, `lineage_id` and `session_id`. Only `mirrors` and `resolved_path` are optional source fields. Each destination requires `alias` and `path`, with optional `resolved_path`. Unknown fields in these control records are rejected. `access.reference` is a bounded reference to actual user authorization established by the agent; typing one does not grant access or prove consent.

Aliases, corpus IDs, proposal IDs and lineage IDs match `[a-z][a-z0-9-]{0,63}`. Use neutral labels, not a person's name or a secret. Source classes are `user-session`, `neutral-export`, `automation`, `subagent` and `synthetic`. The class is explicitly declared, never inferred from a temporary path. A source outside `included_classes` is counted as an excluded file and is not opened. `session_id` supplies a fallback for exports without a native session ID. A native session identifier takes precedence when its supported record supplies one. `lineage_id` describes the declared underlying origin; do not invent independent origins for copied evidence.

All budget values are positive integers. Hard ceilings are 256 selected source/destination files, 16 MiB per file, 64 MiB combined source/destination bytes, 1 MiB per physical line and 50,000 decoded events. The caller must choose limits within those ceilings. Manifest/review/decision control files have an independent 2 MiB bound. A canonical casebook has a 32 MiB bound. File count includes excluded source entries and destination entries. Byte totals count opened files. Event budget counts decoded events before time filtering. The line limit covers physical lines, including a compact neutral JSON object's line.

Only regular readable files are accepted. No glob, directory scan, recursive traversal, `~` expansion or environment home fallback exists. Paths inside `.codex`, `.claude`, `.ssh`, `.aws` or `.gnupg` are refused before and after resolution. This is additional defense, not a substitute for platform permissions. An explicitly selected file symlink requires the exact absolute resolved file target in its `resolved_path` field. That target's directory may be written through a normal parent alias such as macOS `/tmp`; its final component must be the file itself, not another link. The output discloses `resolved_target_declared: true`, while the private manifest contains the actual target. Normal parent-directory aliases, including macOS `/tmp`, resolve to one canonical target without requiring a false file-symlink declaration. A denied target stays denied.

Each opened source is bounded, captured once and checked for changes to its inode, size, modification time and change time before, during and after capture. SHA-256 and parsing consume those same captured bytes. A changed file is not accepted. These checks do not lock external writers or prove the source was truthful.

## Dates and coverage

`window.start` and `window.end` are inclusive local dates in the explicit IANA timezone. The example becomes `[2026-10-01T04:00:00Z, 2026-10-03T04:00:00Z)`. Filtering uses each event's timestamp, never session start, filename or filesystem modification time. Explicit offsets retain their instants. Naive timestamps use the declared zone only when the local wall time is unambiguous and exists. Missing, date-only, malformed, DST-fold and nonexistent timestamps are excluded and counted in `unknown_time`.

`complete` says selected included files were captured and decoded without source/mirror failures. `coverage_complete` additionally requires no unknown event times. Either failure produces exit `3`. Valid dated members can still stage when some events have unknown times; the gap remains visible. A parsing failure rejects that source's entire batch, including a valid prefix. An unavailable selected destination retains its own alias/code diagnostic and partial status while good source events remain available. Staging that partial result invalidates dependent destination/context claims instead of freezing an old successful target snapshot. A later successful rescan reads it afresh; there is no cursor to advance past a failure. Handoff requires complete source and dated coverage.

`outside_window`, `unknown_time`, `quoted_or_empty`, `excluded_class`, `linked_duplicates`, `same_identity_duplicates`, `repeated_native_ids`, `ignored_records`, `excluded_injected_context`, `unknown_results`, `included_events`, `selected_bytes` and `declared_sessions` are separate counters. `excluded_class` counts selected files, not unread events. `same_identity_duplicates` counts agreeing copies across selected exports; `repeated_native_ids` counts repeated IDs within one source. `excluded_injected_context` counts native records whose user text has a known injected host wrapper. `ignored_records` includes records that produce no admitted items, including such wrappers; these counters must not be summed as disjoint totals. None proves that all host history types were understood.

## Supported export layouts

Adapters are explicit. There is no generic recursive traversal or auto-detection.

Before native Codex/Claude user text is attributed to a human, the parser excludes known host-injected record prefixes: `# AGENTS.md instructions`, `<recommended_plugins>`, `<environment_context>`, `<app-context>`, `<in-app-browser-context`, `<skill>`, `<codex_internal_context`, `# Applications mentioned by the user:`, `<command-name>`, `<command-message>`, `<local-command-stdout`, `<system-reminder>`, `<task-notification` and `Caveat: The messages below were generated`. Leading whitespace/case does not bypass the check. In Claude exports, a slash-command record keeps its nonempty `<command-args>` text as the person's message and drops the rest of the wrapper; an empty-argument command record stays excluded. Otherwise an injected text block suppresses user-message text in that native record; actual tool-result blocks remain typed tool evidence. Separate legitimate direct user records remain available. This is a known-wrapper boundary, not a claim to detect every possible injection.

### Codex, `adapter: "codex"`

JSONL objects support:

- `type: "session_meta"`, with `payload.id` as session identity. Its timestamp does not limit later events
- `type: "response_item"`, with `payload.type: "message"`, role `user` or `assistant`, and `content` entries of `input_text` or `output_text` with a string `text`
- `type: "event_msg"`, with `payload.type: "user_message"` or `"agent_message"`, and string `payload.message`
- `response_item` `function_call` or `custom_tool_call`, with `name`, `call_id` and JSON object/string `arguments`, or `input`
- `response_item` `function_call_output` or `custom_tool_call_output`, with `call_id` and `output`

Top-level `timestamp` is the event timestamp. Top-level `id`, then `payload.id`, provides the event ID. Without one, identity derives from event content, session and timestamp, never row position. `turn_context`, `reasoning`, `compaction`, token counts and the listed lifecycle/command telemetry types are ignored. Other event types block that source with an explicit unsupported-type code. Duplicated user messages across different native record IDs remain separate observations unless linked explicitly; possible overlap is shown in candidate grouping.

### Claude, `adapter: "claude"`

JSONL `type: "user"` and `"assistant"` records read top-level `uuid`, `sessionId` and `timestamp`, then `message.role` and `message.content`. Content may be a string or a list of typed blocks:

- `text` with string `text` becomes message evidence
- Assistant `tool_use` with `id`, `name` and object `input` becomes an actual tool-call record
- User `tool_result` with `tool_use_id`, `content` and optional Boolean `is_error` becomes tool evidence. It never becomes a user instruction
- `thinking`, `redacted_thinking`, image and document blocks are not read as text evidence

`isMeta` records are always excluded. `isSidechain` is excluded unless the manifest explicitly selects a `subagent` source and includes that class. User-role text in selected subagent/automation exports is retained with `delegated`/`automated` actor provenance and cannot generate human-feedback or user-method signals. Actual tool calls/results remain usable. Known `summary`, `system`, `progress`, `file-history-snapshot` and `queue-operation` records are ignored. Other record/block types are unsupported. For multiple emitted blocks, native IDs append `:0`, `:1` and so on to the UUID; indices count emitted supported blocks. The manifest's mirror IDs use those exact suffixes.

### Neutral events, `adapter: "neutral"`

A JSON object uses integer `schema_version: 1` and an `events` list. Each event requires `id`, `session_id`, `timestamp`, `actor` and `kind`. Optional fields are `text`, `tool`, `command`, `call_id` and `outcome`.

```json
{"schema_version":1,"events":[{"id":"copy-a1","session_id":"copy-session","timestamp":"2026-10-01T04:05:00Z","actor":"user","kind":"message","text":"Please verify the final CSV."}]}
```

Actors are `user`, `assistant` and `tool`. Kinds are `message`, `tool_call` and `tool_result`. A tool call requires actor `assistant` and a nonempty `call_id`; a result requires actor `tool` and the corresponding `call_id`. Outcomes are `success`, `failure` and `unknown`. A supplied event's actor/outcome is provenance supplied by the exporter, not a verified account or authenticated execution.

### Original Design neutral exports, `adapter: "design"`

Original exported files enter directly, without rewriting their fingerprint or pretending a summary is user speech:

```json
{"schema_version":"1.0","records":[{"source_type":"design-neutral-export","fingerprint":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","created_at":"2026-10-01T12:00:00Z","project_id":"project-bbbbbbbbbbbbbbbbbbbb","signal_class":"user-method","summary":"Inspect the saved export before delivery.","impact":"Catch a malformed final file.","method":"Check the file, then inspect the result."}]}
```

Each record requires exactly the shown fields except optional `impact` and `method`. The fingerprint is 64 lowercase hex characters; project identity is `project-` plus 20 lowercase hex characters. Forbidden raw fields such as `exact_quote`, `path`, `source_path` and `event_path`, and other unknown fields, are rejected. `feedback` and `friction` map to `recurring-feedback`; `repair` maps to `repeated-repair`; `missed-tool`, `cost-decision` and `user-method` keep their classes.

Records become `actor: "reported"`, `kind: "reported_summary"` evidence with `provenance: "supplied-summary-not-direct-observation"`. The original fingerprint is retained as `origin_fingerprint`; the project becomes a hashed declared-project context. Identical fingerprint duplicates are idempotent. Conflicting reuse of a native identity is rejected. Summary text cannot create an executed-command signal. These are declared labels, not newly established diagnoses.

### Commands and grouping

Only actual matched native/neutral call records for `Bash`, `bash`, `shell`, `exec_command`, `shell_command`, `functions.exec_command` or `functions.shell` generate command summaries. The compiler retains only the first executable's safe basename. It discards arguments and tool result bodies. Shell wrappers therefore remain `bash`, `python3` or the observed wrapper; the compiler does not infer nested commands.

A matched result with an explicit integer `exit_code`/`returncode`, the known `Process exited with code N` text, or Claude `is_error: false/true` establishes a reported success/failure. Otherwise outcome stays `unknown`. A call only inherits a matched result inside the selected window at or after the call time. Orphan results are counted and cannot create command-failure evidence without an observed command call. Quoted commands never become execution. Contradictory outcomes remain unknown.

The nine signal classes are retained. User-text regexes propose repeated task, feedback, follow-up, repair, missed-tool, cost and user-method topics. Actual command calls/results supply the command classes. Grouping uses exact normalized text or command name; it deliberately does not claim semantic paraphrase detection. Each candidate includes member IDs, event count, declared session/context counts, success count, possible unlinked overlaps, unreviewed confidence and a next-review instruction. Simultaneous matching text from different sources is retained but flagged as possible overlap and cannot support recurrence by itself. Project contexts do not inflate the declared-session count. Different wording, exceptions and opposing statements remain inspectable separate records. All cause, applicability and owner judgments belong to review.

## Identity, mirrors and the redacted record boundary

An event ID hashes adapter, declared origin lineage, native session identity and native event identity. Adapter-session and underlying context identities are separate hashes. Source aliases plus line number, native-ID hash, source-byte SHA-256 and event-record digest preserve local verification. IDs do not expose native strings. Equal basenames do not collapse sources. Across the selected exports, a repeated underlying native identity is checked before any dictionary merge. Contradictory observations invalidate every involved source with `cross_source_id_conflict`; source order cannot choose a winning version. Agreeing copies count once, use a deterministic source-alias primary locator and preserve the other source/native-ID/hash locators in `mirrors` with `relationship: "same-native-identity"`. Their snapshots are therefore required for freshness checks too.

A mirror entry links one source-native event ID to a selected source alias and native event ID. It may reference a later source in the manifest. The linked events must both be admitted and agree on actor, kind, redacted text, command summary and outcome. Chains resolve to one event. Missing targets, conflicts or cycles block affected source evidence; uncertain similarity is never silently deduplicated. Changing declared mirror mappings changes the source contract digest and invalidates old affected cumulative evidence.

The record boundary contains only fixed schema fields and redacted/opaque values. No native raw JSON, reasoning, tool arguments, result bodies, exact source paths, filenames or free-form metadata are persisted. Redaction covers explicit private terms, matched case-insensitively, common secret assignments/key formats, URLs, email addresses, absolute paths, identifier/phone-like patterns and long opaque tokens. Notes, review text, decision reasons and rendered handoffs use that boundary too. Fixed keys, generated opaque IDs and digests remain structurally intact. `private_terms` must be strings of 4 to 1,000 characters, at most 128 terms, and cannot be typed record IDs or full digests.

The casebook stores only a digest of the private-term list. Every command that reads or mutates it requires the matching selected manifest so later review/decision notes cannot bypass that policy. Changing the corpus privacy policy is blocked. Use a newly selected casebook for a changed policy and retire the old state under appropriate deletion authority; no immutable archive is required. Do not hand-edit the canonical state to make its hashes pass. If a suspected secret has already been stored, stop sharing that state and arrange a privacy correction before reuse. Automated redaction is not a guarantee that unknown secrets or sensitive meaning were removed. Review the whole intended output before separately authorized sharing.

## One scoped casebook

The schema contains `schema_version`, `corpus_id`, a fixed contract with timezone/privacy digest, `generation`, current source/destination snapshots, active redacted `events`, historical authorized `windows`, `last_scan`, reviewed `proposals` and declared `decisions`.

By default, each staged manifest replaces the selected source membership for that corpus. Classes are per-scan selections, not permanent corpus settings. Previously selected but now omitted, unavailable, excluded or changed sources lose their active evidence. Unchanged source snapshots retain previously admitted dated events for explicit cumulative use. Scanning the same evidence again does not add occurrences. Source path changes with identical content and declared identity do not by themselves invent a new observation. No cursor or parallel registry exists.

For an explicitly requested cumulative continuation, add stage-only `--retain-other-sources`. Previously admitted omitted or excluded sources and destinations then remain stored evidence, labelled `stored-not-rechecked` in the cumulative report. They do not enter the current result. Selected missing or changed sources still invalidate their affected members. This permits a later neutral-only window in the same casebook without claiming to have rechecked unrelated past sources. Omit the flag to replace membership and retire omitted active evidence.

`report --scope current` includes only the last scan's event IDs, candidates from those members, and reviewed proposals whose entire support/counterevidence set lies inside that current set. It omits previous-revision decisions. `--scope cumulative` explicitly includes active evidence from the authorized window union, current proposal revisions and all declared decision history. Reports describe stored snapshots and cannot establish current external authority. Historical windows describe where evidence was previously admitted, not a guarantee that all historical evidence remains active after source changes.

Mutations create an exclusive sibling `casebook.json.lock`, read/verify the expected digest under that lock, validate the updated state, write a private temporary file in the same directory, flush and fsync it, then atomically replace the canonical file. The program attempts directory fsync where supported. All cooperating writers use the same canonical lock path. It checks the prior digest again before replace. A conflict fails instead of overwriting the winning writer. A normal failure removes its own temporary file and lock. A hard kill may leave a lock or unused temporary file; verify no writer is running before an authorized operator removes that abandoned transient file. The old canonical file or complete replacement remains the sole authority. Filesystem/power-loss guarantees still depend on the platform. Noncooperating tools must not edit this casebook concurrently.

## Reviewed proposal import

`revise` requires the complete following structure. The filled, runnable fictional example is in `assets/records.json`.

- `proposal_id`: stable safe slug, separate from revision identity
- `observed_problem`: sourced observation, with uncertainty stated
- `evidence_ids`: one or more distinct active event IDs
- `diagnosis`: `category`, `confidence`, `rationale`. Categories are `missing-method`, `missed-trigger`, `ignored-guidance`, `broken-tool`, `unresolved`, `verified-resolution`; confidence is `low`, `medium` or `high`
- `counterevidence`: `event_ids` and substantive `analysis`. Member IDs must also exist in active evidence; an empty list does not justify skipping analysis
- `destination`: one of the two exact structures below
- Optional `context_artifacts`: up to 64 unique `{target_alias, sha256, rationale}` entries for inspected supporting artifacts. The importer normalizes omission to an empty list
- `proposed_change`: `kind` of `investigation`, `repair` or `method`, plus exact `text`
- `applicability`, `exceptions`, `privacy_notes`: nonempty review text
- `acceptance_checks`: 2 to 20 nonempty independently useful check descriptions
- `review`: `reviewer_reference` and `reviewed_at` with an explicit UTC offset or `Z`

A located destination is `{status:"located",owner_class:"instructions",target_alias:"delivery-rule",sha256:"THE_SCANNED_DIGEST",rationale:"What was inspected and why it is the target."}`. Owner classes are `instructions`, `skill`, `tooling`, `workflow`, `documentation` and `unresolved`. The target alias/digest must match a complete selected destination snapshot.

An unresolved destination is `{status:"unresolved",owner_class:"unresolved",investigator:"workflow-reviewer",reason:"The source of the bad invocation has not been located."}`. It is valid substantive work. It requires an investigation proposal and a named investigator. The compiler does not fabricate a repair target just to satisfy a schema.

Use `context_artifacts` for current guidance, help, contracts or other supporting files even when the bad caller or repair target remains unresolved. Each alias/digest must match a complete selected destination snapshot. These references are part of the proposal revision, become stale if the recorded snapshot changes and must be freshly matched during handoff. A repair's target and its supporting artifacts are separate references. The filled example binds both the adequate delivery rule and current checker help without pretending either is the unlocated bad caller.

The importer validates fields, member existence, selected destination/supporting snapshots and safe strings. It cannot judge whether the diagnosis is true or acceptance checks are good. Text fields are nonempty and generally at most 6,000 characters; snippets are at most 600. Reviewer/actor references have smaller bounds. Source locators remain available for the agent's real review.

Each successful import appends revision number `1`, `2` and so on, with the sanitized complete proposal, evidence digest and immutable revision digest. Even identical re-imported prose creates a new review revision. It does not inherit approval. The latest decision attached to an earlier revision remains historical.

## Declared decision record

A decision file has exactly `proposal_id`, `revision_digest`, `decision`, `actor_reference`, `decision_reference`, `decided_at`, `scope` and `reason`. `decision` is `approve`, `reject`, `defer`, `revoke` or `supersede`. `scope` must be `handoff-only`. The timestamp requires an explicit offset or `Z`. Use the exact latest revision digest returned by `revise`; a stale revision cannot receive a new decision.

The agent must establish the actual user decision and reference before invoking this command. A quoted transcript approval, neutral source record or fabricated actor reference is not consent. The script validates declared data only. Approval requires currently active matching evidence and the stored destination snapshot. Later rescan changes make that approval stale. Decisions form a sequence/hash chain and reference real stored revisions. Reports, revision imports and handoffs reject broken record digests or identities. This catches structural tampering; an attacker who rewrites data and recomputes all hashes has not been cryptographically authenticated by any of these checks.

Report states are `reviewed-awaiting-decision`, `approval-recorded-currentness-unchecked`, `rejected`, `deferred`, `revoked`, `superseded` or `stale-evidence-or-destination`. None means a change was applied or proved useful.

## Checked handoff

`handoff` verifies the expected current casebook digest, latest proposal revision, latest exact approval, active member evidence and current snapshots for every supporting, counterevidence and mirror source by reading the exact selected manifest again. Unrelated historical sources need not be reselected. It also rechecks a located destination's current bytes and every `context_artifacts` snapshot, including those supporting an unresolved investigation. Every supporting and counterevidence member must be admitted by the handoff manifest's current date/class scope and match the stored event-record digest. Matching whole-file hashes cannot bypass an empty or narrower event scope; use a manifest window that actually includes all members, rather than silently borrowing cumulative evidence. Incomplete sources, unknown event times, changed membership/bytes, stale proposals, newer reject/defer/revoke/supersede decisions and changed destinations block it. It reads the casebook again after source checks to catch an intervening state mutation.

A successful output includes `scope` with corpus/scope identity, the exact date interval, selected source classes, declared budgets, completeness flags, coverage counters and interpretation/privacy limits. It has `status: "handoff-ready"`, the exact revision and latest declared decision, redacted member evidence, casebook digest, receiver requirements and explicit false values for `consent_authenticated`, `destination_changed`, `applied` and `outcome_proved`. Its authority is `investigation-only` for unresolved ownership, otherwise `proposal-handoff-only`. It is a point-in-time snapshot. The receiver must recheck the current canonical state and real user decision before acting; a saved earlier handoff cannot outlive revocation. Any destination edits, installation, external sharing or additional inspection still need their own authority.

## Regression command and limits

```sh
python3 evals/practice-compiler/test_practice_compiler.py
```

The tests invoke only the public CLI against synthetic temporary files. They exercise actual native-shaped and neutral exports, source-boundary/time controls, all nine classes, original Design intake, positive command outcomes, redaction, cumulative scope, reviewed revisions, approval/revocation, stale snapshots, contention and failed atomic writes. POSIX file-size-limit failure injection is skipped on other platforms. Cloud execution is not Codex or Claude native-host qualification, a Python 3.9 interpreter run, macOS execution, a privacy proof, authenticated consent or evidence of a real learned improvement.
