# Bundle: Forest Rebirth (Kōda Canonical Pair)

Preserved worked example, not a current model capability claim or a user-approved recipe. Check actual upload roles and selected-surface controls before use. Final artistic acceptance belongs to the user or the creative reviewer explicitly designated for the current task.
Reference for the Kōda four-color arrow convention. Aggressive contemporary dance, 15s, 12 panels.

## Brief

- Subject: a feminine forest spirit, simple stick-figure previs mannequin
- Motion register: aggressive contemporary dance, fast
- Environment: dark void transforming into rebirth forest with growing vines and rising light
- Duration: 15 seconds
- Aspect: 16:9
- Palette: deep emerald, slate black, gold light spill
- Panels: 12 (3 by 4 grid)
- Target image model: GPT Image 2
- Target video model: Seedance 2.0

## Stage 1 prompt (GPT Image 2)

```
Create a professional cinematic previs storyboard sheet.

PROJECT: Forest Rebirth
SEQUENCE: aggressive contemporary dance, forest spirit transformation
DURATION: 15 seconds
PANELS: 12 in a 3 by 4 grid
ASPECT: 16:9
TONE: ritualistic, mythic, intense

HERO FRAME (top section, large): feminine forest spirit silhouette, arms spread, vines twisting up her body, gold light from above, dark emerald background. Use this as the visual anchor for palette and identity.

GRID PANELS (12 panels arranged 3 wide by 4 tall below the hero frame): each panel is a simple stick-figure previs mannequin in a different pose, with motion arrows, timing bracket, camera grammar, and SFX cue.

Panel 1 [0 to 1.25s]: wide static, mannequin curled on dark floor. Camera arrow: still. Subject arrow: slow rise. SFX: low hum.
Panel 2 [1.25 to 2.5s]: medium push-in, mannequin uncurls, arms reach up. Camera arrow: push forward. Subject arrow: extension up. Light arrow: faint gold from above. SFX: deep bass swell.
Panel 3 [2.5 to 3.75s]: low angle close, mannequin's face tilts up. Camera arrow: tilt up. Subject arrow: head extension. SFX: breath in.
Panel 4 [3.75 to 5s]: wide tracking right, mannequin leaps. Camera arrow: arc right. Subject arrow: leap. Environment arrow: vines emerge from ground. SFX: whoosh.
Panel 5 [5 to 6.25s]: medium static, mannequin lands in second position. Camera arrow: still. Subject arrow: hard landing. Environment arrow: vines spread outward. SFX: impact thud.
Panel 6 [6.25 to 7.5s]: orbit, mannequin spins. Camera arrow: circular. Subject arrow: rotation. Light arrow: gold expands. SFX: rising tone.
Panel 7 [7.5 to 8.75s]: low angle wide, mannequin throws arms wide. Camera arrow: pull back. Subject arrow: extension out. Environment arrow: vines climb up. SFX: percussive hit.
Panel 8 [8.75 to 10s]: close push-in, mannequin's eyes open. Camera arrow: push in fast. Subject arrow: still. Light arrow: gold floods. SFX: glass shatter.
Panel 9 [10 to 11.25s]: medium tracking left, mannequin sweeps low. Camera arrow: arc left. Subject arrow: sweep. SFX: low whoosh.
Panel 10 [11.25 to 12.5s]: bird's eye, mannequin centers in a vine-formed circle. Camera arrow: overhead. Subject arrow: centered stillness. Environment arrow: vines form a circle. SFX: chorus rise.
Panel 11 [12.5 to 13.75s]: wide static, mannequin stands tall, vines fully grown around her. Camera arrow: still. Subject arrow: still. Light arrow: gold sustained. SFX: sustained note.
Panel 12 [13.75 to 15s]: medium pull back, full forest revealed, mannequin in center. Camera arrow: pull back fast. Subject arrow: stillness. Environment arrow: forest in full bloom. SFX: final swell, then silence.

FOOTER LEGEND (bottom of sheet):
Red arrow = camera movement
Blue arrow = subject motion
Yellow arrow = light change
Green arrow = environment response

STYLE: hand-drawn previs sketch feel, rough but readable. Stick figures over rendered figures. Prioritize clarity of motion and framing.
PALETTE: deep emerald, slate black, gold light spill. Monochrome panels acceptable, color reserved for the hero frame.
ASPECT: 16:9.
NEGATIVE: photorealistic rendering, text inside panels other than timing brackets and SFX, watermarks, garbled glyphs.
```

## Stage 1 expected output description

A landscape 16:9 sheet. Top half is the colored hero frame: forest spirit silhouette with vines climbing her body, gold light from above, deep emerald and slate background. Below the hero is a 3 by 4 grid of 12 monochrome panels, each containing a stick-figure pose with colored arrows, a timing bracket in the top corner, and a brief SFX cue at the bottom. A legend bar runs along the bottom edge mapping the four arrow colors.

## Stage 2 prompt (Seedance 2.0)

```
Animate this storyboard into a continuous 15-second cinematic shot.

Start frame: @Image1 (the hero frame from the storyboard).
Reference: @Image2 (the full 12-panel storyboard grid).

Follow the panel order exactly as sequential beats. Do not reinterpret as one static image. Maintain character consistency with @Image1 throughout.

[0 to 1.25s] Beat 1: wide static. Forest spirit curled on dark floor. Slow rise begins. SFX: low hum.
[1.25 to 2.5s] Beat 2: slow push-in. She uncurls, arms reach up. Gold light begins from above. SFX: deep bass swell.
[2.5 to 3.75s] Beat 3: low angle close-up. Her face tilts up, breath in. SFX: breath in.
[3.75 to 5s] Beat 4: tracking arc right. She leaps. Vines emerge from the ground beneath her. SFX: whoosh.
[5 to 6.25s] Beat 5: medium static. Hard landing in second position. Vines spread outward. SFX: impact thud.
[6.25 to 7.5s] Beat 6: orbit shot. She spins. Gold light expands around her. SFX: rising tone.
[7.5 to 8.75s] Beat 7: low angle wide, camera pulls back. Arms thrown wide. Vines climb behind her. SFX: percussive hit.
[8.75 to 10s] Beat 8: fast push-in to close-up. Her eyes open. Gold light floods the frame. SFX: glass shatter.
[10 to 11.25s] Beat 9: tracking arc left. She sweeps low. SFX: low whoosh.
[11.25 to 12.5s] Beat 10: bird's eye overhead. She centers inside a vine-formed circle. SFX: chorus rise.
[12.5 to 13.75s] Beat 11: wide static. She stands tall, vines fully grown around her. Gold light sustained. SFX: sustained note.
[13.75 to 15s] Beat 12: medium pull-back. Full forest revealed, she stands at center. SFX: final swell, fading to silence.

Camera: 35mm equivalent, shallow depth of field, cinematic motion blur.
Palette: deep emerald, slate black, gold light spill. Maintain palette across all beats.
Style: cinematic live-action realism. No text overlays, no subtitles, no watermarks.
Aspect: 16:9.
```

## Notes on expected output

- The video model should produce one continuous 15-second shot that visibly moves through the 12 beats in order.
- Common drift: Seedance 2.0 sometimes compresses 12 panels into 8 to 9 visible beats. If this happens, increase panel count to 16 in Stage 1 or split into two 7.5-second halves and stitch in post.
- The hero frame is the identity anchor. Style drift between the rough storyboard aesthetic and the rendered video output is expected and acceptable. Identity (silhouette, palette, lighting style) is what matters.

## Variant family

Canonical Director's Board (Stage 1 Skeleton 1) plus Seedance Beat-by-Beat (Stage 2 Skeleton 1). This is the reference pair the skill defaults to when none of the specialized skeletons fit.
