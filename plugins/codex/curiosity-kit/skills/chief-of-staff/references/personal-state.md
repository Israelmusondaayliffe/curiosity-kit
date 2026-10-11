# Minimal personal state and trustworthy deltas

Use an existing suitable native task record first. A bounded one-off answer needs no store. When comparison or recovery needs durable evidence, use the smallest task-owned record; no home-directory database, service, global journal or automatic learning subsystem is required.

## Observation contract

The [baseline example](../assets/attention-baseline.json) shows the shape, not real observations or default responsibilities. Keep these concepts even if the host uses a different native schema:

- Schema version and unique observation identity; actual local creation/inspection time in UTC, source timezone and selected responsibility.
- Source/account identity, authorized scope, query and start/end boundary semantics. A source time, event date, evidence cutoff and local observation time are different fields.
- Per-source success/error and completeness, page/cursor coverage and unresolved gaps. `complete` means the declared query was fully observed, not all possible source data exists.
- Items with source-native identity and relevant revision, usable source link, material facts, source timestamp if actually supplied, actual observed time, classification and uncertainty. Namespace IDs by source/account. Equal text is not equal identity.
- Comparable prior observation identity and exact source/file revision used. A latest filename is not enough to select among several responsibilities or concurrent runs.

Use explicit null/unknown when a source field was not supplied. Preserve the original timestamp string where relevant; normalize timezone-aware parsed values for comparisons without inventing precision. Reject malformed/naive timestamps when a real instant is required. If the apparent observation lies in the future, reconcile the clock/source issue before asserting freshness. A fresh local reread of old content does not make the underlying event new.

For a stable material fingerprint, serialize only the fields that affect meaning, with stable key order and normalized unordered lists. Exclude local read times and transient display formatting. Keep original source facts accessible; a digest helps compare, it does not replace provenance or prove authenticity. A content change may be immaterial, while urgency can change with time independently of content.

## Save and read back without losing evidence

Pick an authorized task-owned directory. Reject a destination that resolves outside that scope or through an unapproved symlink. Legitimate OS aliases must be handled by the actual platform's resolved owned root, not by assuming all `/tmp` or `/var` paths behave alike.

Prefer a new immutable observation file with a unique identity, created exclusively/no-clobber. If a file with that identity exists, compare it; do not overwrite different evidence. Write valid UTF-8 in the declared format, then reopen, parse and compare actual saved bytes/data and identity. Record the actual saved path and hash if useful. A planned path, tool call request or supplied `persisted_at` field is not successful readback.

For an existing mutable native record, use its real revision/CAS mechanism if available. Otherwise establish one writer and check current bytes/revision before an authorized atomic replacement, retaining the previous version. Do not claim this creates a transactional lock across processes or services. If concurrent ownership is uncertain, stop the conflicting update or use a new immutable version rather than overwrite it. Reject truncation, invalid schema or size limits before replacing an existing record.

A write failure leaves the prior good observation available. Keep failed partial output separate from the canonical record and do not point future comparisons at it. Never overwrite a newer user edit with the last in-memory copy.

## Commitment and notification state are different

A commitment record needs outcome, owner, authoritative source, real deadline or unknown, current status, completion/progress evidence, remaining next action and any separately agreed reminder. All paths that mark it complete require an actual completion observation or attributed user report. A generic update route cannot bypass that invariant.

A notification record refers to the exact content/version and intended destination. Its states are prepared, pending, uncertain, delivered, declined or cancelled as applicable. Delivered requires an actual supported send/readback receipt or a directly observed successful in-conversation response, not just a brief file or digest. Keep uncertainty if a timeout follows dispatch. Source baseline advancement must not mark an unsent notification delivered or suppress its later settlement.

Store only minimal relevant private facts. Do not copy full inboxes, personal plans, credentials, tokens, account exports or private transcripts into a baseline or public evidence. A worker receives only its task-relevant projection; a public artifact uses only content authorized for that audience. Privacy filters alone cannot prove no sensitive information remains.

## Compare, migrate or repair a baseline

Before comparison, check schema, responsibility, source/account and query/window compatibility. Report the mismatch and compare only genuinely shared scope; do not call unlike queries a complete delta. Preserve missing-page or connector-failure uncertainty. Use explicit source resolution/tombstone or user confirmation for completion; simple absence is insufficient.

Baseline health checks are read-only. They must not initialize storage, migrate schema or rewrite a status field. Report exact invalid fields, missing source references, stale observations and absent readback proof. Existing valid information stays intact.

If a migration is requested, keep the original. Convert a legacy Markdown sidecar or old schema into a new versioned record, carrying original identity/unknowns and pointing to the old source. Do not invent missing timestamps, reconstruct missing historical proof or silently normalize away ambiguous fields. Validate actual saved readback and a subsequent comparable delta before considering the new format sufficient. Removal of old evidence is a separate authorized cleanup.

A requested restore first previews the exact source backup and current target/version. Validate both without modifying either. Simulate ordered changes on a separate owned scratch copy so later changes see earlier ones. If the target changed, rebase or ask; do not force it. Apply only the authorized scoped restoration and verify readback, preserving the failed version separately. Local file restoration cannot undo an external message or account action.
