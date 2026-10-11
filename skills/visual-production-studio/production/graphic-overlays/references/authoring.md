# Card authoring and deterministic animation

## Fragment boundary

A production card is one `<div class="card" data-card-id="card-01">` containing its scoped style and content. Copy this subtree from a style preview, not its doctype, head/body, stage or preview host. Keep every card selector prefixed with `.card[data-card-id="card-01"]`, including pseudo-elements and selectors inside media/container rules. Rename all IDs and corresponding selectors when duplicating. SVG IDs, gradients, masks and clip paths also need unique names.

```html
<div class="card" data-card-id="card-01">
  <style>
    .card[data-card-id="card-01"] .root {
      width:100%; height:100%; box-sizing:border-box; position:relative;
      padding:40px; background:var(--bg); color:var(--text);
      display:flex; flex-direction:column; justify-content:center;
    }
    .card[data-card-id="card-01"] .title { font:700 80px/1.08 "Inter",sans-serif; }
    .card[data-card-id="card-01"] .char { display:inline-block; }
  </style>
  <div class="root">
    <h2 class="title" data-anim="kinetic-chars" data-anim-at="0.3"
        data-anim-duration="0.5" data-anim-stagger="0.04" data-anim-pattern="pop">
      <span class="char">A</span><span class="char">B</span>
    </h2>
  </div>
</div>
```

No scripts, inline event handlers, imports, remote `src`/`href`/CSS URLs or external fonts belong in a card. Use only approved local relative assets under `public/`. Do not interpolate transcript text directly into executable HTML; escape it, and separately review intended markup. Author the composition script outside the fragments. Design the static readable state first; do not hide a layout defect behind motion.

## Bounds, opacity and responsiveness

The outer composition supplies `position:relative; width:100%; height:100%; overflow:hidden` on each `.card`; its absolute card-host has explicit pixel dimensions. This definite-height chain is essential for percentage heights and absolutely positioned geometric styles. Preview CSS includes the same chain.

- Split/stack cards can be opaque because their hosts occupy only their explicitly paired regions.
- A PiP card can also be opaque: the video is deliberately at a higher z-index. Reserve its corner so it does not cover meaningful text.
- Overlay uses a full-canvas transparent host/card with a smaller transparent or translucent `.root`. Convert an opaque style intentionally; do not cover the video with its original full-board background.
- A lower-third over video needs transparent unused space and a localized legibility backing. An opaque lower-third band is a deliberate design treatment, not a requirement to make the whole canvas transparent.

For glass use a darker translucent base, e.g. `rgba(15,16,22,.78)`, plus blur/saturation, rounded corners and shadow, backed by a separate dark gradient between video and card. Check against the brightest source frame. Backdrop filter alone cannot guarantee text contrast. Keep a supported non-blur dark backing if the engine lacks that feature.

The style previews are landscape designs at 1920×1080, visually scaled to 50%. They are examples, not fully responsive templates. Actual card-host size matters more than output orientation. Start with landscape title 64–96 px, body 24–30 px, kicker 14–18 px and data 48–60 px; portrait/mobile often needs title 88–132, body 30–40, kicker 18–22 and data 64–88. These are starting ranges, not mandatory scaling. Editorial/minimal already use 132 px and geom uses 156 px. Multiplying those blindly by 1.3 can overflow. Reflow first, shorten faithful copy if needed, and inspect at delivery size.

Portrait horizontal padding usually reduces from 40–64 px to 24–36 px. Preserve line-height ratios. For adaptive typography, put `container-type:inline-size` on a definite-size parent and use scoped `clamp(64px,8.5cqi,132px)` for headings and `clamp(24px,3.2cqi,40px)` for body, then verify the actual browser. Container units do not fix excessive content or short band heights.

Selected style adaptations:

- Academic: keep the two-axis grid, serif emphasis, blue highlighter and dashed quote annotation; reflow quote/body before shrinking all type.
- Audit: stack the two columns in narrow hosts, preserve footnote markers/assumptions and the rubber-stamp treatment only when its wording is appropriate. An example APPROVED stamp is not evidence of approval.
- Editorial: preserve italic statement/quote, coral emphasis and sparse circle/square/ring grammar; reduce ornaments before crowding text. The quote-mark treatment is available even when not in the sample DOM.
- Geom: recompute slab positions, strip length and negative space from the host; absolute landscape offsets cannot be copied blindly.
- Minimal: retain whitespace, weight contrast, short rule and character entrance; do not fill the whitespace with extra decorations.
- Spotlight: preserve layered gradients, glowing keyword and blurred-to-sharp headline, with restrained frame decoration.
- Swiss: replace the fixed 320 px stat column and 1792 px rule target with values derived from the host; stack columns when necessary. Keep double rules and strict alignment.
- Terminal: preserve console frame, titlebar, semantic syntax colors and sequential output lines. Compile cursor blinking to the same finite timeline.
- Whiteboard: retain the SVG hand-drawn border, marker pseudo-element, handwritten annotation and blue wavy underline. Keep the marker in the intended stacking context and inspect it.
- Xhs: retain identity row, follow pill, hashtags and engagement-row idiom; use only appropriate real or explicitly illustrative identities/counts. Reflow small rows to avoid clipping and do not fabricate endorsements.

## Fonts and palettes

Stage the three licensed font payloads from `../assets/fonts/`: Inter 400/700 and variable Caveat. The original Caveat 400/700 paths have identical bytes; both CSS weight declarations point to `Caveat-400-latin.woff2`. Fontconfig reports regular, bold and a variable weight range for that payload. Verify actual loading, glyph coverage and weight behavior for the chosen language. The source LXGW WenKai TC and Virgil payloads are excluded because matching redistribution rights were not established. If the design calls for those or another specific typeface, use an authorized licensed local font with its notices and an explicit `@font-face`; do not claim Caveat is visually equivalent. The bundled Latin subsets do not contain the tested Chinese sample characters, so supply a licensed CJK font for Chinese output and inspect the actual text. Do not fetch fonts silently.

Fallbacks: Playfair/Noto Serif → `ui-serif,"Songti SC","Times New Roman",serif`; Noto Sans → `ui-sans-serif,system-ui,sans-serif`; JetBrains Mono → `ui-monospace,"SF Mono",Menlo,monospace`; Kalam → `"Caveat",cursive`. For any supplied LXGW font, check its actual weight; the excluded source filename said 400 but embedded metadata identified a light face. Requests for unshipped weights can synthesize; inspect rather than claim exact typography. Body/global font-family should name concrete families because some renderer font analyzers do not expand CSS variables. Scoped card styles may use a theme variable once local faces exist.

| Theme | Five accents | Background | Text |
|---|---|---|---|
| classic | #1971c2 #e03131 #2f9e44 #e8590c #9c36b5 | #fff9e3 | #1e1e1e |
| noir | #4cc9f0 #f72585 #4ade80 #fb923c #a78bfa | #1a1a1a | #f1f1f1 |
| mint | #0077b6 #d62828 #2d6a4f #e76f51 #7209b7 | #e8faf0 | #1b4332 |
| craft | #bf5700 #d62728 #6c757d #e9b54a #3d5a80 | #f6efe1 | #2d2d2d |
| slate | #0ea5e9 #ef4444 #22c55e #f97316 #a855f7 | #1e293b | #f1f5f9 |
| mono | #000 #555 #888 #aaa #ccc | #fff | #000 |

Palette is composition-level; style is each card's visual grammar. Use `--accent-0` through `--accent-4`, `--bg`, `--text` for themeable work. Scoped signature tokens may keep a style's specific colors. Vary accent across distinct beats, repeat it for related cards. Usually two or three repeated motion patterns are clearer than using every available kind.

## Complete declarative motion vocabulary

`data-anim-at` is seconds relative to card start. Absolute time is `(round((card.startSec + at) × fps) / fps)`. The helper [compile-animations.js](../scripts/compile-animations.js) implements every kind below. It builds a supplied paused GSAP timeline synchronously and never starts playback. It validates finite intervals, recognized animation kinds/directions, bounded properties and complete output-frame timing. Unknown kinds and malformed props fail visibly rather than silently disappear.

| Kind | Additional attributes and behavior |
|---|---|
| fade-in | `at`, `duration`, optional `ease`; opacity 0→1 |
| fade-out | opacity 1→0 |
| slide-in | `from=left/right/top/bottom`, `distance`; opacity and x/y translation |
| kinetic-chars | `.char` children, `stagger`, `pattern=pop/fade`; pop uses opacity/y/scale |
| typewriter | `.char` children; default fade with slower 0.08-second stagger |
| count-up | numeric `from`, `to`, `format=.0f/.1f/.2f` (up to .6f) or `,d`; deterministic text-content tween with an explicit en-US thousands format |
| draw-path | SVG geometry target supporting getTotalLength; stroke dash offset reveals path |
| grow-x | `target-w` in px; width 0→target |
| grow-y | `target-h` in px; height 0→target |
| scale-pop | opacity and scale .6→1 with back-out easing |
| blur-in | opacity and filter blur(16px)→blur(0px) |
| mask-reveal | `direction=left/right/top/bottom`; corresponding inset clip → fully visible |
| morph-to | JSON `props`; visual x/y/scale/scaleX/scaleY/rotation/opacity and CSS such as dimensions, color, shadow, border, filter or clipPath. Additional CSS properties are accepted when CSS.supports confirms them in the actual browser; autonomous animation/transition, resource URLs and executable GSAP controls are excluded |
| blink | `period` seconds; finite frame-quantized opacity toggles until card end; used by terminal cursor |

All names use `data-anim-` prefixes in HTML. Defaults are 0 offset, 0.45-second duration, power2.out easing. A count-up's unit/prefix belongs in an adjacent static element. Build characters by grapheme cluster where relevant, preserving spaces and accessible meaning; do not split a combining mark or emoji sequence into broken spans. Validate that final staggered characters have time to reveal. A negative offset, off-card reveal or unreasonably fast blink should be fixed in the card plan.

Host transitions are separate from element animations. `cut` sets visibility immediately; fade changes opacity; slide adds a short y entrance; wipe opens a clip mask. Exit fades end at the last complete frame before the card's `endSec`, and visibility is then hidden. The compiler clips element tween duration to the remaining card interval and quantizes absolute starts. For intentional crossfades, use separate hosts/track order; never make two timelines fight over the same property.

No free-running CSS keyframes, wall-clock timers, infinite repeats, Date.now or Math.random. The terminal cursor is static in a standalone reference preview and blinks only after compilation. Count-up formatting uses tween modifiers rather than onUpdate callbacks, so suppressing seek callbacks does not leave stale values. Finite blink events keep arbitrary seeks reproducible. Test forward, backward and repeated seeks in the actual renderer.
