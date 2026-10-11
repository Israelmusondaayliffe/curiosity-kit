# Graphic overlay design library

Choose a tone, then how much canvas the speaker versus content needs, then compatible frame decoration. Read only the selected resources. Ten styles × four layouts × three frames describes 120 nominal design combinations, not 120 prevalidated outputs. All require source-grounded content and inspection at the actual host size.

## Layouts

- [split](layouts/split.html): equal card/video halves; card left in landscape, above in portrait. Both rectangles are explicit, overriding the generic side-panel zone.
- [stack](layouts/stack.html): speaker above a full-width takeaway; explicit paired card bounds override the generic lower-third zone. Landscape top video is 1892×548 inside margins; portrait source-height targets are 844 at 1080×1920 and 593 at 1080×1350.
- [pip](layouts/pip.html): content owns the full canvas and an aspect-preserving video pill sits above it in a reserved corner. All four corners are supported. Keep clean frame/pill chrome by default.
- [overlay](layouts/overlay.html): full-canvas source viewport, independent dark legibility gradient and smaller glass card; unused card surroundings remain transparent.

The three standard canvases are 1920×1080, 1080×1920 and 1080×1350. Tall canvases use the portrait planning label. Each layout header covers all three ratios. [geometry.mjs](../scripts/geometry.mjs) resolves arbitrary positive dimensions and source aspect. Do not scale only PiP height for 4:5. Use object-fit:contain unless source cropping was requested.

A layout is an authoring recipe, not a renderer primitive. Its card zone is one of five descriptive placement categories. Actual paired pixel bounds go on the card host and outer video wrapper; the storyboard has no per-card layout field and no stock CLI parses it.

## Styles

| Style and preview | Distinct construction | Typical use and caution |
|---|---|---|
| [academic](styles/academic.html) | Warm paper, two-axis notebook grid, serif type, blue kicker/highlighter, mono timing, dashed coral quote, character emphasis | Reflective explanation, interviews, analytical context; preserve annotation hierarchy |
| [editorial](styles/editorial.html) | Cream, huge italic serif statement/quote, coral first-letter accent and square, yellow dot, blue ring, highlight strip | Quotations, emotional takeaways, announcements; Playfair is not bundled, use the documented serif fallback |
| [minimal](styles/minimal.html) | Black-on-white hierarchy, weight contrast, 132 px example headline, broad whitespace, short black rule, character-pop entrance | Quiet, precise emphasis; keep its restraint |
| [spotlight](styles/spotlight.html) | Layered purple gradients, glowing kicker dot/keyword, dramatic serif headline, blur-in, off-white body | Emotional or cinematic moments; clean frame avoids colliding decoration |
| [geom](styles/geom.html) | Black ground, chartreuse and pink opposing slabs, rotated white stripe, heavy outlined type and negative space | Punchy launches/highlights; recompute absolute shapes for the actual host |
| [whiteboard](styles/whiteboard.html) | Warm paper, Caveat handwriting stack (licensed supplied CJK font when needed), jittered SVG border, orange kicker, yellow marker, blue wavy annotation | Teaching and hand-drawn reflection; verify target glyphs and marker stacking |
| [audit](styles/audit.html) | Lined/radial manila paper, ruled report header, two-column justified serif, footnote markers, tilted red stamp and assumptions | Investigative/financial/report tone; stamp text and metrics are illustrative, not verified approval |
| [terminal](styles/terminal.html) | Dark monospace console, bordered window, file-path titlebar, semantic green/amber/magenta/blue syntax, sequential output and blinking cursor | Engineering rigor; blink must use the finite master timeline |
| [swiss](styles/swiss.html) | Double rules, mono issue/time, strict headline/stat grid, sans headline and red emphasis/slab | Data-led precision; fixed example columns and rule length need actual-host reflow |
| [xhs](styles/xhs.html) | Cream/pink social format, gradient avatar, identity/subline/follow pill, hashtags, heart/comment/save/share row | Social/lifestyle packaging; identities and counts must be grounded or clearly illustrative |

These are complete preview HTML documents. Extract only their scoped `.card[data-card-id]` subtree for a real card. The preview wrapper supplies definite sizing and 50% display scale. Declarative motion does not execute in the static previews. Copying a full document into a card would import global CSS and duplicate wrappers.

## Frames

- [clean](frames/clean.html): deliberate absence of decoration. Default for full-canvas overlay and PiP; PiP may add its own rounded pill ring/shadow.
- [hairline](frames/hairline.html): two inset strokes, accent halo and four explicit corner spans, all kept aligned by a shared outer video wrapper.
- [polaroid](frames/polaroid.html): white card, inset photo, broad Caveat-caption margin and upright striped blue tape. The outer wrapper includes the chrome; the inner photo has local coordinates.

Production [frame CSS](frames.css) and [composition instructions](composition.md) use one geometry owner. Fade or move decoration with the same paused timeline. Do not independently tween an inner photo to full-stage coordinates.

## Starting combinations

Interview/dialogue: academic × stack or audit × split. Launch: editorial × overlay or geom × PiP. Analysis: audit × split, Swiss × stack or terminal × PiP. Social portrait: xhs × overlay or editorial × stack. Tutorial: terminal × split or whiteboard × PiP. Emotional narration: spotlight × overlay or whiteboard × overlay. Restrained presentation: minimal × split or Swiss × overlay.

Use warm-paper styles (academic/editorial/whiteboard/xhs) with polaroid on split/stack; clinical styles (audit/swiss/terminal/minimal) with hairline; experimental geom/spotlight with clean. PiP/overlay normally use clean. These recommendations can be changed for the brief; a cramped or overlapping combination needs redesign rather than blind copying.

Read [authoring.md](authoring.md) for responsive typography, local-font fallbacks, palettes, card isolation and complete animation declarations. References supply design methods, not factual content, verified glyph coverage or universal responsive behavior.
