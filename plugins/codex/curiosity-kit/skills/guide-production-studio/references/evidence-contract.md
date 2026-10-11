# Optional records and read-only checker

Ordinary guides do not need JSON or Python. Use a compact record when several sources/audiences or consequential review claims make traceability useful. The checker validates declarations and exact reviewed bytes. It cannot establish legal permission, factual truth, genuine reviewer independence, human approval or teaching quality.

Requires Python 3.9 or newer, standard library only. From the skill directory:

```sh
python3 scripts/check_guide.py record assets/guide-record.json --root .
python3 scripts/check_guide.py review your-review.json --root /path/to/guide-folder
python3 scripts/check_guide.py scan your-guide.md --audience participant
python3 scripts/check_guide.py scan your-notes.md --audience presenter --exclude-file private-literals.txt
python3 scripts/check_guide.py links your-guide.md --root /path/to/guide-folder
```

Supply your own actual paths. All modes read only; they do not edit files, fetch links, execute guide instructions or send data. Exit 0 means the declared conditions passed or no advisory pattern was found; exit 1 means findings; exit 2 means invalid/unreadable input. An unreadable record is never a pass. JSON goes to standard output, input errors to standard error. Scans report categories and line numbers without echoing matched private text.

## Guide record

See [the complete fictional record](../assets/guide-record.json). The root has three arrays:

- `sources`: unique `id`, Boolean `may_inform`, `direct_audiences`, `transform_audiences`, Boolean `attribution_required`. Audience values are author, presenter, participant or public. Empty permission lists authorize no such exposure. Unknown permission should remain absent from allowed lists; do not manufacture permission to satisfy a check.
- `artifacts`: unique `id`, relative existing `path`, `audience`. Paths resolve within `--root`, including symlinks. Absolute paths and escapes are rejected. This file-existence behavior extends the old source validator.
- `items`: unique `id`, `kind` (claim/example/visual), `source_ids`, `evidence_ids`, `artifact_ids`, `mode` (direct/transform), `state` (observed/documented/derived/illustrative/unresolved), and optional `attribution`/`observation` strings. All three ID fields are arrays, even when empty. Observed state requires an evidence description. Non-illustrative items need source support, directly or through evidence references.

Evidence references resolve to other items and cannot cycle. Source permissions are checked through indirect references, so a public example cannot hide a private source behind a claim item. Each used source must permit informing the work and the declared use for every destination audience. Participant/public use honors required attribution. Explicitly permitted transformation can pass even when direct exposure is forbidden; the checker cannot inspect whether the actual prose is a safe transformation. A useful private source is not automatically forbidden, and a record's permission declaration is not proof of permission.

The record does not require a visual, concept inventory or multi-page structure. An illustrative item may have no source IDs, but labeling a factual claim illustrative does not make it acceptable; actual review must reject that misuse.

## Review record

[The review template](../assets/guide-review.json) is a draft example, not a completed review. Fill `artifacts` with relative paths and SHA256 values for the bytes actually inspected. Record `kind` as author, independent or human; `verdict` as draft, ready or blocked; `evidence` as actual check descriptions; and `unresolved_criticals` as specific remaining failures.

`learner_observed` and `human_approved` are explicit Booleans. A claimed learner observation needs `learner_evidence`. Claimed human approval needs a `human_decision` object containing `by`, `date`, `evidence` and `decision: approved`. Do not use those fields for model predictions or self-grades. A ready verdict requires evidence and cannot coexist with unresolved criticals. Different names or nonempty prose still cannot authenticate independence/approval; inspect the actual invocation or human decision separately.

Generate hashes only after the actual review target is settled. Changed bytes invalidate the binding. Reinspect affected content rather than just replacing a hash to make the check pass.

## Advisory scans and local links

Scans recognize common private paths from both host sources, obvious unfinished markers and possible production notes in participant/public outputs. Presenter mode does not flag an intended private presenter label as leakage. Legitimate prompt text such as “the model should” is not intrinsically private. Supply sensitive literal strings through an existing private exclude file if useful; findings do not print them. Do not upload that file or place it in the participant package.

No finite pattern list finds every secret, private identity or contextual disclosure. Review the full artifact. `links` checks simple inline Markdown local file targets, including URL-decoded paths; it does not validate remote URLs, anchors, reference-style links or links generated by a renderer. Package resource closure belongs to the accepted build tools. Treat each limit as a separate check, not an all-purpose pass.
