# Bundle: Nordic Warrior vs Dragon (UISDC Epic Fantasy Pair)

Preserved worked example, not a current model capability claim or a user-approved recipe. Check actual upload roles and selected-surface controls before use. Final artistic acceptance belongs to the user or the creative reviewer explicitly designated for the current task.
Reference for the densest single-image previs artifact: character sheet + environment concept + 8-shot grid + lighting transitions + audio reference + palette swatches all in one composite. 15s epic fantasy.

## Brief

- Subject: a female Nordic warrior wielding a rune-axe versus an ice dragon
- Motion register: combat choreography, fast
- Environment: blizzard on icy ruins, dragon perched on a frozen cliff
- Duration: 15 seconds
- Aspect: 16:9
- Palette: cold blue, slate grey, white blizzard, rune-axe glows blue, dragon-fire warm orange contrast
- Panels: 8 beats plus character sheet section plus environment map section
- Target image model: GPT Image 2
- Target video model: Seedance 2.0

## Stage 1 prompt (GPT Image 2)

```
Create a complete film director's storyboard design board (production bible) in 16:9 aspect ratio.

PROJECT: Frostfang
SEQUENCE: epic fantasy, female Nordic warrior versus ice dragon
DURATION: 15 seconds
PANELS: 8-beat sequence
LAYOUT: dense production sheet with four labeled sections in this order:

SECTION 1 (top-left, character design): female Nordic warrior turnaround sheet. Front view, side view, back view, close-up of face. Show braided hair with fur cloak, runed leather armor, rune-axe in right hand. Neutral pose. Single character, consistent design across all four views.

SECTION 2 (top-right, environment concept): overhead camera map of the battlefield. Show the warrior's start position, dragon's perch on the cliff, blizzard direction, ice ruin pillars, key sight lines. Bird's eye top-down view with directional arrows for blocking.

SECTION 3 (middle band, 8-shot storyboard grid in 2 rows of 4 panels): stick-figure previs mannequins for both warrior and dragon, with motion arrows, timing brackets, camera grammar, SFX cues. Detail per panel below.

SECTION 4 (bottom band, three sub-strips):
- Lighting transitions strip: 8 color squares showing the dominant light per beat (cold daylight, dragon-fire warm orange, rune-axe blue glow, etc.)
- Audio reference strip: 8 SFX cue labels under each panel
- Palette swatches: 5 color chips (cold blue, slate grey, white, rune blue, dragon orange)

STORYBOARD GRID PANEL DETAIL:

Panel 1 [0 to 2s]: wide static. Warrior walks toward camera through blizzard, axe at her side. Dragon visible in background, distant, on cliff. Camera arrow: still. Subject arrow: forward walk. Environment arrow: snow drift right to left. SFX: wind howl, footsteps on ice.

Panel 2 [2 to 4s]: medium push-in. Warrior raises rune-axe, axe begins to glow blue. Camera arrow: push forward. Subject arrow: arm raise. Light arrow: blue glow from axe. SFX: rune hum, deep bass.

Panel 3 [4 to 6s]: wide tracking right. Dragon launches from cliff, wings spread, fire building in throat. Camera arrow: arc right following dragon. Subject arrow: dragon dive. Light arrow: orange glow in dragon's throat. SFX: dragon roar, wings beat.

Panel 4 [6 to 8s]: low angle close-up. Dragon-fire jets toward camera. Warrior in foreground rolls to her right. Camera arrow: still low. Subject arrow: warrior rolls right. Environment arrow: fire blasts left to right. SFX: fire whoosh, sizzle on ice.

Panel 5 [8 to 10s]: medium static. Warrior rises from roll, axe in both hands, fully glowing blue. Dragon banks for second pass. Camera arrow: still. Subject arrow: rise to stance. Light arrow: rune blue dominant. SFX: rune hum intensifies.

Panel 6 [10 to 12s]: orbit shot. Warrior leaps toward dragon, axe overhead. Camera arrow: circular orbit right. Subject arrow: vertical leap. SFX: leap whoosh, rising tone.

Panel 7 [12 to 14s]: wide static. Axe connects with dragon's neck, blue flash, dragon recoils. Camera arrow: still. Subject arrow: strike contact. Light arrow: blue and orange clash. SFX: impact crack, dragon screech.

Panel 8 [14 to 15s]: bird's eye, pull back fast. Dragon falls into the ice ruins, warrior lands in heroic stance, blizzard returns to dominant. Camera arrow: pull back overhead. Subject arrow: warrior lands, dragon falls. SFX: distant crash, wind howl resumes.

FOOTER LEGEND:
Red arrow = camera movement
Blue arrow = subject motion (warrior and dragon, distinguished by line weight)
Yellow arrow = light change
Green arrow = environment response

STYLE: dense production-design feel, mix of finished character renders (Section 1), schematic map (Section 2), rough storyboard sketches (Section 3), strip illustrations (Section 4). Hand-drawn quality dominant in Section 3.
PALETTE: cold blue, slate grey, white blizzard, rune blue, dragon orange. Swatches shown explicitly in Section 4.
ASPECT: 16:9.
NEGATIVE: watermarks, garbled glyphs, photoreal rendering inside storyboard panels (keep panels rough), text inside panels other than timing and SFX.
```

## Stage 1 expected output description

A dense 16:9 production sheet. Top half split: left has a four-view character turnaround of the Nordic warrior; right has an overhead schematic map of the battlefield. Middle band has 8 storyboard panels arranged 4 wide by 2 tall. Bottom band has three strips: lighting transitions, audio cues, and color palette swatches. The whole sheet reads as a director's production bible for the 15-second sequence.

## Stage 2 prompt (Seedance 2.0)

```
Animate this sequence into a continuous 15-second epic fantasy combat shot.

Identity reference: @Image1 (warrior front-view crop from the character sheet; do not render the sheet or treat its neutral pose as the opening scene).
Reference: @Image2 (the full production design sheet with character, environment map, 8-panel storyboard, and palette strip).

Follow the 8-panel storyboard order exactly as sequential beats. Maintain warrior identity (braided hair, fur cloak, runed leather armor, rune-axe) across all beats. Maintain dragon identity (ice dragon, white scales, blue underbelly, orange throat-fire).

[0 to 2s] Beat 1: wide static. Warrior walks toward camera through heavy blizzard. Rune-axe at her side. Dragon distant on cliff in background. SFX: wind howl, ice crunch footsteps.
[2 to 4s] Beat 2: slow push-in. Warrior raises rune-axe. The axe begins to glow blue. SFX: rune hum, deep bass build.
[4 to 6s] Beat 3: wide tracking right. Dragon launches from cliff, wings spread, orange fire glowing in its throat. SFX: dragon roar, wing beats.
[6 to 8s] Beat 4: low angle close-up. Dragon-fire jets toward camera. Warrior in foreground rolls right out of frame edge. SFX: fire whoosh, ice sizzle.
[8 to 10s] Beat 5: medium static. Warrior rises into combat stance, axe in both hands fully glowing blue. Dragon banks in mid-air for a second pass. SFX: rune hum intensifies, wing flap.
[10 to 12s] Beat 6: orbit shot, circular arc right. Warrior leaps vertically toward dragon, axe raised overhead. SFX: leap whoosh, rising synth.
[12 to 14s] Beat 7: wide static. Axe connects with dragon's neck. Blue flash collides with orange flame. Dragon recoils. SFX: impact crack, dragon screech.
[14 to 15s] Beat 8: bird's eye, fast pull-back overhead. Dragon falls into the ice ruins below. Warrior lands in a hero stance. Blizzard returns to dominant. SFX: distant crash, wind howl resumes.

Camera: 35mm equivalent. Shallow DoF on character beats (1, 2, 5), wide DoF on combat beats (3, 4, 6, 7, 8).
Palette: cold blue and slate grey dominant. Rune-axe blue glow and dragon orange fire are the only warm accents. Palette stays consistent across all beats.
Style: cinematic live-action epic fantasy. Heavy practical effect feel (snow particles, fire embers).
Aspect: 16:9. No text overlays, no subtitles, no watermarks.
```

## Notes on expected output

- This is the densest Stage 1 brief in the skill. Expect 2 to 3 image-gen iterations before the sheet renders cleanly. The character sheet section is usually the first thing to drift.
- For Stage 2, providing the character sheet section as @Image1 (warrior front view crop) and the full sheet as @Image2 reduces character drift across beats meaningfully.
- The blue-vs-orange palette logic is the visual narrative spine. Reinforce it explicitly in Stage 2 ("rune-axe blue glow and dragon orange fire are the only warm accents") or Seedance will spread color elsewhere.
- 8 panels for 15s of combat is at the loose end. If the dragon-versus-warrior beats feel rushed, scale to 12 panels and reduce per-beat duration.

## Variant family

Character-Driven Narrative Board (Stage 1 Skeleton 5) plus Seedance Beat-by-Beat (Stage 2 Skeleton 1). The structural delta is the production-bible density: character sheet + environment map + storyboard + lighting strip + audio strip + palette swatches in one composite. This is the most ambitious single-image Stage 1 the pattern supports.
