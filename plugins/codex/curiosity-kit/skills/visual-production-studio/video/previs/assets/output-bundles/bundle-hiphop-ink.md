# Bundle: Hiphop Ink-Brush Dancer (@abxxai Canonical Pair)

Preserved worked example, not a current model capability claim or a user-approved recipe. Check actual upload roles and selected-surface controls before use. Final artistic acceptance belongs to the user or the creative reviewer explicitly designated for the current task.
Reference for monochrome ink-wash style and beat-synced per-panel timing. 8-panel pattern for ~15s.

## Brief

- Subject: a male hip-hop dancer rendered in ink-brush style, stick-figure previs mannequin in panels
- Motion register: aggressive hip-hop choreography (breaking, popping, freezes), medium-fast
- Environment: infinite white space, ink trails follow the body
- Duration: 15 seconds
- Aspect: 9:16 (vertical for social) or 16:9 (cinematic), pick per platform
- Palette: pure black ink on pure white, no other colors
- Panels: 8 (2 by 4 grid or 4 by 2)
- Target image model: GPT Image 2
- Target video model: Seedance 2.0

## Stage 1 prompt (GPT Image 2)

```
Director-style PREVIS action storyboard sheet, 8 continuous frames, minimal stick figures.

PROJECT: Hiphop Ink
SEQUENCE: aggressive hip-hop choreography in monochrome ink-brush style
DURATION: 15 seconds
PANELS: 8 in a 2 by 4 grid
ASPECT: 9:16
TONE: minimalist, percussive, kinetic

SUBJECT: a male hip-hop dancer as a simple stick-figure previs mannequin in each panel. Ink-brush trails emanate from the body, following the motion path.
ENVIRONMENT: pure white infinite space, no horizon, no props.
ACTION: per panel below.

Panel 1 (0:00 to 0:02): static wide. Mannequin in idle stance, weight on right leg. Ink trail: minimal, pooled at his feet. SFX: deep bass accent.
Panel 2 (0:02 to 0:04): medium static. Mannequin drops into a low squat, one arm up. Ink trail: brush drag follows the dropping motion. SFX: brush drag, sharp downbeat.
Panel 3 (0:04 to 0:06): low angle medium. Mannequin spins into a footwork pose. Ink trail: circular swirl around legs. SFX: snare hit, whoosh.
Panel 4 (0:06 to 0:08): close push-in. Mannequin pops a chest hit, arms locked. Ink trail: starburst behind chest. SFX: clap on the beat.
Panel 5 (0:08 to 0:10): wide tracking left. Mannequin slides on knees. Ink trail: long horizontal smear. SFX: ink slide, hi-hat ride.
Panel 6 (0:10 to 0:12): bird's eye. Mannequin spread on the floor in a freeze. Ink trail: full body outline in ink wash. SFX: bass drop, silence.
Panel 7 (0:12 to 0:14): medium pull back. Mannequin rises to standing, arms swing wide. Ink trail: vertical streaks. SFX: rising synth.
Panel 8 (0:14 to 0:15): wide static. Mannequin in final pose, arms crossed. Ink trail: settles into a single drop. SFX: final hit, then silence.

FOOTER LEGEND:
Red arrow = camera movement
Blue arrow = subject motion
Yellow arrow = light change (unused, palette is monochrome)
Green arrow = environment response (ink trails)

STYLE: pure black ink-brush on pure white. Stick figures with calligraphic stroke quality. Brush ink trails are part of the visual language.
PALETTE: monochrome. Black ink only.
ASPECT: 9:16.
NEGATIVE: color, text inside panels other than timing and SFX, watermarks, photorealism.
```

## Stage 1 expected output description

A vertical 9:16 sheet. 8 panels arranged 2 wide by 4 tall. Each panel shows a stick-figure dancer in a different pose with ink-brush trails marking motion path. Each panel has a small timing label in the top corner and an SFX note at the bottom. Pure black and white throughout.

## Stage 2 prompt (Seedance 2.0)

```
Animate this storyboard into a continuous 15-second video.

Structural reference: @Image1 (the actual full 8-panel storyboard). The opening action follows panel 1; do not render the grid. No separate clean start-frame upload is assumed.

Follow the panel order exactly as sequential beats. Maintain ink-brush style and monochrome palette throughout. Maintain dancer identity and silhouette.

[0:00 to 0:02] Beat 1: wide static. Dancer in idle stance, weight on right leg. Ink pools at his feet. SFX: deep bass accent.
[0:02 to 0:04] Beat 2: medium static. Dancer drops into a low squat, one arm up. Ink trail drags behind the motion. SFX: brush drag, sharp downbeat.
[0:04 to 0:06] Beat 3: low angle medium. Dancer spins into a footwork pose. Ink swirls around his legs. SFX: snare hit, whoosh.
[0:06 to 0:08] Beat 4: fast push-in to close-up. Dancer pops a chest hit, arms locked. Ink starburst behind the chest. SFX: clap on the beat.
[0:08 to 0:10] Beat 5: wide tracking left. Dancer slides on his knees. Long horizontal ink smear behind him. SFX: ink slide, hi-hat ride.
[0:10 to 0:12] Beat 6: bird's eye overhead. Dancer in a freeze, spread on the floor. Full body outlined in ink wash. SFX: bass drop, then silence.
[0:12 to 0:14] Beat 7: medium pull-back. Dancer rises to standing, arms swing wide. Vertical ink streaks behind him. SFX: rising synth.
[0:14 to 0:15] Beat 8: wide static. Dancer in final pose, arms crossed. Ink settles into a single drop. SFX: final hit, then silence.

Camera: 50mm equivalent, shallow depth of field.
Palette: pure black on pure white. Ink-wash style, no color leakage.
Style: cinematic but rendered in ink-brush aesthetic. Brush trails are visible behind every motion.
Aspect: 9:16. No text overlays, no subtitles, no watermarks.
```

## Notes on expected output

- Seedance 2.0 tends to drift toward color even when monochrome is specified. Reinforce "pure black on pure white" and "no color" in the prompt. If drift persists, add "high-contrast monochrome only" and post-process to grayscale if needed.
- The ink trail is the environmental response in this variant. It plays the role that vines play in Forest Rebirth.
- Beat duration of ~1.9s per panel is at the slow end of feasible for hip-hop. If music has a faster BPM, scale up to 12 panels and tighten beat duration to ~1.25s.

## Variant family

Director-Style Action Storyboard (Stage 1 Skeleton 1 variant) plus Seedance Beat-by-Beat (Stage 2 Skeleton 1). Monochrome ink-brush is the structural delta; everything else follows canonical.
