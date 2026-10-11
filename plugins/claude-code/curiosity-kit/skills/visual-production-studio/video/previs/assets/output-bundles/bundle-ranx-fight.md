# Bundle: Ranx Cyberpunk Fight (Atlas Cloud High-Density Pair)

Preserved worked example, not a current model capability claim or a user-approved recipe. Check actual upload roles and selected-surface controls before use. Final artistic acceptance belongs to the user or the creative reviewer explicitly designated for the current task.
Reference for the highest-density variant: 16-panel grid, 15s, ~0.94s per beat. Three-model pipeline (GPT Image 2 for character + storyboard, Nano Banana 2 for environment, Seedance 2.0 for video). Dual-character combat.

## Brief

- Subject: two cyber tactical agents, "Ranx" (player) versus an unnamed opponent in asymmetric tactical gear
- Motion register: hand-to-hand combat, fast
- Environment: cyberpunk industrial wasteland, wet alley with neon signs and steam vents (generated separately via Nano Banana 2)
- Duration: 15 seconds
- Aspect: 16:9 or 9:16
- Palette: cyberpunk neon (cyan, magenta, electric yellow) on wet black, steam grey
- Panels: 16 (4 by 4 grid)
- Action beats: 试探 → 冲刺 → 格挡 → 闪避 → 勾拳 → 反击 → 压制 → 膝撞 → 近身 → 倒地 (probe, sprint, block, dodge, hook, counter, pin, knee strike, clinch, fall)
- Target image model (Stage 1): GPT Image 2 (character sheet + 16-panel storyboard)
- Target image model (parallel): Nano Banana 2 (cyberpunk environment concept)
- Target video model: Seedance 2.0

## Stage 1A prompt (GPT Image 2 — character + storyboard)

```
Design a high-density combat storyboard production sheet in 16:9.

PROJECT: Ranx
SEQUENCE: 15-second cyberpunk hand-to-hand combat between two agents
DURATION: 15 seconds
PANELS: 16 in a 4 by 4 grid
ASPECT: 16:9
TONE: brutal, fast, kinetic

LAYOUT (three sections):

SECTION 1 (left column, character design): two-character turnaround sheet.
- Ranx: asymmetric cyber tactical gear, left side hard armor with glowing cyan trim, right side bare arm with circuit tattoos. Short hair, cyber visor over one eye.
- Opponent: full hard armor, magenta trim, full visor helmet, both arms armored.
Show front view, side view, and combat stance for each character. Maintain identity across the sheet.

SECTION 2 (right side, 4 by 4 storyboard grid): 16 panels of stick-figure combat choreography. Character A (Ranx) marked with blue motion arrows, character B (opponent) marked with purple motion arrows. Camera motion in red arrows. Environment response (steam, debris, neon flicker) in green arrows.

SECTION 3 (footer strip): action beat labels under each panel column (probe, sprint, block, dodge, hook, counter, pin, knee strike, clinch, fall, and continuation beats), legend, palette swatches.

STORYBOARD GRID PANEL DETAIL:

Row 1 (panels 1 to 4):
Panel 1 [0 to 0.94s]: wide static, two agents face off at 8 meters distance in wet alley. SFX: ambient rain, neon hum.
Panel 2 [0.94 to 1.88s]: low angle medium, Ranx steps forward in probe stance. Opponent shifts weight. SFX: footstep, breath.
Panel 3 [1.88 to 2.81s]: medium tracking, Ranx sprints. Camera pushes with him. SFX: sprint impact.
Panel 4 [2.81 to 3.75s]: wide close, both agents collide, opponent raises forearm to block. SFX: clash.

Row 2 (panels 5 to 8):
Panel 5 [3.75 to 4.69s]: close push-in on Ranx face, eyes through visor. SFX: heartbeat thud.
Panel 6 [4.69 to 5.63s]: medium static, Ranx throws right hook. SFX: wind whoosh.
Panel 7 [5.63 to 6.56s]: low angle close, opponent ducks. Hook misses. Steam vents in background. SFX: dodge whoosh, steam hiss.
Panel 8 [6.56 to 7.5s]: medium tracking right, opponent counters with left jab to Ranx's chest. SFX: hard hit.

Row 3 (panels 9 to 12):
Panel 9 [7.5 to 8.44s]: wide static, Ranx staggers back, opponent advances. SFX: stagger footsteps.
Panel 10 [8.44 to 9.38s]: low angle medium, Ranx pivots and slams opponent into a wall. SFX: body slam.
Panel 11 [9.38 to 10.31s]: close static, Ranx pins opponent at the throat. Neon flicker in background. SFX: pin grip, neon buzz.
Panel 12 [10.31 to 11.25s]: medium static, Ranx drives knee into opponent's gut. SFX: knee impact.

Row 4 (panels 13 to 16):
Panel 13 [11.25 to 12.19s]: wide tracking, opponent crumples to the ground. SFX: body drop.
Panel 14 [12.19 to 13.13s]: low angle wide, Ranx stands over opponent, breathing heavy. Rain falls. SFX: heavy breath, rain.
Panel 15 [13.13 to 14.06s]: medium pull-back, Ranx turns and walks away from camera. SFX: footsteps fade.
Panel 16 [14.06 to 15s]: bird's eye, Ranx walks out of frame, opponent motionless in alley. SFX: distant neon hum, rain.

FOOTER LEGEND:
Red arrow = camera movement
Blue arrow = Ranx (character A) motion
Purple arrow = opponent (character B) motion
Green arrow = environment response

STYLE: hand-drawn storyboard feel, rough but readable. Panels are monochrome line art, character sheet is rendered.
PALETTE: cyan, magenta, electric yellow, wet black, steam grey. Swatches shown in footer.
ASPECT: 16:9.
NEGATIVE: photoreal rendering inside storyboard panels, text inside panels other than timing and SFX, watermarks, garbled glyphs.
```

## Stage 1B prompt (Nano Banana 2 — environment concept, parallel)

```
Create a wide cinematic concept art piece in 16:9 aspect ratio.

Subject: a cyberpunk industrial alley at night. Wet asphalt reflecting neon signs (cyan and magenta). Steam venting from grates. A row of shipping containers stacked on one side. Power cables overhead. Light rain falling. No figures, environment only.

Mood: brutal, claustrophobic, beautiful in a bleak way. Reference Blade Runner 2049 and Ghost in the Shell aesthetic blends.

Palette: dominant wet black and steam grey. Neon accents in cyan and magenta. Distant electric yellow window glow.

Style: photoreal concept art, no text, no watermarks, no figures. 16:9.
```

## Stage 1 expected output description

Two artifacts:

1. From GPT Image 2: a dense 16:9 storyboard sheet with a two-character turnaround section on the left, a 4 by 4 panel grid on the right (16 monochrome line-art combat panels with blue and purple motion arrows for the two fighters plus red camera arrows and green environment arrows), and a footer strip with action beat labels, legend, and palette swatches.

2. From Nano Banana 2: a wet cyberpunk alley concept piece, no figures, neon cyan and magenta on wet black, steam vents and overhead cables. This is the environment reference for Stage 2.

## Stage 2 prompt (Seedance 2.0)

```
Animate this combat sequence into a continuous 15-second cyberpunk fight scene.

Identity reference: @Image1 (Ranx character front view crop from the character sheet; do not render the sheet or use its neutral pose as the opening scene).
Reference 1: @Image2 (the 16-panel storyboard sheet, for shot structure and timing).
Reference 2: @Image3 (the Nano Banana 2 cyberpunk alley environment concept, for setting fidelity).

Follow the 16-panel order exactly as sequential beats. Maintain both characters' identity across all beats. Maintain environment fidelity using @Image3.

[0 to 0.94s] Beat 1: wide static, both agents face off at 8 meters in wet alley. Ambient rain, neon hum.
[0.94 to 1.88s] Beat 2: low angle medium, Ranx steps forward in probe stance. Opponent shifts. SFX: footstep, breath.
[1.88 to 2.81s] Beat 3: medium tracking forward with Ranx as he sprints. SFX: sprint impact.
[2.81 to 3.75s] Beat 4: wide close, collision. Opponent raises forearm to block. SFX: clash.
[3.75 to 4.69s] Beat 5: close push-in on Ranx's face through cyber visor. SFX: heartbeat thud.
[4.69 to 5.63s] Beat 6: medium static, Ranx throws right hook. SFX: wind whoosh.
[5.63 to 6.56s] Beat 7: low angle close, opponent ducks. Hook misses. Steam vents behind. SFX: dodge whoosh, steam hiss.
[6.56 to 7.5s] Beat 8: medium tracking right, opponent counters with left jab to Ranx's chest. SFX: hard hit.
[7.5 to 8.44s] Beat 9: wide static, Ranx staggers back. Opponent advances. SFX: stagger footsteps.
[8.44 to 9.38s] Beat 10: low angle medium, Ranx pivots and slams opponent into the wall. SFX: body slam.
[9.38 to 10.31s] Beat 11: close static, Ranx pins opponent at the throat. Neon flicker. SFX: pin grip, neon buzz.
[10.31 to 11.25s] Beat 12: medium static, Ranx drives knee into opponent's gut. SFX: knee impact.
[11.25 to 12.19s] Beat 13: wide tracking, opponent crumples to the ground. SFX: body drop.
[12.19 to 13.13s] Beat 14: low angle wide, Ranx stands over opponent, breathing heavy. Rain falls. SFX: heavy breath, rain.
[13.13 to 14.06s] Beat 15: medium pull-back, Ranx turns and walks away from camera. SFX: footsteps fade.
[14.06 to 15s] Beat 16: bird's eye overhead, Ranx walks out of frame, opponent motionless. SFX: distant neon hum, rain.

Camera: 28mm equivalent for wides, 50mm for closes. Handheld feel on combat beats, static on bookend beats.
Palette: wet black and steam grey dominant. Neon cyan and magenta accents. Electric yellow distant window glow. Consistent palette across all beats.
Style: cinematic photoreal cyberpunk. Practical effects feel for hits (no exaggerated comic-book impact).
Aspect: 16:9. No text overlays, no subtitles, no watermarks.
```

## Notes on expected output

- This is the highest panel density in the skill. ~0.94s per beat is at the floor for Seedance 2.0; expect some beats to be visually short or to blur into the next. That is acceptable for combat pacing.
- Style locking across three models (GPT Image 2, Nano Banana 2, Seedance 2.0) is the documented losing battle. Do not try to enforce pixel-fidelity between the storyboard sketches and the rendered video. The storyboard is structural direction, the Nano Banana environment is aesthetic reference, the rendered video is its own thing.
- Character identity for two combatants is the biggest drift risk. Mitigation: crop each character's front view from the GPT Image 2 character sheet and provide both as @Image1 and a second character anchor in Stage 2 if your video tool supports it.
- For 9:16 vertical (social), reduce to 12 panels and crop combat to closer framing.

## Variant family

Fight Choreography High-Density (Stage 1 Skeleton 4) plus Seedance Beat-by-Beat (Stage 2 Skeleton 1) plus parallel Nano Banana 2 environment concept. The structural delta is the three-model pipeline and the 16-panel ceiling. Closest in-the-wild anchor: Atlas Cloud Ranx tutorial.
