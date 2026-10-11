# Ingest and normalize

Use for a new bounded source set, explicit registration, a refresh against a previous observer snapshot, or a suspected duplicate/corrupt run. Complete the intake requested; do not create a monitoring service.

Read [ownership and inputs](../references/ownership-and-inputs.md), [source profiles](../references/source-profiles.md) and the relevant fields in [record contract](../references/record-contract.md). Use the exact CLI in [cli.md](../references/cli.md).

## 1. Establish the capture

Identify the allowed roots/files and the intended namespace/profile for each. A supplied manifest makes this repeatable; registration may preserve a local root selection for later explicitly requested reads. Do not fall back to CODEX_HOME, CLAUDE_HOME or a user's home directory merely because an original producer once used it.

Choose an output directory owned by this task and outside the source tree. Record the requested operation, time/cohort filters and previous snapshot if any. Check missing roots before interpreting discovery as an empty cohort. An intentionally empty valid export and an unavailable directory are different outcomes.

Keep the smallest complete capture. For a single snapshot, read that snapshot and its explicitly allowed closure. For legacy multi-file runs, read the named state/contract/receipt material the profile requires. Registering a Graph root does not authorize arbitrary sibling projects. Do not recursively follow evidence paths supplied in source content without a matching allowed path.

## 2. Capture and validate

Run the helper against the explicit manifest. It captures a bounded file set, validates regular paths, parses captured bytes and records content hashes. Inspect each issue rather than accepting only a successful process exit.

Reject malformed JSON, unsupported schema versions, invalid identity fields, conflicting native IDs, unsafe aliases, oversized/deep inputs and impossible measurement types. Preserve per-source IDs and reasons. A missing optional cost is an unknown field; missing required state prevents a run-state claim. A source changing during capture is a changed-source issue, not a trustworthy mixture of revisions.

State the coherence basis. A set of individually hashed legacy files is not thereby a transactional snapshot. Frozen exports or immutable closures permit stronger claims only to the extent their bindings were checked. Do not refresh or lock producer state to close a gap.

## 3. Map authoritative fields

Use the explicit producer profile's state and revision locations. Never search all nested objects for the first `status`, `success`, `approved`, `iteration` or `cost` key. A historical receipt can explain an attempt but cannot replace current whole-run state. A child node's successful verdict cannot promote the graph. A LoopKit contract's iteration policy object is not the completed iteration count.

Retain native spellings and raw labels alongside normalized meanings. Separate:

- run closure/terminality from successful process completion;
- current machine judgment from a historical receipt;
- artifact verification from human acceptance;
- approval to execute or publish from approval of the result;
- exact exhaustion codes from ordinary notes mentioning an iteration;
- native event/label timestamps from the observer's ingestion timestamp.

Fields without trustworthy evidence remain null/unknown with a reason. Reject string coercion, nonfinite or negative cost/duration values and booleans disguised as numbers. A genuine measured zero is valid only with an explicit measured basis and unit.

## 4. Resolve identity and revisions

The logical key is producer + namespace + native run ID. Revisions and attempts sit beneath that key. A copied directory with identical bound evidence remains one logical run. Changing only the label or cost produces a new evidence revision, not a new task/trial.

Use a supported producer revision order or explicit bound supersession. Do not choose a winner using mtime, directory order, ingestion order or a lexically larger filename. Equal-ID conflicting evidence without a valid order remains a conflict and is excluded from a single-current claim. Record the competing snapshot IDs so it can be resolved without losing evidence.

Preserve immutable historical revisions and update only the observer's current selection. Include authoritative newer nonterminal/corrected evidence in intake so a stale terminal success cannot remain current where the producer permits that transition. An accepted LoopKit terminal-to-active transition is unsupported and must be rejected; do not invent a recovery operation to justify it. An unsupported transition and a valid source correction are not interchangeable.

An absent previously seen source is not an implicit cancellation, deletion or new successful run. Report current intake failure/absence and distinguish any available stale historical evidence. Do not present a prior healthy snapshot as a complete current read.

## 5. Retain judgment and measurement evidence

For judgments preserve observation ID, target artifact/task, criterion, rubric/version, role, value, event time and any supersession/adjudication relationship. A raw legacy “accepted” label may be visible descriptively but does not become a calibrated pair without target/rubric binding. Use the audit method to decide eligibility, not intake-time guesswork.

For measurements preserve unit/currency, measured/estimated/unknown basis, incremental/cumulative scope, attempt/operation identities and coverage. Keep distinct charged attempts; replace revised cumulative values only for the same supported scope. Do not add cache/reasoning subsets to inclusive token totals or sum parent costs with covered child costs. Keep rejected measurements visible in issues; do not replace them with zero.

## 6. Return intake results

Return the derived snapshot location/identity and reconcile source selection to:

- newly observed logical runs and new evidence revisions;
- unchanged inputs and copied duplicates;
- current terminal and current nonterminal records;
- retained historical revisions;
- excluded conflicts, incomplete sources and corrupt/unsupported reads.

Use the helper's emitted categories; do not sum overlapping categories as if they were disjoint. Name every excluded source and next useful evidence request. If all sources fail, return error; if some fail, return partial. Empty valid inputs may be complete and empty, but not a success-rate claim.

Inspect source fingerprints and the normalizer's actual provenance for any read-only claim. Do not say “no changes” when only output rows were unchanged and a source was not readable. If the user requested only registration/intake, stop with this result. Otherwise pass the exact snapshot and question to report or audit.

## Small behavior checks for this method

These are expected semantics, not assertions that a test has run:

- Given one run copied into two selected locations, intake counts one logical run and exposes the duplicate evidence locations.
- Given a terminal run plus a later target-bound human label, intake retains history and one current run.
- Given blocked LoopKit state with a successful old receipt, the current run remains resumable/nonterminal.
- Given one corrupt source among valid sources, the result is partial with that source ID, never an unchanged healthy report.

If delegating intake, give the worker only the approved inputs, profile, output boundary and previous snapshot. Require these same results and read-only constraints; delegation is optional and does not replace the local procedure.
