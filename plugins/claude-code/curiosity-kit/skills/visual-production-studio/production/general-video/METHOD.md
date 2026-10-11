# General video authoring

Author a custom video composition at the requested length, format and style: title cards, brand/sizzle reels, modular narratives, montages, loops, procedural graphics and combinations of media/text/audio. This is the genuine native-authoring fallback when a specialist does not fit. Preserve explicitly selected Remotion, HyperFrames or another available actual engine; migration is a separate requested operation.

Build only the requested piece. A title card does not automatically acquire more scenes, captions or music. For a small color/timing/layout edit, inspect the existing source and change that element directly, preserving unrelated timing. For a vague commission, clarify only decisions that materially affect the result: audience, destination/platform, content priority and whether one result or meaningfully different variations are wanted. Specific briefs skip discovery.

## From idea to scene plan

1. Read the project and reference assets. Existing frame.md, design.md or DESIGN.md supplies brand truth; resolve conflicting documents against user direction rather than blending arbitrarily. Record exact colors, fonts, source/rights, constraints and output.
2. Write a one-sentence visual idea tied to the meaning of the subject, not just its letters. A security tool might use perimeter/locking behavior; a meditation piece might use breath/tide. A literal sober title card is equally valid when requested.
3. Establish a compact design specification with palette roles, hierarchy, local fonts/weights, grid/safe margins and motion treatment. The optional creative recipes below preserve dense editorial detailing, restrained typography and other source approaches without imposing “8–10 elements, two unrequested” on every brief. Use the density that helps this piece.
4. For multi-scene work, expand the brief into one consistent scene plan: story/purpose, exact text, source evidence/assets, rhythm, duration, aspect/fps, tracks, transitions and audio. A single scene or minor edit doesn't need a parallel planning artifact.
5. Choose architecture. A short single-scene piece can be one file; roughly three or more hard scene boundaries or reused scenes usually benefit from modular subcompositions. Separate source authoring from cutting an already finished video. This method does not fabricate live data, camera footage or unsupported native engine features.

## Layout first, then motion

Build each scene at its most visible hero moment before adding animation. Fully size root and percentage-height ancestors. Use a full-scene flex/grid content container with padding, gap and border-box; reserve absolute positioning for deliberate overlays/decorations. A 1920×1080 design may use 120px/160px padding, but scale according to actual platform safe regions rather than blindly copying it. Never replace safe padding with bare gap.

Position delayed elements at their eventual visible places in CSS. Animate from explicit start states into that layout, with scoped IDs and `fromTo` where seek reproducibility needs explicit endpoints. Temporal reuse of one region still requires every element's own valid hero-frame position; check crossings. Glows, shadows and depth stacks are intentional overlap only when designed. The requested static/quiet hold does not need decorative motion.

For HyperFrames, load only the actual selected engine contract and needed GSAP recipes. A root composition is visible body markup; a nested one uses the engine's template contract. Register synchronously constructed paused finite timelines under matching composition IDs. Every timed media clip has stable identity, start/duration/track and source trim/volume as needed. Use CSS z-index for visual stacking until a version-specific fixture proves otherwise. Framework-owned media remains muted video plus a separate audio track; don't start it via wall-clock callbacks. No render-time network, Date.now or unseeded randomness. Count-up callbacks need seek-enabled event behavior, forward/backward tests and clamped bounds. Native Remotion instead uses its actual frame/sequence/readiness contracts; do not translate APIs merely to fit this method.

## Selected craft details

- Kinetic typography: preserve reading order, emphasis and purposeful stagger. Select entrance, scale/weight change, slam, underline or reveal according to language rhythm. Readability wins over effects.
- Title/lower-third/callout/PiP: choose anchor, hierarchy, safe area, frame and transparency; mask/subject occlusion requires actual compositing support. A CSS card is not a person matte.
- Logo/mark: use real vector/source artwork; draw-on, depth layers and scale-swap are possible recipes. Preserve geometry, lockup clearspace and final hold.
- Numbers/charts: use supplied data with labels/units/baselines; counting, bars/fills and dynamic scale must map to actual values. Don't animate a wrong intermediate number as if factual.
- Product/UI: real source screenshots or recordings, intentional camera/scroll/cursor/click behavior and readable target states. Never invent available product interactions.
- Music/audio-reactive: pre-extract beat/band/amplitude information, select restrained phrase or rhythmic mapping, and use deterministic timing. Load music-to-video for its complete specialized analysis/templates.
- Multi-scene: choose cuts, crossfades, pushes, wipes or other actual recipes based on story. Keep outgoing content visible through a transition when it supplies transition pixels. Only add independent exits where the planned boundary calls for them.
- Modular: independent scene files get one contract each; don't manually nest engine-managed timelines twice. Check source URLs relative to the loader, not just the HTML file on disk.
- Editorial detail: optional data bars, labels, registration marks, subtle material/background texture and edge anchors can reinforce a visual world. They must carry information or a conscious aesthetic role; omit them in a sparse brief.

## Media and audio

Use [media preparation](../media-use/METHOD.md) for local adoption, provenance and explicit source/provider selection. Keep local assets and fonts renderable offline. Do not generate/retrieve music for a request that didn't call for it.

Where an actual compatible media engine exists, a neutral request describes lines `{id,text,sfx}`, selected provider/voice/speed and explicit BGM mode/query. Returned audio_meta voices carry paths, duration and word timings; BGM/SFX carry local paths and cue timing. Choose retrieve versus generate deliberately, await pending output and verify requested tracks exist. Map words to captions and align audio under the selected engine; do not claim bundled audio synthesis. The frame-workflow adapter and [execution contract](../faceless-explainer/references/frame-production.md) may be used when this project adopts that actual storyboard schema, not as a universal router.

## Verify and deliver

Inspect static hero layouts, boundary frames, empty periods and peak overlap, then real playback/audio. Confirm brief fidelity, brand, content, timings, legible holds, safe regions, glyphs, clipping, alpha, source correspondence and finite deterministic seeks. Run the installed engine's lint/validate/inspect and actual render when requested. If an animation-map helper isn't installed, report that exact missing automated check and review choreography directly; don't claim a nonexistent command succeeded.

Use draft output for iteration. Fix the smallest owned source, rerun affected checks and regenerate output. At handoff supply the stable verified preview when available and the requested rendered artifact/source. Delivery-QC records observed dimensions/fps/duration/audio and explicitly distinguishes source/metadata/visual/semantic checks. A generic FFmpeg still montage is not native HyperFrames or Remotion parity.
