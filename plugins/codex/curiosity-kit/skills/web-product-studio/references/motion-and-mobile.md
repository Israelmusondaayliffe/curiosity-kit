# Motion, gestures and mobile craft

Load for a real interaction, motion-review or mobile-platform problem. [Visual craft](visual-craft.md) owns the broader design system; [verify](../playbooks/verify.md) owns acceptance and evidence. The entry and host contract govern actions and tools. Recipes here adapt Emil's audited methods, with explicit exceptions and device limits; they do not require a library, donor runtime or Apple-like visual style.

## Decide before animating

Work in this order:

1. **Frequency:** a shortcut or action used hundreds of times should feel immediate; tens of repeats favor little or no motion. Occasional transitions can orient; rare explanation/celebration can spend more time. Never make repeated input wait for decorative motion.
2. **Purpose:** name feedback, spatial continuity, state indication, explanation or justified rare delight. A static change may serve the job better. Functional data should not drift merely to decorate a dashboard.
3. **Cost:** assess attention, vestibular motion, input latency, rendering work and dependency cost. Respect the product's existing timing/tokens and accepted personality.
4. **Mechanism:** prefer the existing suitable primitive. Use a CSS transition for a retargetable state change; supported `@starting-style` for simple entry; keyframes for a predetermined sequence; Web Animations API for programmatic control; an already-available spring/gesture tool when continuity needs it. Check the actual support/API instead of installing a library for a fade.
5. **Behavior:** choose properties, origin, path, timing and interruption/exit together. Input remains available throughout. A gesture starts from the current on-screen state and carries velocity, not from an obsolete target.
6. **Variants and proof:** implement reduced-motion/static behavior and pointer-capability handling with the effect. Review live or recorded temporal behavior, including repetition and interruption. A pair of endpoint screenshots cannot show a jump between them.

Use explicit transition properties. Transform and opacity are often cheaper than layout-changing properties, but CSS, WAAPI, a full transform string or `clip-path` is not a universal guarantee of compositor execution. Inspect actual browser/library behavior and measure important effects under representative load. A short measured height transition or isolated indicator-width change can be valid. Avoid inherited parent-variable updates that cause large descendant recalculations when a scoped element transform suffices. Do not add `will-change` everywhere.

## Values are starting points with context

Prefer accepted project tokens. Where no suitable values exist, these source examples offer a coherent starting vocabulary:

```css
/* Illustrative tokens, not mandatory replacements for a project's system. */
:root {
  --motion-out: cubic-bezier(0.23, 1, 0.32, 1);
  --motion-move: cubic-bezier(0.77, 0, 0.175, 1);
  --motion-drawer: cubic-bezier(0.32, 0.72, 0, 1);
}
```

Ease-out commonly makes entry and response immediate; ease-in-out can connect two established positions; `ease` can suit color/hover; linear progress communicates elapsed proportion. Exit curves depend on the actual path and feedback, not a universal ban or command. A delayed-feeling ease-in deserves inspection, not automatic replacement when it serves the accepted choreography.

Typical starting ranges: press 100–160ms, tooltip 125–200ms, dropdown/select 150–250ms, occasional modal/drawer 200–500ms. Repeated UI should usually settle quickly, but a blanket 300ms gate would wrongly reject the source's intentional toast/drawer/hold recipes. Record the purpose of longer or layout-affecting examples and inspect them. Reduced-motion and static alternatives are exempt from regular-motion aesthetic expectations.

## Component recipes

Choose the row that matches the actual job, then supply its semantics and state handling from the project's components.

| Recipe | Concrete starting treatment | Details that must work |
| --- | --- | --- |
| Press feedback | About `scale(.97)` with a 160ms response, or an immediate color/depth change | Visual feedback on press; ordinary activation commits through correct click/release semantics, with cancellation intact |
| Popover/menu/select | Opacity plus `scale(.95)`, roughly 200ms ease-out | Transform origin reflects the actual trigger; repositioned/edge-flipped popup uses the correct origin |
| Tooltip | Opacity plus `scale(.97)`, around 125ms | Initial accidental-hover delay; neighboring tooltips can appear immediately once the group is active; labels remain usable by keyboard |
| Modal | Centered `scale(.96)`/opacity near 250ms; coordinated backdrop | Center origin is appropriate here; focus/inertness and close behavior remain independent of animation |
| Drawer/sheet | Own-height `translateY(100%)` to zero, up to 500ms with drawer curve | Direction and content height remain coherent; dragging requires the gesture method below |
| Toast | Retargetable opacity/transform around 400ms `ease` | This is a purposeful slower personality example. Preserve stable identity when updating, pause eligible timers while hidden/interacting, and avoid hover gaps in stacks |
| Accordion | Measured height plus opacity near 200ms | Layout-property exception: content height changes/localization remain correct; reverse from current height, preserve expanded semantics and inspect cost |
| Occasional group entrance | Small translation/opacity with 30–80ms stagger, e.g. 50ms | Never hold interaction or required content behind delayed appearance; no repeat on every routine scroll |
| Hold-to-confirm | Linear progress over about 2s, release/reset around 200ms | Progress depiction is only presentation. Implement hold completion, early release, pointer cancel, lost focus, keyboard alternative and duplicate prevention; it supplies no permission for a real action |
| Tab indicator | Clip a visual active-state layer to the selected tab, e.g. 250ms | Keep one semantic set of controls. Decorative duplicate labels are hidden from accessibility/focus; measure after font/size changes |
| Scroll reveal | Once-only clip/mask reveal, e.g. 600ms for a marketing explanation | Default content stays available if observation/animation fails; use only where the reading task benefits |
| Drag-dismiss | Direct manipulation followed by a velocity-aware settle | Distance and signed recent velocity guide intent; canceled/rapidly reversed gestures must not jump or commit unexpectedly |
| Difficult crossfade | Optional subtle blur near 2px with ~200ms opacity after simpler timing fixes fail | Do not hide a poor state transition with expensive blur; inspect on the target device |
| Programmatic motion | WAAPI when code control is needed without a library | Own cancellation, replacement and cleanup; synchronize the final logical/visual state and honor reduced motion |

### Small construction examples

This press treatment keeps hover capability separate and removes nonessential movement for a reduced-motion preference. Keep the project's focus treatment alongside it.

```css
.action {
  transition: transform 160ms var(--motion-out), background-color 120ms ease;
}
.action:active { transform: scale(.97); }
@media (hover: hover) and (pointer: fine) {
  .action:hover { background-color: var(--action-hover); }
}
@media (prefers-reduced-motion: reduce) {
  .action { transition: none; }
  .action:active { transform: none; }
}
```

For a trigger-anchored popover, use the primitive's actual origin/enter/exit attributes, not an invented API:

```css
.popover {
  transform-origin: var(--resolved-origin, center);
  transition: opacity 200ms var(--motion-out), transform 200ms var(--motion-out);
}
.popover[data-entering], .popover[data-exiting] {
  opacity: 0;
  transform: scale(.95);
}
@media (prefers-reduced-motion: reduce) {
  .popover { transition: none; }
  .popover[data-entering], .popover[data-exiting] { transform: none; }
}
```

Entry/exit attributes must be removed at the correct lifecycle boundary; a stale attribute can hide a working control. Use presence support already in the project or a simple explicit state, then test canceled opening/closing. `translateY(100%)` refers to the element's own height, useful for a content-sized drawer. `scale()` also scales its children; inspect type sharpness and click geometry before choosing it.

For hold progress, `clip-path: inset(0 100% 0 0)` to `inset(0 0 0 0)` draws a left-to-right fill. For a comparison slider, vary one inset over two aligned images. A soft-edge reveal needs a mask rather than a hard clip. These visual techniques do not provide event logic, accessible alternatives or an action's authorization.

For a tab's clipped active copy, remove duplicate semantics and pointer handling. For a programmatic effect, cancel or retarget the prior animation before starting another; cleanup must not reset to an obsolete start frame. Keyframes can be appropriate for fixed sequences, while transitions often retarget state changes more simply. Gesture continuity may require a spring rather than either.

## Continuous gestures

Use the platform or installed accessible component when it already meets the job. For a custom gesture, specify ownership and state explicitly: idle → tracking → settling or canceled. Avoid a boolean collection that permits contradictory drag/close states.

1. On pointer-down, provide feedback and preserve the grab offset. Track the owned pointer ID; do not let a second finger take over. Acquire pointer capture where appropriate.
2. Resolve intent after a small product/device-tested movement threshold. Preserve normal page scrolling on the axes the component does not own. Track a short history of position/time, not only start/end, for recent release velocity.
3. During direct manipulation, follow the pointer from the current presentation value. Update a scoped value efficiently. Do not snap the element's center to the finger or animate behind it with a decorative lag.
4. On release, use direction, distance and velocity to choose the valid destination. A short quick flick and a long slow pull can express the same intent; an average absolute speed alone loses reversal information. Guard zero/invalid elapsed time and keep units explicit.
5. Project momentum if the interaction needs it, then choose a permitted snap point. The audited example `projected = current + (velocityPxPerSecond / 1000) * d / (1 - d)`, with `d` near .998, is a tunable deceleration model, not a universal threshold. Bound and measure it for the actual component.
6. Resist progressively beyond bounds instead of a frozen hard stop where appropriate. One illustrative rubber-band model is `(overshoot * dimension * c) / (dimension + c * abs(overshoot))`, with positive dimension and an example `c=.55`.
7. Settle with the current value and release velocity. Prefer little/no overshoot for routine UI; a momentum-driven physical interaction may justify bounce. Spring parameters depend on the selected API: duration/bounce and mass/stiffness/damping are not interchangeable units. When normalizing velocity by remaining distance, guard the zero-distance case.
8. Permit reversal and re-grab during settling. Carry the current velocity when the tool supports it; do not lock input until completion. Release capture/listeners on completion, `pointercancel`, lost capture and teardown. Canceled gestures must restore a coherent state without committing an unintended action.

Test fast and slow release, opposite-direction reversal, re-grab mid-flight, second touch, pointer leaving bounds, scroll coexistence and canceled input. Supply tap/click and keyboard alternatives for the same task. A drag handle or animation does not replace an accessible command.

## Motion, material and input alternatives

- Reduced motion can use a short opacity/color transition or an instant state change. Remove nonessential spatial travel, parallax and overshoot while retaining understandable state feedback. Do not demand residual animation.
- Hover/fine-pointer queries target capability, not a guessed device category. Touch and mouse can coexist. Core actions remain available without hover.
- For reduced transparency or increased contrast where supported, use a more solid surface and clear border rather than relying on blurred content beneath. Keep a functional fallback on browsers without these preference features.
- A modal scrim focuses a blocking task; a nonblocking panel should preserve context. Material weight, overlap and shadow can signal depth, but stacking translucent layers can destroy legibility.
- Sound/haptic feedback is optional, capability-dependent and separately scoped. If used, tie it to the actual event, coordinate timing and give users control; no unsupported promise of native feedback.

## Mobile symptoms and targeted fixes

Apply the smallest remedy where its reason holds. Inspect current framework/browser support; do not copy a global mobile reset or change network/debug settings merely to test.

| Symptom | Mechanism to inspect | Scoped remedy and qualification |
| --- | --- | --- |
| Hover remains after tap | Touch-emulated hover | Gate decorative hover with `(hover: hover) and (pointer: fine)`; retain press/focus feedback |
| Flash on tap competes with design | Browser tap highlight | Remove/adjust `-webkit-tap-highlight-color` only where equivalent visible press feedback exists |
| Bottom controls hidden by browser chrome | Large versus visible viewport | Dynamic `dvh` may suit an app shell; stable small `svh` may suit a hero. Prefer content-friendly minimum heights; test chrome expansion/collapse |
| Input focus unexpectedly zooms | Small mobile input text | Adequate input text, often at least 16 CSS px for relevant mobile browsers; never disable zoom with `user-scalable=no` or `maximum-scale=1` |
| Wrong keyboard or slow task entry | Input semantics/hints | Correct type/inputmode, autocomplete, autocapitalize/autocorrect and enterkeyhint for the field; preserve legitimate input formats |
| Tap feels delayed | Feedback waits for release or gesture arbitration | Immediate press feedback and suitable `touch-action: manipulation`; activation still follows cancelable ordinary semantics |
| Inner scroll moves the page behind | Scroll chaining | `overscroll-behavior: contain` on the relevant scroller; root suppression only for a genuine app/canvas need, not every reading page |
| Fixed chrome overlaps notch/home indicator | Edge-to-edge layout and safe-area padding | Where appropriate, `viewport-fit=cover` plus `env(safe-area-inset-*, 0px)` padding on affected fixed surfaces; test orientation/standalone mode |
| Long press selects control text | Selectable labels on a gesture/control | Scope `user-select:none` and any necessary vendor treatment to controls; content, identifiers and error text remain copyable |
| Horizontal gesture fights vertical scrolling | Ambiguous gesture-axis ownership | A custom horizontal gesture can leave vertical panning to the browser with `touch-action:pan-y`; use `none` only on a surface owning all axes. Native scroll-snap may be simpler |
| Status/browser bar clashes with theme | Stale or mismatched theme metadata | Match actual top-surface `theme-color` to current light/dark state; inspect relevant PWA metadata only when installed mode is in scope |
| Keyboard covers a bottom input/action | Layout versus visual viewport and platform resize behavior | Inspect with keyboard open; consider supported viewport behavior without assuming a meta flag works everywhere |

A safe-area example for a real edge-to-edge sheet is `padding-bottom: calc(1rem + env(safe-area-inset-bottom, 0px))`. It supplements ordinary spacing. Do not add it twice through nested shells. Preserve content scrolling and browser zoom; a mobile-looking UI that prevents them is broken.

Desktop emulation is useful evidence for dimensions, reflow and some media-query states. Hardware-dependent claims require representative physical-device observations: browser chrome, software keyboard, touch feel, safe areas, landscape and installed-PWA behavior if targeted. Older representative hardware can expose costs concealed by a fast desktop. If unavailable, state precisely which behavior is unverified rather than claiming mobile-native completion.

## Name an effect when terminology matters

Use the closest term and distinguish plausible alternatives. This glossary is descriptive, not a demand to implement every effect:

- Appearance: fade changes opacity; slide translates; scale changes size; pop adds an overshoot; reveal uncovers; enter/exit describes lifecycle.
- Timing: keyframes specify stages; interpolation/tween fills between values; stagger offsets a group; orchestration coordinates effects; delay precedes movement; duration measures a timed effect; fill mode controls retained boundary styles; stepped motion changes discretely.
- Geometry: translate, scale, rotate and skew change pose; perspective/3D tilt adds depth; transform origin is the anchor; origin-aware motion visibly relates to its trigger.
- State: crossfade swaps opacity; morph changes shape; shared-element transition connects an identifiable object between views; layout animation interpolates geometry; direction-aware transition distinguishes forward/back; accordion expands/collapses content.
- Scroll: scroll reveal reacts to entry, scroll-driven progress tracks position, parallax changes layer speeds, page/view transitions connect destinations or states.
- Feedback: hover/press treatment acknowledges input; hold progress shows deliberate duration; drag/reorder/dismiss expresses direct manipulation; rubber-banding resists beyond bounds; shake/ripple are feedback motifs.
- Easing and physics: ease-out decelerates, ease-in accelerates, ease-in-out does both, linear is constant; cubic Bézier defines a timing curve. Spring stiffness pulls, damping dissipates, mass affects response; bounce overshoots; momentum/velocity carries movement; perceptual duration differs from final spring settlement.
- Ambient: marquee, loop, alternate/yoyo, orbit, pulse, float and idle motion repeat or continue without a new input. Their attention cost still needs justification.
- Effects: blur softens; clip cuts a hard shape; mask supports graded edges; a comparison slider wipes aligned views; line drawing traces a path; text morph/ticker/typewriter changes glyphs; skeleton/shimmer depicts pending structure; tabular numerals keep digits aligned.
- Performance and principles: jank/dropped frames indicate missed rendering deadlines; compositing may move a prepared layer; layout thrashing repeats costly layout work. Anticipation, follow-through and squash/stretch describe physical cues. Purpose, frequency, continuity and reduced motion decide whether any belongs here.

## Review and repair

Inspect a scoped effect's purpose, frequency, origin, path, timing, interruption, performance, preference variants and token cohesion. First delete unjustified movement; then reduce it; then fix continuity/easing/origin/property cost; polish last. Record the exact location, before/after observation and reason. A code-only concern stays a hypothesis until observed when the finding depends on feel.

Replay at normal speed, then slow it or step frames to locate jumps, overlapping states and coordination errors. Return to normal speed before judging the fix. Exercise rapid repeated input and cancellation while the page is busy. Verify completed work and control availability alongside a trace; a higher frame-rate number alone does not prove the experience improved. Preserve changed-build/state identities in the evidence and name any hardware or measurement gap.
