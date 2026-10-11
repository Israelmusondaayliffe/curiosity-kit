# Offline evaluation artifact contract

`../scripts/lab.py` is a Python 3.9+ standard-library artifact processor. It never calls a model, opens a URL, follows an artifact path embedded in JSON, executes supplied code, installs software, or runs a provider campaign. The execute playbook owns actual authorized host invocation. This helper can prepare packets and process records collected by that host.

## Public commands

Run from the skill directory; choose a new temporary output directory before trying the synthetic example:

```sh
python3 scripts/lab.py check-plan assets/plan.example.json
python3 scripts/lab.py freeze assets/plan.example.json --out /tmp/mpl-demo-frozen.json
python3 scripts/lab.py prepare /tmp/mpl-demo-frozen.json --out /tmp/mpl-demo-packets.json
python3 scripts/lab.py normalize /tmp/mpl-demo-frozen.json assets/raw.example.json --out /tmp/mpl-demo-normalized.json
python3 scripts/lab.py verify /tmp/mpl-demo-frozen.json /tmp/mpl-demo-normalized.json
python3 scripts/lab.py decide /tmp/mpl-demo-frozen.json /tmp/mpl-demo-normalized.json --out /tmp/mpl-demo-decision.json
```

The example is synthetic. The expected decision is `outcome: no_decision`, `hypothetical_rule_outcome: select:B`, with a `synthetic_evidence` blocker. No model quality was measured. Use fresh filenames if those files already exist: exclusive creation rejects overwrites, including overwriting an input or symlink target. The helper does not create missing parent directories.

Exit 0 means the requested processing succeeded, including a valid no-decision. Exit 2 means invalid input or an I/O error, with a diagnostic on stderr. `verify` recomputes normalized content and aggregates; it does not authenticate source receipts. Consumers must inspect the decision's outcome and blockers, not interpret exit 0 as deployment approval.

Only explicitly named CLI files are read. Every file must be JSON with unique object keys and finite numbers. The helper rejects booleans where integers/numbers are required, unsupported top-level/control fields, duplicate trial identities, and unsupported scorer or metric kinds. Output JSON is strict and deterministic apart from the freeze receipt timestamp. Never edit normalized totals to repair evidence: preserve the input, correct its producer, and write a new artifact.

## Content identity and freezing

The frozen envelope has schema `mpl-frozen-v1`, `plan`, `digest`, `frozen_at`, and `identity_limit`. The digest is SHA-256 of the plan serialized with Python's `json.dumps(sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)`, encoded UTF-8. This is the versioned contract, not RFC 8785 canonical JSON. Integer `1` and float `1.0` have distinct encodings. The digest excludes the envelope, so it never hashes itself.

All material is inline JSON: prompt text, native configuration, tools, parser, candidate-specific composite workflow description if needed, case inputs, expected outputs and scorer. A candidate digest binds its entire candidate object; a case digest binds its entire case object. The plan digest binds these plus design, environment, retry rules, budget, population and decision rules. The helper verifies all three identities on every attempt. Changing any of these requires a new plan and new evidence; old rows cannot acquire a new identity by copying a new digest onto them.

For media or external datasets, inline the explicit immutable content/manifest needed to identify the experiment in the case input. A URL alone identifies only the URL string. The executor must record and verify byte digests of accessed content and include the immutable manifest before freeze; this helper does not dereference or hash outside files. Do not claim content binding for omitted bytes, inaccessible artifacts or mutable URLs. Native configuration is preserved without interpretation: structural validity is not provider compatibility.

`frozen_at` is an unauthenticated local operation receipt. Matching hashes do not prove preregistration, data rights, permissions, the truth of outputs, identity of the served remote model, or a stable provider alias. Chronology and deployment scope need separately reviewable evidence. A changed prompt synthesized from winning candidates is a new candidate, not an inherited winner.

## Plan schema: mpl-plan-v1

Use `assets/plan.example.json` as the complete specimen. Required keys:

- `experiment`: nonempty experiment identifier.
- `population`: exact task population and intended claim scope.
- `environment`: object containing nonempty `host` and `profile_revision`; add relevant endpoint, region, runtime, tool or renderer observations as data. No universal provider parameter translation is attempted.
- `baseline`: existing candidate ID.
- `repetitions`: positive integer; all candidate/case pairs use this same fixed count.
- `candidates`: at least two unique objects, each with exactly `id`, `prompt` (nonempty string), `native_config` (object), `tools` (array), `parser` (object).
- `cases`: nonempty array of unique objects, each with exactly `id`, `input` (JSON), `demonstrations` (array), `output_contract` (text/object), `expected` (JSON), `scorer` (below), `exposure` (`held_out`, `development`, `unknown`), and `family` (nonempty string).
- `retry`: exactly `max_attempts` (positive integer) and `transient_statuses` (unique subset of `timeout`, `transport_error`). An empty subset or maximum one prohibits retry.
- `resources`: exactly `currency`, `cost_basis` (`measured` or `estimated_marginal`), `latency_region`, `max_total_cost` and `max_candidate_mean_cost`. Currency and region are nonempty strings; ceilings are nonnegative finite numbers or null.
- `rule`: exactly the required fields below, with two optional fields.
- Optional `stopping_rules`: nonempty array of nonempty strings stating the preregistered safety, permission or other campaign stops beyond the resource ceilings. They are bound by the plan digest and reviewed against the raw campaign status; the helper does not execute or interpret them.

Families preserve sampling context; this implementation weights every case/repetition equally. Family weighting, adaptive/sequential trials, paired statistical estimators, custom utility formulas and significance tests are not implemented. An unsupported rule fails validation rather than silently substituting a different analysis. Use a separately justified manual method and an honest no-decision until its required evidence exists. Repetitions do not turn one case into multiple independent tasks.

### Rule and resource semantics

Required rule fields: `metric`, `aggregation: uniform`, `threshold`, `minimum_improvement`, `tie: no_decision`. Optional: `quality_threshold`, `on_insufficient_improvement` (`no_decision`, the default, or `retain_baseline`).

Supported metrics:

- `trial_pass_rate`: passed terminal trials divided by all planned trials when the matrix is complete, higher is better, inclusive minimum `threshold` in [0,1].
- `mean_score`: arithmetic mean of terminal trial scores, higher is better, inclusive minimum `threshold` in [0,1].
- `mean_latency_ms`, `total_latency_ms`: average per-trial or total observed latency in milliseconds, lower is better, inclusive maximum `threshold`.
- `mean_cost`, `total_cost`: average per-trial or total cost in the declared currency/basis, lower is better, inclusive maximum `threshold`.

Every per-trial resource total includes every attempt, including failed retries. Candidate means divide totals by trial count, never successful-request count. Latency measures the declared region only, not automatically wall time across gaps, queue time, scoring, tools or the whole campaign. Preserve additional measured regions in raw source/trace data, but do not combine them with this metric. Cost does not silently include unknown tool charges, subscriptions, credits or excluded resources. Where applicable, include pricing date and coverage in environment/source and assess comparability. Estimated marginal cost is not a billing total.

Resource-based ranking requires `quality_threshold`, an inclusive mean-score floor [0,1]. It can also accompany a quality metric. `max_candidate_mean_cost` is an additional feasibility gate; `max_total_cost` checks all campaign attempts. These are audit checks, not live budget enforcement. The actual runner must implement stop rules and preserve stopped/incomplete work.

The unique best feasible candidate wins only when its directional improvement over baseline reaches `minimum_improvement`, measured in primary metric units. A best baseline can be retained when it meets the gates. An exact tie among the best feasible candidates always yields no-decision. When a challenger is best but improvement is too small, default no-decision; `retain_baseline` instead retains an eligible baseline. The gate never selects an ineligible baseline merely because evidence is missing. No candidate meeting all thresholds means no-decision.

Unknown optional cost remains null and does not invalidate a quality-only outcome. A required cost ceiling, cost ranking, or latency ranking cannot pass with unknown required measurements. No zero imputation, success-only denominator, unannounced tie-break, or unsupported uncertainty claim is made. Sums/means use exact rational forms of the accepted JSON numeric values before finite JSON-number rendering; improvement differences use those rendered decimal values, avoiding binary-subtraction artifacts at ordinary decimal boundaries. This is arithmetic, not a statistical tolerance.

## Request packet visibility

`prepare` projects only candidate ID, case ID, repetition, prompt, native_config, tools, parser, input, demonstrations and output_contract. It excludes expected answers, scorers/rubrics, exposure/family, full plan, review and evidence digests. The output's separate executor-only `identities` object gives the plan, per-candidate and per-case digests that each raw attempt must carry; never forward it in a packet. Legitimate few-shot outputs and declared task schemas survive. Candidate-visible text must itself be audited: a secret accidentally placed in `input` remains visible by design.

The output holds packets for all trials. Give the runtime only the individual packet appropriate to that request; do not give the candidate the full packet collection. IDs must be neutral if blinding is claimed. Keep the frozen plan and raw identity receipts in the executor/evaluator compartment. Projection is not filesystem access control, cryptographic blinding or proof of an isolated host. The host must actually deny candidate access to evaluator material. A readable sibling directory invalidates an isolation claim.

## Raw schema: mpl-raw-v1

Required root keys: `schema`, `plan_digest`, `attempts` (array), `campaign_status`. Optional `review`. Campaign status is one of `complete`, `partial`, `budget_stop`, `safety_stop`, `permission_stop`. A producer's complete label cannot repair missing trials or invalid records. There is no run-level provenance override.

Each attempt requires:

- `candidate`, `case`, `repetition` and `attempt`. Repetition/attempt are positive integers. Together the first three identify one trial; the fourth identifies one actual request within it.
- `plan_digest`, `candidate_digest`, `case_digest`, calculated at collection against the frozen content.
- `status`: `ok`, `refusal`, `timeout`, `transport_error`, `permission_denied`, `error`, or `safety_stop`.
- `stop_reason`: nonempty text. Complete successful responses use `complete`, `stop`, `end_turn`, or `refusal`. `max_tokens`, `length`, `truncated`, `incomplete` always block selection even if JSON parses. Other successful-response reasons are unknown delivery and block selection. `safety_stop` and `permission_denied` reasons block the campaign regardless of status. Preserve an unmapped native reason in `source` rather than relabeling an uncertain stop complete.
- `output`: the complete raw response as text, including refusal or partial output. Never replace it with extracted grade or a summary.
- `evidence`: `observed`, `synthetic`, or `unknown`, set per actual attempt. Synthetic or unknown evidence anywhere blocks a real recommendation.
- `source`: object with a nonempty `receipt` and preferably `observed_model`. Include actual host/job/request references, observed resolved version, timestamps, native stop details and receipt provenance when available. Null/missing served model is a disclosed drift limitation. A receipt string is not authenticated by this helper.
- `cost` and `latency_ms`: nonnegative finite numbers or null. All costs use the plan's declared currency and basis.
- `usage`: object of nonnegative finite numbers/null, or null if unknown. No guessed token counts.

Optional: `assessment`, supplied `score` and `passed` (checked against grading), and `trace` (JSON evidence only; never executed). Record any actually authorized artifact/tool observation in trace/source, with immutable output identity and a receipt. A performed-work flag or promise text is not evidence of execution. Deterministic output checks can establish only their specified output contract; richer behavioral/artifact claims require actual collected observations and attributed review. Do not fabricate missing traces or read private host transcripts.

### Attempts and retries

Expected coverage is the exact Cartesian candidate × case × repetition set. Repeated rows from A cannot replace missing B rows, even when row counts match. Attempts must have unique, consecutive IDs starting at 1 within each trial. They may arrive in any array order; numbering determines request order. All attempts are retained verbatim in normalized `raw`.

Every nonfinal attempt must have an eligible frozen transient status and no grade. No retries follow a terminal success, refusal, permission failure, safety stop or truncated output. The final attempt fixes the trial outcome; the helper never chooses the best observed score. Exhausted transport/error attempts remain terminal execution failures with unknown task grades and an explicit `terminal_execution_failure` blocker. They do not become wrong-answer score zero. An unfinished partial campaign still blocks a recommendation. Correct task refusal can pass exact/JSON/imported grading; it is different from a campaign safety stop.

## Scoring

Closed scorer kinds:

1. `{"kind":"exact_text"}`: exact string equality, no whitespace/case cleanup. Expected must be text. Score is 0 or 1, pass iff score 1.
2. `{"kind":"json_equal"}`: parse the full raw output as strict JSON and compare canonical representations to expected JSON. Duplicate keys, nonfinite values, malformed JSON and trailing text fail the task. Type distinctions are retained; true is not 1 and 1.0 is not 1. Score 0 or 1, pass iff 1.
3. `{"kind":"imported","rubric":"...","pass_threshold":0.8}`: attributed external human/model assessment. Score is [0,1], pass iff score meets the frozen threshold. It is not independent machine verification.

A complete assessment has exactly `status` (`ok`/`error`), `grader` (identity string), `grader_config` (object), `rubric_digest` (digest of the full case scorer), `output_digest` (digest of the raw output string), `receipt`, `explanation`, and `score`. Receipt/explanation must be nonempty. An error assessment must have null score and remains ungraded. Missing assessments or incomplete receipt fields are preserved but ungraded; no grade is manufactured. Complete mismatched receipt bindings or invalid score types fail validation. Imported scores remain an assertion even with all receipt fields present.

Terminal request failures have unknown task grades and block selection; the frozen v1 metric does not define a zero-score execution-failure treatment. Missing/failed subjective grading is also unknown. A completed task-level error response or correct refusal can instead use `ok`/`refusal` status and be graded against its declared expected behavior. Recovered permitted transient attempts use the final valid response while retaining every attempt and its resource measurements. Supplied scores/passed flags cannot contradict recomputed or attributed grades. No expressions, Python, imports, commands, judge models or arbitrary plugin scorers run from this helper.

## Normalized evidence and decision readiness

Normalization retains raw evidence, its digest, the plan digest, exact missing trials, observed counts, per-trial terminal status/grade/provenance/resource totals, per-candidate aggregates and structural blockers. Score minima/maxima describe observed spread; they are not confidence intervals. Partial aggregate denominators are observed trials and are non-decisional. On complete matrices they equal planned denominators.

`verify` and `decide` recompute normalization from retained raw evidence and compare the entire normalized artifact. They reject tampered counts, grades, totals, missing sets or raw digests. This catches post-normalization inconsistency, not a forged but internally consistent original record. Keep original source records and independent provenance.

Selection additionally requires a review object with exactly `reviewer`, `receipt`, `scope` (equal to the plan population), `limitations` (array of nonempty strings), and `checks`. The exact check keys are `chronology`, `sample_adequacy`, `data_rights`, `comparability`, `grading`, `isolation`, `deployment_scope`. Each is `{ "status": "supported" | "unknown" | "failed", "evidence": "a nonempty receipt/reference or limitation" }`. Unknown/failed checks block selection. No single readiness boolean is accepted.

This is a transparent manual-review gate, not authenticated review. A caller can falsely assert support; the helper cannot detect that solely from JSON. Independently inspect evidence, sample/population mismatch, exposure, native compatibility, chronology, permission, artifact completion and source truth before using the rule outcome. Development or unknown-exposure cases block deployment selection even with a full matrix.

The decision reports `outcome`, `hypothetical_rule_outcome`, eligible candidates, metric/direction/values, all blockers, per-record evidence classes and explicit limitations. The hypothetical field shows arithmetic only; it is never a real recommendation from synthetic/mixed evidence. `outcome: select:<id>` is a conditional, declared-rule result supported by the supplied observations and review assertions, not an autonomous deployment action or statistical guarantee. Finish the human-readable selection memo with exact scope, findings, limitations, confidence basis, rollback and missing native checks.

## Boundaries

Legacy rows missing plan/prompt/scorer identities cannot be retroactively promoted by filling them from a new freeze. Preserve and describe those original records separately; they are unsupported for automated selection until valid new collection exists. This v1 processor deliberately rejects foreign raw schemas instead of inventing provenance through a permissive mapper.

Local tests exercise synthetic processing only. They do not demonstrate model quality, account access, actual blinding, provider acceptance, natural-language routing, native installation or production behavior. Neither fingerprints nor an asserted reviewer approval changes that boundary.

## Prompt and audit structural checks

The separate `scripts/promptcheck.py` reads one explicit UTF-8 input and prints JSON. Commands are `prompt-package FILE`, `audit FILE`, `text FILE` and `xml FILE`. Exit 0 means these limited local checks passed; exit 2 means invalid shape, XML or input. It always reports `provider_compatibility: not_checked`, `runtime_verified: false` and `claims_authenticated: false`. It never edits inputs, fetches sources or runs a model. The realistic [prompt](../assets/prompt-package.example.json) and [clean-audit](../assets/audit.example.json) specimens are synthetic and have unverified target behavior.

A prompt package has integer schema_version 1, operation create/migrate/diagnose, target, nonempty prompt, format plain/xml, nonempty requirements and checks, native_configurations and limitations. Each requirement has a unique id, text and kind task/facts/output/policy/tool/verification. A check names known requirement_ids, a method and status planned/passed/failed/blocked; claimed executed pass/failure needs a receipt string. The checker validates the claim's shape, not its truth.

Target has provider, model, interface, verification unverified/documented/executed, checked_at and sources. Documented/executed targets need an ISO date and sources; executed also needs execution_evidence. Unverified targets need a limitation. Native configurations each have label, scope target/source_example, values object and sources. Nonempty active target settings need cited support; quoted source examples remain distinct. Every object is checked, not only the first model/effort substring. Actual compatibility still requires the applicable current provider/interface check.

An audit has source model/interface/prompt_sha256, target, findings, unsupported_parameters, coverage and boolean verification_required. Findings can be empty. Each finding has unique id, location, evidence, consequence, action, severity and certainty. Unsupported settings name their scope, evidence and action. Coverage names inspected and missing evidence; partial/blocked coverage must state what is missing, while complete coverage cannot hide a missing item.

Declared XML is parsed as a whole document or sibling fragments. Real document-type declarations are refused; text inside CDATA is not interpreted as a declaration. Plain text containing comparisons or quoted tags is not automatically treated as XML. Duplicate JSON keys and nonfinite values are rejected. Literal repeated-line advice skips fenced/quoted examples where detected and remains advisory; it is not a semantic-duplication test or instruction-removal mandate. The tool never bans verification, source quotations or user-required formatting.
