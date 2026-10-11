# Pattern Anatomy

Current use: follow [previs method](../../methods/previs.md) and `validation-contract.md` for mode-specific timing, actual upload roles, autonomy and evidence. Version names and provider behavior in imported examples are historical, unverified here; reuse their craft without treating them as current native controls or rankings.
Structural details of the Previs-to-Sequence pattern. Load this for any mode that produces or reads a storyboard composite.

## Panel count guidance

| Duration | Slow / atmospheric | Medium / narrative | Fast / action | Combat / high-density |
|---|---|---|---|---|
| 5 s | 4 | 5 | 6 | 6 |
| 10 s | 6 | 8 | 9 | 10 |
| 15 s | 8 | 9 to 12 | 12 | 16 |
| 20 s | 9 | 12 | 14 | 16 |
| 25 s | 12 | 14 | 16 | 16 |

These are editorial starting points, synchronized with recommend_panel_count.py. For 15-second medium work, twelve is the script default; nine or another requested count remains valid. Counts over sixteen or durations over twenty-five seconds call for a readability check, not an automatic refusal or provider-limit claim.

Grid shapes: 2x4 (8 panels), 3x3 (9 panels), 3x4 (12 panels), 4x4 (16 panels). Pick by aspect ratio. 16:9 grids favor wider rows. 9:16 grids favor taller columns.

## Panel content schema

Annotated timed boards use the following vocabulary. Simple grids and commercial tables omit or relocate fields as their format requires:

1. **Subject pose.** Minimal stick-figure or wireframe. Gesture-level only. No facial detail.
2. **Motion arrows.** Color-coded by domain (see arrow logic below). Direction and curvature matter. Arrow length suggests speed.
3. **Timing bracket.** Beat range in seconds, e.g. `[0-2s]`, `[2-4s]`. Beat math: 8 panels over 15 s = ~1.9 s per beat. 12 panels = ~1.25 s per beat. 16 panels = ~0.94 s per beat.
4. **Camera grammar token.** Lens (24mm, 35mm, 50mm, 85mm, macro), angle (low, high, eye-level, bird's eye, Dutch), distance (ECU, CU, MS, WS, ELS), movement (static, pan, dolly, tracking, crane, orbit, push-in, pull-out, whip-pan).
5. **SFX cue.** Brief parenthetical or square bracket label. "(whoosh)", "[deep bass accent]", "(brush drag)".
6. **Panel number or shot label.** Numeric sequence (1, 2, 3...) or scene/shot notation (S1, S2).

Optional per-panel additions:
- Emotion or beat label ("decisive", "reversal", "impact")
- Quick palette swatch
- Dialogue placeholder (rare in this pattern, typically pushed to Stage 2)

## Motion arrow color logic. Kōda canonical.

Default convention from Kōda (@aimikoda) Forest Rebirth artifact:

- **Red** = camera movement
- **Blue** = subject motion
- **Yellow** = lighting change or highlight
- **Green** = environment response (growth, particles, debris, wind)

When colored arrows are used, declare the legend in a Stage 1 footer ("Legend: Red=camera, Blue=subject, Yellow=light, Green=environment"). The image model needs the explicit mapping to render arrows consistently.

For multi-character work (fight scenes), use:
- Red = camera
- Blue = character A subject motion
- Purple = character B subject motion
- Yellow = light
- Green = environment

For simpler 2-color setups (common in observed variants), drop to:
- Red = camera
- Blue = everything subject-related

State the convention used in the prompt. Image models will not invent a consistent legend without explicit instruction.

## Timing structure

Fifteen seconds recurs in the worked examples. It is an editorial example duration, not a current provider limit.

Beat structure options:

- **8 panels / 15 s**: 1.9 s per beat. Wide, atmospheric, narrative.
- **9 panels / 15 s** (3x3): 1.67 s per beat. Balanced narrative.
- **10 panels / 15 s**: 1.5 s per beat. Standard.
- **12 panels / 15 s**: 1.25 s per beat. Fast or shot-dense.
- **16 panels / 15 s**: 0.94 s per beat. Combat or rhythm-driven.

Use the table and script for starting counts. Segment a longer sequence only when it improves readability or the selected surface actually requires separate clips.

For explicit timed boards, write concrete ranges and mirror them in Stage 2. Terse/reference and untimed grid forms may omit brackets; the validator checks only the applicable contract.

## Camera grammar tokens

Standard cinematographic vocabulary the image model and video model both understand.

**Distance**: ECU (extreme close-up), CU (close-up), MCU (medium close-up), MS (medium shot), MLS (medium long shot), WS (wide shot), ELS (extreme long shot).

**Angle**: low angle, high angle, eye-level, bird's eye, worm's eye, Dutch (canted).

**Lens**: 24mm wide, 35mm standard, 50mm normal, 85mm portrait, 135mm tele, macro, fisheye, anamorphic.

**Movement**: static, pan (left/right), tilt (up/down), dolly (in/out), tracking (lateral or follow), crane (rising/falling), orbit, push-in, pull-out, whip-pan, handheld, Steadicam, gimbal float.

**Composition**: rule of thirds, center frame, symmetrical, leading lines, frame within frame, over-shoulder (OTS), POV, two-shot.

For Stage 1, embed tokens compactly: "35mm low angle MS, dolly in".

For Stage 2, expand into descriptive language: "Camera pushes in on a 35mm lens from a low angle, framing her medium shot, dollying forward as she lifts the axe."

## SFX notation by model

Use descriptive SFX and dialogue cues where requested. Native audio-reference or voice tokens in worked examples require verification on the selected surface. Silent work needs no sound placeholders.

In Stage 1 panels, keep SFX cues short and platform-neutral: `(deep bass accent)`, `(ceramic crack)`, `(brush drag)`. The Stage 2 prompt translates them to model syntax.

## Aspect ratio handling

Stage 1: aspect ratio is declared in the image model prompt (e.g., `16:9`, `9:16`, `1:1`, `21:9`). The composite layout respects this aspect. Panel grids reshape to fit (3x3 works for square or 16:9, 2x6 vertical works for 9:16).

Stage 2: the video model inherits the aspect ratio from the input image or an explicit aspect parameter. State it again in Stage 2 prompts even when redundant. Some models (Seedance 2.0) honor the reference image aspect; other surfaces require explicit declaration.

Observed dominant aspect: 16:9 (cinematic). Emerging: 9:16 (social verticals), 1:1 (square ads).

## Hero frame and grid relationship

The hero frame is the anchor image. It locks:
- Character design and identity
- Color palette
- Lighting style
- Composition language
- Aesthetic register

The grid panels are the temporal expansion of the hero. They depict shot-level choreography but should not reinvent the visual world. In a well-built composite, every panel reads as a derivative of the hero frame.

In Stage 2:
- **Hero frame** = an identity/style anchor. It is an I2V start frame only if an actual clean opening-frame asset is supplied and matches the opening shot; its tag follows actual upload order.
- **Grid composite** = the structural reference. Its actual upload tag drives panel order and timing; never substitute a fictional second upload.

Some workflows separate them as two uploads. Others use one composite image with the hero as an inset or featured panel. Both are valid.

## Stage 1 to Stage 2 handoff

The normal handoff is external: write Stage 1, receive the user’s rendered board, inspect it, then write Stage 2. Explicitly authorized image execution may supply the board on a capable host; it never removes the visual-read requirement.

Make the handoff explicit in FULL-CHAIN mode:

> "Run this in GPT Image 2 (or your image model of choice). Upload the resulting composite back here and I will write Stage 2."

Then end the turn. The next user message (the upload) triggers Stage 2 generation.

Never simulate the image generation. Never invent panel content for an image that does not exist. If the user has not uploaded the composite, ask them to.

## Multi-character handling

When the storyboard depicts two or more named characters:

**Stage 1 additions:**
- Character reference sheets as a side panel (front, side, back, expressions, costume).
- Per-character arrow color (character A = blue, character B = purple).
- Character labels in each panel ("A blocks", "B counters").

**Stage 2 additions:**
- Upload character sheets as separate references (`@Image2`, `@Image3` in Seedance).
- Use actual reference roles and identity descriptions. Native seed or attachment controls require selected-surface verification.

Three-image stack (storyboard + character A sheet + character B sheet) is common in the UISDC Wuxia and Atlas Cloud Ranx variants.

## Style drift acknowledgment

Storyboard aesthetic (hand-drawn, low-detail, annotated) and final video aesthetic (photoreal, cinematic) are intentionally different. The storyboard is a structural tool, not a style reference. Image-to-video models tend to interpret the storyboard's drawn aesthetic as suggestion rather than directive.

Mitigation in Stage 2 prompts: state the target visual style explicitly ("cinematic photoreal, 35mm anamorphic, soft natural light"), describe the storyboard as a "shot structure and timing reference" rather than a visual reference, and provide a separately rendered hero frame if pixel-level identity matters.

When the user wants the final video to look like the storyboard (rare, but observed in ink-brush variants), say so explicitly in Stage 2 ("preserve the ink-wash monochrome aesthetic of the reference"). Even then, expect some style migration toward the video model's defaults.
