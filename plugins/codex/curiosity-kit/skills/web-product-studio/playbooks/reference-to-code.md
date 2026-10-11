# Translate a visual reference into a working interface

Use for a supplied screenshot, URL, mockup, approved generated comp or existing rendered design. [The entry](../SKILL.md) governs scope and source precedence. This method owns extraction and faithful translation; [build](build.md) owns implementation behavior and [verify](verify.md) owns acceptance. If the request is only for an image, use [design](design.md).

## 1. Preserve the source before interpreting it

Identify the authoritative artifact, version and intended view. For an image, record its actual dimensions, crop/scale and any known viewport/device-pixel ratio. For a URL, record the exact route, capture time, viewport, theme, relevant data/session state and any redirects. Do not critique a login wall as if it were the requested page. Bind saved source bytes and captures using the evidence contract; a URL or filename alone is not a stable design identity.

Inspect the complete frame/page first, then readable section and detail views. Preserve the original. A crop, zoom or annotation is an inspection derivative with a pointer to that original; it reveals the same pixels. Regeneration creates a different proposal and cannot resolve what the original secretly contained. If a source is unavailable, identify exactly what cannot be observed and continue only with stated assumptions or another approved source.

For live pages, distinguish observing from interacting. Use the selected browser adapter within the task's action/origin/data scope. Read visible content and computed styles when supported; do not infer access to source code, authenticated states or hidden APIs from a screenshot. Record what was actually inspected, including pagination or page regions not reached.

Separate three evidence classes in the working record:

- Observed: visible wording, measured bounds, actual rendered styles, an interaction performed with its result.
- Inferred: probable grid, spacing token, unseen responsive rule, likely control behavior. State the rationale and confidence where it could change the build.
- Unknown: illegible copy, offscreen section, unavailable asset, unobserved hover/error/auth state or breakpoint. Preserve the gap rather than presenting it as source fact.

## 2. Extract the whole system, from composition to detail

Do not reduce the reference to a palette and a list of components. Work through these lenses at useful image scale. Record what changes implementation, not a paragraph of taste adjectives.

| Lens | Inspect | Translate into |
| --- | --- | --- |
| Purpose and visual priority | Section job, first focal point, supporting evidence, primary/secondary action, eye path | Semantic order and priority; what must remain prominent at narrow widths |
| Content | Exact readable nav, headline, subhead, section titles, CTA, labels, prices, names/roles, captions, footer | Content inventory with source status; illegible and fictional material remain labeled |
| Typography | Family character, serif/sans/mono role, size/weight ratios, leading, tracking, case, line count/wrap, alignment | Available verified fonts or declared approximation; role tokens and responsive measure |
| Page geometry | Outer gutters, width constraints, column ratios, offsets, grid lines, header size, section ordering and heights | Container/grid rules with fluid constraints and deliberate breakpoints |
| Local spacing | Headline-to-support, support-to-action, text-to-media, card gap/padding, nav spacing, CTA grouping | Reusable spacing relationships and contextual exceptions |
| Controls | Button height/width/padding, shape/radius, fill/outline/link hierarchy, icon placement, visible states, inputs | Semantic controls and state styles; unseen states specified separately |
| Components | Card/block anatomy, shared baselines, repeated variants, badges, dividers, panel nesting, disclosure | Component boundaries driven by repeated behavior/structure, not every rectangle |
| Color | Background/surface, text hierarchy, accent/action, border/shadow tint, image grade, gradient direction | Semantic color roles and checked contrast pairs; keep intentional palette logic |
| Media | Subject scale, crop/focal point, aspect ratio, frame, overlap/bleed, transparency, layering, lighting | Original usable assets where available, responsive crop rules, meaningful alt/decorative status |
| Icons and texture | Stroke/fill weight, optical size, alignment, material/noise strength, fine lines | Consistent icon family and bounded surface treatment, with necessary assets verified |
| Depth and motion | Z-order, shadow direction/softness, perspective, anchored origin, visible timeline frames | Layer model; motion hypothesis distinguished from observed temporal behavior |
| Rhythm and density | Image/text balance, repeated versus exceptional sections, calm/dense cadence, negative space | Full-page sequence and grouping that survives componentization |

Measure ratios before pretending to know exact pixels. A 640-pixel screenshot may be scaled from a larger CSS viewport. Sample repeated alignments to infer a grid, then test the inference in the browser. Use actual DOM/computed values when legitimately available; screenshot estimates stay estimates. The goal is faithful geometry and hierarchy, not false OCR precision.

Readable text is part of the composition, but visible text is not automatically an approved business fact. Keep supplied source wording subject to the entry's content-honesty rules. Generated testimonials, metrics or contact details remain fictional even when legible. Do not solve awkward wrapping by rewriting approved copy without authority.

## 3. Decompose assets and implementation responsibilities

Map the page to semantic regions and reusable components: header/navigation, main sections, controls, media and footer where present. For each, name its content source, behavior, responsive change and comparison view. Separate page imagery from the reference image depicting the page.

Use real frontend for text, navigation, forms and controls. A full-page screenshot as a background cannot satisfy an interactive implementation. A decorative image can remain raster; a structured vector may suit SVG; a real spatial or procedural effect may require another medium under the design gate. Choose that medium deliberately instead of replacing a hard effect with a superficially similar placeholder.

For assets, prefer accessible originals from the approved source/project with suitable usage rights. Record actual paths, dimensions and intended role. If only a reference capture exists, a faithful crop may support inspection or an authorized image use, but it does not create a licensed original asset or recover obscured pixels. State a missing asset and use an explicitly approved substitute when needed. New generation is a conditional gap-filling stage in design, never an automatic prerequisite.

Keep repeated media in stable aspect-ratio frames with declared focal points and `object-fit` behavior. Reserve dimensions before load. Review the crop rather than relying on its name: the product, face or distinguishing feature may disappear on mobile. Match radius and frame logic across siblings without forcing every image into the same ratio.

## 4. Interpret responsiveness without rewriting the design

If desktop and mobile references exist, compare them directly before guessing breakpoints. Identify what stays invariant and what changes: content order, alignment, navigation, density, crop, line length, control reach and priority. Determine behavior at intermediate widths from constraints, then inspect those widths. Two screenshots do not prove every in-between state.

If only one width exists, carry the same information hierarchy into an explicitly inferred responsive interpretation:

- Let type and gutters scale within legible limits; constrain long text by measure rather than stretching it across the screen.
- Collapse columns when content requires it, preserving reading and focus order. CSS visual reordering must not create contradictory keyboard/screen-reader order.
- Move supporting visuals or details when needed; never hide a required action or fact just to match the first fold.
- Preserve the source's focal point and crop intention. A desktop side image may become a full-width supporting frame instead of a tiny thumbnail.
- Keep controls discoverable without hover. Use meaningful navigation adaptation rather than shrinking labels until they fit.
- Permit intentionally scrollable comparison tables or code regions when their job requires it, with a clear affordance and contained overflow. The whole page should not accidentally scroll sideways.
- Inspect real narrow containers, not only a device preset. A reusable card in a sidebar may have less space than on a phone.

For the first view, inspect a representative small laptop as well as the main reference size: headline, supporting context, primary action and important media should remain readable without crowding. A hero need not contain the entire product. Do not impose a universal heading line count or change approved wording to meet one. For phone chrome, keyboard, safe-area and gesture work, load [motion and mobile](../references/motion-and-mobile.md); emulated layout alone does not qualify physical-device behavior.

## 5. Implement in fidelity-preserving passes

1. **Skeleton and content:** real semantic order, section sequence, exact approved copy/data and working behavior seams. Confirm nothing requested vanished during decomposition.
2. **Macro geometry:** page width, grid, region proportions, focal media, first-view framing and section rhythm. Fix these before shadows and tiny offsets.
3. **Type and color:** install no speculative font; apply verified roles, leading, wrapping, palette and contrast. Check whether fallback rendering changes geometry.
4. **Components:** controls, cards, dividers, icon alignment, media crop, shared baselines and state variants. Remove accidental wrapper layers introduced by component convenience.
5. **Responsive and stress states:** apply the observed/inferred rules; load actual adverse content and inspect the resulting flow.
6. **Micro-craft:** optical alignment, border/shadow logic and justified motion after the identity is intact.

Use the project's conventions and native checks from build. Preserve distinctive composition, generous or dense spacing as intended, image/text balance and controlled exceptions. Do not flatten an editorial composition into repeated generic rows, or add decorative micro-labels to fill space the source deliberately leaves open. Conversely, keep a source's useful dense dashboard grouping rather than forcing marketing-page minimalism.

## 6. Compare actual output with the locked source

Capture the implementation at matched viewport, content, theme, scroll/state, font readiness and other relevant conditions. Open and inspect both artifacts; an existing filename or plausible image header is insufficient. Compare same-size views and useful overlays/diffs when available, then inspect the full page so local success does not hide cumulative rhythm drift.

Classify differences rather than endlessly tweaking:

- Material: wrong identity/hierarchy, composition, scale, content, crop, required view or behavior. Repair the responsible constraint or medium.
- Translation decision: an unseen responsive/control state implemented consistently; record and judge against the brief.
- Secondary polish: minor non-contract optical or surface refinement; prioritize by actual effect.

Use the canonical severity and high-stakes rules in verify when applicable. Pixel differences can locate a mismatch; font rasterization and dynamic content can inflate them, and a low pixel error can conceal broken behavior. A deterministic refactor-parity check preserves frozen existing pixels/states; screenshot-inspired recreation follows a selected design with explicit tolerances. Keep those two acceptance modes separate.

For a mismatch, state source observation → current observation → likely cause → smallest correction → fresh comparison. Example: all content below the title drifts down, while local gaps match; inspect font metrics and title wrapping before subtracting arbitrary margin from every section. Changed code, asset, font, reference or fixture invalidates affected evidence. Finish by exercising the controls and durable outcomes under verify, not by awarding completion from an attractive screenshot.

## Worked translations

### A. One product hero, desktop source only

Illustrative extraction: at the source width, text occupies about two fifths of the content region and a framed product occupies the remainder. The headline is the strongest text; two actions have visibly different weight. The media's focal object sits above its center. Treat these ratios as estimates until rendered.

Implementation: preserve text-first semantic order, use a constrained two-column grid, size the heading by its observed proportions, and reproduce the frame with the original product asset. At the content-driven collapse point, place actions before media; keep the focal crop visible. Label mobile stacking as inferred. Compare a small-laptop capture for first-view balance, then a narrow capture for wrapping and action reach. Do not replace this source with a newly generated hero or populate it with invented proof badges.

### B. Four-section editorial site

The source sequence is a restrained title → large image story → compact evidence list → closing action. Extract the change in density and image scale, not just four component names. The image may bleed wider than the text measure, while captions return to the text grid. Build those separate constraints rather than wrapping every section in the same card/container. At narrow widths, preserve the image-caption relationship and the list's evidence order. Compare full-page cadence after matching each section locally.

### C. Dense comparison screen with approved mobile view

Desktop aligns plan titles, prices, feature rows and actions. Mobile changes the comparison strategy rather than shrinking every column. Preserve the provided mobile structure; test long labels and missing values with visible sample fixtures. Amounts remain readable, actions remain reachable, and differences have labels beyond color. A decorative font swap or cinematic hero is outside this translation. Verify selection/details behavior separately from the matched render.
