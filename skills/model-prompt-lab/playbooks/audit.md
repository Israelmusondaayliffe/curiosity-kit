# Audit a prompt or migration

Audit mode inspects and reports. It does not replace the production prompt, edit a repository, change configuration, execute a model or install a helper unless the user separately requested that action. A clean audit with zero findings is valid.

## Establish the evidence

Read the actual source prompt, target request and supplied configuration, not just filenames or a previous summary. Record source/target model and interface, prompt identity, task, user boundaries, required output and evidence available. Ask only for a missing item that prevents a useful assessment. Missing runtime access is a coverage limit, not proof a prompt is defective.

For current model settings, use [provider guidance](../references/provider-guide.md). Distinguish current official instruction, historical captured guide, author-reported behavior, actual task observation and inference. A file called official or a recent access date does not prove its content is current for the selected interface.

## Inspect the whole contract

Check the following against the actual request and source:

- Job, audience, facts, required content and intended downstream use remain explicit and consistent.
- Check duplication by meaning, not just identical wording, including within the same sentence, bullet or section: each obligation has one owning statement, other steps/tools/output requirements reference it, every distinct requirement and its specificity remain, and examples may demonstrate rules.
- Input sources and imported text have a clear role; quoted instructions cannot grant new authority.
- Output schema, examples, missing values, ambiguity, error envelope and completion status agree. Parseable JSON can still be wrong or truncated.
- Actual tools have valid names, inputs, return/error shapes and action boundaries. A stated tool is not installed merely because the prompt names it.
- Model IDs and native settings belong to the target model/endpoint, with dated support. Keep source-before examples separate from active settings.
- Prompt compensation, effort, history, context, caching and narration are not conflated. A client/parser defect should not be disguised as a text edit.
- Stable user policy, safety/approval rules, source facts and meaningful verification have not been removed under a simplification slogan.
- Evaluation criteria are discriminating and preserve important failures. A count, filename or self-issued pass is insufficient when content or side effects matter.
- A long-run or fallback request retains the actual methods and tools it needs. Refer to those local methods for the affected branch, not just their names.

When wording is redundant but harmless, mark an optional measured simplification rather than a required defect. When a current fact is unverified, mark the recommendation provisional. Do not invent a finding to fill a schema or satisfy a minimum count.

## Findings and completion

For each finding give an identifier, the precise location, evidence, consequence, severity and smallest proposed action. Explain what would disconfirm an uncertain hypothesis. Account for unsupported parameters separately, including whether they are active or merely quoted. Distinguish a prompt defect, configuration problem, missing evidence and later integration issue.

A structured audit can follow [audit.example.json](../assets/audit.example.json) and be checked with `python3 scripts/promptcheck.py audit PATH`. The checker verifies declared structure, not the truth of the finding. The array may be empty. If all required inputs were inspected and no material issue was found, say so with the inspected scope. If a missing source blocks a conclusion, return partial or blocked coverage with that exact source named.

Deliver the audit ledger, evidence limits, unsupported-setting inventory and verification decision. For an authorized later rewrite, [migration](migrate.md) can consume the ledger. Do not silently append a replacement prompt to an audit-only deliverable or claim that a proposed fix was tested.
