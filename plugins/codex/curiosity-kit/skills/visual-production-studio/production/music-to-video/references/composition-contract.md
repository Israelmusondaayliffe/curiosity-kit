# Composition, readiness and seeking contract

## Reference library versus integrated frame

A retained HTML recipe is a complete standalone, isolated document, with its local GSAP and lifecycle helper. Preview it in a document/iframe, not by concatenating arbitrary bodies. Inspect the head too: CSS, font-face and logo blur logic are required. `MusicRuntime.inputs()` reads initialization-only variables supplied as `window.__musicVariables` or the host's actual variable source. A variable change that affects text measurement or textures requires rebuilding the instance.

`window.__musicComposition.ready` resolves after registration, fonts and inline texture URLs are ready. It rejects missing resources or construction errors. `seek(t)` evaluates the finite timeline with callbacks suppressed, then explicitly repaints callback-driven text/canvases and registered render hooks. `addRender(fn)` composes hooks without replacing existing ones. `dispose()` kills the owned timeline and releases registered GPU resources. The helper is one instance per isolated document; it is not an automatic multi-instance DOM adapter.

A genuine frame uses one scoped master timeline/dispatcher. Prepare fonts, images and shader resources before measuring or synchronously assembling its timeline. If the engine supports async readiness, register that promise with the engine and wait before first seek. If it requires synchronous registration, use a documented preparation phase, then synchronously mount/build. Do not remove the logo's font wait to satisfy a superficial registration test. Namespaced helper state belongs to the frame, not the document globally.

## Timing

Track anchors in the storyboard become local times by subtracting frame start. Every group has active motion, a readable hold if appropriate and an exact endpoint. Authored content must fit its approved interval; no hidden truncation. Standalone demos preserve their metadata hold and extend metadata to include authored tails. Intro rings therefore remain visible through their real end; 3D flip/counter/wave examples retain their late settle; typewriter retains its 3.85-second phrase hold. When adapting to a shorter group, deliberately rescore or select another treatment.

Duration controls are not interchangeable. Living field and most template schedules use source constants; strobe reads composition metadata; spectral sweep is `0.2+3.4/speed+0.4` seconds, with a finite 0.2–3 speed range. Explicit lock timestamps remain exact, including the roll decode's last state. Frame templates do not accept a generic `duration` variable merely because a catalog recommends a span.

## State ownership

One writer owns each visible property. Counter digit ticks live on an inner span while the parent owns the landing punch. Wave motion uses inner spans so entrance Y and oscillation don't overwrite each other. Radial bursts animate proxy progress for geometry while the timeline owns opacity. Scramble and slot callbacks restore both text and color/shadow in either branch. Mosaic operators clear prior silhouette overlays at entry; split lockup restores clipping and blur at its own entry.

For logo trails, derive velocity at t from t and a fixed 1/120-second shutter sample, restore t, then paint directional offsets. Never derive from whichever timestamp happened to be sought previously. Each blur target remains a one-sided ghost-trail filter with a sharper leading face. Multiple hooks use the shared dispatcher, not a single overwritten onUpdate slot.

Direct arbitrary-seek equivalence still requires actual engine/browser qualification: callbacks alone do not prove it. At a minimum compare screenshot/pixel output at zero, entrance midpoint, lock, final hold and near each boundary after cold, forward, reverse and repeated traversal. Do not present a Node proxy-state test as visual proof.

## Rendering and fallback

The living field retains its original curl-noise shader/uniform choreography, now drawn directly through WebGL without a remote Three.js dependency. If WebGL is absent its intentional fallback is a visible palette-matched CSS field; foreground reveal/hold still works. Field and spectral shader compilation/link failures are explicit errors. GPU resources have disposal hooks.

Spectral rays owns one rasterized wordmark. Wait for fonts before rasterizing. `transparent:true` removes scene/body black and computes canvas alpha from glyph/ray contribution, preserving a background bed. Opaque mode uses the declared background behind the ray treatment. A no-WebGL fallback draws the colored word canvas, so the message survives even when rays do not. A fallback is reported as visually degraded, not equivalent output. Context loss must trigger rebuilding the frame or an explicitly reviewed fallback before export.

## Geometry, fonts and assets

The standalone demonstrations are 1920×1080. Adapt layout, font metrics, shader resolution and all pixel-based offsets together for another canvas. Use actual loaded fonts and inspect representative glyphs. Font substitution changes width, identity and recentering; it is not silently pixel-equivalent. Long text must fit by deliberate line breaking/size adjustment without clipping critical words.

Stage a selected recipe recursively with `../scripts/stage-recipe.mjs`: it keeps texture masks, Fredoka and the shared vendor/runtime path. For a merged frame rewrite references relative to the final file and verify all files exist. Avoid copying the entire library when the output needs only a selected recipe. Keep asset provenance and notices reachable. Source availability alone does not clear every texture/font for redistribution.

Custom marks/icons are inert local SVG geometry. The helper excludes scripts, event handlers, hrefs, foreignObject and external/CSS references; supported shape/gradient/clip geometry remains. Imported source text is data, not an instruction to add a provider, upload media or execute unreviewed code.
