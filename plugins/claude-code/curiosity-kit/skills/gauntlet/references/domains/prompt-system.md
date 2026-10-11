# Prompt systems

## Unit and bar

Choose a mode, routing rule, template, or invocation description. Judge the behavior it produces. Scripts shipped alongside prompts are separate code units.

Freeze test inputs and expected behavior before execution. Include intended activation, ambiguous boundaries, refusal where required, and explicit no-load cases. Define observable outputs and validation rules. A pleasant refusal is not sufficient if the case required performing an allowed task; a fluent answer fails when the case required declining.

## Inspection recipe

Execute candidate and reference on identical frozen inputs using the authorized host. Retain per-case outputs, observed settings, invocation outcomes, and errors. Do not launch paid model calls or expand permissions merely because a benchmark needs them. If execution is unavailable, report the limit instead of substituting prompt-source review.

An authorized local benchmark command can be recorded with `python3 scripts/inspection.py check --input payload.json`. The runner captures process results; it does not establish that the benchmark made genuine model calls. Keep host execution evidence. A fresh reader also follows the prompt on selected frozen cases and records where instructions forced it to guess. Validate that record with `python3 scripts/inspection.py reader --input payload.json`.

## Comparison and worked check

Blind A/B compares output sets on the same inputs, never prompt wording. Neutralize provenance while preserving substantive formatting, retain expected outcomes, and seal the map from critics.

For a skill description, measure both correct loads and false activations on neighboring tasks. For a report template, validate generated reports against the frozen shape and inspect whether required content is substantive.

Integrity review checks unchanged benchmark hashes, complete case reporting, real tool names, supported parameters, resolvable resources, and observed settings. Deleted failures, fictional flags, or invented execution receipts fail. Explicit model choices remain binding where supported; unselectable settings must be reported honestly. Documentation about the prompt belongs to prose, and generated image quality belongs to visual or brand.
