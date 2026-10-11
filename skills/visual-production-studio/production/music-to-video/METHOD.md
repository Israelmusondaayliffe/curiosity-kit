# Music-driven video production

Turn one music track, optional supplied media and a brief into a complete music-led video. The track controls the timing; typography and procedural design can carry the entire film without stock assets. This method covers energetic beat-cut work, calm phrase-led work, kinetic promos, word/lyric treatments and music-grounded image/video montage. Website acquisition and narration-first stories belong to their respective production methods. Preserve an explicitly requested narration extension through the assembler's optional audio metadata, with conscious ducking and separate sync review.

Use this operation when actual composition/source or rendering is requested. A request for a music-video prompt alone does not authorize rendering, music generation, installation or upload. The name `music-to-video` remains a discovery alias.

## Load only the relevant depth

Start here and read the timing/plan references for the current phase. Select templates with `references/template-catalog.md`, or free composition with `references/motion-primitive-catalog.md`. For a plan-only deliverable, read the timing/schema and selected concept description needed to make the plan complete. At frame construction, read the entire chosen HTML including head, styles, helper scripts, shaders and local assets, plus the frame authoring contract. Planning alone does not require construction-source reads. The nine templates and 37 primitive demonstrations are substantive editable designs. Four template programs remain available. The texture-flip recipe accepts supplied licensed PNG masks; the 66 source masks are not bundled because their redistribution rights were not established. Nine additional concepts have complete composable recipes in `references/catalog-recipes.md` and its small JavaScript implementation; they are not standalone HTML examples.

The complete input/dependency manifest is `references/implementation-manifest.json`. The lifecycle and adaptation contract is `references/composition-contract.md`. Do not load all demonstration source just to choose one.

## 0. Establish the project and execution boundary

Record the user's intended deliverable, track/source, duration or selected track interval, canvas, FPS, copy/lyrics, supplied assets, brand constraints and acceptable intensity. Use a meaningful project directory, such as `videos/midnight-drive/`, inside the authorized output location. Keep all working and final assets there. Never overwrite the music source.

Discover the actual capabilities before promising render: installed Node for helpers; Python plus librosa/numpy/soundfile and FFmpeg for the analyzer; a qualified HyperFrames composition engine and browser for HTML rendering; ffprobe for output inspection. The engine/player/CLI are external prerequisites, not vendored by this operation. An installed prompt/generation tool is not an HTML renderer. If a prerequisite is absent, provide useful plan/source work and identify the exact unrun step. Do not execute `npx` in a way that silently installs a missing runtime.

Use the supplied track or extract its audio with installed FFmpeg using argument-array subprocess calls. Probe duration and available audio streams. Put the chosen audio at the project input path `<project>/assets/bgm.mp3` (supplied or explicitly staged media, not a bundled skill file), or pass its actual local path with `--bgm`; a WAV is not renamed to MP3 without encoding. Record original source, chosen interval, rights and any trim/fade. If no track exists, ask for one or propose a named music-generation/retrieval route. Provider availability or credentials do not authorize payment, sharing private material, account login, installation or a provider switch. Never ask for API keys in chat. Local generation also requires an actually available, authorized model/runtime. There is no autonomous-mode exception to those boundaries.

Initialize an engine project only when the selected installed engine needs one and no project manifest exists. Preserve an existing manifest and chosen frame rate. Stage supplied photos/video with:

`node <method>/scripts/stage-assets.mjs --from <authorized-media-directory> --hyperframes <project> --into public`

The staging helper never fetches URLs, rejects path escape/symlink escape and refuses same-name/different-byte collisions. For recipe assets, use `stage-recipe.mjs` rather than the user-media stager. It preserves the recipe graph, licensed bundled fonts and shared local vendor/runtime paths. For `held-text-strobe-burst`, first stage the recipe, then use the same `stage-assets.mjs` command with `--into music-library/references/templates/held-text-strobe-burst/assets/texture-mask-text/masks` to copy an authorized directory of licensed PNG masks. Set the existing `frames` input to the selected mask basenames and colors, for example `[{"texture":"paper","bg":"#101127","fill":"#ff5a2c"}]` for a supplied `paper.png`. Preserve the burst timing, tint, mask clipping and readiness checks. Missing frames or masks block that recipe; a plain fill is not a texture-equivalent result.

Gate: actual local audio, chosen canvas/FPS, input inventory, output location and execution status are known. Missing requested audio is a blocker; a deliberately silent source preview must be labeled and explicitly selected.

## 1. Establish one canonical audio map

Run the included analyzer once for the current audio identity, when its dependencies exist:

`python3 <method>/scripts/analyze-beatgrid.py <project>/assets/bgm.mp3 -o <project>/audiomap.json --print`

Its output includes duration/sample rate, tempo, beats/downbeats, energy phases, onset events, drum-like classifications, rolls, silences, hard stops, key moments and phrases. These are signal heuristics, including a four-beat-meter assumption. They are not guaranteed musical truth. Check salient anchors against the source; ambient, rubato, irregular-meter and weak-onset music may require phrase-led timing. Do not run competing analyses repeatedly just to obtain a preferred score.

When the analyzer cannot run, do not fabricate its output. A supplied or manually reviewed map is a supported alternative: keep `audio.duration_sec`, source identity and explicit `manual_anchors:[{"t":seconds,"source":"source reference","reason":"audible phrase boundary"}]`. Mark analysis as supplied/manual and omit unmeasured rhythmic claims. Do not claim to have listened if only metadata was available.

An input change invalidates the previous map. Keep a source hash, interval and analyzer/dependency identity with the project's analysis record. The canonical map can be corrected when evidence supports it; record the correction and revalidate affected groups instead of changing timestamps to conceal sync defects.

Gate: finite positive track duration and a source-grounded anchor map. No grid evidence means `phrase_flow`, not forced beat cuts.

## 2. Lay out frames before visual details

Read `references/frame-skeleton.md`. Create `STORYBOARD.md`, with strict inline JSON for machine-read data as shown in `references/storyboard-format.md`. Set the canvas once: landscape 1920×1080, portrait 1080×1920, square 1080×1080 or the explicit requested dimensions; preserve the actual FPS, including decimal rates.

Cut frames at meaningful musical changes: a hard stop, surge/drop, roll edge, sustained onset gap, major energy/phrase change. Usually a few distinct treatments are enough; a fast track does not require one frame per beat. Every frame names a source file, track-time `[start,end]`, matching duration, `pacing`, mood and the musical situation. Frames tile zero through track end without gaps or overlap.

`beat_cut` requires credible rhythmic anchors. `phrase_flow` follows phrase/energy changes and readable holds; do not impose per-onset swaps on it. Leave groups unfilled at this phase so structure is considered separately from copy and decoration.

Gate: complete interval skeleton, honest pacing, no invented musical claims. This skeleton is not yet a buildable plan.

## 3. Author and approve the full treatment

Read `references/planning.md`, the selected catalog and `references/montage.md` only if media is involved. Write `frame.md` from the user's brand or a genuinely available licensed preset: exact font files/families/fallbacks, type roles, palette, contrast pairs and safe regions. A missing sibling preset directory is not a reason to claim a preset was copied.

Each frame contains one or more groups, tiling that frame. Select exactly one treatment per group:

- Template: bind actual supported content/color variables and musical roles. Its demo beats are not the current audio map. Preserve distinctive composition, easing, texture and readable holds while reauthoring its schedule.
- Free design: name a dominant system plus a small compatible primitive set. One background bed at a time; generally one structural move and at most one texture. Preserve distinct mechanisms such as RGB split, colored trails, stroke-fill, mask reveal, spatial packing and in-place reveal.
- Supplied assets: beat-cut to real anchors, slow Ken Burns/crossfade for phrase flow, or a dimmed media bed under legible typography. Keep source aspect unless an explicit crop/reframe is chosen. No arbitrary on-beat cuts in a phrase-flow group.

Builds resolve on their named anchor. Use early motion for a beat landing and slightly delayed motion for a reactive entrance; don't stretch a 0.2-second accent across a whole phrase. Let silence reduce visual density. Dense strobe/flip runs are brief, with an intentional clean state afterward. Ask about flash sensitivity when the requested intensity makes it relevant; an intense strobe recipe is optional.

Write track-time anchors and role bindings, not millisecond tween choreography. Inline objects/arrays use valid JSON with quoted keys. The validator checks real anchor membership, ordered frame/group tiling, paths, template/primitive IDs and pacing conflicts:

`node <method>/scripts/validate-plan.mjs --hyperframes <project> --storyboard <project>/STORYBOARD.md --audiomap <project>/audiomap.json`

Show a short frame-by-frame treatment and approve substantive creative choices when approval is still needed. An already approved plan or explicit end-to-end construction request covers ordinary implementation/testing within its scope; don't ask again merely because a phase changed. Do not silently change copy, audio identity, visual target or provider to make a check pass.

Gate: a complete validated plan, complete brand surface and the applicable user approval.

## 4. Build one composition per frame

Use `sub-agents/frame-worker.md` as the complete authoring contract, whether one worker or several do the work. Delegate independent frames only when useful; each writer owns one file. Pass the exact frame block, audio map, brand, selected complete recipes, staged assets, canvas/FPS and output stem. Keep all audio in the root unless the explicit narration extension is in use.

Convert track time to frame-local time by subtracting the frame start. Build one paused finite master timeline. Group visibility changes are instantaneous and cover the whole group interval. Preserve head-only helpers, type measurement, shader uniforms, SVG filters and all required texture/font assets. Rename IDs, class selectors, CSS variables, SVG filter references and global helpers when integrating recipes; namespacing only IDs is insufficient. Two copies of the same recipe must remain independent.

Standalone references are isolated 1920×1080 documents. They are not components to concatenate. The included lifecycle supports font/texture readiness, explicit post-seek callbacks and disposal for those standalone pages. For a real frame, adapt those mechanisms to the engine's actual mount/readiness/seek contract and frame scope. For portrait/square, redesign wrapping, alignment and safe areas while keeping the artistic mechanism; never claim that stretching a landscape canvas is native portrait layout.

Preserve a whole score's intent: intro glyph ringing must finish; card depth/wipes retain paint order; mosaic overlays reset before a clean wall; split-lockup restores clipping/filter state after expansion; spectral rays use one registered wordmark; logo trails derive from a fixed shutter sample; type shuffles retain font-correct recentering. Remove demo-loop resets when authoring a terminal exit, while keeping the source example available.

Gate: each complete frame file has matching stem/composition ID/timeline key, exact approved duration, actual readiness behavior and no missing dependency. A file existing does not prove it renders.

## 5. Assemble and verify timing

`node <method>/scripts/assemble-index.mjs --hyperframes <project> --storyboard <project>/STORYBOARD.md --audiomap <project>/audiomap.json`

The assembler validates the plan again, checks each frame's ID/duration, stages local GSAP, retains canvas/FPS, mounts frame clips at their explicit starts and places BGM on lane 11. Root duration includes all hard-cut holds. Optional approved voice metadata uses lane 10. Frame changes are hard cuts; there is no hidden transition injector.

Missing requested music, a mismatched interval, bad canvas JSON or escaped project path fails rather than becoming a warning. `--silent` creates only an explicitly muted deliverable/preview. Never use it to conceal an absent requested soundtrack. Assembly does not resolve/render the engine's `data-composition-src` references by itself; the qualified engine must mount them.

Gate: source, audio, interval and dimensions agree exactly. Repeated assembly is deterministic for the same inputs.

## 6. Inspect and render through the selected engine

Run the actual installed engine's lint, validation and frame inspection against the assembled project. Discover its commands/version; don't assume an external CLI has a particular current syntax. Use the user-approved renderer and actual chosen FPS, not a hard-coded 30. Do not install a runtime merely to make this phase available.

Inspect zero, every frame/group boundary on both sides, the strongest surge/drop, all hard stops, long holds and the last frame. Compare cold/direct, forward, backward and repeated seeks at the same time. Verify actual font loading, glyph coverage, long/localized text, safe margins, overlay cleanup, composite alpha, visible fallback content and simultaneous render hooks. Review rhythm and soundtrack continuity in the actual video, not only stills.

Render the requested output when authorized. With ffprobe verify dimensions, rational FPS, duration/frame count, codec/container and requested audio stream. Listen/check sync where a listening capability exists; metadata does not prove it. Inspect actual representative frames and motion before calling the artifact successful. Missing browser/GPU/engine is BLOCKED or UNRUN, never PASS. State fallback mode and visual loss; a CSS field/text-only fallback is not shader-equivalent.

Deliver source when requested, the verified playable file when available, and concise duration/dimensions/FPS/audio status plus remaining limitations. Resume at the first missing gate: audio → analysis → skeleton → full plan → frames → assembly → engine inspection/render. If inputs changed, invalidate only affected evidence and rebuild the dependent stages.
