# Remotion → HyperFrames API Map

Source-derived mechanics retained from both pinned editions. Examples are recipes, not automatic permission to install, fetch, upload or execute source. Verify dependencies and adapters against the selected runtime; historical measurements are not current qualification. The owning METHOD.md controls semantic/loss handling.

Source-derived translation table; verify the selected runtime version and the semantic checks below. Load this reference when starting a translation
to know the high-level mapping; load the per-topic references for fragile
details (timing, transitions, etc.).

## Reading this table

- **`drop`** = remove only after verifying that the target replaces every required behavior. Readiness and side effects are never presumed redundant.
- **`see references/X.md`** = the mapping is non-trivial; read the linked file.
- **`refuse + interop`** = the skill bows out and recommends the runtime adapter
  pattern from [PR #214](https://github.com/heygen-com/hyperframes/pull/214).

## Composition root

| Remotion                                             | HyperFrames                                                                                                          |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `<Composition id durationInFrames fps width height>` | root `<div id="stage" data-composition-id data-start="0" data-duration="<dur/fps>" data-fps data-width data-height>` |
| `defaultProps={...}`                                 | `data-*` attributes on `#stage` (one per scalar prop). Nested objects/arrays — see [parameters.md](parameters.md)    |
| `schema={z.object(...)}`                             | not represented in HTML; the schema lives in the agent's translation step only                                       |
| `calculateMetadata` (sync)                           | resolve at translation time, write concrete values into `data-*`                                                     |
| `calculateMetadata` (async)                          | **refuse + interop** — see [escape-hatch.md](escape-hatch.md)                                                        |
| `registerRoot(RemotionRoot)`                         | drop                                                                                                                 |
| `<AbsoluteFill style>`                               | `<div style="position:absolute;inset:0;{style}">`                                                                    |

## Sequencing

See [sequencing.md](sequencing.md) for nesting and stagger details.

| Remotion                                   | HyperFrames                                                                                               |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `<Sequence from={F} durationInFrames={D}>` | `<div data-start="<F/fps>" data-duration="<D/fps>" data-track-index="N">`                                 |
| `<Series>` + `<Series.Sequence>`           | siblings with sequential `data-start` values                                                              |
| `<Loop durationInFrames={D}>`              | finite repetitions or modulo local-frame evaluation clipped to the composition; see sequencing.md                            |
| `<Freeze frame={F}>`                       | evaluate descendants at the fixed frame F, preserving outer visibility and nested clocks; never a no-op |

## Timing

See [timing.md](timing.md): this is the most consequential section.

| Remotion                                                   | HyperFrames                                                                                                        |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `useCurrentFrame()`                                        | drop — HF seeks the timeline. The math derived from `frame` becomes an animatable property of a paused GSAP tween. |
| `useVideoConfig()` for `fps` / `durationInFrames`          | drop — read from `data-fps` / `data-duration` on `#stage`                                                          |
| `interpolate(frame, [a,b], [x,y])` (linear)                | `gsap.fromTo(t, {p:x}, {p:y, duration:(b-a)/fps, ease:"none"})` at offset `a/fps`                                  |
| `interpolate(frame, [a,b,c,d], [x,y,y,z])` (multi-segment) | three `gsap.to` calls at offsets `a/fps`, `b/fps`, `c/fps`                                                         |
| `interpolate(..., {easing: Easing.bezier})`                | GSAP `CustomEase.create("c", "M0,0 C${a},${b} ${c},${d} 1,1")`                                                     |
| `spring({frame, fps, config: {damping, stiffness, mass}})` | GSAP `back.out(N)` — see [timing.md](timing.md) for damping → overshoot table                                      |
| `interpolateColors(frame, range, colors)`                  | `gsap.to({...}, { backgroundColor, color, duration, ease })` — GSAP handles color tweens natively                  |
| `Easing.in / .out / .inOut(power)`                         | explicit source easing function, or verified matching GSAP exponent; see timing.md                                                             |

## Media

See [media.md](media.md) for trim, volume ramps, and decoder notes.

| Remotion                               | HyperFrames                                                                 |
| -------------------------------------- | --------------------------------------------------------------------------- |
| `<Audio src volume>`                   | `<audio data-start data-duration data-track-index data-volume src>`         |
| `<Audio playbackRate startFrom endAt>` | `data-playback-rate`, `data-trim-start`, `data-trim-end`                    |
| `<Video src>`                          | `<video muted playsinline data-start data-duration data-track-index src>`   |
| `<OffthreadVideo>`                     | `<video>` — HF doesn't need the off-thread variant (uses headless Chrome)   |
| `<Img src>`                            | `<img>`                                                                     |
| `<IFrame src>`                         | `<iframe>` only after verifying the selected renderer screenshot/readiness support       |
| `staticFile("x.png")`                  | `"assets/x.png"` — copy the file into `hf-src/assets/` next to `index.html` |
| `delayRender()` / `continueRender()`   | replace the readiness barrier, then remove calls only after proving equivalent waiting            |

## Transitions

See [transitions.md](transitions.md).

| Remotion                                                                       | HyperFrames                                                                                               |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `<TransitionSeries>` + `<TransitionSeries.Transition presentation={fade()} />` | manual `gsap.to(scene, {opacity: 0/1, duration})` crossfade at the boundary                               |
| `slide()`, `wipe()`, `clockWipe()`, `fade()`                                   | HF [shader-transitions](https://hyperframes.heygen.com/catalog/blocks) package presets — pick the closest |
| `linearTiming({durationInFrames})`                                             | duration in seconds (`/fps`)                                                                              |
| `springTiming({config})`                                                       | duration in seconds, ease `back.out` — see [timing.md](timing.md)                                         |

## Lottie

See [lottie.md](lottie.md).

| Remotion                        | HyperFrames                                                                                                       |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `<Lottie animationData={data}>` | `<div id="lottie-N">` + `<script>const anim = lottie.loadAnimation({...}); window.__hfLottie.push(anim)</script>` |
| `loop` / `playbackRate` props   | translate only after checking player seek behavior; HF adapter seeks absolute time via `goToAndStop`              |
| `@remotion/lottie` runtime      | pinned local lottie-web dependency after authorization; replace the React wrapper                                                                    |

## Fonts

See [fonts.md](fonts.md).

| Remotion                                            | HyperFrames                                                                                 |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `loadFont()` from `@remotion/google-fonts/<Family>` | `@font-face` rule referencing the Google Fonts CSS, OR `<link>` to Google Fonts in `<head>` |
| Local font via `@font-face`                         | same — paste the rule into `<style>`                                                        |
| System font fallback                                | document the font-fallback divergence cost (see [eval.md](eval.md))                         |

## Parameters

See [parameters.md](parameters.md).

| Remotion                      | HyperFrames                                                                                   |
| ----------------------------- | --------------------------------------------------------------------------------------------- |
| `z.object({foo: z.string()})` | `data-foo` on `#stage` (the schema is implicit in HTML structure)                             |
| nested array prop (`stats[]`) | repeated HTML markup with per-instance `data-*` attrs                                         |
| Zod default values            | bake defaults into the HTML directly                                                          |
| Zod runtime validation        | not represented; if validation matters, validate in the translation step before emitting HTML |

## React patterns

| Remotion                                           | HyperFrames                                                      |
| -------------------------------------------------- | ---------------------------------------------------------------- |
| Custom React subcomponent (pure, prop-driven)      | inline as repeated HTML using the prop interface as the template |
| `useState` driving animation                       | **refuse + interop**                                             |
| `useReducer` driving animation                     | **refuse + interop**                                             |
| `useEffect(fn, [deps])` (non-empty deps)           | **refuse + interop**                                             |
| `useEffect(fn, [])` (mount-once side effect)       | inspect and preserve startup work, cleanup and readiness; queueMicrotask alone is not readiness  |
| `useCallback`, `useMemo`                           | inline only verified pure computations/callbacks; preserve semantics                                   |
| Custom hook (pure derivation of `useCurrentFrame`) | inline the body                                                  |
| Custom hook with state/effects                     | refuse + interop                                                 |

## Distributed rendering

`@remotion/lambda` and `@remotion/cloudrun` are deployment configuration;
orthogonal to the rendered composition itself. The skill emits these as
**warnings** (not blockers) and drops them in step 3 (Generate) with a note
in `TRANSLATION_NOTES.md`. HF is single-machine today; document the gap.

| Remotion                   | HyperFrames                                            |
| -------------------------- | ------------------------------------------------------ |
| `@remotion/lambda` import  | drop the import (warning `r2hf/lambda-import`)         |
| `renderMediaOnLambda(...)` | drop the call; note in `TRANSLATION_NOTES.md`          |
| `@remotion/cloudrun`       | drop the import + call; note in `TRANSLATION_NOTES.md` |

## When to bow out entirely

If any blocker pattern is present, recommend the runtime interop pattern from
[PR #214](https://github.com/heygen-com/hyperframes/pull/214) instead of
attempting translation. See [escape-hatch.md](escape-hatch.md).

The blockers are documented in [the source linter](../scripts/lint_source.py)
with original T4 fixtures retained in the development eval tree, not shipped as runtime assets.
