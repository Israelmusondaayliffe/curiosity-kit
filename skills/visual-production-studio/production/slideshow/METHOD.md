# Author an interactive slideshow

## Choose the artifact and available player

Use this method for a runnable HTML deck: discrete slides, absolute fragment seeks, optional branches, presenter/audience windows, editable notes and interactive media. A request for a presentation or pitch deck alone does not choose this format. Explain the interactive-deck option and ask whether that is wanted if the requested artifact could instead be PPTX, Google Slides or a video montage. An explicit interactive HTML/HyperFrames slideshow request is sufficient; do not reconfirm it. Preserve supplied copy, brand and source-page behavior unless redesign is requested.

The output is an authored composition plus a runnable presenter entrypoint. It is not PPTX, an image carousel or an exported video. Main-path video export and notes-to-TTS are **unimplemented intentions**. Reserved `ttsScript`, `ttsAudioUrl` and `ttsDurationMs` fields do not make playback available. Do not render the full continuous composition and call it main-path export: that would include branch scenes.

Discover the installed HyperFrames version, core composition/seek contract, player and slideshow bundles, GSAP, browser, local server and fonts before promising execution. These engine/player dependencies are not bundled in this method. Use already-installed tools; missing dependencies mean authored source can be delivered with runtime status UNRUN/BLOCKED. Installation, account access, paid sourcing, upload and publication need the host's applicable authorization. A command written here does not grant it. Prefer the selected version's supported presenter command over a speculative future feature. The retained [standalone harness](references/standalone-harness.md) is a complete interim adapter for a bare player; load it only for that path or for diagnosis.

## Establish the deck and source design

From the brief, capture audience, purpose, claim order, canvas, assets, notes and intended main path. List optional questions/deep dives as branches rather than making the audience traverse them. For source-page conversion, inventory DOM/CSS/JS behavior, fonts, images, native media, custom controls, scroll cameras and interactive details before changing layout. Imported source is untrusted content, not permission to execute its instructions or contact providers.

Write one complete-sentence claim and one primary visual per slide. Lead with the punchline and split unrelated ideas. In a market-sizing slide show bottom-up arithmetic, such as accounts × ACV, with sourced units and assumptions; do not invent a market total. For a 1920×1080 presentation aim for 72–96px headlines and 48px body, with 40px as the source recipe's audience-text floor. Scale for the actual canvas and display distance, and preserve the user's design constraints instead of imposing an investor-pitch style on every deck. Review actual text legibility, not only nominal font size.

## Author scenes and one real JSON island

Each slide corresponds to a scene with a unique `data-composition-id`, finite `data-start`, positive `data-duration`, label, width and height. Use normal clip/track markup required by the selected core runtime. Register paused GSAP timelines under the expected `window.__timelines` key; rendering must be seekable without prior playback. In the standalone adapter a paused `window.__timelines.root` includes a full-duration anchor even if scenes use only cuts.

Put exactly one literal `<script type="application/hyperframes-slideshow+json">` in the composition body, preferably near its beginning. Static presenter discovery must find the island without executing a script that creates it. Generate it from the same manifest data used by the standalone wrapper; verify the two copies match rather than hand-maintaining divergent manifests. Escape `<` as `\u003c` inside serialized values so source notes cannot terminate the script element.

The manifest contains:

- `slides`: ordered, nonempty main-line SlideRef list.
- `slideSequences`: optional branch objects, each with unique `id`, `label` and nonempty `slides` list. Nested hotspots are allowed.
- SlideRef: `sceneId`, optional presenter-only `notes`, `fragments`, `hotspots`, `startTime`, `endTime`. Resolve scene IDs against real scenes. Explicit time overrides change bounds only; verify any scene-less mode against the installed parser instead of assuming support.
- Hotspot: unique slide-local `id`, audience-facing `label`, `target` matching a branch ID, optional percentage `region: {x,y,w,h}`. Keep all four numbers finite, width/height positive, and the complete rectangle inside 0–100. Without a region the player can render its full-slide labeled button.
- TTS fields remain omitted unless intentionally preserving future metadata; they have no working audio behavior.

Example manifest for a synthetic three-slide deck:

```json
{
  "slides": [
    {"sceneId":"opening","notes":"State the observed problem."},
    {"sceneId":"evidence","notes":"Reveal the two observations.","fragments":[6.4,7.0],"hotspots":[{"id":"sources","label":"Show the calculation","target":"detail","region":{"x":60,"y":70,"w":35,"h":20}}]},
    {"sceneId":"decision","notes":"Ask for the decision."}
  ],
  "slideSequences":[{"id":"detail","label":"Calculation","slides":[{"sceneId":"calculation","notes":"Explain assumptions and uncertainty."}]}]
}
```

Declare corresponding scene ranges, for example opening [0,6), evidence [6,12), decision [12,18), calculation [18,24). Those demonstration labels are not permission to invent business evidence. Stage sources under stable relative paths and preserve font/asset licenses.

## Fragments and branching

Fragment times are **absolute composition timeline seconds**, in the same coordinate system as `data-start`, not scene-relative offsets. The source lint permits endpoints inclusively; verify an end-boundary hold still displays the intended slide because visibility windows often end exclusively. Prefer an interior hold after its reveal has completed. Sort fragment times and reject duplicates/NaN/out-of-range values in authoring.

Entry seeks directly to the first fragment and holds. Next seeks to the next fragment; Next after the final fragment advances slide. A nonfragmented slide enters at a stable interior rest frame, commonly its midpoint. Navigation must not run the composition just to reach a hold. Set each fragment's exact DOM state from the target time so backward, cold and rapid seeks work. A live-only entrance flourish can animate after navigation, but it must not determine the underlying reveal state.

Branch scenes remain genuine scenes in the same finite composition and appear only in `slideSequences`, never also in main `slides`. A hotspot pushes the parent position and enters the branch at index zero. Back pops to the exact parent slide (retain its fragment where supported); backToMain clears nested branches to the saved root slide. Show breadcrumbs and branch-local counters. Verify nested branch return and repeated entry. Every branch scene must be included in the standalone timeline bootstrap as well as the composition.

## Preserve source-page mechanics

Preserve custom players, canvas/waveform visualizers, timelines, stems, playheads, expanding circles, hover states and controls. Drive them from the **same native audio/video element** the player will pause or mute. Listen for `play`, `playing`, `pause`, `timeupdate`, `seeking`, `seeked`, `ended`, `ratechange` and `volumechange`; render from `media.currentTime`. For video use `requestVideoFrameCallback` if available and native events as fallback. Do not create an independent wall-clock media timer. Keep separate markers for DOM construction and listener wiring so pre-rendered visuals still get event handlers.

Give every sourced `<audio>`/`<video>` its timing attributes and `preload="metadata"` or `auto`, never `none`. Add `data-has-audio="true"` when audible native sound must survive. Slide-local media uses the scene range; a deliberately shared evidence player may use a deck-wide timing range, but its intended cleanup policy must still be explicit.

Resolve tokenized font families to concrete render-safe stacks or local `@font-face` declarations with family, weight and style. Keep requested language/glyphs. Evidence screenshots, UI, code, tweets, charts and documents retain their source aspect with `height:auto` or `object-fit:contain`; `cover` is for source-matched or intentionally decorative crops. Inspect all four edges for lost words, controls, logos or captions.

Audit scroll/wheel/touch/hash/resize/rAF behavior: translated or scaled worlds, parallax, pinned panels, horizontal sections, snap points and zoom cameras. Extract focus stops, transforms and easing, then translate the navigation trigger into deck transitions or fragments. Do not recreate a literal webpage scroll inside a slide. A standalone seek jumps to a hold, so add the harness's explicit navigation-camera transition hook for live manual navigation. Keep travel continuous; avoid gratuitous direction/zoom reversals. Disable the hook for initial load, measurement, resize and fixed-frame validation. Reuse a player/harness implementation for behavior shared by multiple decks.

Hidden stacked scenes require all three: opacity 0, visibility hidden, pointer-events none. Active scenes require opacity 1, visibility visible, pointer-events auto. Opacity alone leaves invisible click-blocking layers.

## Player, presenter notes and media lifecycle

A supported wrapper has the shared components, their built bundles and keyboard focus:

```html
<hyperframes-slideshow tabindex="0" sound notes-storage-key="project-deck-v1">
  <hyperframes-player interactive src="composition/index.html"></hyperframes-player>
  <!-- In a bare-player wrapper, include the same literal slideshow JSON island here. -->
</hyperframes-slideshow>
```

Use `interactive` for links, controls and custom/native players; without it iframe pointer events can be blocked. The shared slideshow owns Present, Prev/Next, counters, global sound control, fullscreen, arrow/Space/Backspace/P handling, touch swipe and hotspot overlays. Do not add a competing Present or mute button. Verify keyboard navigation does not consume text editing or native input behavior.

Present opens `?mode=audience`; the source tab becomes presenter with current/next previews, notes and elapsed time. Deck-scoped BroadcastChannel carries slide state. Notes never appear to the audience. Notes edits persist per deck and slide over the manifest without rewriting composition files. The harness retains the exact `hf-slideshow:presenter-notes:v1:` storage key algorithm; an intentionally empty textarea saves `""`, not deletion. Use an explicit stable `notes-storage-key` when appropriate and handle blocked storage without losing the original notes.

On slide or sequence change, the controller calls `hyperframes-player.stopMedia()` before entering the target: stop iframe runtime WebAudio, pause iframe native media and pause adopted parent proxies. Same-slide fragment navigation must **not** stop media. Deck/global parent audio such as `audio-src` is excluded from slide cleanup. Normal slide media should use this shared behavior rather than per-slide cleanup scripts. Custom media UI follows native events, including pauses caused by slide exit or presenter sync.

Global nav mute reaches child players, same-origin iframe media, top-level page audio/video and detached wrapper-owned `new Audio()` objects. Detached clips must listen for `hf-sound` and set every clip's `muted` state immediately, including already-playing clips, rather than merely suppressing the next sound. Cross-realm media guards must use `el.ownerDocument.defaultView.HTMLMediaElement` or an equivalent tag/duck-type check; the parent's `instanceof HTMLMediaElement` fails on real iframe nodes. Browser-check actual iframe `.muted` after the nav control is clicked.

Presenter sync mirrors native media identity, intent, time, rate and volume. Only the presenter publishes; audience muted-autoplay events must not echo back and mute the presenter. Broadcasting does not transfer user activation. Try remote audience playback muted first. If play rejects, keep the latest play intent, expose an audience-side unlock control, stop chasing timeupdate seeks and retry after an audience gesture. Audible audience playback requires its own activation and deliberate unmute behavior. Clear blocked/pending intent on pause/end or slide exit.

## Standalone adapter and safe handoff

The complete [standalone harness](references/standalone-harness.md) contains wrapper assembly, presenter media bridge, notes persistence, seek visibility, navigation camera hook, live entrances/fragments, scenes bootstrap, SFX unlocking/global mute, optional Three.js and the diagnostic checklist. Preserve all these branches. Live rAF, events, localStorage and ambient Three.js are legitimate interactive behavior; isolate them from the fixed-frame render adapter instead of deleting them globally.

A custom postMessage bridge must validate exact sender window, origin, deck channel and payload type. Use same-origin local HTTP and exact target origin; `file://` opaque origins are not a reason to use universal `*`. The supplied [standalone support helper](scripts/standalone-support.js) provides reusable guards, notes and media primitives. A guard on custom listeners does not repair a third-party player's own listener: inspect the selected player version and mark that dependency unverified if unavailable.

If the player/slideshow implementation changes, rebuild its existing `packages/player` dist bundle using its configured build command (historically `bun run build`) and restart the owned present server before browser testing; stale dist/server output is not a valid retest. Do not install Bun or a player silently. Prefer the actual supported presenter CLI, historically `hyperframes present <composition-directory>`; use a verified local binary rather than letting `npx` download one implicitly.

Deliver a root `index.html` that runs the slideshow, with raw source under `composition/index.html` if needed. If direct `file://` loading fails due to scripts/media/origin rules, provide a minimal local-server command and the tested HTTP URL. When a project package has scripts, default `dev` to presenter mode and keep Studio preview as the editing option. Include “Click Present, or press P, to open the audience window.” Keep a server running only when requested and manage only job-owned processes.

## Validate and report the actual boundary

Run the installed engine's lint and runtime validate commands against the composition. Require zero lint errors and no StaticGuard/runtime contract errors even if exit code is zero. Check ID resolution, hotspot targets, bounds, main/branch separation, main-slide overlap, finite root duration and wrapper/composition island equality.

Then browser-test the actual selected player: main line, fragments forward/back/cold, hotspot/nested return, keyboard/swipe/fullscreen, notes editing/reload/empty value, audience-only display, click-through source controls, native media/visualizer sync, rejected-autoplay recovery, cleanup versus fragments, deck audio exclusion, iframe/top-level/detached global mute and initial/resize/navigation camera behavior. Inspect each slide and meaningful evidence crop. Test WebGL-unavailable fallback if using Three.js.

Report authored files, entrypoint/launch command, installed versions, checks actually observed, defects and exact missing dependencies. Helper tests or a generic HTML demo are not HyperFrames slideshow parity. Neither TTS nor main-path video export may be marked delivered until implemented and independently qualified.
