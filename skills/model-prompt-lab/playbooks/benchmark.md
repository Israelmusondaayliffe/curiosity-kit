# Design the comparison and freeze its rules

A benchmark serves one decision. Define the decision before looking at candidate outputs: whether to change a prompt, model, effort setting, tool route or deployment configuration. Prompt-only benchmark design is a complete deliverable without running it.

## Frame a meaningful comparison

Read existing prompts, requirements, baselines and prior failures. Name the deployment population and consequence of choosing incorrectly. Identify what varies and what must stay controlled. Preserve the user's selected models; do not replace an unavailable candidate to make the experiment easier. A model-only comparison, prompt comparison and composite fallback comparison answer different questions.

Write the claim the evidence should support, such as fewer wrong classifications at a bounded cost on a named input population. Define an observable task outcome. A file's existence, the model's confidence or a valid schema is insufficient where factual content, complete coverage or actual effects matter.

Use representative cases with explicit inputs and expected behavior:

- Success cases cover real core work and its important variation.
- Boundary cases cover ambiguity, uncommon inputs, context length, partial evidence and tool limits.
- Failure cases cover malformed input, missing dependencies, unavailable tools and correct refusal or handoff behavior.

Name case families, provenance, exclusions and development versus selection exposure. Repetitions of one item are not new independent cases. Keep actual private data within its authorized destination; synthetic replacements may test mechanics but do not establish the real traffic distribution. If a case category genuinely does not apply, document the reason instead of adding an irrelevant example.

## Specify scoring and fairness

For each required outcome choose an observable assertion or named rubric. Exact text or JSON equality is appropriate only when exact output is the actual requirement. For subjective work, define concrete anchors, grader identity/configuration, evidence, abstention and disagreement resolution. Calibrate judgments against human-reviewed specimens where needed. A judge's successful request is not a correct grade. Avoid exposing model labels or answer keys unnecessarily, and counterbalance presentation order when it matters.

Record the primary metric, its unit/direction, denominator, aggregation, practical improvement threshold, hard quality/safety/deployment gates and any tie-breakers before execution. Distinguish latency to the user from inference, tools, queues and grading. Keep all attempts, rejected work and timeouts in the accounting. A faster candidate that did less work has not won. Unknown cost is not zero. Source version, rate date/currency and estimated versus measured cost remain separate from account-level credits.

Before freezing, check that each assertion and metric can separate the candidates on these cases: a scorer that every candidate is certain to pass or fail, or that cannot observe the required difference, gets replaced first. Record any model, tool or environment setting that can drift and verify it before the comparison.

Compare fairly tuned deployable configurations. State intentional constraints rather than concealing them. Match inputs, tool permissions, parser, observation route and grading. Interleave or block run order when warmup, cache or load may matter. Name uncertainty and the minimum independent evidence needed for the decision. Do not copy a fixed repetition count or a generic significance test into every workload.

## Freeze an executable or honestly incomplete plan

Read [the evaluation contract](../references/evaluation-contract.md) before authoring helper artifacts. Use [plan.example.json](../assets/plan.example.json) as a synthetic specimen, replacing its actual task fields. The helper supports a deliberately bounded fixed-design contract. It is not a general statistics engine. If the required weighting, metric or stopping analysis is unsupported, preserve the full requested plan and state the separate analysis needed; do not silently substitute pass rate.

Bind the full prompt, native configuration, tool/return schemas, parser, input/expected evidence and scorer. Record the actual host/backend, observed model resolution where available, profile revision and unavailable prerequisites. A mutable alias is not a weight snapshot. Describe candidate-visible instructions, inputs, demonstrations and acceptance criteria separately from evaluator-only answers/rubrics and executor provenance.

Freeze trial and retry rules. A trial is candidate × case × repetition; retries are attempts within it. Name allowed transient failures, maximum attempts, how the terminal attempt determines the outcome, whole-trial resource accounting and safety/budget stops. Put budget ceilings in `resources` and other preregistered stops in `stopping_rules`. A changed prompt or environment is a new experiment, not a retry. Keep a fixed full-coverage selection design for the local helper; a plan-compliant early stop may still be non-decisional.

Run:

- `python3 scripts/lab.py check-plan PLAN.json`
- `python3 scripts/lab.py freeze PLAN.json --out FROZEN.json`
- `python3 scripts/lab.py prepare FROZEN.json --out PACKETS.json`

Use new output paths; preserve prior evidence. Inspect the emitted packets. They must retain legitimate task examples and schema while excluding evaluator-only material. Actual directory/tool isolation is a later host requirement; a digest does not enforce blinding.

## Return or continue

Return the complete plan/specification, frozen identities if created, case coverage, rubric, budget/stops and readiness gaps. Local freeze proves the declared artifact identity, not chronology or consent. State whether preregistration is observed, supplied or unknown. No raw outputs means no result.

If execution was requested and authorized, proceed to [execute](execute.md). If not, stop with the finished plan. Never fill result fields with expectations or start a paid campaign merely because a plan validates.
