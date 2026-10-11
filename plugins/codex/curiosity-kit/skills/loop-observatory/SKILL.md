---
name: loop-observatory
description: Ingest explicitly selected loop evidence, compare outcomes across engines, models, versions or time, and audit paired machine and human judgments. Produces source-linked JSON and Markdown with honest coverage and costs. Does not execute, schedule, accept or repair a loop.
---

# Loop Observatory

Turn a bounded set of loop records into an answer the user can check: what finished, what people accepted, what it cost where measured, where judges disagreed, and which evidence would settle an unresolved problem. Keep canonical producer records read-only. Write only derived observer outputs to a separate, explicitly selected destination.

## Select the work

Start from the user's question and supplied sources. Ask only for missing scope that materially changes the answer: which roots/exports, which period or cohort, or where derived files may go. For an ordinary small request, one explicit manifest and one local report are enough. No permanent telemetry service, dashboard, scheduler, agent panel, sibling skill or global account-home scan is required.

- **Register or ingest runs:** follow [ingest](playbooks/ingest.md). This includes bounded discovery, supported source profiles, duplicates, immutable revision history, corrupt/incomplete inputs and source fingerprints.
- **Compare results, versions, models or periods:** ingest if needed, then follow [report](playbooks/report.md). This includes acceptance, duration, iterations, exhaustion, stop reasons, costs and meaningful unknown groups.
- **Check judge quality or later human disagreement:** follow [audit](playbooks/audit.md). Pair the same artifact and criterion under the same rubric; do not label a judge defective from a disagreement count alone.
- **Prepare the next repair step:** follow [handoff](playbooks/handoff.md). Return an unresolved evidence-bound handoff to the execution owner. Do not start the repair or claim it is fixed.

Focused requests use the focused method; a comparison need not turn into a full calibration campaign. The three former specialist identities are reachable through these local methods, not separate installation dependencies.

## Shared working contract

1. Read [ownership and inputs](references/ownership-and-inputs.md) before selecting sources. Use [source profiles](references/source-profiles.md) and [record contract](references/record-contract.md) when normalizing unfamiliar records. Unknown formats require an explicit mapping, not recursive first-key guessing.
2. Freeze source selection, namespace, producer/profile and requested time/cohort basis. Keep logical run, revision, attempt, artifact and observation identities separate. A copied run or late human label is not another trial.
3. Distinguish lifecycle closure, process completion, machine verdict, artifact verification, human acceptance and delivery. An approval to launch or upload is not output acceptance. A blocked/resumable run is not terminal merely because no work is happening now.
4. Preserve missing, rejected, stale and conflicting evidence explicitly. Neither a successful child node nor a missing cost can promote the whole run to success or free work.
5. Count one defensibly current revision per logical run. Preserve history, including authoritative corrections that retire an older terminal view where that producer permits them. Accepted LoopKit does not permit terminal reopening.
6. Compare only compatible judgment pairs and comparable cohorts. Give every rate its numerator, denominator and coverage. Explain material task/rubric/label-selection differences before any ranking.
7. Use the included Python standard-library helper for deterministic intake and exports. [CLI and examples](references/cli.md) gives its actual public interface. Resolve the script relative to this skill; do not assume a host-specific home or import another skill's runtime. If execution is unavailable, disclose that and perform only a clearly labeled manual analysis of supplied evidence; never fabricate a command result.
8. Inspect the actual JSON and readable report before delivering: source IDs, selected current revisions, exclusions, pairs and arithmetic must agree. [Worked cases](references/worked-examples.md) shows the important denominator and identity traps.

## Return the useful answer

Lead with the finding, then scope and evidence limits. Link or attach the derived JSON/Markdown when the channel supports it. Include enough source identity to reproduce the cohort without publishing private paths or content to another audience. A useful short result might be: “Two of three labeled runs were accepted; one further run has no human label. Two of three comparable judge/human pairs disagree. Known spend is USD9 across three of four runs, so all-cohort cost per acceptance is still unknown.”

A complete unchanged intake may yield a no-new-result response for the same analytical request. A missing source, newly corrupt read, changed question, new cutoff or late label requires a fresh result or visible blocker. Conditional no-change behavior does not create or verify a schedule.

Read [source provenance](references/sources.md) only for lineage or licensing questions. Original and benchmark material informs the local method; it grants no authority to execute producers, modify judges, share private reports or distribute source code.
