# Saved artifact contracts

JSON artifact helpers are optional when useful. The dossier checker is required for saved dossiers and optional for unsaved in-context work; record blocked/not-run honestly when it cannot run. Conversation and routing do not otherwise require JSON, a subprocess, or a persistence service. All adjacent examples are **synthetic demonstrations**, not evidence or user choices. The synthesis example starts pending with a null final record. Replace sample content deliberately; never infer real consent from an example or validator pass.

## Invocation and limits

From the skill directory:

- `python3 -I -B scripts/validate_artifact.py router FILE.json`
- `python3 -I -B scripts/validate_artifact.py synthesis FILE.json`
- `python3 -I -B scripts/validate_artifact.py register FILE.json`
- `python3 -I -B scripts/dossier_check.py FILE.md --effort standard --pace slow --json`
- Add `--as-of YYYY-MM-DD` only to dossier checking when a reproducible evidence date is needed. It defaults to today's date and is the validation clock for detecting impossible future observations, not the decision's historical evidence cutoff. Keep a historical decision cutoff in the dossier's scope; later actual retrieval/inspection dates remain later dates and must not be checked against that older cutoff. CLI effort/pace are optional consistency assertions; declared document metadata governs. Mismatch fails.

Python 3.9+; stdlib only. The scripts read the supplied file, write only their report to stdout, never alter artifacts or create caches, and make no network calls. JSON reports are emitted on successful reads and file/encoding/JSON errors. Exit 0 = structurally valid; 1 = structurally invalid; 2 = invalid invocation or unreadable/malformed JSON input. Argparse invocation errors use stderr. Dossier's retained `--json` flag is accepted; its report is always JSON. Legacy Markdown parsing errors are structural failures, exit 1.

The explicit field contracts below replace the original custom schema dialect. There is no generic schema interpreter, external schema dependency, or automatic repair. Additional synthesis/register fields are permitted for useful context; the narrow router rejects additional fields so an unvalidated second dispatch instruction cannot masquerade as routing metadata.

A pass establishes neither actual specialist loading nor evidence relevance, truth, sufficient research, meaningful distinctness, calibrated confidence, observable tests, or user authority. Review those against original sources and conversation. `execution_authorized: false` is a required boundary, never a substitute for checking the meaning of a handoff. Do not run execution merely because a saved artifact passes.

## Router JSON

Exactly five fields:

- `route`: one scalar route below
- `specialist`: the matching exact method slug
- `decision`, `rationale`: nonblank strings
- `execution_authorized`: Boolean false; numeric zero is invalid

Mappings: interview → grill-me; wayfind → decision-wayfinder; challenge → assumption-challenger; explore → multi-direction-explorer; synthesize → decision-synthesizer; register → assumption-register; prioritize → curiosity-compass; match → candidate-matcher-and-brief-builder; productize → proof-to-product-mapper.

This records one primary method only. Later branch-scoped composition is governed by the playbooks, not encoded as an extra dispatch here.

## Synthesis JSON

Required nonblank strings: `decision`, `decision_owner`, `horizon`, `stakes`, `evidence_sufficiency`, `recommendation`, `immediate_next_action`, `handoff`.

`reversibility`: reversible / partly-reversible / irreversible. `confidence`: low / medium / high. `execution_authorized`: Boolean false.

`criteria` and `change_conditions`: nonempty lists of nonblank strings. `evidence`, `counterevidence`, `risks`, `conditions`, `missing_evidence`: lists of nonblank strings; honestly empty lists are allowed subject to the state requirements below. Evidence strings identify their actual source or claim reference and support scope; the checker tests type, not provenance truth.

`options`: nonempty objects with unique nonblank `id`, and nonblank `name`, `case_for`, `case_against`. `recommended_option` is an existing option ID, or null when declining.

Exact `evidence_state` values:

- `recommend`: nonempty evidence and an existing recommended option. Sufficiency remains a substantive judgment.
- `recommend provisionally`: nonempty evidence, missing evidence and conditions; existing recommended option; reversible choice. Review conditions/change triggers must bound the provisional use.
- `decline pending evidence`: null recommended option and nonempty missing evidence. Evidence may be empty. The prose must genuinely decline; the checker cannot infer this from natural language.

`user_choice_gate` requires `state` (pending / complete), `authority` (user / delegated), `choice`, `authority_source`. Pending requires null choice and final record, and user authority; authority_source may be null. Complete requires `choice` to be an existing exact option ID and nonblank `authority_source` pointing to the actual user choice or explicit delegation. This source must be checked against the conversation; arbitrary text cannot create authority. A completed user choice may differ from the recommendation, including after a recommendation was declined for lack of evidence.

`final_decision_record` must exist and be null until complete. Once complete it has nonblank `selected_option` (exactly matching choice), `rationale`, `review_trigger`, `immediate_next_action`, `next_owner`; and string lists `accepted_risks`, `rejected_alternatives`, `unresolved_evidence`. Rejected alternatives are other existing option IDs. Lists may be empty. Scope approval and execution authorization remain separate.

## Register JSON

Nonblank `decision` and `decision_ref` identify the actual decision. `assumptions` is a nonempty array with unique nonblank IDs.

Each assumption has nonblank `statement`, `load_bearing`, `kill_condition`; `kind` factual / behavioral / capability / timing; `status` untested / supported / weakened / falsified / expired; `confidence` low / medium / high; `reversibility` reversible / partly-reversible / irreversible.

`owner` and `test` must be present and nonblank strings or explicit null. A null owner/test requires untested status, not a fabricated owner or procedure. `supporting_evidence` and `contradicting_evidence` are string lists with source/claim references and scope. Supported or high-confidence records require supporting evidence; weakened/falsified require contradicting evidence. This presence check does not validate evidentiary appropriateness or calibrate confidence.

`history` is a nonempty ordered array: each revision has `date` YYYY-MM-DD, `from_status` (null initially, then the preceding status), `to_status` (one of the statuses), nonblank `reason`, and string-list `evidence`. Dates are nondecreasing; the final status matches the current record. Supported/weakened/falsified/expired revision targets require evidence or an explicit expiry basis. Preserve old revisions when evidence changes; do not erase contradiction. Manual review must check evidence-driven transition validity, actual source dates, and the observable kill threshold.

## Markdown dossier

The original headings, source table and effort/pace operation are preserved. The helper no longer counts duplicate rows/headings as research or demands arbitrary source/finding quotas. It checks structural completeness and reports source count, explicitly declared unique origins, coverage, findings and recent publication fraction. These diagnostics do not establish sufficiency.

Required metadata: `**Effort mode:** light / standard / deep`; `**Subject pace:** fast / standard / slow` (Fast-moving / Slow-moving accepted); `**Source mode:** web / supplied / mixed`; `**Assessment:** bounded / incomplete`. All modes use the same honesty checks; light reduces inquiry scope, not verification integrity. A bounded dossier is bounded evidence for review, not certified readiness.

Required sections: `## Subject Summary`, `## Evidence Sufficiency`, `## Limitations`, `## Open Questions`, `## Dimensions Covered`, `## Findings by Dimension`, `## Expert Disagreement Map`, `## Source List`. Explicit `None.` is allowed for limitations/open questions only when truthful. Incomplete dossiers need substantive limitations, never just `None.`.

Coverage retains `**Covered:**` and `**Skipped:**` bullet lists. A skipped bullet is `- Name: substantive reason`. Names are unique case-insensitively across both lists. Each covered name matches one `### Dimension N: Name` section. Each normal covered section has at least one `#### Finding ID: Title` with nonblank `**Claim:**` and `**Sources:**` followed by bullet IDs matching the source table. Finding IDs are globally unique.

A sound-plan/no-material-finding result uses `**Disposition:** no-material-finding` with nonblank `**Rationale:**` and no invented findings. An evidence gap uses `**Disposition:** unresolved`, rationale and no findings, and requires an incomplete assessment. The default disposition is covered for compatibility. Justified skips need no dummy findings.

Disagreement map: `**State:** disagreement / consensus / unassessed`; nonblank `**Scope:**` describing actual bounded search/review; `**Sources:**` bullet IDs. Consensus is explicit bounded no-material-disagreement, not universal agreement. Unassessed requires incomplete assessment. Disagreement state includes `### Disagreement A: Topic` (letters or numeric labels accepted), nonblank `**Position 1:**`, `**Position 2:**`, and `- Advocates:` and `- Reasoning:` for each position. Mere headings are insufficient.

Source table retains `ID | Source | Tier | Date Published | Date Accessed | Notes`; add `Origin | Access | Event Date | Date Inspected` as available. Headers determine columns, so ordering is flexible. IDs and normalized exact locators are unique. The Source cell accepts a bare HTTP(S) URL, a Markdown link `[Title](https://example.org/report)`, or a meaningful supplied/local source locator. Link labels do not distinguish sources. HTTP(S) scheme/host case and fragment differences are normalized; path case, query contents and trailing slash are preserved. Unfilled `[Title]` placeholders remain invalid. IDs appear in claim references. Use a common Origin identifier for syndicated copies/common underlying evidence; hosts are not assumed independent. Missing Origin is a warning and is never counted as independent. Origin declarations require review.

Tier is A/B/C/D; D emits a warning and cannot alone substantiate a material claim without qualitative review. Access, when supplied, is read / supplied / inaccessible / metadata-only; missing access warns. Supplied-only mode must not claim a web read. Record inaccessible bodies honestly; metadata is not a body read.

Dates are YYYY-MM-DD or unknown (n/a accepted). Publication, retrieval (Date Accessed), event and local inspection dates remain separate. Invalid/future dates fail. Unknown publication dates remain in the recent-fraction denominator. Windows use calendar months (12/36/60 by pace), not 30-day approximations. Slow foundational evidence never fails merely for being old; all freshness relevance is reviewed against the claim. Unknown or unavailable data is not invented to satisfy the checker.

Report `evidence_ready` is always null for valid bounded evidence (not certified), false for incomplete/invalid. A structurally valid incomplete dossier may be handed on only as an explicit limitation or missing-input result under the method's phase gate; exit zero never silently converts it to complete evidence.

## Adaptation provenance

Coordinator checks retain the useful responsibilities of original blobs `936eba2e939c4ce379381bee472fba1ab29a2b43` and the richer personal synthesis validator `9e444f24b60b71cdbdeeaa3a6634a0e3cc67965c`. Markdown dossier checking adapts `0d39980e7c10b0f44dc4f2b270eeed2776310c10`. Intentional changes are explicit artifact-specific checks instead of a generic schema dialect; stable typed choice IDs with authority references; honest empty lists and gaps; register evidence/history; explicit Markdown exception states and provenance; and diagnostic counts/recency instead of padded quotas. This is repaired structural checking, not measured equivalence of reasoning or native-host execution.
