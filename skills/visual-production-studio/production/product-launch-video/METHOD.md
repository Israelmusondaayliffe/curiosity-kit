# Product launch video

Market, launch, promote or reveal a product using a source-grounded story and its actual brand/product evidence. SaaS/app releases, feature reveals and company promos belong here; a neutral website tour belongs to website-to-video, a text lesson to faceless-explainer and a PR mechanism explanation to pr-to-video.

## Establish the product and promise

Read the supplied brief/script/URL and existing project before asking anything. Resolve the audience, one promise, proof, desired action, platform, duration, aspect/language, narration/captions, brand rules and deliverable. Never invent performance, availability, pricing, testimonials or endorsements. Exact supplied scripts and claims remain exact when requested; if the source doesn't support a promised benefit, flag it.

For a URL, use the actual website capture workflow/installed capture capability to freeze visible text, tokens, images, screenshots/video and source inventory. Capture and generation are different actions. For a supplied brief without a URL, create the source packet from it; don't pretend it was captured. Keep capture/extracted/visible-text.txt, tokens.json and an asset-descriptions.md ledger for real media. Include each asset's path, subject, shape, quality, brand/source, rights and intended role. A raw directory listing is not an asset selection.

The expected project and helper sequence are fully specified in [frame production](../faceless-explainer/references/frame-production.md). `<METHOD_DIR>` resolves to this product-launch-video directory, whose shared helpers resolve directly to shared-storyboard/scripts and whose source-specific helpers remain local. Dependencies are checked at execution; companion presets/media/animation engines are not silently installed.

## Choose the launch story

Load [story design](references/story-design.md) for full archetypes, beat mechanics, narration modes, asset selection and pacing. Preserve its alternatives: problem–agitate–solution, future pacing, demonstration, before/after/bridge, and feature→benefit. Choose from the real product and goal, not a forced universal marketing shape. A demo shows a real transition in the product; future pacing is framed as a possible experience; before/after must not fabricate measured outcomes.

Write one STORYBOARD.md and SCRIPT.md when narrated. Every frame has a narrative job, exact copy, visual scene, duration, transition, narration and named asset_candidates from the inventory. Pick assets without making the user perform routine curation. Ask only if the source is inadequate or a meaningful creative/product choice is unresolved. Keep product UI text and brand identity legible. Plan the close/CTA appropriate to the actual requested action.

## Brand and frame direction

Adopt the existing frame.md/design.md or choose an available preset. The build-frame helper remixes token roles while preserving palette geometry, font roles and caption skin identity. Verify the actual result against the product. A preset may guide composition; it must not override explicit brand rules.

Read [visual design](references/visual-design.md), [composition](references/composition.md), and selected [motion language](references/motion-language.md) recipes. Enrich the existing storyboard with video-wide direction and per-frame effects/focal/roles, preserving the accepted story/script/transition/assets. Source assets remain real: don't replace UI or logos with invented approximations. Stage named media before dispatch:

```bash
node <METHOD_DIR>/scripts/stage-assets.mjs --storyboard ./STORYBOARD.md --hyperframes .
```

Nested paths preserve identity. An ambiguous basename, missing requested media or user-owned destination conflict is a blocker. Do not stage every capture indiscriminately. The assembly backstop repeats this check.

## Build and finish

Use [frame worker](sub-agents/frame-worker.md) for complete frame construction requirements. Each worker reads only the named storyboard frame, frame.md and actual required recipe/asset bodies, and writes one HTML file. Audio can be prepared while planning but actual voice duration wins before final timing. Await caption generation before assembly; transitions are injected from canonical durations so reruns are stable.

Inspect the product hero, feature proof and CTA at readable holds and during transitions. Check UI fidelity, typography, footage continuity, claimed feature behavior, actual source attribution, captions, audio and visual hierarchy. Engine lint/inspect is necessary for native delivery and insufficient for marketing truth. Render only the requested format within authority, then run delivery QC. Deliver the current artifact and source when asked, with observed duration/dimensions/fps and any untested native engine or provider boundary.
