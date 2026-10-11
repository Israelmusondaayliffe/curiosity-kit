# Scaling Axes

Current use: follow [previs method](../../methods/previs.md) and `validation-contract.md` for mode-specific timing, actual upload roles, autonomy and evidence. Version names and provider behavior in imported examples are historical, unverified here; reuse their craft without treating them as current native controls or rankings.
Seven axes define the prompt-engineering surface for Previs-to-Sequence. Load when building Stage 1 prompts or generating variants.

## Axis 1: Subject Archetype

The type of entity being animated.

**Observed:**
- Female warrior (Nordic, fantasy, sci-fi)
- Male dancer (hip-hop, contemporary, breaking)
- Cyber tactical agent (combat, action)
- Martial arts heroes (Wuxia, paired)
- Luxury product (perfume bottle, watch, fragrance)
- Pop celebrity (MV, fashion)
- Anime chef (Teppanyaki performance)
- Dragon, robot, mythical creature
- Sports athlete

**Structurally compatible, not yet observed:**
- Vehicles (car commercial fly-by, motorcycle chase)
- Architecture fly-throughs
- Food (close-up, hero shot pour)
- Microscopic or scientific subjects
- Particle systems or abstract forms
- Typography or kinetic text
- Data visualization in motion

**Impact on prompt construction:**
- Human subjects demand character-consistency systems (reference sheets, character-locking syntax).
- Product subjects demand macro-detail fidelity (texture, reflection, label legibility).
- Abstract subjects tolerate higher motion ambiguity (good fallback when models struggle with humans).
- Multi-character work requires per-character arrow colors and reference uploads.

## Axis 2: Motion Register

The type, speed, and complexity of movement.

**Observed:**
- Aggressive contemporary dance (Kōda)
- Hip-hop breaking (Abdul Shakoor)
- Combat (sword, martial arts, gunplay)
- Slow atmospheric dolly (cinematic)
- Product macro rotation (luxury ads)
- Subtle facial micro-expressions
- Idle breath, ambient motion
- Cooking choreography (Teppanyaki)

**Structurally compatible, not yet observed:**
- Parkour, gymnastics
- Underwater swimming
- Zero-gravity float
- Crowd simulation
- Cloth or fabric simulation
- Liquid pour or splash
- Explosion debris
- Time-lapse or hyperlapse

**Impact:**
- Fast motion -> 12 to 16 panels for 15 s.
- Slow motion -> 8 panels is enough.
- Complex multi-agent choreography -> color-coded arrows per agent.
- Subtle motion -> emphasize palette and lighting changes in arrows rather than position changes.

## Axis 3: Camera Grammar

The cinematographic language applied.

**Observed:**
- Dolly, pan, crane, orbit, handheld, static
- Push-in, pull-out, tracking
- Bird's eye, Dutch angle
- Shallow depth of field, 35mm, 50mm, macro
- Whip-pan (in hip-hop variants)

**Structurally compatible, not yet observed:**
- Snorricam (chest-mounted subject lock)
- Split-diopter
- Time-lapse, slow-motion ramp
- Match cut, jump cut
- POV (first-person)
- Drone shot, aerial
- 360 rotation
- Steadicam glide

**Impact:**
- Varied camera grammar -> higher panel count needed.
- Describe the camera move clearly; actual execution depends on the selected model and surface. These examples do not establish a model ranking.
- For static or slow camera, panel count can drop. The camera is doing less work.

## Axis 4: Environment Logic

How the setting responds to and interacts with subject motion.

**Observed:**
- Static infinite white space (Hiphop Ink)
- Forest with particle regrowth (Forest Rebirth)
- Blizzard with wind physics (Nordic Warrior)
- Cyberpunk wet alley, neon and steam (Ranx)
- Convenience store with stable fluorescent and neon
- Battlefield with fire and smoke

**Structurally compatible, not yet observed:**
- Underwater caustics
- Crowd reactive behavior
- Destructible environments
- Weather transitions mid-shot
- Day-to-night cycles
- Reflective surfaces, mirrors

**Impact:**
- Environment-responsive motion arrows (green) become critical when the setting is an active participant.
- Static environments simplify Stage 1.
- Dynamic environments demand higher annotation density and explicit "environment responds to action" language in Stage 2.

## Axis 5: Color and Palette Logic

The palette and lighting design enforced across the sequence.

**Observed:**
- Ink-brush monochrome (Hiphop Ink)
- Nordic cold blue and slate (Nordic Warrior)
- Cyberpunk neon-on-black (Ranx)
- Wuxia warm earth tones (UISDC Wuxia)
- Luxury high-key white and gold (ZuLi)
- Convenience store fluorescent plus neon

**Structurally compatible, not yet observed:**
- Technicolor saturated
- Black-and-white film noir
- Thermal vision palette
- HDR hyper-real
- Pastel anime
- Chromatic aberration as aesthetic
- Duotone

**Impact:**
- Palette is defined in the hero frame and should propagate through the grid.
- Inspect palette continuity in actual outputs. Repeat the relevant palette relationship where useful without claiming that repetition guarantees fidelity.
- Always describe the palette explicitly in Stage 2 even when redundant with the reference image.

## Axis 6: Audio and SFX Structure

How sound design is specified and executed.

**Observed:**
- Music-driven beat sync (hip-hop MV)
- Per-panel SFX cues (whoosh, impact, ambient)
- Dialogue tokens (Kling `<<<voice_1>>>`, Veo `"line"`)
- Ambient atmosphere only
- Silent

**Structurally compatible, not yet observed:**
- Foley-grade detailed SFX per beat
- Spatial audio
- Dynamic music that adapts to action intensity
- Voiceover narrative integrated per beat

**Impact:**
- Where the selected surface supports native audio, include requested sound cues directly.
- Where the selected surface lacks audio, keep sound notes as post-production guidance. Do not infer audio capability from an old model list.
- Beat-synced audio benefits from higher panel density.

## Axis 7: Aspect Ratio and Duration

Output format and target duration.

**Observed:**
- 16:9 dominant (cinematic)
- 15 s sweet spot
- 9:16 for social shorts
- Durations: 5 s (Midjourney V1), 8 to 10 s (Hailuo, Pika), 15 s (canonical), 21 s (Midjourney V7), 25 s (Pika Pikaframes)

**Structurally compatible, not yet observed:**
- 21:9 ultra-wide
- 4:3 retro
- Multi-aspect hybrid output (vertical inside horizontal)

**Impact:**
- Duration determines panel count and beat density.
- Aspect determines composition language. Vertical 9:16 favors center-frame compositions and limits wide pan moves. Cinematic 21:9 favors lateral camera moves.
- Choose segmentation for readability and the actual selected surface’s clip limit. Twenty-five seconds and fifteen-second segments are examples, not universal limits.

## Variant generation math

With 7 axes and around 6 to 10 documented values per axis (plus more unobserved), the combinatorial space is large. For brief generation of variants:

- Fix 3 axes (subject, environment, duration). Vary 4. Yields 4 to 6 distinct creative directions per brief.
- Fix 1 axis (typically subject or product). Vary 6. Yields high diversity, good for moodboard or pitch decks.
- Write the requested number of variations within this skill.

When a brief is thin or contradictory, use a brief clarification within this skill first to surface gaps in these seven axes. Common gaps: motion register unspecified, palette inferred but not declared, aspect ratio missing, audio intent unstated.
