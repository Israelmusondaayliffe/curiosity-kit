# Composition, frames and export

## Stage a complete local dependency cluster

Use the operation directory as `METHOD_DIR` and the chosen new project directory as `WORK_DIR`. Keep asset and helper relationships together. No `agents/` host metadata, test fixtures or research history belongs in the rendered public directory.

```sh
mkdir -p "$WORK_DIR/public/assets/fonts" "$WORK_DIR/public/assets/vendor" "$WORK_DIR/public/scripts" "$WORK_DIR/public/cards"
cp "$METHOD_DIR/assets/fonts/"*.woff2 "$WORK_DIR/public/assets/fonts/"
cp "$METHOD_DIR/assets/vendor/gsap.min.js" "$WORK_DIR/public/assets/vendor/"
cp "$METHOD_DIR/scripts/compile-animations.js" "$WORK_DIR/public/scripts/"
cp "$METHOD_DIR/references/frames.css" "$WORK_DIR/public/"
cp "$METHOD_DIR/templates/composition.html" "$WORK_DIR/public/index.html"
mkdir -p "$WORK_DIR/public/licenses"
cp "$METHOD_DIR/NOTICE.md" "$WORK_DIR/public/NOTICE.md"
cp "$METHOD_DIR/../embedded-captions/licenses/third-party-licenses/fontsource/inter.txt" "$WORK_DIR/public/licenses/"
cp "$METHOD_DIR/../embedded-captions/licenses/third-party-licenses/fontsource/caveat.txt" "$WORK_DIR/public/licenses/"
```

The template is a synthetic six-second split example, not an automatic storyboard compiler. Replace duration, fps, canvas, video path, paired geometry, card contents and timing with the inspected source and authored plan. The commands retain the MIT attribution and canonical Inter/Caveat notices for a reusable HTML bundle. The exported font notices are in public/licenses. Check the [dependency notice mapping](../licenses/README.md) before redistributing other bundled assets; staging does not establish their clearance. Never copy a source fixture containing a private asset just because it exists.

Sparse source keyframes can make timestamp seeking inefficient. If observed, create a workspace-only staging copy with a roughly one-second keyframe interval: for 30 fps, `-g 30 -keyint_min 30 -sc_threshold 0`. This does **not** make every frame a keyframe; all-intra requires `-g 1` and much more storage. Re-encoding is not bit-identical preservation. Do not change playback speed or add `-r` blindly to variable-frame-rate source. Inspect actual rendered motion and end time.

```sh
ffmpeg -n -i "$VIDEO_PATH" -c:v libx264 -crf 18 -g 30 -keyint_min 30 -sc_threshold 0 \
  -pix_fmt yuv420p -movflags +faststart -an "$WORK_DIR/public/input-video.mp4"
```

The above deliberately stages picture only. Keep original audio separately for final muxing. If the renderer is known to ingest an audio track, use one documented audio route and verify it; never mix two duplicate source-audio tracks. For a source that is already reliably seekable, staging a copy without re-encoding may suffice.

## One coordinate owner, one timeline

`#stage` has fixed width/height, clips overflow and declares `data-composition-id="graphic-overlays"`, `data-start="0"`, `data-duration`, `data-fps`, `data-width`, `data-height`. Source video begins at zero and spans the complete source duration. `#video-wrap` is the only video/frame stage-coordinate target. The video itself fills its local viewport with `object-fit:contain` and `playsinline`.

Each timed card host has `class="card-host clip"`, explicit bounds, hidden initial visibility, start/duration and track index. Its child `.card` fills the host. Use `data-duration`, not data-end; use `data-track-index`, not data-layer. CSS z-index controls ordinary browser paint order as well: PiP video 4 > card 2; overlay video 1 < legibility gradient 2 < card 3. Track index alone is not a replacement for CSS paint order.

Resolve paired geometry with [geometry.mjs](../scripts/geometry.mjs) during authoring. It is an ES module for local Node or supported authoring tools, not an async render dependency. Write its numbers into the assembled HTML/GSAP script. `zoneBounds` returns the independent annotation zones; `layoutBounds` returns matched video/card geometry plus the overlay glass rectangle. These two interfaces intentionally differ for split and stack.

```js
const tl = gsap.timeline({paused:true});
GraphicOverlayAnimations.compileCard(tl, document.querySelector('.card-host'), {
  startSec:1, endSec:7, fps:30, transition:'fade'
});
// A separate authored layout transition on the same timeline:
tl.to('#video-wrap', {left:960, top:0, width:960, height:1080,
  duration:0.6, ease:'power2.inOut'}, 7.5);
window.__timelines = window.__timelines || {};
window.__timelines['graphic-overlays'] = tl;
```

Initialize the wrapper at the first scene's rectangle. Prefer transforms for ornamental motion, but explicit wrapper dimensions/position are appropriate when changing video layout. Avoid simultaneous overlapping tweens on one target/property. Complete a geometry change in a gap where possible, or explicitly design the card/video overlap during the change.

## Frame DOM contract

[frames.css](frames.css) supplies reusable frame chrome. Apply its styles to the outer `#video-wrap`. Children use local coordinates; they never receive canvas coordinates. Set `--frame-scale` to `min(1, outerWidth/480, outerHeight/360)` for small polaroids, matching `frameInsets` in geometry.mjs. Recompute that value for a changed frame size or transition chrome opacity to avoid abrupt small-frame decoration changes.

Clean:

```html
<div id="video-wrap" class="video-wrapper frame-clean">
  <div class="video-viewport"><video src="input-video.mp4" muted playsinline></video></div>
</div>
```

Hairline keeps the video viewport and decoration as siblings **within** the common outer wrapper, so moving the wrapper moves both:

```html
<div id="video-wrap" class="video-wrapper frame-hairline">
  <div class="video-viewport"><video src="input-video.mp4" muted playsinline></video></div>
  <div class="hairline-deco" aria-hidden="true">
    <span class="tick tl"></span><span class="tick tr"></span>
    <span class="tick bl"></span><span class="tick br"></span>
  </div>
</div>
```

Polaroid uses a white inset card, locally inset photo viewport, broad caption area and upright striped blue washi tape:

```html
<div id="video-wrap" class="video-wrapper frame-polaroid" style="--frame-scale:1">
  <div class="polaroid-card">
    <div class="video-viewport"><video src="input-video.mp4" muted playsinline></video></div>
    <div class="polaroid-caption">A source-grounded label</div>
  </div>
  <div class="washi" aria-hidden="true"></div>
</div>
```

The polaroid outer rectangle includes the white card, caption and tape; the photo rectangle is smaller. Keep all upright as this recipe's design choice. Do not infer a personal user preference from upstream design history. Source video remains contained in the actual photo rectangle. Fade chrome before switching to clean PiP or overlay; animate any frame change on the master timeline. Changing class names must not accidentally remove `video-wrapper`, clip semantics or source-video timing attributes.

PiP adds `.pip-pill` to clean framing: 14 px radius, white/black ring and shadow, with video above card. Decorative polaroid/hairline frames are normally reserved for split/stack. Full-bleed overlay suppresses decoration and uses the independent legibility layer. If source/canvas aspect differs, “full-canvas viewport” still letterboxes with contain; true full-bleed cropping needs an authorized reframing decision.

## Render and inspect

These are source workflow command forms; confirm against the installed CLI:

```sh
hyperframes snapshot "$WORK_DIR/public" --at 5
hyperframes render "$WORK_DIR/public" --skill=graphic-overlays -o "$WORK_DIR/rendered-picture.mp4" --fps 30
```

A snapshot tool may choose its own output path; use the actual returned path. Run installed lint/doctor checks if supported. Build synchronously; no async setup, promises, autoplay or timers in the composition. Fonts/assets must be local and staged before render begins. Explicitly verify browser feature support for backdrop-filter, text stroke, box-decoration-break, container units and color-mix if used.

Inspect actual pixels at start/end, every card's readable state, onset/exit, each layout transition and a bright source frame. Check full-source motion instead of a frozen frame under animated cards. Compare arbitrary repeated seeks, including cursor and counters. For dense or non-Latin material, inspect the actual target glyphs and line breaks. A successful render exit is insufficient.

## Preserve source audio and duration

A muted HTML video is useful for deterministic visual rendering, but does not promise audible output. Explicitly restore original audio when the renderer did not do so. For an MP4-compatible source audio codec, prefer copying its stream:

```sh
ffmpeg -n -i "$WORK_DIR/rendered-picture.mp4" -i "$VIDEO_PATH" \
  -map 0:v:0 -map 1:a:0? -c:v copy -c:a copy -t "$SOURCE_DURATION" \
  -movflags +faststart "$WORK_DIR/output.mp4"
ffprobe -v error -show_streams -show_format -of json "$WORK_DIR/output.mp4"
```

Check container compatibility first. If audio copying is impossible, document an explicit compatible transcode such as AAC rather than claim bit identity. Do not use `-shortest` as a substitute for validating a prematurely short picture render. Original offsets, multi-track language requirements, silence and rotation need source-specific handling. Verify the final streams and audible beginning/middle/end, no doubled audio, no drift, correct source duration within frame/codec tolerances and no unintended black tail. An audio-less input stays audio-less unless adding audio was requested.

Requested preview servers are local, temporary and use the installed supported preview command. Public sharing or upload is a separate action. Deliver actual outputs and intermediates with concise verified limitations, then leave the original and work directory intact.
