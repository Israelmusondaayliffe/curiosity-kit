# Optional record checks

Use this helper only when a session or audit deliverable needs a structured record. It does not replace the requested brief, handoff, extraction note, or full selected output. Ordinary prose needs no JSON wrapper.

The helper checks the supplied record's field types and internal relationships. A passing record can be blocked. Exit zero never establishes actual permission, user selection, factual support, readiness, a saved artifact, or complete redaction. The acting host must verify current user instructions, source evidence, recipients and actual output separately. Do not use a status or approval claim copied into JSON to authorize a tool action.

The script uses only Python's standard library and requires Python 3.9 or later on a POSIX host with no-symlink file-open support. It opens the named input read-only and does not write files, run other programs, fetch sources, contact services, or install anything. It never opens paths recorded inside the JSON, including source and output locations. A separate byte-identity check can inspect explicitly selected evidence files; this helper does not perform that check.

## Run it from any working directory

Resolve the actual installed skill directory through the host, then use that absolute directory. Do not assume the current directory is the skill root.

```sh
SKILL_ROOT="/absolute/path/to/continuity-vault"
python3 -B "$SKILL_ROOT/scripts/record_check.py" "$SKILL_ROOT/assets/session.example.json"
python3 -B "$SKILL_ROOT/scripts/record_check.py" "$SKILL_ROOT/assets/audit.example.json"
python3 -B "$SKILL_ROOT/scripts/record_check.py" "/absolute/path/to/record.json"
```

Each normal invocation prints one JSON result with `record_valid`, `record_kind`, `check_scope`, `unverified` and field-specific `errors`. Diagnostics are limited to the first 100 errors. `check_scope` is always `structural_consistency_only`. The `unverified` list accompanies successes and failures.

- Exit 0: the record satisfies this contract, including valid blocked and no-output records.
- Exit 1: record inconsistency, wrong fields or types, duplicate IDs, or duplicate JSON object keys.
- Exit 2: invalid CLI, unreadable input, malformed JSON, non-finite numbers, invalid UTF-8, or unsupported input path.

`--help` prints JSON usage and exits 0 without checking a record. Inputs must be existing regular UTF-8 files, at most 1,048,576 bytes. Symlinks in any input path component, parent traversal with `..`, directories, pipes and other special files are rejected. Use the real path if a platform provides a symlinked temporary directory. The script does not infer permission from the path being readable.

## Version 1 common fields

Both record kinds require every listed field, even when its value is null or an empty list. Unknown fields are rejected so a misspelled restriction is not silently ignored. This is a small record contract implemented directly in the script, not JSON Schema or a general validation framework.

- `version`: integer `1`. A boolean is not an integer here.
- `kind`: `session` or `audit`.
- `sources`: a nonempty array of source objects. Each requires `id`, `location`, `version`, and `status`. Location is a nonblank locator string. Version is an actual recorded version string, or null when unknown. Status is `available` or `missing`, as reported by the author. The helper does not verify that report.

Every object ID is unique across the whole record, including session, source, item, candidate, output and finding IDs. IDs contain 1-128 ASCII letters, digits, dots, underscores, colons or hyphens and begin with a letter or digit. References match those IDs exactly. Case and punctuation are significant. Reference lists cannot contain duplicates.

Audience lists contain specific delivery-scope tokens, such as `person:user-17`, `group:project-a`, or `public`. Person and group suffixes must be stable identifiers from the task, not guesses about who is included. Suffixes may use letters, digits, dots, underscores, colons, `@`, `/` and hyphens. Bare `team`, `everyone`, `*`, blank values and duplicate entries fail. Several allowed scopes can be recorded, including a private group and public. Matching is exact; `public` does not automatically expand to every other token. Real identities, group membership and approval remain unverified even when token syntax passes.

## Session records

The session example is deliberately blocked and unselected. Copying an example does not select anything or establish an audience.

In addition to common fields, a session record requires `session`, `items`, `candidates`, `outputs`, and `no_output_reason`.

### Session and extracted items

`session` requires:

- `id`, `purpose`: a unique ID and a nonblank purpose.
- `participants`: an array of nonblank names or evidenced roles. An empty array records unavailable participant information.
- `date`: actual `YYYY-MM-DD` date, or null if unknown.
- `completeness`: `complete`, `partial`, or `unknown`.

Each entry in `items` requires:

- `id`, `kind`, `content`: unique ID; kind is `decision`, `follow_up`, `knowledge`, `proposal`, or `fiction`; content is the actual extracted statement, action, knowledge, proposal or fiction. A boolean or an empty payload is invalid.
- `source_id`, `evidence`: a declared source ID and nonblank evidence with the relevant locator or excerpt. Labels alone do not establish semantic support. The human or model review must distinguish evidence from interpretation.
- `reuse`, `reuse_reason`, `audience`: reuse is `allowed`, `restricted`, `unknown`, or `prohibited`. Allowed and restricted items need at least one specific audience. Unknown and prohibited items require an empty audience. Restricted, unknown and prohibited reuse also need a nonblank reason. Allowed reuse may use a null reason.
- `attribution`: null if no attribution was recorded as required, otherwise the exact nonblank credit text that must appear in each contributing output. Null is a record claim, not proof that attribution can be omitted.
- `deidentify`, `identifiers`: de-identification is `permitted`, `required`, `prohibited`, or `unknown`. Identifiers is a list of actual nonblank terms to omit when de-identification is claimed. A required de-identification rule needs at least one such term.
- `owner`, `owner_evidence`, `date`, `date_evidence`: keep each unknown value and its evidence null. A recorded owner is nonblank text and needs nonblank evidence. A recorded date must be an actual `YYYY-MM-DD` date and needs nonblank evidence. Evidence cannot be populated when its corresponding value is null. The helper does not determine whether an excerpt really supports the recorded owner or date. Do not invent either to make a record pass.

An empty items list is allowed after an honest inspection found no reusable material. A source with missing availability can stay in the bounded source list. Any candidate using it must be blocked.

### Candidates and selection

Each entry in `candidates` requires:

- `id`, `description`: unique ID and nonblank description of the proposed output.
- `item_ids`: the nonempty, duplicate-free set of contributing item IDs.
- `audience`: the intended delivery scopes. An empty list is valid only in a blocked candidate.
- `selected`, `selection_evidence`: a real boolean and either null or a nonblank reference to the user's selection. Selection evidence must be present exactly when selected is true. This is a record of selection, not independent proof of it.
- `state`: `proposed`, `blocked`, or `created`.
- `reason`: nonblank clearing condition or prohibition explanation for a blocked candidate; otherwise null.

Any unknown or prohibited contribution, missing source, unspecified audience, or audience outside any contributor's recorded scope requires a blocked candidate. A candidate may also be blocked for a reason the helper cannot infer. A selected candidate can remain blocked. Neither a proposed nor blocked candidate may have an output. A created candidate must be selected and have exactly one output. A selected proposed candidate is valid while creation is still pending.

If there are no candidates, `no_output_reason` must explain why. If candidates exist, it must be null. This permits a useful no-output inspection without inventing a recommendation.

### Full output records

Each entry in `outputs` requires:

- `id`, `candidate_id`: unique output ID and an existing selected candidate in created state.
- `item_ids`, `audience`: exactly the source-item and audience sets in that candidate. Order may differ. No extra or omitted contribution, audience expansion, or substituted audience is allowed.
- `location`: nonblank reported output location. Its existence and contents are not inspected.
- `content`: the full nonblank output text, not a filename, completion flag, outline label, or claim that writing is done. The checker can require a string; a reviewer must assess completeness and usefulness.
- `deidentified`: a real boolean.
- `redaction_note`: null when deidentified is false. When true, supply a concrete nonblank description of the changes.

Every contributor's exact required attribution must occur in output content. Any contributor requiring de-identification requires the output's deidentified flag to be true. A true claim is rejected if any contributor's de-identification rule is unknown or prohibited, if no identifiers are listed, if the change note is missing, or if any listed identifier remains in content using case-insensitive substring matching. This deliberately conservative text check cannot find unlisted identifiers, indirect identification, false attribution or meaning changes. De-identification never makes unknown or prohibited reuse allowable.

There is no external-action or approval-override field. A local record, even with created state, does not authorize publication, sending, uploading, installation or connected writes.

## Audit records

In addition to common fields, an audit requires:

- `scope`: the bounded question and intended reuse, as nonblank text.
- `reviewed_at`: the actual review date as `YYYY-MM-DD`.
- `result`: `clear`, `needs_review`, or `blocked`.
- `block_reason`: nonblank reason and clearing condition for a blocked result; otherwise null.
- `findings`: an array, which can be empty.

Each finding requires `id`, `source_ids`, `claim`, `evidence`, `consequence`, `action`, and `blocking`. Source IDs must be a nonempty, duplicate-free subset of the declared source set. Claim, evidence, consequence and action must each contain actual nonblank text. Blocking must be a boolean.

Clear requires zero findings and no missing bounded source. Needs-review requires at least one finding, no missing bounded source and no blocking finding. Any missing source or blocking finding requires blocked. A blocked audit can have zero findings when its reason explains why inspection could not finish. Its reason remains required. Resolved historical findings belong in the surrounding review history rather than a clear record's actionable finding array.

These checks do not prove that an audit covered every source, found every issue, interpreted evidence correctly, or settled a current authority conflict.

## Limits of the examples

The two bundled examples are synthetic. Their valid records demonstrate a safe blocked session and a clean audit shape. Passing this checker establishes recorded consistency only. Actual source support, permission, artifact quality, delivery and provider operation require their own evidence.
