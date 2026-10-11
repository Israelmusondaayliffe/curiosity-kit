# Timing translation: interpolate, spring, easing

Source-derived mechanics retained from both pinned editions. Examples are recipes, not automatic permission to install, fetch, upload or execute source. Verify dependencies and adapters against the selected runtime; historical measurements are not current qualification. The owning METHOD.md controls semantic/loss handling.

The single most consequential reference. Easings and timings are what readers
notice; getting them wrong costs more SSIM than any other translation choice.
The original source reports April 2026 tier measurements. They are historical evidence, not validation of this build or a new migration.

## Conversion: frames → seconds

HF's timeline is in seconds. Remotion is frame-based. Always:

```
time_seconds = frame / fps
```

So at fps=30:

- frame 15 → 0.5 s
- frame 30 → 1.0 s
- frame 90 → 3.0 s

Do this conversion once when translating, not at runtime.

## interpolate: linear

```tsx
const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
```

Translates to:

```js
gsap.to(target, { opacity: 1, duration: 1.0, ease: "none" }, 0);
// fromTo if the property starts at 0 and CSS doesn't already set it
gsap.fromTo(target, { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "none" }, 0);
```

`ease: "none"` matches Remotion's default linear interpolation. CSS sets the
`from` value if your initial state is in CSS; otherwise use `fromTo`.

`extrapolateLeft`/`extrapolateRight` defaults to `"extend"` in Remotion but
`"clamp"` is what the agent will see most often. GSAP doesn't extend: values
hold at the start and end of the tween. So for `clamp`, GSAP matches; for
`extend`, you'd need to extend the input range manually before emitting.

## interpolate: multi-segment

```tsx
const opacity = interpolate(frame, [0, 15, 75, 90], [0, 1, 1, 0]);
```

Three keyframed tweens at offsets `[0]/fps`, `[1]/fps`, `[2]/fps`:

```js
const tl = gsap.timeline({ paused: true });
tl.to(target, { opacity: 1, duration: 0.5, ease: "none" }, 0);
tl.to(target, { opacity: 1, duration: 2.0, ease: "none" }, 0.5);
tl.to(target, { opacity: 0, duration: 0.5, ease: "none" }, 2.5);
```

The T1 source fixture retains its historical score in development evidence. Measure the actual target anew.

## spring → GSAP back.out

Remotion's `spring()` is the most lossy translation. The mapping is approximate
and requires a declared approximation budget plus source-specific comparison; no universal SSIM bound follows.

| Remotion `spring` config                          | GSAP equivalent                                      | Validated in                     |
| ------------------------------------------------- | ---------------------------------------------------- | -------------------------------- |
| `{damping: 12, stiffness: 100, mass: 1}` (snappy) | `back.out(1.4)` over ~0.7 s                          | T2, T3 (TitleScene)              |
| `{damping: 14, stiffness: 90, mass: 1}` (calmer)  | `back.out(1.2)` over ~0.7 s                          | T3 (StatCard)                    |
| `{damping: 8, stiffness: 200}` (very bouncy)      | `back.out(2.0)` or `elastic.out(1, 0.5)` over ~0.6 s | not validated; budget ~0.05 SSIM |
| `{overshootClamping: true}`                       | `power3.out` over ~0.6 s (no overshoot)              | not validated                    |

**Rule of thumb**: `back.out(N)` overshoot ratio ≈ `(stiffness / damping^2) * 1.4`. For
`damping:12, stiffness:100` that gives `1.4 * 100/144 = 0.97`, which is close to
the validated 1.4 (the formula is rough; tune by visual). Default duration is
~0.7 s for the typical config.

When the spring's `delay`/`from`/`to` are non-default, scale the duration
proportionally.

## interpolate with custom easing

```tsx
import { Easing } from "remotion";
interpolate(frame, [0, 30], [0, 1], { easing: Easing.out(Easing.cubic) });
```

| Remotion                     | GSAP                                                                                   |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| `Easing.in(Easing.linear)`   | `ease: "none"`                                                                         |
| `Easing.out(Easing.cubic)`   | `ease: t => 1 - (1 - t) ** 3`                                                                   |
| `Easing.inOut(Easing.cubic)` | explicit source cubic in/out function; verify half-way branches                                                                 |
| `Easing.out(Easing.poly(N))` | `ease: t => 1 - (1 - t) ** N` (validate N and source definition)                           |
| `Easing.bezier(a,b,c,d)`     | `CustomEase.create("c", "M0,0 C${a},${b} ${c},${d} 1,1")` (requires CustomEase plugin) |
| `Easing.elastic(bounciness)` | `ease: "elastic.out(${bounciness}, 0.3)"`                                              |
| `Easing.bounce`              | `ease: "bounce.out"`                                                                   |
| `Easing.back(overshoot)`     | `ease: "back.out(${overshoot * 1.7})"` (Remotion's overshoot scale differs)            |

## interpolate driving non-numeric properties

```tsx
const color = interpolateColors(frame, [0, 30], ["#ff0000", "#0000ff"]);
```

GSAP does color tweens natively:

```js
gsap.to(target, { color: "#0000ff", duration: 1.0, ease: "none" }, 0);
```

Same for `backgroundColor`, `borderColor`. The `from` value is read from CSS
or the inline style.

## Custom count-up / number tweens

When Remotion uses a frame-driven number ramp (`Math.round(value * eased)`):

```tsx
const t = interpolate(frame, [0, 45], [0, 1]);
const eased = 1 - (1 - t) ** 3; // cubic ease-out
const value = Math.round(target * eased);
return <div>{value.toLocaleString()}</div>;
```

GSAP equivalent: tween a counter object, write `textContent` on update:

```js
const counter = { v: 0 };
tl.to(
  counter,
  {
    v: target,
    duration: 1.5,
    ease: t => 1 - (1 - t) ** 3,
    onUpdate: () => {
      el.textContent = Math.round(counter.v).toLocaleString();
    },
  },
  0,
);
```

The explicit cubic formula preserves its exponent; GSAP power naming must not be assumed to match. Verify exact integer counter values at selected frames, including cold and reverse seeks. Whole-frame SSIM can hide wrong digits. The counter keeps the containing scene clock unless an actual Sequence shifts it; a delayed card entrance alone must not delay its number ramp.

## Stagger via per-instance prop

When custom subcomponents take a `delayInFrames` prop:

```tsx
<StatCard delayInFrames={i * 12} value={...} />
```

Translate to GSAP timeline offsets:

```js
cards.forEach((card, i) => {
  const start = base + i * (12 / fps); // i * 0.4s at fps=30
  tl.to(card, { ... }, start);
});
```

The original T3 demonstrates three card entrances at 0.0/0.4/0.8 s. That entrance schedule does not shift counters using the parent scene frame.
