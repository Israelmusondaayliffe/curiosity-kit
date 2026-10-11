# Research

## Unit and bar

Separate commissioned questions, source collection, claim tracing, and synthesis where each is independently inspectable. Synthesis depends on the evidence work. Freeze source-kind coverage, claim-support requirements, and a bounded counterevidence search, including an approved measurable quota where appropriate. Set these from the question, never from invented universal source counts. An empty search does not justify manufacturing disagreement.

Prefer primary evidence. Record source identity, date, origin, and the distinction between sourced fact, observation, inference, assumption, and recommendation. Count distinct underlying sources, not repeated citations or syndicated copies. Preserve credible disagreements in the synthesis itself.

## Inspection recipe

Extract material claims from the actual memo. For each, record location, `support` as supported, contradicted, unsupported, or cannot-verify, a reason, and `sources_checked` with file paths and relevant exact quotes. Even unsupported claims need the sources checked. Run `python3 scripts/inspection.py claims --input payload.json` and save its result. The script validates files, hashes, excerpts, and counts. It cannot infer truth, completeness, primary-source status, or live URL reachability. A fresh integrity judge must do that work; missing access remains uncertainty.

A separate fresh reader answers frozen commissioned questions from the memo alone. Record guesses and unanswerable questions, then run `python3 scripts/inspection.py reader --input payload.json`. Blind comparison is useful for a synthesis against a comparable review. Source ledgers and coverage checks use direct evidence, not pretend blindness.

## Verification-only example

Given a finished memo and frozen sources, preserve their bytes. Launch no builder. A claim that conflicts with a source is contradicted; a claim absent from every checked source is unsupported. Name both independently of the memo's polish. Keep quality and integrity reviewers separate and fresh. Export evidence and an honest failed or unverifiable result through the main Gauntlet workflow. Never repair the memo during a verification-only task or convert unavailable evidence into a pass.
