# Unslop: source-faithful cleanup

This is the package's single cleanup owner. Never infer authorship from prose, a word or a score. Improve the writer's actual text, preserving meaning, source boundaries and personality. No sibling Unslop skill is required.

## Modes

DETECT reports located defects and suggested remedies without rewriting the source. REWRITE makes authorized minimum-effective changes and returns complete usable text first. DELIVERY is one silent proportional check of the final authored result; it does not restart the writing workflow. Short replies need no temporary file, scanner report or reviewers. Child cleanup never invokes Scribe, another cleanup method, learning or independent reviewers.

## Read in order

1. Intent and voice: establish audience, purpose, stakes, protected material and the writer's evidenced sentence behavior. Use the selected guides/samples, not a packaged personal profile. Preserve facts, opinions, emotions and experiences actually supplied; neutrality can be right when the source is neutral.
2. Provenance and certainty: compare with notes/sources when present. Remove, ask about or clearly qualify unsupported connective tissue. A source-blind scan can ask whether a motive is established, but cannot declare it invented. Restore the actual degree of confidence.
3. Causality and structure: use [structural checks](../references/structural-checks.md). Let examples disagree; do not complete every uncertainty into a lesson or every piece into a framework. Inspect argument self-commentary before defending it as voice.
4. Sentence and lexical craft: consult [47 pattern families](../references/pattern-catalog.md), [word options](../references/word-options.csv) and [lexicon](../references/lexicon.csv) only where useful. These are contextual diagnostic aids, not bans or statistical authorship claims. A precise technical term or a deliberate signature construction can remain.
5. Repair and verify: make the smallest edit that fixes the actual reader problem. Recheck affected meaning and exact material, then read for unnatural smoothing or manufactured personality. Restore what a well-intended edit erased. Do not iterate merely to improve a numerical score.

## What to preserve

Protect quotations, code, shell commands, logs, structured data, citations, links, legal wording, identifiers, parameters, exact prompt blocks and user-required phrases. Apply cleanup to surrounding authored prose. Typography inside a quotation is not editable style. Use `wlm.py protect BEFORE AFTER` and --exact for designated blocks when working with files; ambiguous markup requires manual inspection. The parser's scope is limited and cannot certify semantic correctness.

Retain justified uncertainty, necessary explanation, purposeful repetition, specific evidence, clear long sentences, a meaningful aside and the writer's actual roughness. Active voice often helps, but passive is correct when the actor is unknown or irrelevant. A simpler word wins only when it preserves precision. Do not invent a number or anecdote to replace a vague sentence.

## Useful diagnostics

`wlm.py scan FILE --profile PROFILE` reports lexical/limited structural candidates outside recognized protected spans. Profiles reflect the actual genre; they do not override user instructions. The full semantic review covers more than the executable detector. `profile` supplies mechanical rhythm counts; `business` supplies cue counts; neither is an editorial verdict. `punctuation` previews or writes a new selected prose file and never edits exact spans intentionally; compare and review before adoption.

## Contextual finish

Ask whether the piece fulfills the request, supports its claims at their actual scope, supplies needed explanation, preserves protected material and sounds recognizably like the evidenced writer. No minimum score or compulsory defect count applies. In detect mode clean the findings, leaving the source unchanged. In rewrite mode return usable copy and only useful requested explanation. DELIVERY runs once on that version.

If meaning, voice or an exact span was damaged, restore it from the original and correct only the identified defect. If the source is missing, state the boundary; if a required check cannot run, report it as unavailable. A clean scan is not readiness. The parent owns independent review and any confirmed learning.
