# Read-only structural checker

Python 3.9+ and its standard library are the only prerequisites. Run from this skill's directory:

```sh
python3 scripts/check_outcome.py brief brief.md
python3 scripts/check_outcome.py review review.md
python3 scripts/check_outcome.py plan assets/plan-example.json
python3 scripts/check_outcome.py experiment assets/test-example.json
python3 scripts/check_outcome.py experiment completed.json --prior planned.json
```

The examples are filled synthetic **planned** records, not evidence of completed work. The plan yields S1 dependency-ready and S2 waiting for verified S1 output version 1. JSON is optional for useful work; do not duplicate an existing source of truth merely to run the checker. If Python/execution is unavailable, use the checks below manually and disclose that the CLI was unrun. An explicitly required CLI gate remains incomplete.

## Input and result contract

Each explicit input must be a regular UTF-8 file of at most 1,048,576 bytes. Explicit input paths may resolve through symlinks; paths recorded inside inputs are never opened. JSON duplicate keys, nonfinite values, wrong types, missing/unknown keys and duplicate IDs are schema errors. IDs are nonempty case-sensitive strings, unique within their own collection; check IDs are local to a slice. Positive integers exclude booleans. Every object uses exactly the documented keys; only plan `controls` may be omitted. Null is permitted only where stated. Nonempty strings must contain at least one non-whitespace character. Arrays may be empty unless explicitly marked nonempty.

Exit codes:
- 0: structurally consistent supplied records; a planned or proposed record can pass without being ready
- 1: well-formed records have structural findings, such as an uncovered requirement, missing canonical section or contradictory completion claim
- 2: invalid input/schema/usage, unreadable file, invalid UTF-8 or oversized input

Output is human-readable. Plan mode prints “Dependency-ready from declared state” and unmet gates by slice. Any structural finding withholds the frontier, avoiding reliance on malformed verified producers. Legitimate pending gates alone are not structural failures. Only planned/active slices can appear; already-active IDs are separately identified and are not new dispatch. Verified work is not offered again. This is not a runnable queue, authorization, source-truth check or semantic certification. No files are written, pointers followed, commands run, network accessed or work performed. Evidence, authority and location strings remain unverified claims to inspect. This is not an OS sandbox or a security boundary against hostile concurrent filesystem replacement.

## Canonical Markdown

Use ATX headings (`## Outcome`, etc.), case-insensitive exact names. Fenced code headings are ignored. Sections continue through nested headings until a same-or-higher heading. Duplicate canonical headings, missing/empty sections and marked instructional slots fail. Links and ordinary bracketed prose pass. Recognized slots are bracketed uppercase TODO/TBD/FILL/FILL IN/INSERT/REPLACE/DESCRIBE/ENTER instructions (unless part of a Markdown link), a name enclosed in double braces, and `<INSERT ...>`.

Brief sections: Outcome; Audience or user; Success evidence; Constraints; Decisions; Requirements; Risks and unknowns; Blockers; Out of scope; Next action.

Review sections: System and user; Current-state map; Diagnosis; Friction candidates; Top recommendation; Future-state allocation; Controls exceptions and recovery; Right-sized pilot; Decisions needed; Proof after pilot.

Within Right-sized pilot include nonempty labeled lines `Scope: ...`, `Owner: ...`, `Baseline: ...`, `Success signal: ...`, `Stop: ...`, `Rollback: ...`, `Review date: ...`, `Exclusions: ...`; optional bullet markers or bold labels work, but a value must follow any closing bold markup (`**Rollback:**` alone is empty). Nested ATX headings with these names and body text also work. The helper checks labels, not whether dates, owners, baselines or reasoning are credible. Unmarked vague instructions and arbitrary user formats require human review; canonical headings are not compulsory user-facing wrappers.

## Plan JSON schema

Top-level: `version` (integer 1), `brief` (object), `requirements` (nonempty array), `slices` (nonempty array), optional `controls` (object).

- brief: `source`, `revision` (nonempty strings); `status` (proposed|accepted); `approval_source` (string|null). Accepted requires an approval source. Proposed plans remain proposals and do not yield dependency-ready work.
- requirement: `id`, `text` (strings). Every listed requirement must appear in at least one slice check. These are the plan's requirements, accepted when the brief is accepted; proposed alternatives belong in decisions rather than silently expanding accepted scope.
- slice: `id`, `title`, `outcome`, `proof`, `owner`, `action_scope` (strings); `checks` (nonempty array); `dependencies`, `blockers`, `evidence` (arrays); `boundaries` (nonempty string array); `state` (planned|active|blocked|verified); `output_version` (positive integer); `asset_ids`, `approval_ids` (unique string arrays); `authority` (string|null, recorded action authority pointer, never inferred permission).
- check: `id`, `description` (strings), `requirement_ids` (nonempty unique string array referencing requirements).
- dependency: `slice` (slice ID), `output_version` (positive integer). Duplicate dependency targets and cycles are rejected. Readiness requires that target's declared verified state at exactly this version, not delivery or publication.
- blocker: `description` (string), `cleared` (boolean), `evidence` (string|null). Cleared requires recorded evidence; uncleared blocks only its slice.
- evidence: `check` (local check ID), `output_version` (positive integer), `source` (string), `result` (pass|fail). One entry per check/version. Evidence must match the current slice version. Verified requires current passing evidence for every check and all declared gates satisfied. Keep older evidence in the actual source history rather than mixing it into the current snapshot.

If present, controls has exactly `assets`, `decisions`, `approvals`, `risks`, each an array:

- asset: `id`, `title`, `owner` (strings); `version` (positive integer); `state` (planned|draft|verified|approved|delivered); `location` (string|null); `decision_ids`, `risk_ids`, `approval_ids` (unique string arrays); `production_slices`, `verification_slices` (nonempty unique slice ID arrays); `delivery_authority`, `delivery_evidence` (string|null).
- decision: `id`, `value`, `source` (strings), `status` (proposed|accepted|deferred|rejected). A verified/approved/delivered asset's governing decisions must be accepted. Preserve the accepted value separately from proposed replacements.
- risk: `id`, `description`, `owner`, `recovery` (strings).
- approval: `id`, `asset` (asset ID), `version` (positive integer), `scope`, `owner` (strings), `status` (pending|approved|rejected), `evidence` (string|null). Approved requires evidence. Historical approval records are valid for their old version. A referenced current action gate must match current asset version, its slice's exact action_scope, and an asset associated with that slice. Pending/rejected/stale gates block the affected action. Private drafting need not name publication approval.

One slice graph is the canonical dependency graph; there is no second asset dependency list or aggregate delivery summary. A slice’s asset_ids may associate any known relevant asset, including an asset awaiting human content review. Association alone does not make the slice a producer or technical verifier. Each explicit asset.production_slices or asset.verification_slices entry must reference an existing slice whose asset_ids includes that asset; the reverse is not required. A pending human-review slice can therefore reference an already verified draft without becoming its technical verification prerequisite or requiring its own approval before review can occur. Produced assets need a location. Verified/approved/delivered assets require declared verified production and verification slices at the asset's exact version. Approved/delivered additionally require at least one named current, evidenced approval, all for that asset. Delivery additionally requires a recorded action-authority source and delivery evidence; those fields are null in other states. Content approval alone grants no publication/send authority. Each actual action still needs the applicable authorization review. Slices explicitly mapped as producers/verifiers use a common output version for those assets; separate production/verification slices where versions differ. Mere asset associations do not impose version equality.

The checker rejects unknown references, cycles, uncovered requirements and inconsistent evidence/state. Active with unmet gates and blocked without any declared gate are inconsistent. Cross-asset consistency and delivery entry paths must be represented as explicit checks where needed; text cannot prove their real coverage. Undeclared dependencies, dishonest evidence, semantic scope and omitted real-world requirements remain human checks. Source changes require human selection of affected slices/assets, output-version increments and renewed checks; the helper never infers changes from file paths.

## Experiment JSON schema

Exactly these top-level fields:

- `version`: integer 1
- `test_id`, `record_id`: nonempty strings; a successor needs a different record_id
- `record_version`: positive integer, beginning at 1
- `recorded_at`: valid ISO calendar timestamp with seconds, an optional fraction of at most 6 digits and explicit timezone (`2026-10-08T12:00:00Z`)
- `predecessor`: null initially, otherwise `{record_id: string, sha256: 64 lowercase hex characters}`
- `execution_state`: planned|completed
- `precommit`: the object below
- `observations`: array of `{id, description, source}` nonempty-string objects; unique observation IDs
- `interpretation`: string|null
- `classification`: not-run|supports|weakens|inconclusive|invalid
- `invalidation_reason`: string|null
- `next_action`, `next_owner`: nonempty strings

Precommit has exactly these nonempty-string fields:
`decision`, `owner`, `riskiest_assumption`, `current_evidence`, `prediction`, `support_rule`, `weakening_rule`, `inconclusive_rule`, `invalidation_rule`, `method`, `sample`, `selection`, `baseline`, `measure`, `independent_oracle`, `time_boundary`, `cost_boundary`, `data_boundary`, `permission_boundary`, `confounders`, `proof_limits`, `raw_evidence_location`, `stop_condition`, `follow_on_condition`.

Version 1 must preserve a planned record with null predecessor. Planned means not-run, empty observations, null interpretation and null invalidation reason. Completed requires actual recorded observations, interpretation and a result classification other than not-run. Invalid additionally requires an exact reason; other results have null invalidation_reason. These are claimed observations, not independently verified truth. Human comparison against the frozen qualitative/quantitative rules determines whether a result really supports, weakens, is inconclusive or is invalid; the helper does not calculate that verdict.

Every record after version 1 requires `--prior` pointing to the explicitly supplied previous file. SHA-256 is over that file's exact UTF-8 bytes, including whitespace and final newline. The helper checks same test ID, version increment of exactly one, predecessor ID/hash, and identical complete precommit. On correction of a completed record, observations and completed state must remain exactly unchanged; invalid evidence cannot be upgraded within that lineage. Changes to method or thresholds require a new test ID and planned version 1. Do not overwrite an earlier record. Retain raw evidence separately as authorized; this tool never creates or verifies a ledger.

The supplied prior is schema/state-checked, but its own predecessor is not read or recursively validated. Passing proves only pairwise consistency. It does not establish genuine chronology, immutable storage, whole-history retention, actual permissions or rule-correct interpretation. Independently compare predecessor records and raw sources before relying on a correction.

## Development verification

From the repository root: `python3 -m unittest discover -s evals/outcome-engine -p 'test_check_outcome.py' -v`. Tests use only isolated temporary records and the public validators/real CLI. They do not contact services or change user records. This cloud result does not qualify native host installation or discovery.
