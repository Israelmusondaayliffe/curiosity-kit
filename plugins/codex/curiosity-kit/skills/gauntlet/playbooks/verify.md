# Independent verification and evidence

## Verification-only route

For finished work, freeze the exact artifact path and bytes, sources and question set, use mode verification-only and allow writes only to the selected evidence/state directory. An explicit verification request can supply scoped approval for this verification job. No builder or improvement-loop critic launches; no artifact/source/question edits. This CLI certifies one finished artifact per run. Multiple independent artifacts require separate runs; do not submit a substitute or a subset as the frozen target. Read the selected domain before designing inspections.

For research/prose, send the [reader proxy](../roles/reader-proxy.md) only the artifact, reader profile and frozen questions. Record its actual answers and guesses. Independently extract material claims and inspect each relevant source, including disconfirming evidence. Build a ledger recording claim location, supported/contradicted/unsupported/cannot-verify, the actual sources checked, exact quotes and reasons. Run `inspection.py reader` and `claims`. These commands check structure, source bytes, quote presence and arithmetic; they cannot infer truth from a matching quote. A fresh integrity judge must check semantic support and whether important claims were omitted. Unknown live reachability stays unknown; frozen supplied sources can be inspected locally.

A contradictory source and an absent supporting source are different defects. Name both precisely. A polished memo cannot pass integrity by quality votes. Export failure evidence and a workbench too; a failure report must not be withheld just because the result was not successful.

## Fresh panel

Use [quality](../roles/quality-verifier.md) and [integrity](../roles/integrity-verifier.md) as separate read-only mandates. Default three judges of each type; minimum two of each. Freeze the count/policy before reviews. Cover at least three perspectives across the panel: acceptance/scope, evidence/correctness, integration/adversarial failure. A judge may hold multiple declared perspectives but may not cross quality/integrity roles or share context. This allows a five-helper verification budget to use one reader plus two quality and two integrity judges; it does not require an extra redundant panel.

Every judge receives only current artifact, approved criteria/bar and relevant inspection/source evidence. They never receive builder rationale, prior reviews, round gaps or another judge's answer. Record actual fresh-session dispatch provenance, model/effort and input boundaries. A missing capability or contaminated context is cannot-verify, never a simulated fresh agent. Verify criteria/reader questions/reference bytes before judging; mismatch invalidates the contract.

Verdicts bind run/piece generation, contract hash, artifact hash, criterion IDs, evidence hashes, reviewer identity and fresh host session. Use the review schema and commands described in [CLI](../references/cli.md). All material criteria need real observations. Host receipts must come from actual host events; synthetic records are valid only as explicitly labelled deterministic test fixtures.

## Script consensus

`review.py consensus` and the state engine's `finalize` compute the outcome. Any integrity fail vetoes; any missing/invalid/cannot-verify evidence blocks certification. All-pass produces verified; a strict quality majority may preserve dissent only for criteria explicitly frozen as nonmaterial, labelled verified-with-dissent. Every criterion is required by default. Any required-criterion failure vetoes a majority pass. A quality tie does not become a win. Required failing criteria cannot be waved away by majority. Investigate disagreement against evidence, then obtain fresh affected judgments; never hand-edit a vote into agreement.

Finalization also checks required workstream readiness, integration, pending launches, frozen input identity and runtime limits. A pass-shaped panel cannot make capped or unfinished work complete. Record the actual computed result; failed/unverifiable remain useful outcomes. Repairs use remaining authorized budget and fresh evidence; material contract changes need renewed approval.

## Reports and learning

Generate report/workbench from canonical state. Return verdict, goal/bar, per-piece observations, commands/exits, claim defects, artifact hashes, what was not verified, dissent, remaining gaps and budget/stop reason. Missing metrics remain not recorded. Rerunnable evidence survives cleanup. The browser page is a local readable view, not a service or scheduler.

A requested retrospective examines actual scoped run records, classifies missing method versus missed trigger, ignored instruction and tool failure, and proposes the smallest useful improvement. Prefer a deterministic check for a mechanical error. Separate observation, hypothesis, proposed change and validation. Do not read unrelated private transcripts or automatically edit global skills, publish tickets or activate schedules.
