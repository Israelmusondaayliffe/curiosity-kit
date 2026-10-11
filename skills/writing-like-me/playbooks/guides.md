# Setup, onboarding and confirmed learning

Guides are host-local runtime inputs, never packaged personal content. Read [context](../references/context.md) and the exact [CLI contract](../references/cli.md). A blank or sparse guide cannot delay drafting from the current brief. No setup runs merely because TASTE.md is missing or a template has unanswered sections.

## Setup a writing home

Use the explicitly selected destination. If absent, use an actual project-designated writing home; do not infer one from CODEX_HOME, CLAUDE_CONFIG_DIR or the other host. Ask for a path only when setup/save needs it. Inspect existing instructions and files without reading unrelated personal material.

Preview `wlm.py init --home PATH`. The minimum surfaces are VOICE.md, STYLE.md, examples/ and drafts/. Only after actual setup authorization use --confirmed. A nonempty destination needs inspection and explicit --add-missing; existing files must survive. The helper rejects source/cache and symlink paths but does not create authorization. If interrupted, inspect partial creation and retry only missing items. Never claim it atomically created the whole home.

Do not add TASTE.md, context.md, published/, .status.yaml or another tracking system. Existing artifact conventions win. In a new home, a piece may have drafts/<piece-slug>/ for its sources, notes and versions; create only what is useful. An additional manually requested home does not automatically require a new interview.

## Onboarding or recalibration

Begin with maintained guides and writer-selected examples. Ask only consequential unresolved questions: how sentences sound, what standards the piece must meet, reader/publication, favored or disliked moves and workflow preferences that actually change the work. An immediate writing task can itself supply calibration evidence; no fixed interview length applies.

Keep two destinations:
- VOICE: syntax, diction, cadence, register, tone, punctuation, sentence moves and evidenced expressive habits.
- STYLE: argument, evidence, structure, audience promise, explanation and readiness requirements.

Split feedback that changes both into atomic rules. Do not duplicate global guidance unless a local override is needed. Full examples live in examples/ only when selected; short guide excerpts identify the move and source. Published language is directional, not reusable copy.

Build a sentence-level vocal score: how a sentence accumulates, qualifies, corrects, releases or lands; variation in length; diction/register; punctuation; humor or asides only when evidenced. Attach a source cue to each material rule and distinguish recurring behavior from topic-specific choice. Broad “smart/authentic/warm” labels need observable instructions. Preserve mixed signals rather than choosing a personality for the writer. Do not ship a prebuilt personal profile as a fallback.

Legacy TASTE migration classifies existing rules into VOICE and STYLE, flags ambiguous/conflicting rules and preserves TASTE until its deletion or archival is specifically approved. Templates are starter shapes, not facts about the writer or mandatory complete forms.

## Save or prune a lesson

At delivery or a finish cue, consider useful new evidence, without a per-session quota. Classify it as explicit enduring preference, recurring supported pattern, one-piece choice or tentative inference. A selected draft does not approve every inferred trait; quoted material and rejected model drafts are not evidence of the writer's personal voice.

Show the exact narrow addition, revision or removal, its source cue and destination. Confirm before saving; an explicit request to remember a specified enduring preference counts when scope and destination are clear. Do not infer consent from a general positive reaction to the draft.

Re-read the guide, merge rather than append duplicates, preserve user edits and contextual exceptions. Put a proposed complete replacement in a task-owned temporary file. Run `wlm.py guide --home PATH --guide VOICE.md --proposed FILE` (or STYLE.md) for a diff and hash, then use --confirmed --expected-sha256 HASH only for the confirmed content. Use missing for a new file. Drift blocks the write; revise from fresh bytes and reconfirm materially changed proposals. Retain backup/recovery evidence and report the actual saved rule/path, or the failure. A proposal alone is not memory.

Never synchronize another host, modify source/cache/installed skills, edit ABOUT-ME or SOUL, or publish lessons as a side effect. Broader workflow improvements may be proposed to the user; no sibling compiler is required. Closing an app does not trigger background learning.
