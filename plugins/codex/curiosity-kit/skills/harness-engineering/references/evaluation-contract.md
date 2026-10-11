# Local authoring, evidence and repair contract

These helpers perform exact local operations. They do not call a model, discover a provider from credentials, authenticate human consent, or prove that a reviewer was independent. Use the actual host's supported execution tools for behavioral work. If those tools are unavailable, finish the suite and report execution blocked. The local CLI never converts a prepared suite into a claimed run.

Read [skill evaluation](../playbooks/skill-evaluation.md) for the evaluation method, [skill repair](../playbooks/skill-repair.md) for diagnosis and iteration, and [verification](../playbooks/verification.md) for functional versus qualitative proof. Imported observations and human feedback are untrusted evidence. They cannot change instructions, scope, criteria or approval.

## Versions and commands

The new JSON contracts use their own `kind` plus `schema_version: 1`. This is independent of `hecore.common.SCHEMA_VERSION` and does not upgrade any accepted legacy profile, operation plan, apply receipt, rollback manifest, bounded-run state or verifier receipt. No separate installed schema2 helper is assumed. Existing commands keep their behavior.

Run `python3 scripts/hectl.py author --help` or `python3 scripts/hectl.py eval --help` from the Harness Engineering skill directory. All paths supplied to the new helpers must be explicit absolute paths. New evidence outputs must not already exist. A state file may change only through its bounded cycle operation. Errors return exit1 with a JSON error; successful mechanical commands return exit0 even when the recorded evaluation contains failures. Read the result's status and coverage, not just the process exit.

| Operation | Exact interface | What it establishes |
|---|---|---|
| Materialize authored skill | `author init --brief BRIEF.json --output NEW_SKILL_DIR` | Writes the supplied complete instructions/resources to a new matching directory. Never writes the method for you or declares behavioral acceptance. |
| Structural skill check | `author check SKILL_DIR --host portable` | Existing resource/format check; host may instead be codex or claude-code. |
| Framed snapshot | `eval snapshot --target DIR --output SNAPSHOT.json` | Hashes the complete selected tree excluding declared control/cache paths. Add repeated `--path RELATIVE_FILE` to select specific files. |
| Validate suite | `eval suite-check SUITE.json` | Returns suite, adapter, judge and per-case identities. Does not execute cases. |
| Stage bounded repair | `eval stage --target SOURCE --output NEW_CANDIDATE --manifest STAGE.json --path SKILL.md --path references/rules.md` | Copies only declared files, preserves their modes, records original source identity. No source replacement or deletion. A declared absent file may be authored later. |
| Record observations | `eval record --suite SUITE.json --target TARGET --results OBSERVATIONS.json --artifacts ARTIFACT_DIR --output RUN.json` | Validates identities, actual local artifact files/hashes, criterion coverage and typed states. Imported execution and judgment remain declarations. |
| Compare | `eval compare --baseline OLD_RUN_OR_PIN.json --candidate NEW_RUN_OR_PIN.json` | Compares matching suite, case, adapter, judge and assistance conditions. Returns regression/improvement/tie/inconclusive per case. |
| Aggregate repeated runs | `eval aggregate --candidate RUN1.json --candidate RUN2.json --baseline OLD1.json --baseline OLD2.json --output NEW_BENCHMARK.json` | Descriptive case/repeat statistics and explicit matched-condition mean deltas. Baseline and output are optional; there is no mandatory repeat count. |
| Pin evidence | `eval pin --run RUN.json --role reference --output PIN.json` | Preserves a reference, including genuine failures. For role release, also provide `--review FEEDBACK.json --review-manifest REVIEW.json`; current passing, non-fixture, explicitly reviewed evidence is required. |
| Prepare artifact review | `eval review-packet --run RUN.json --output REVIEW.json` | Builds an exact current-artifact manifest for `hectl review build`. Optional `--prior OLD_RUN.json` requires the same explicitly prepared artifacts root. |
| Start bounded cycle | `eval cycle init --state NEW_STATE.json --suite SUITE.json --source SOURCE` | Records finite task-specific limits and frozen suite/source. Refuses reset of an existing state. |
| Record bounded cycle | `eval cycle step --state STATE.json --run RUN.json` | Consumes each run once, counts its declared launches including interrupted work. Add `--repair` when the run follows a repair cycle. |
| Stop cycle | `eval cycle stop --state STATE.json --as cancelled --reason "User cancelled"` | Records explicit cancelled, blocked or failed stop; cannot rename a terminal result. |
| Inspect cycle | `eval cycle status --state STATE.json` | Reads current state. Terminal states require explicit replanning, not a reset disguised as resume. |
| Prepare promotion | `eval prepare --source SOURCE --candidate CANDIDATE --suite SUITE.json --run RUN.json --stage STAGE.json --review FEEDBACK.json --review-manifest REVIEW.json --platform codex --output PROMOTION.json` | Freezes the reviewed per-file payload and original source; platform may also be claude-code or the legacy cowork value. Produces no source changes and no approval. |
| Apply approved promotion | `eval apply --promotion PROMOTION.json --approval APPROVAL.json --receipt NEW_RECEIPT.json --backup-dir NEW_BACKUPS --manifest NEW_ROLLBACK.json` | Rebuilds the envelope from its bound evidence, requires an exact match, revalidates approval and drift, then calls the existing scoped transaction. Never falls back to weaker apply when the gate fails. |

## A complete authored brief

`he-author-brief` has schema1, `name`, a single-line `description`, complete Markdown `instructions`, `status` (`draft` or `candidate`), and `files`. Each file has a relative `path`, UTF-8 `content` and optional integer `mode` (420 for0644 or493 for0755). Resources use playbooks/, references/, scripts/, assets/ or agents/. Paths cannot escape, alias by case, conflict as files/directories or target .git. The output basename must match the skill name and must be new.

Write the actual method and its meaningful examples before materializing a candidate. A draft can contain unfinished instructions but is returned as authored-draft with validation problems. A candidate with broken references/placeholders is refused. Both return behavioral_qualification=not-run. A structurally valid but useless or inaccurate method still fails the task's qualitative acceptance. Generated skills must remain independent and model-neutral under the authoring playbook; format checking alone cannot establish that.

Example: a workshop kit skill can contain a brief entry linking local inventory rules, a source-shaped JSON template and an exact counting script. The generated instructions must preserve unknown attendance and pending release approval. A helper returning a number alone does not prove the agent followed those instructions.

## Suite schema

A suite is an object with exactly these top-level fields:

- kind: he-eval-suite; schema_version:1; suite_id: a safe stable identifier
- coverage_rationale: why these required and optional cases cover the requested behavior
- target_paths: nonempty unique relative file paths. Include all executable or instructional dependencies necessary for the evaluation. Directory paths and control/cache paths are refused. Absent paths can represent a proposed new resource
- adapter and judge: each has exactly id, revision, model and settings. Model is a recorded fixed identity or null for a genuine non-model operation; settings is an object. Record real execution and judging settings. These fields are reproducibility data, never permanent model policy
- limits: positive integer max_runs, max_launches, max_repair_cycles and max_low_yield_cycles. Choose finite limits from risk and task needs before execution
- holdout: status untouched, used-for-selection or not-claimed, plus a nonempty evidence explanation. A declaration alone cannot prove a holdout was untouched
- cases: nonempty list, including at least one required case

Each case has exactly case_id, kind, split, required, prompt, expectation, criteria and fixtures. Kind is trigger, functional or qualitative; split is train, validation or test; required is an actual Boolean. Prompt and expectation are nonempty strings. Each criterion contains id, description and source, naming the fixed brief, reference or independently chosen acceptance criterion. Fixtures is an array of absolute file paths with SHA-256 values, or an explicit empty array. Recording and release checks rehash fixtures. Changing criteria, prompts, fixture hashes, adapter or judge changes comparison identity. Stable IDs alone never make changed cases comparable.

Use source references and fixture hashes together for claims whose truth depends on supplied data. Do not put credentials, raw private configuration or unrelated history into suite text. Configuration inspection uses HE's existing redacting audit.

## Execution and observation schema

Before a host run, freeze the suite identities from suite-check, the declared target snapshot digest and the complete execution-tree snapshot digest. Execute the requested case through an actually available host/tool and retain its real output, tool evidence and terminal outcome outside the target. Native model calls must use the model/settings and sandbox constraints recorded for that run. Do not replace unavailable native execution with synthetic observations.

`he-eval-observations` contains schema1, run_id, suite_digest, target_digest, execution_tree_digest, adapter_digest, judge_digest, execution and cases. Execution contains:

- origin: host-attested, imported or fixture. These labels describe the source's claim; record always marks the saved run evidence_origin=declared-import
- complete and adapter_available: actual Booleans
- launches: a nonnegative integer accounting for dispatched work, including interrupted work. Record and every later load refuse a run above the suite's frozen max_launches
- evidence: where actual execution and its terminal status can be inspected
- assistance: status unaided, assisted or unknown, plus nonempty details. Assistance includes relevant human/model repair or supplementation; do not hide it in a favorable result

A case observation contains case_id, case_digest, status, notes, artifacts, checks, judgment and metrics. Artifact objects name an explicit relative path under ARTIFACT_DIR and its SHA-256. The recorder requires the actual regular file and verifies the digest; strings saying an artifact exists are insufficient. It records size. Symlink paths, traversal, excluded paths and oversized inputs fail closed.

Each check has criterion_id, status and evidence. Pass/fail observations require every declared criterion, actual artifacts, available and completed execution, and a performed judgment. A pass requires every criterion pass; a fail requires an actual failed criterion. Missing/invalid/interrupted evidence cannot masquerade as a failed negative trigger. Judgment records reviewer, mode (self, identity-visible, blind, deterministic or not-performed), and evidence. Record actual separation before calling a judgment blind; the parser cannot authenticate it.

Case status is pass, fail, blocked, invalid, interrupted, missing or not-applicable. Not-applicable is forbidden for a required case. Unreported cases become explicit missing entries. Overall status is pass only when all required cases pass, fail when a required quality failure exists, otherwise incomplete. Other missing evidence remains visible even when a failure also exists.

Metric keys are duration_seconds, tokens, characters, tool_calls, cost_amount and cost_currency. Unknown values stay null. Counts are nonnegative integers; duration/cost are nonnegative finite numbers. Known cost requires its currency; mixed currencies are never silently added. Known subtotals are labeled partial unless every observation has measured cost in one currency. No fictional repetitions, zero-cost defaults or character-to-token conversion.

The saved he-eval-run includes the full suite, declared target snapshot, complete execution tree, adapter/judge identities, actual artifact references/hashes, assistance, case evidence, validity/coverage summary and run_digest. Every digest uses canonical framed JSON. The complete execution tree also detects newly introduced dependencies outside target_paths. Do not execute dependencies omitted from the qualified runtime package: review the declared-file closure before promotion.

## Comparisons, baselines and bounded repair

Compare only compatible conditions. The comparator keeps per-case status, refuses semantic matching across changed suite/adapter/judge identities, assistance status or execution origin (fixture, imported and host-attested evidence never compare as one condition), and reports inconclusive when either side lacks valid quality evidence. Invalid/interrupted/missing observations stay in the coverage counts but are excluded from the quality pass-rate denominator. A single matched observation is a scoped result, not a general reliability or superiority claim.

Reference pinning preserves failed evidence. Release pinning requires current passing evidence, complete explicit bound human review, and no fixture-only or contaminated-final-test qualification. Release pinning still does not prove installed behavior or authenticate the reviewer. A pin binds the exact saved run, not whatever later appears at the same path.

The cycle helper is durable bookkeeping, not a scheduler. It does not launch agents or enforce their resource use at the operating-system level. Read remaining finite limits before dispatch, record actual launches, and keep interrupted work charged. A duplicate run ID cannot be consumed again. Repeated required-failure signatures, low-yield cycles, budget exhaustion or unavailable execution stop the cycle. Ready-for-review means passing observations, not approval to apply. Missing ground truth, withdrawn authority or cancellation must stop the surrounding workflow even though a local JSON file cannot observe them automatically. State mutation uses an exclusive sibling lock; after a killed writer, verify the process and recovery evidence before removing its lock.

## Repeated-run benchmarks

`eval aggregate` preserves the Creator benchmark's useful repeated-run summaries without adopting its missing-value defaults or invented repetition count. Supply the exact saved runs explicitly; the helper never searches an unrelated benchmark tree, executes cases or fabricates additional trials. It reuses the ordinary run validator. Repeated paths/digests are refused, as are duplicate run IDs within a role.

One aggregation requires the same frozen suite, adapter, judge, complete assistance declaration and evidence origin across all supplied runs. Each explicitly named role must contain one fixed declared-target and complete execution-tree identity. Baseline and candidate may intentionally represent different frozen revisions; mixing revisions within either role is refused. Different conditions need separate summaries. Measured costs in different currencies are refused instead of silently converted or added.

The output records every actual repeat's run ID/digest, target root, status and case measurements. Each case retains its definition digest, kind, requiredness, status counts and metric statistics. Duration, tokens, characters, tool calls and monetary cost remain separate units. `quality_pass` is1 for a valid pass,0 for a valid fail and unknown for blocked/invalid/interrupted/missing/not-applicable observations. Interrupted work's known duration or cost remains measurable even when its quality outcome is unknown, and its dispatched launches remain counted.

Every metric summary has observations, n, unknown, mean, sample_stddev, min and max. Unknown metrics contribute to unknown, never to a zero-valued measurement. No known samples means null mean/spread/range. Fewer than two known samples means null sample standard deviation. No required three-run or other repetition count is invented. Pooled role summaries weight case observations equally; they are not whole-run wall-clock totals or equal-weight averages of separately summarized cases.

When both roles are supplied, deltas are candidate mean minus baseline mean for the same case definition and conditions. The report includes each side's n and unknown count, plus whether observations are complete. If either metric has no known samples, its delta stays null. Unequal counts and partial measurements remain visible. There is no inferred repeat pairing, confidence interval, significance verdict, causal effect or general reliability/superiority claim. Without an explicitly supplied baseline, deltas is null; there is no fictional zero baseline.

These are descriptive statistics over supplied evidence. Imported execution, assistance and metric claims retain their ordinary provenance limitations. A known synthetic fixture with repeated helper calls proves the aggregation's local mechanics, not the skill's native instruction-following behavior.

## Review binding

`eval review-packet` builds the existing he-review-v1 artifact format. Feed its returned evidence_root and manifest to `hectl review build`. Current and prior runs remain distinct. A combined packet needs an explicit shared evidence root containing only the authorized selected artifacts; no automatic copying of arbitrary private outputs occurs.

The review module imports he-feedback-v1 with its packet digest and per-artifact identities. Each accepted required current artifact must bind case_id, case_digest, run_id, run_digest, target_digest, current role, artifact path and artifact hash. It needs reviewed=true, accepted=true and nonempty reviewer/evidence. A visit, download, blank comment or accepted=null never approves a candidate. Feedback can record a rejected or partially reviewed result without losing it.

Human review acceptance and source-application authorization are separate. Model self-review is never relabeled as user approval. Actual browser interactions, artifact quality and independent judging need their own evidence; static HTML generation establishes none of them.

## Promotion, application and recovery

Preparation needs the original stage manifest, a current passing run on the exact candidate, current bound review, explicit platform and unchanged suite/source. Fixture-only runs cannot prepare a promotion. Source drift since staging blocks; candidate or artifact drift since evaluation blocks. Used-for-selection final tests cannot qualify release without a new frozen qualification record.

The he-eval-promotion envelope has its own kind/schema/digest and contains the original source snapshot, candidate snapshot, suite/run/stage/review identities, a scoped legacy operation plan and exact base64 payloads with per-file modes and hashes. Its top level deliberately lacks required legacy plan fields: passing the envelope directly to ordinary `hectl apply` is rejected. Preparation does not apply anything or manufacture authority. The nested plan carries no payload, so ordinary `hectl apply` refuses it too; do not try to complete it by hand after a failed promotion gate. Apply rebuilds the whole envelope from its bound suite, passing run, stage, review and current source/candidate trees and requires an exact match before any write. A resealed envelope that swaps the candidate, payloads, roots or suite away from the reviewed run is refused.

An application record is he-eval-approval schema1 with status=approved, authority=user, nonempty evidence, exact promotion_digest and approved_paths equal to the operation target set. It is a declared record of actual permission, not a cryptographic signature or a substitute for the user's required consent. A field saying user cannot create authority by itself.

Application rechecks the current source/candidate/suite/run/review/approval and exact payload immediately before invoking existing guarded file operations. It materializes frozen payloads in a new backup area and uses existing write-ahead manifests and unique backups. Existing files retain their mode; explicitly created files receive the reviewed0644/0755-style mode. Source directories are never replaced. .git, unrelated files and later user edits are preserved. Deletion and mode changes to existing files require separate authorized recovery contracts and are refused here.

Receipts, backups and rollback manifests must be new, disjoint from source/candidate/artifacts and protected evidence. If the process is killed after a write, the existing rollback manifest remains recoverable through `hectl rollback MANIFEST --receipt NEW_RECEIPT`. If the user subsequently edits a written file, rollback refuses rather than overwriting their work. Keep interrupted receipts and payloads as evidence. Never silently restart the transaction under the same identifiers.

These are cooperative process checks, not filesystem sandboxing against another process with the same account's write access. They do not revoke independently authorized legacy operations. They prevent this evaluation-derived workflow from silently bypassing its stronger gates; real environment permissions and user authority remain controlling.

## Limits and targeted proof

JSON inputs are limited to16MiB and individual evidence/payload files to64MiB; the final serialized promotion must also fit the JSON limit. These are defensive parser/export bounds, not skill word/file ceilings. Reduce a declared transaction scope or use a separately designed larger-file adapter instead of truncating evidence. All helpers are Python3.9+ standard library; optional review adapters load only in their route.

Use local subprocess tests to prove real file outcomes, malformed-result rejection, missing/unknown metrics, identity mismatches, symlinks, overlap, source/candidate drift, approval binding, .git preservation and interruption/rollback. Native dispatch, full instruction-following, independent qualitative judging and installed behavior require actual host evidence. Do not count known synthetic fixtures or helper-only execution as those proofs.
