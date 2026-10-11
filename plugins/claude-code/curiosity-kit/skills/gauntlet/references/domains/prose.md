# Prose

## Unit and bar

Name an argument, opening, section, paragraph class, or transition set, including its exact span. Compare like spans against real, lawfully available reference passages. References establish clarity, compression, argument order, and deletability. They do not authorize copying a writer's voice. Freeze any word limit and reader questions before revisions.

## Inspection recipe

A fresh reader receives the current artifact, intended reader profile, and frozen questions, without the builder's explanation. Have it perform the text's intended job. For an opening, ask what it argues and why the reader should continue. For instructions, ask the reader to follow them and identify every guess. For a summary, ask questions the underlying report answers, using only the summary.

Save answers with artifact locations, `guessed`, and `answerable` fields. Validate the artifact hash and unchanged question file using `python3 scripts/inspection.py reader --input payload.json`. This checks records, not semantic correctness or actual reader independence. Retain host evidence of the reader run.

Audit factual claims using `python3 scripts/inspection.py claims --input payload.json`. Each claim needs its location, support judgment, reason, and sources actually checked. Exact quotations must occur in stored source text. A fresh integrity judge checks whether those words support the assertion and whether the ledger omitted material claims.

## Comparison and integrity

Blind-pair complete passages with neutral names and sealed provenance. Ask which conveys more relevant information, orders its reasoning better, and loses less when cut. Reject feedback that merely asks for the reference author's cadence.

For a technical explainer, a stylish passage still fails if the reader must invent a configuration step. Never soften questions after a poor result or reuse evidence from an earlier draft. Unsupported facts remain integrity defects regardless of prose quality. Use research when source discovery is the main challenge and strategy when the deliverable is a decision.
