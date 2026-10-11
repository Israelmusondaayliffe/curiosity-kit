# Pull request to video

Explain an actual GitHub code change through readable code and its behavior/mechanism. Keep PR acquisition, offline ingestion, optional contributor media, story design and rendering separate. This is an authored snapshot of a PR, not a live-at-render dashboard or an exhaustive code/security review. A multi-PR release reel uses general-video with an explicit broader source plan.

## Ground the change

Resolve the authorized PR URL, owner/repo#number or checked-out-repo context. Prefer an available read-only GitHub connector; the bundled deterministic CLI acquisition uses an installed authenticated gh. Authentication, installation and private-source transmission remain separate permissions. Estimate length from additions+deletions and file count only as an initial guide: ~20–40s for ≤50 changed lines, ~40–70s for 50–200, ~70–110s for 200–600, ~110–180s for larger/25+ files. One clear headline can stay short despite a huge diff. User duration overrides the heuristic.

```bash
node <METHOD_DIR>/scripts/fetch-pr.mjs --pr '<verified-reference>' --out-dir ./capture
node <METHOD_DIR>/scripts/ingest.mjs --pr-json ./capture/pr.json --diff ./capture/diff.patch --out-dir ./capture/extracted
```

Fetch records capture-session identity, timestamp, complete file pagination, expected changedFiles count, immutable session artifacts and SHA-256. Failed pages, cap/count mismatch or missing diff produce incomplete status and nonzero exit. Ingestion rejects current incomplete/tampered capture instead of recycling old files. Existence alone isn't current evidence. An explicitly supplied offline PR JSON/diff is supported, but document source freshness and completeness; do not imply an API fetch occurred.

Ingest keeps full source facts plus representative abbreviated hunks in visible-text.txt, tokens.json and people.json. Read full diff for selected code beats. Separate opener, commit authors/coauthors, reviewers, commenters, assignees and merger; a reviewer is not necessarily a code author. Filter obvious bots, retain login-less named authors as text, and never infer endorsement. Optional credits may use two to six verified avatars; avatar failure can yield text credits, never fabricated faces. The fetch helper permits only scoped assets and GitHub avatar sources with bounded image retrieval.

## Explain the code's effect

Read [story design](references/story-design.md) for complete changelog, feature-reveal, fix-explainer and refactor-walkthrough alternatives, PR frame types, hooks, word budgets, voice mode and credits. Explain the change, not the diff's file order. Usually select two to four real, small, legible hunks. A fix story needs the prior behavior, causal change and observed/proposed outcome; distinguish a code inference from a tested behavior. A refactor distinguishes reorganized mechanism from externally changed behavior. Never turn a representative snippet into an exhaustive correctness claim.

Use [code vocabulary](references/code-vocabulary.md) for all nine code-animation blocks and the 24 documented skins, input shapes, use cases and limitations. Preserve code-diff, code-morph, code-typing and the other registry choices as distinct tools; the registry bodies are external dependencies, not bundled implementations. Validate availability before naming a submission ready. Install blocks only with required permission and once before parallel workers to avoid races.

## Visual system and production

References to `hyperframes` or `npx hyperframes` mean a verified, already-installed executable; never use them to trigger an implicit package download.

The original recipe's named claude preset is a warm editorial/navy Code Surface design, not a model/provider preference. It remains an available recipe when installed. Explicit user brand/style takes precedence. Don't claim the preset is bundled or force it on a custom request. Read [visual design](references/visual-design.md), [shared composition](../faceless-explainer/references/composition.md), [shared motion language](../faceless-explainer/references/motion-language.md) and the selected code block details. The code block owns its internal code animation; surrounding effects choreograph the surface without fighting it.

Follow the complete [frame-production contract](../faceless-explainer/references/frame-production.md), using shared-storyboard/scripts for common helpers and this owner's distinct captions/source scripts. No website capture or general captured-asset inventory is required. Storyboard asset_candidates is empty except verified supplied media/credits avatars. A code frame names its real block as focal, exact source file/hunk, source language, highlighted change, reveal sequence, explanatory copy and timing.

[Frame workers](sub-agents/frame-worker.md) receive one frame, frame.md, canvas/caption band, actual animation directory and code-vocabulary path. They cannot change the source diff/storyboard. Audio is optional per brief; real voice duration is synchronized before frames/captions. This owner retains its distinct font fallback branch: the explicit `--allow-remote-fonts` Google Fonts import remains a network-dependent option, not a substitute for verifying local requested family/weight/glyphs.

## Verification and handoff

Review code text against the frozen diff, syntax/line breaks, focus/highlight progression, before/after values and explanation of mechanism. Compare narrated claims with actual test evidence if supplied. Credits are accurate roles with appropriate consent/rights for media; no claims of participation beyond evidence. Run actual engine lint/validate/inspect and inspect boundaries/readable holds, then render and delivery-QC the requested output. Report the PR snapshot identity, final file metadata and exactly which semantic/native checks ran. Incomplete PR evidence blocks code claims even if an old MP4 remains on disk.
