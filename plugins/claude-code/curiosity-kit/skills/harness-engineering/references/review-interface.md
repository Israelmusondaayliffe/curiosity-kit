# Offline human review

Use this method when a person needs to edit trigger cases, inspect tuning history, or judge current/prior artifacts and benchmark evidence. These are three separate jobs. `hectl review` prepares a local HTML file and validates explicitly exported JSON. It does not run a model, serve a port, save browser state automatically, modify a skill, select a winning description, or grant application authority.

Read [evaluation-contract.md](evaluation-contract.md) for the evaluation record and its validity requirements. A prepared review is not an executed evaluation. A person's declared review is not authenticated consent or a release receipt.

## Prepare the selected evidence

1. Choose one mode: `trigger`, `history`, or `artifacts`.
2. Create a manifest with `schema: "he-review-v1"`, `mode`, an optional `title` and optional `notes`. The schemas below list supported fields. Unknown top-level fields fail validation.
3. For artifact review, declare only the files this person is authorized to see. Use one explicit evidence directory, contained relative POSIX paths, and actual SHA-256 content digests. Nested paths are supported. Include relevant final replies, supporting notes and grading evidence; do not silently substitute a summary for an essential artifact.
4. Put the HTML output outside the evidence directory, in an existing directory. Outputs must be new paths. Keep originals unchanged.
5. Build and open the HTML in a supported browser. Inspect the actual rendered view before sending it to a reviewer.

```sh
python scripts/hectl.py review build --manifest /scratch/review-manifest.json --evidence-root /scratch/evidence --output /scratch/review.html
```

The local command needs Python 3.9 or newer. Core generation, validation and import use only the standard library. The optional XLSX preview imports an already installed `openpyxl` only while reading an XLSX artifact. It never installs a parser. Missing or failing optional parsers leave the rest of review usable and show an explicit limitation.

## Trigger-query editing

```json
{
  "schema": "he-review-v1",
  "mode": "trigger",
  "title": "Workshop summary trigger cases",
  "queries": [
    {"case_id": "positive-1", "query": "Summarize the workshop decisions", "should_trigger": true, "partition": "development"},
    {"case_id": "negative-1", "query": "Translate this sentence", "should_trigger": false, "partition": "validation"}
  ]
}
```

Each case has a stable `case_id`, nonempty `query`, boolean `should_trigger`, and optional `partition`, one of `development`, `validation`, `final`. Omitted partition means development. IDs use letters, numbers, underscores, periods and hyphens, begin with a letter or number, and contain at most 128 characters. There must be 1 to 1,000 cases. Query text is limited to 20,000 characters.

The page edits text, labels, partitions and IDs, adds a query and focuses that new query's text, and removes a selected query. Export refuses duplicate IDs and identical query text with conflicting labels or partitions. Identical text with the same label and partition can remain as distinct identified cases; do not count such repetition as independent coverage. The UI does not change the evaluator's suite or classify cases automatically. Exported edits need a new validated suite revision before execution. Final cases used in tuning cannot still support an untouched-holdout claim.

## Tuning-history inspection

```json
{
  "schema": "he-review-v1",
  "mode": "history",
  "title": "Description tuning history",
  "history": [{
    "iteration_id": "attempt-1",
    "description": "Summarize workshop decisions and next actions.",
    "partition": "development",
    "status": "evaluated",
    "metrics": {"passed_cases": 2, "total_cases": 3, "tokens": null},
    "selection_rationale": "Retained for another development test; final cases are untouched."
  }]
}
```

History is read-only. Each entry requires unique `iteration_id` and `description`; `partition`, `status`, `metrics`, and `selection_rationale` are optional. An empty history remains empty, with no fabricated winner. Include the actual denominators, criterion version, split use, failures and selection rationale inside metrics or explanatory notes. Numbers are presented as supplied; the viewer does not recalculate a score or guess preferred direction. Unknown values remain null. A characters count is never relabeled tokens.

## Current/prior artifacts and benchmarks

```json
{
  "schema": "he-review-v1",
  "mode": "artifacts",
  "title": "Workshop artifact review",
  "runs": [{
    "run_id": "candidate-run-1",
    "case_id": "workshop-summary",
    "case_digest": "<actual 64-character lowercase SHA-256>",
    "run_digest": "<actual run-record digest>",
    "target_digest": "<actual target snapshot digest>",
    "role": "current",
    "status": "pass",
    "label": "Candidate, first recorded run",
    "notes": "Declared imported execution, not authenticated by the viewer.",
    "metrics": {"duration_seconds": 2.1, "tokens": null, "characters": 872},
    "grading": {"criterion": "Names the next action", "evidence": "Action appears in the closing paragraph"},
    "artifacts": [{"path": "current/nested/summary.md", "sha256": "<actual file digest>"}]
  }],
  "benchmark": {"paired_cases": 1, "notes": "Descriptive evidence only; no superiority claim."}
}
```

Replace example digest placeholders before building. `runs` contains 1 to 1,000 entries; each entry requires the exact identity fields shown and an explicit artifact list. `role` is `current` or `prior`. The same `run_id` may span distinct `case_id` values; the pair must be unique. Different case-definition digests under one displayed case ID trigger a visible unmatched-comparison warning. File identity includes the full nested relative path, so path-separator normalization cannot merge two files. Each artifact has exactly `path` and `sha256`; strip optional evaluator `size` metadata when constructing this manifest.

`grading`, `metrics`, `benchmark` hold JSON presentation data. Include exact observed values and units rather than inferred aggregate zeros. Up to 200 declared artifacts per run are supported. Missing or oversized artifacts show errors for current and prior outputs alike; neither is quietly omitted. A run with no artifacts explicitly remains unqualified. Next/previous buttons, the case selector and Alt+Left/Alt+Right navigate cases without changing review state.

To adapt a `he-eval-run`, map every case to one review run row: copy the record's `run_id` and `run_digest`, use the case's `case_id` and `case_digest`, copy `target_snapshot.digest` as `target_digest`, copy its actual status/metrics/notes/judgment, and declare its artifacts. Explicitly assign current/prior roles. When two run records use different evidence roots, prepare an authorized isolated evidence copy with distinct relative paths and unchanged content digests; do not quietly scan or export either entire tree.

## Preview boundaries

- UTF-8 text, Markdown, JSON, code, HTML and SVG render as text nodes. HTML and SVG never execute in the page. A source preview does not establish visual correctness of an HTML/SVG artifact.
- Recognized PNG/JPEG/GIF/WebP signatures get raster previews. Decode failures produce an explicit incomplete-preview message. A valid signature is not proof that the image decodes; inspect the rendered image.
- PDF is download-only, with an explicit visual-page-review gap. Open it in a trusted viewer. The review page embeds no PDF plugin, frame, or active object.
- XLSX uses optional installed `openpyxl` with read-only loading, no external-link preservation, and formulas displayed as text. Every worksheet, including hidden sheets, gets a named cell preview when limits permit. This is not formula recalculation, chart rendering, formatting fidelity or print-layout review. Tasks requiring those need a trusted workbook application before acceptance.
- XLS, ODS and other binary formats are download-only. A download link is useful access, not evidence that required inspection occurred.

XLSX preview limits are 5,000 ZIP members, 32 MiB declared expanded content, 50 sheets, 500 rows and 100 columns per sheet, 50,000 cells total and 2 MiB displayed cell text. XML entity/DOCTYPE declarations and non-supported null-byte encodings refuse preview. A cap, corrupt file or absent parser produces a visible partial/download-only state. Required all-sheet/cell coverage cannot be claimed from a truncated preview. No macros or formulas execute.

Files are capped at 8 MiB each and 24 MiB of included artifact bytes per packet. Manifests and imported feedback are capped at 4 MiB. Symlinks, traversal and evidence/output overlap are refused. A symlinked ancestor is also refused, including macOS `/tmp` and `/var`; pass canonical paths such as `/private/tmp/...`. CLI errors print `{"error": ...}` and exit 1. Oversized artifact records stay visible as errors. The exported HTML contains the selected artifact contents and comments; treat it as sensitive as those inputs. File selection is the caller's authorization boundary, not an automatic redaction guarantee.

## Explicit feedback and JSON roundtrip

Each artifact has an independent reviewed checkbox, decision selector, reviewer identity, evidence/inspection notes and additional comment. Visits and blank comments do not accept anything. Accept/reject requires the checkbox plus nonempty reviewer and evidence fields. Clearing reviewed clears its decision. The page does not imply that every case was reviewed merely because some rows are complete.

Click **Export review JSON**. The browser requests a download; the page cannot confirm that the browser actually saved it. Check the file. Edits remain only in the tab until export. A warning appears for changes, and the browser is asked to warn before unloading unsaved changes. Some browsers may suppress that prompt, so export remains the reliable persistence step. Reopening the original HTML starts from its embedded state, not from a previous tab's changes. There is no hidden browser storage or server autosave.

Click **Import review JSON** to restore exported state for this exact packet. Import validates identity and fields before replacing state. Replacing unsaved edits asks explicitly. Invalid JSON, oversized files, wrong-packet data and stale case/run/target/artifact bindings fail visibly without changing existing edits. Repeated export does not invent new review timestamps or completion states.

The feedback format is:

```json
{
  "schema": "he-feedback-v1",
  "packet_digest": "<canonical manifest digest>",
  "queries": null,
  "reviews": {
    "<canonical identity digest>": {
      "identity": {
        "case_id": "workshop-summary",
        "case_digest": "<digest>",
        "run_id": "candidate-run-1",
        "run_digest": "<digest>",
        "target_digest": "<digest>",
        "role": "current",
        "artifact_path": "current/nested/summary.md",
        "artifact_sha256": "<digest>"
      },
      "reviewed": true,
      "accepted": true,
      "reviewer": "Reviewer name or stable identity",
      "evidence": "Inspected the saved action list against the source notes.",
      "comment": ""
    }
  }
}
```

Digests use SHA-256 over UTF-8 JSON with sorted object keys, compact separators, literal Unicode and no non-finite numbers. The identity digest binds all identity fields. `queries` holds the edited query array only for trigger mode and is null otherwise. `accepted` is null until an explicit decision; false means reject. Missing reviews remain missing. Reviewer declarations do not authenticate who clicked or convey application permission.

Validate and persist exported feedback through the CLI:

```sh
python scripts/hectl.py review import --manifest /scratch/review-manifest.json --feedback /scratch/downloaded-feedback.json --output /scratch/validated-feedback.json
python scripts/hectl.py review build --manifest /scratch/review-manifest.json --evidence-root /scratch/evidence --feedback /scratch/validated-feedback.json --output /scratch/review-with-feedback.html
```

Import writes a new file atomically and refuses replacement of an existing destination. A changed manifest gets a different packet digest. Keep older review files with their original manifest; do not relabel them current. Evaluation preparation must independently verify the run, target and artifact digests, sufficient required artifact coverage and actual user authorization. A syntactically valid exported acceptance cannot make invalid, stale, missing or unreviewed evidence pass.

## Completion and failure

The review task is complete when the intended mode opens correctly, required artifacts are readable or explicitly blocked, edits/decisions survive an export/import roundtrip, and the person receives the honest coverage/limitations. For required visual or all-sheet work, unsupported or incomplete preview blocks that aspect until a trusted viewer is used. Keep such evidence and the user's decision distinct from the page's structural checks.

Test the actual browser: ordinary and hostile text, keyboard navigation, new-row focus, current/prior separation, edits across case changes, explicit no-decision/reject/accept, wrong-packet import, repeated export, unsaved reload and exact JSON roundtrip. Python generation and schema tests alone do not establish browser behavior.
