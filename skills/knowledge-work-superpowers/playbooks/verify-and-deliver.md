# Verify and deliver

Use this method before a substantive completion, accuracy, readiness or delivery claim. Verify the exact claim you intend to make on the actual final artifact. A previous review, correct-looking outline or successful structural check does not establish that the finished work satisfies the request.

## Bind the final check

Identify the current brief, final artifact/version, sources supporting decisive claims, prior findings and required output destination/format. Reread the final artifact after the last edit. If source or artifact bytes changed after an earlier check, identify what that check depended on and refresh the affected proof. Unchanged valid evidence can be reused with its actual scope; freshness does not require rerunning unrelated checks for a new timestamp.

For each completion claim:

1. Name what observation or result would establish it.
2. Perform the relevant actual check using available authorized tools.
3. Read the output and its failures, limits or missing coverage.
4. Compare the result with the requirement, not just an exit code.
5. Repair in-scope failures and rerun the affected check, or report the real unfinished state.

“File exists,” “record parses,” “claims inspected,” “render viewed,” “review passed,” “user accepted” and “message delivered” are different claims. Keep them separate.

## Check the work, not only its record

### Requirements and reader outcome

Match the actual result to every required question, section, comparison and output. Check scope, audience, template, length, protected wording and intended decision or action. Required examples or instructions must be filled and usable, not headings awaiting content. Apply the same checks to a delivered evidence record or notes, whose wording keeps the main artifact's population and denominator limits, and to direct answers in the final reply, including any requested sentence count or format. A plan-only request must remain a plan; a full-report request cannot end with a research plan.

Inspect the promised output rather than nearby evidence. A complete source ledger does not prove a complete memo. A technically true statistic can still mislead when the denominator or condition is absent. Keep requirement and evidence/quality verdicts distinct.

### Sources and final wording

For each material assertion, inspect the actual supporting passage or data beside the final wording. Verify quotation fidelity, exact numbers, units, scope, attribution and citations. Open the cited source when the task requires live access. Distinguish full read, excerpt, inaccessible primary and secondary account. Do not report a link checked merely because it is syntactically valid.

Recheck volatile facts for the decision's relevant time, within the allowed source scope. A supplied-sources-only task does not permit adding external research; disclose that live freshness was outside scope. Separate the source's publication/update/effective date from your access date. A fresh fetch of an unchanged old record is not new evidence.

Confirm that corrections govern the affected clause, repeated summaries are not independent support, and relevant counterevidence remains in the final result. Facts, inference, dispute and recommendation must remain distinguishable after editing. Check titles, captions, transitions and executive summaries as well as the body.

### Calculations and data

Rerun consequential arithmetic using an appropriate actual deterministic tool. Inspect inputs and expected result independently; a calculator does not know that you chose the wrong denominator. Check units, populations, period, exclusions, rounding and comparable baselines. Trace changed values to every affected table, statement and recommendation. Record the actual command or calculation and result when reproducibility matters.

### Findings and authority

Inspect open review findings. Confirm each claimed fix against the current artifact; retain rejected feedback with evidence and deferred limitations with reasons. Critical or Important unresolved defects block unqualified completion. Missing independent review remains missing; self-review is not converted into independence by a role label.

Confirm that confidentiality, allowed source access, write locations and external-action boundaries held. A recommendation, plan field or reviewer note is not approval to execute it. Do not expose private raw material in a public artifact merely because it supported the analysis.

### Format and destination

Check the actual required output:

- Markdown/text: reopen the saved bytes, inspect full content, internal consistency and meaningful links. If a rendered view is required, actually inspect it.
- Document, PDF, spreadsheet or slides: use available format-specific parse/open/render tools and inspect the final exported version, relevant pages/sheets/slides and any formulas or layout on which usefulness depends.
- Interactive or visual artifact: exercise the requested relevant behavior and view the final version through supported tools. Source inspection alone is not browser or accessibility proof.

Do not substitute an HTML file for a requested PDF without saying the requested export remains unfinished. If tooling is unavailable, return the useful supported artifact and exact pending format check. Do not install software or create a service as an implied verification step.

Check the output location and name, preserve earlier versions or obtain authority for replacement, and verify the user can use the returned link/file through the actual supported delivery route. A local path on one machine may not be reachable from another. Do not claim external recipient access without evidence.

## Exact evidence checker

When a file deliverable requires a traceable evidence record (because the user asks for one or the governing completion gate requires a checkable record), read the [full contract](../references/evidence-contract.md), resolve this skill's actual root and run:

```sh
python3 /actual/skill/root/scripts/check_evidence.py /approved/task/evidence.json
python3 /actual/skill/root/scripts/check_evidence.py /approved/task/evidence.json --artifact /approved/task/final.md
```

The paths illustrate invocation; use real resolved authorized paths. Python 3.9+ is required. The checker reads only explicit inputs, validates declared structure/references/access/review state and can compare the selected artifact's bytes with recorded review identity. It does not fetch source locations or render output. The [filled example](../assets/evidence-example.json) deliberately remains unreviewed; never turn it green by falsely changing review fields.

Inspect the returned findings. A schema error, an unresolved review, a stale artifact hash and a semantic claim failure are different problems. Fix the underlying fact or perform the missing check; do not manipulate metadata to obtain exit 0. When recording a real review, bind it to the actual artifact and honest verdicts. A declared reviewer name or passing status is not independent evidence of a review.

Canonical Markdown markers help detect unknown declared references, but cannot find every unsupported sentence. Other formats receive only file-presence/identity checks from this helper. It cannot certify truth, source independence, comprehensive claim coverage, correct arithmetic, live freshness, visual quality, authorization, consent or delivery. For tasks without a required shipped-checker gate, equivalent user records can be checked manually with that limitation stated; no dummy `deliverable.md` or copied shadow document is required. If the gate is required and the checker cannot run, useful work may continue, but that gate remains incomplete.

## Package the useful result

Record the actual artifact name/version, format, location, intended use and checks. Preserve only the supporting evidence the task needs, in approved storage: brief/plan, useful source and claim records, consequential review dispositions, calculations and verification results. One compact working note may serve several roles. Do not expose a large private research archive merely to make delivery look thorough.

For continued or long work, ensure the progress record points to durable accessible artifacts. Include the governing decisions and why, current source/version bounds, material blockers and the next check. If work used temporary files, preserve required final evidence through the authorized destination before cleanup. Do not delete unrelated state or the only recovery copy.

Use the [delivery note](../assets/work-record-templates.md) when useful. Lead with the actual answer/artifact and then:

- What was completed and the exact location.
- Which relevant checks actually ran and what remains unverified.
- Limits that affect use of the result.
- One next action if the user needs one.

Sending, publishing, sharing, moving or deleting have their own applicable authority. If the user explicitly authorized a supported external action, perform only that action and verify its result. Otherwise finish at the private artifact/handoff. Never infer publication or delivery to another person from file creation.

## Terminal states

- **Completed:** the requested artifact exists in its agreed usable form/location, essential requirements have evidence, and the handoff is complete.
- **Completed with named limits:** the requested result is usable within an explicit scope, with nonessential limitations stated where they matter. Do not use this label to hide a required failed outcome.
- **Partially completed:** useful outputs exist, but part of the requested scope remains unfinished. Name it and the consequence.
- **Blocked:** the remaining required action needs a specific unavailable source, tool, decision or authority. Preserve independent finished work and state exactly what would unblock it.

Do not call a helper pass final acceptance, an unobserved service action delivered, or a finite failed campaign successful. Honest scope is part of the deliverable.
