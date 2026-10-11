# Graphic overlays on an existing video

Create transcript-timed titles, lower-thirds, quotes, data callouts, diagrams, side panels and picture-in-picture cards while the complete source clip continues playing. Design each card from the actual material, author scoped HTML, assemble one deterministic GSAP composition, and render through the available HyperFrames installation.

Use this method for “package my video”, graphic cards, kinetic takeaways and on-screen graphics. Plain spoken-word subtitles belong to embedded captions; a standalone unnarrated logo sting belongs to motion graphics. New videos from a topic, URL or PR use the relevant creation method. Retiming, recutting, recoloring, source cropping and audio redesign are separate editing requests. Moving/scaling a contained video window is supported here; it does not authorize changing the source shot or cutting its content.

## Load only what this job needs

Read this method, then [the design index](references/DESIGN_INDEX.md) and the selected style, layout and frame. For implementation, use [card authoring and animation](references/authoring.md), [composition and export](references/composition.md), and the owner-local assets/scripts. The ten style documents are previews containing reusable card subtrees, not production-ready MP4s or whole-document fragments. No nested skill or external design-framework read is required.

## 1. Establish the output and available execution

Use the user's existing brief and files. Determine source clip, intended audience, output ratio, visual direction, whether the requested result is a plan/HTML or a rendered MP4, and how dense the cards should be. Do not turn prompt-only or planning work into rendering, installation or provider calls.

When material choices are missing, ask once about ratio, layout, style group and density, bundling into the channel's supported question limit. Do not re-ask values already supplied. An instruction to choose defaults authorizes choosing a source-compatible ratio, stack layout, a tone-matched style and automatic density; briefly state those choices. A requested specific style, card count or bespoke design takes precedence over the suggested recipes.

Check the actual local tools without implicitly fetching packages:

```sh
command -v hyperframes ffmpeg ffprobe
hyperframes --help
hyperframes doctor
```

If HyperFrames is a project-local binary, resolve the installed executable there. Avoid plain `npx` that may download software. Installation, Whisper model downloads, remote services, publication and spending require their applicable authorization. Inspect the installed CLI help before relying on command/flag compatibility. Rendering needs a supported headless browser, a working local media stack and enough workspace disk. Local Whisper is the intended transcription route; “local” does not mean the selected model is already cached. Hardware browser mode can help on supported macOS systems, but must not override security or assume every host has a GPU.

If the renderer is unavailable, finish authorized planning, fragments and composition work and describe the exact unrun stage. A direct FFmpeg diagnostic is useful evidence, but is not a substitute claim that HyperFrames rendered the HTML.

## 2. Inspect the full source and retain intermediates

Work in a new, unambiguous project directory, conventionally `videos/<project-name>/`. Preserve the original clip and avoid collisions with previous exports. Retain:

- `metadata.json`: probed dimensions, duration, frame-rate fraction, streams
- `audio.mp3` or another supported transcription extraction
- `transcript.json`: flat word array with `text`, `start`, `end`
- `storyboard.json`: card timing/content planning record
- `public/cards/<card-id>.html`: individual scoped card fragments
- `public/index.html`: assembled deterministic composition
- rendered video and the final source-audio-preserving `output.mp4`

```sh
ffprobe -v error -show_streams -show_format -of json "$VIDEO_PATH" > "$WORK_DIR/metadata.json"
ffmpeg -n -i "$VIDEO_PATH" -vn -c:a libmp3lame -q:a 2 "$WORK_DIR/audio.mp3"
```

Read actual metadata; `r_frame_rate` is a fraction, not a decimal to parse loosely. Check rotation, variable frame rate, sample aspect ratio and whether audio exists. Keep the full duration. An audio-less clip may use supplied notes/visible actions or a user-supplied transcript; do not claim it was transcribed. A constant output frame rate can be chosen explicitly for rendering without changing the source playback duration.

## 3. Transcribe and correct without moving speech

With the installed CLI and an available approved local model:

```sh
hyperframes transcribe "$WORK_DIR/audio.mp3" -d "$WORK_DIR" --json --model small.en
```

`small.en` is an English-specific example. Choose an appropriate installed model for the language; do not silently translate. Confirm the observed output schema. The working transcript contract is `[{"text":"word","start":0.1,"end":0.4}, ...]`, not a `segments` or `words` wrapper. If the actual tool emits another schema, explicitly normalize to this flat array while preserving timings.

Fix supported ASR errors in word text, names, punctuation and technical terms; retain each word's start/end. Group into sentences at punctuation and meaningful pauses for planning. Flag uncertain claims rather than manufacture missing words or evidence. Clamp every card end and composition duration to media duration; ASR often overshoots the final word. Do not stretch the video to match the ASR tail.

## 4. Choose cards from the transcript

Use meaningful takeaways, explanations and visual emphasis rather than repeating every word. There is no fixed card archetype, compulsory story arc or maximum count. Quotes remain faithful; numeric claims retain units, source qualification and denominators. Sample claims, social counts and approval stamps in previews are illustrative and must be replaced or omitted.

The optional automatic pacing recipe starts with a medium-density pace:

| Source duration | Base seconds per card |
|---|---|
| Under 60 seconds | 6–8 |
| 60 seconds to 3 minutes | 8–12 |
| 3–10 minutes | 12–20 |
| 10–30 minutes | 20–35 |
| Over 30 minutes | 30–60 |

Multiply by 0.7 for rapid distinct claims/numbers, 1.0 for mixed narrative/data or 1.5 for reflective repeated ideas. The source recipe is `max(5, round(duration / (basePace × densityMultiplier)))`, with fewer ≈ 0.6× and more ≈ 1.5×. Keep the five-card floor as this named automatic packaging recipe, not a reason to disregard a requested one-card treatment or make an extremely short clip unreadable. Use a supported count and readable holds; explain an exception instead of inventing takeaways. No upper clamp is required. For example, a 121-second dense clip at 10×0.7 seconds/card yields about 17 cards; a five-minute medium-density interview at 16 seconds/card yields about 19.

For holds beyond 15 seconds, plan staged details, number builds or subpoints. Long chapters may use separate HTML sub-compositions with `data-composition-src` when the installed renderer supports them. Preserve continuous video/audio and explicit global timing; chapter chunking is not permission to recut the source.

The stable v3-style planning convention is:

```json
{
  "schemaVersion": 3,
  "composition": {"fps":30,"width":1920,"height":1080,"durationSeconds":12,"layout":"landscape","themeId":"classic","seed":42},
  "videoTrack": {"sourcePath":"input-video.mp4","startSec":0,"endSec":12,"bounds":{"x":0,"y":0,"width":1920,"height":1080}},
  "subtitles": {"enabled":false},
  "cards": [{"id":"card-01","intent":"Explain the first supported takeaway","startSec":1,"endSec":7,"accentIndex":0,"zone":"side-panel","contentHints":{"title":"A supported takeaway","detail":"A concise source-grounded explanation"},"transition":"fade"}]
}
```

This is an authoring record, not an asserted HyperFrames parser/schema. No stock CLI consumes it. Required card fields are `id`, `intent`, `startSec`, `endSec`, `accentIndex` (0–4), `zone` and `contentHints`; optional `archetype` is a free-form memory aid and `transition` is cut/fade/slide/wipe. The content bag can contain kicker, title, detail, data, quote or other useful hints. Layout/style/frame decisions are separate authoring choices, not an invented `card.layout` field. Visual design lives in HTML. Card IDs are stable and unique. Times are finite, positive-length, inside the media and normally non-overlapping; intentional overlap needs explicit track and paint order.

## 5. Resolve visual direction and paired geometry

Recommend 16:9 at 1920×1080 for source aspect ≥1.5, 9:16 at 1080×1920 for ≤0.7, otherwise 4:5 at 1080×1350. These are suggestions, not source-match guarantees or platform requirements. Both tall outputs use `composition.layout="portrait"`; geometry uses the actual width/height.

Select a layout: split for equal speaker/content weight; stack for speaker above a summary; PiP for a card-led composition; overlay for transparent/glass annotation on continuous full-canvas video. Select style by tone, not merely topic. Warm paper groups academic/editorial/whiteboard/xhs; clinical groups audit/swiss/terminal/minimal; experimental groups geom/spotlight. Bespoke styling is supported too.

Auto-frame defaults: split/stack use polaroid for warm paper, hairline for clinical, clean for experimental; PiP uses clean with its own pill chrome; overlay uses clean. Spotlight usually benefits from clean. An explicit request can alter these choices, but show the consequences of cramped portrait PiP or decoration over full-bleed video before promising it fits.

Use [geometry.mjs](scripts/geometry.mjs) to resolve the selected layout's **paired** card and video rectangles. Set the card-host bounds from that result and tween the single outer `#video-wrap` to the video bounds. Generic zones remain available for independent annotation:

- `fullscreen` and `video-overlay`: full canvas; video-overlay expects transparent surroundings
- `lower-third`: bottom 30%
- `side-panel`: right 42% in landscape, bottom 40% in portrait
- `whiteboard-area`: landscape inset 40 pixels; portrait bottom 45%

The split recipe explicitly overrides generic side-panel placement with card left/video right, or card top/video bottom in portrait. Stack explicitly overrides the generic lower-third with its matched lower card rectangle. A zone label alone never constructs a layout. Read the selected layout's header for exact values at all three ratios. PiP maintains source aspect using both dimensions, including 4:5; reserve its corner in the card content. Default `object-fit:contain` preserves the full source image. Cropping with `cover` is a deliberate source-reframing choice and needs an appropriate user request.

One outer `#video-wrap` owns stage coordinates for every frame. Clean uses no extra decoration. Hairline decoration and the video are siblings **inside** that wrapper and share its local rectangle. Polaroid uses the same outer wrapper around inset photo, caption and tape. Never apply stage coordinates to its inner photo/video. Animate or fade decorations on the same master timeline, and verify their intermediate positions.

## 6. Author, assemble and check the real composition

Build each card's readable static hero frame before animating. Extract only the chosen preview's `.card[data-card-id]` subtree. Rename IDs/selectors, replace illustrative content and adapt to actual host bounds. Use [authoring.md](references/authoring.md) for scope, all animation kinds, fonts, palettes and responsive design. Retain the style's useful composition grammar; copying a palette alone does not reproduce it.

Use [composition.md](references/composition.md) and [the composition template](templates/composition.html). Stage local fonts, local GSAP and the animation compiler. Cards contain no script or autonomous CSS animation. One paused timeline is registered at `window.__timelines["graphic-overlays"]`, built synchronously with finite duration and frame-quantized times. No random clock, timers, network assets, media `.play()` calls or infinite repeats belong in the render path. Every timed host has both `card-host` and `clip`, `data-start`, `data-duration` and `data-track-index`.

Inspect boundaries, first/last frames, all card hero states, layout transitions, bright-video readability and representative mobile-size views. Seek out of order and repeat the same timestamp to catch cursor/count-up or media nondeterminism. Check typography, glyph fallback, accidental occlusion, card overflow, PiP corner conflicts and the source's actual face/content. Technical checks do not establish visual quality.

## 7. Render, verify audio and deliver

Run the installed HyperFrames snapshot/lint/render commands supported by its help. Render at the chosen actual canvas and fps, then verify duration, dimensions, streams, continuous source playback and original audio. Use the source-audio mux guidance in [composition.md](references/composition.md); a muted browser video element is not evidence that the export has sound. Do not introduce an outro or duration extension unless requested. A neutral requested outro may hold a wordmark/tagline for roughly 1.5–2 seconds, but extending beyond the source needs an explicit ending/background/audio decision.

Deliver the requested file plus concise provenance: work/output locations, storyboard, fragments, assembled HTML, ASR model actually used, card count/pacing, and any unrun or failed checks. Do not label an HTML preview as a finished video. Preview servers and share links are optional requested follow-ons, not automatic public uploads. Preserve the workspace and source. The [MIT notice](NOTICE.md), applicable [font-license mapping](licenses/README.md) and GSAP's own header/terms stay with reused material; separate dependencies do not inherit the surrounding MIT license.
