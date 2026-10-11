# Stage 2 Skeletons

Current use: follow [previs method](../../methods/previs.md) for mode-specific timing, actual upload roles, autonomy and evidence. Read [validation contract](validation-contract.md) for saved structured handoffs. Version names and provider behavior in imported examples are historical, unverified here; reuse their craft without treating them as current native controls or rankings.
Choose the requested model, version, surface and prompt form. Preserve actual panel order; retain explicit timing when supplied or requested. Terse board-reference and sparse keyframe forms need no invented timestamps. Imported syntax is a craft example; the selected current profile controls native support.

## Choose a skeleton

Read the selected section plus [actual reference handling](#actual-reference-handling) and [compression rules](#compression-rules):

- [Seedance English timed beats](#skeleton-1-seedance-20-english-beat-by-beat)
- [Seedance role-aware multi-sheet references](#skeleton-1b-seedance-20-beat-by-beat-with-role-aware--tags-multi-sheet-bible)
- [Seedance Chinese terse form](#skeleton-2-seedance-20-chinese-terse-form)
- [Veo structured clips](#skeleton-3-veo-31-structured-clip-format)
- [Kling multi-shot and voice cues](#skeleton-4-kling-30-multi-shot-with-voice-tokens)
- [Generic I2V and sparse keyframe transitions](#skeleton-5-generic-i2v-fallback)

## Skeleton 1: Seedance 2.0 English Beat-by-Beat

Use for: Seedance 2.0 with English-language pipeline. Most documented variant pair (a recurring pair in the imported examples; frequency not verified).

```
Duration: [N] seconds. Start frame: @Image1 (hero frame from storyboard). Reference: @Image2 (storyboard grid composite).

Follow the storyboard panel order exactly as sequential keyframes. Do not reinterpret the storyboard as a single image. Each panel = one beat in the video timeline.

[0-Xs] Beat 1 (Panel 1): [camera move], [subject action]. [environment response]. SFX: [cue].
[Xs-Ys] Beat 2 (Panel 2): [camera move], [subject action]. [environment response]. SFX: [cue].
[Ys-Zs] Beat 3 (Panel 3): [camera move], [subject action]. [environment response]. SFX: [cue].
...
[(N-X)-Ns] Beat N (Panel N): [camera move], [subject action]. [environment response]. SFX: [cue].

Camera: [lens, e.g. 35mm anamorphic, shallow DoF]. Style: [visual style, e.g. cinematic photoreal, soft natural light]. Palette: [color description].

Maintain character consistency with @Image1 throughout. Keep the subject identity from the actual identity reference: [subject description].

No text overlays. No subtitles. No watermarks.
```

**Worked example: Forest Rebirth Stage 2 (Seedance 2.0 English)**

```
Duration: 15 seconds. Start frame: @Image1 (hero frame, bone-white forest spirit kneeling in mossy clearing). Reference: @Image2 (12-panel storyboard composite).

Follow the storyboard panel order exactly as sequential keyframes. Each panel = one beat. Do not treat the storyboard as a single image.

[0-1.25s] Beat 1 (Panel 1): WS static, bone-white forest spirit kneels in deep contraction in the mossy clearing. Forest is muted, pre-bloom. SFX: low ambient wind, single breath.
[1.25-2.5s] Beat 2 (Panel 2): MS handheld, sharp arm extension upward, fingers splay. First bioluminescent tendril rises from the moss at her knee. SFX: soft pulse hit.
[2.5-3.75s] Beat 3 (Panel 3): ECU push-in on her spine arching, vertebrae visible through translucent skin. Light flickers along the spine. SFX: brush drag.
[3.75-5s] Beat 4 (Panel 4): MS orbit 90 degrees around her low spinning sweep, one leg extended through grass. Grass grows in the arc of the sweep. SFX: rising harmonic.
[5-6.25s] Beat 5 (Panel 5): WS crane-up tracking her vertical leap, body fully extended. Bioluminescent pollen burst at lift-off. SFX: thump and breath.
[6.25-7.5s] Beat 6 (Panel 6): CU whip-pan around her mid-air twist, hair and limbs trailing teal light. SFX: whip pass.
[7.5-8.75s] Beat 7 (Panel 7): MLS tracking, hard landing into a low crouch, ground responds with a circular pulse of growth. SFX: deep impact.
[8.75-10s] Beat 8 (Panel 8): WS static, entire forest pulses with light, fast bloom wave moves outward from her crouch. SFX: chord swell.
[10-11.25s] Beat 9 (Panel 9): MS tracking, outward arm sweep, particles rise from the moss in her wake. SFX: rising shimmer.
[11.25-12.5s] Beat 10 (Panel 10): CU whip-pan toward camera, her face still featureless but tilted forward. SFX: whip and tonal hit.
[12.5-13.75s] Beat 11 (Panel 11): MLS, open-armed pose, forest fully regrown around her in deep saturated green and teal. SFX: held chord.
[13.75-15s] Beat 12 (Panel 12): WS dolly-out, she stands centered in the restored world, light settles. SFX: long exhale.

Camera: 35mm anamorphic, shallow DoF for close-ups, deep DoF for wide shots. Style: mythic photoreal, dusk volumetric god-rays, soft natural light with bioluminescent accents. Palette: desaturated forest greens, bone-white subject, bioluminescent teal accents.

Maintain character consistency with @Image1 throughout. Subject: bone-white humanoid forest spirit, sinuous limbs, no facial features.

No text overlays. No subtitles. No watermarks.
```

## Skeleton 1B: Seedance 2.0 Beat-by-Beat with Role-Aware @-tags (Multi-Sheet Bible)

Use for: Seedance 2.0 English when the user has uploaded a multi-sheet character bible (turnaround sheet, wardrobe sheet, emotion sheet) alongside the storyboard composite. The role-aware structure declares each `@-tag` with its role and explicit do-not-render directive so sheets never bleed into the rendered video.

This complete local skeleton preserves the role-aware character-bible method; no external template is required.

```
SUBJECTS:
@Image1 is the main character. [Compact character description: who they are, canonical look, identity markers from the hero shot, build, hair, signature wardrobe.] Use @Image1 as the persistent visual anchor across every shot. Whenever this character appears, preserve their face, build and signature look. Follow the board for cutaways, absence, pose and expression.

REFERENCES (consistency only, never rendered as standalone images):
@Image2 is the character turnaround sheet. Use it to keep face, head shape, body proportions, and hair consistent across angles. Do not render @Image2 in the video. Do not show multi-view turnaround layouts, character sheet boxes, view labels, or any sheet-style framing.
@Image3 is the wardrobe sheet. Use it to keep clothing, materials, colors, and accessories consistent. Do not render @Image3 in the video. Do not show wardrobe breakdowns, garment labels, fabric swatches, or any catalog-style layout.
@Image4 is the emotion sheet. Use it to keep facial expressions within the character's emotional range. Do not render @Image4 in the video. Do not show expression grids, emotion labels, or any expression-sheet framing.

STRUCTURAL GUIDE (do not render, sequence reference only):
@Image5 is the storyboard composite. Follow the panel-by-panel sequence shown in @Image5 exactly. Each panel = one beat in the video timeline. Do not render @Image5 in the video. The final video does not show panel borders, panel numbers, timing brackets, annotation arrows, grid layout, or any storyboard-style framing.

Duration: [N] seconds.

[0-Xs] Beat 1 (Panel 1): [camera move], [subject action]. The character (@Image1) [specific action]. [environment response]. SFX: [cue].
[Xs-Ys] Beat 2 (Panel 2): [camera move], [subject action]. The character (@Image1) [specific action]. [environment response]. SFX: [cue].
[Ys-Zs] Beat 3 (Panel 3): [camera move], [subject action]. The character (@Image1) [specific action]. [environment response]. SFX: [cue].
...
[(N-X)-Ns] Beat N (Panel N): [camera move], [subject action]. The character (@Image1) [specific action]. [environment response]. SFX: [cue].

Camera: [lens, e.g. 35mm anamorphic, shallow DoF]. Style: [the requested FINAL video style; preserve the reference drawing style if intended, otherwise name the desired treatment]. Palette: [color description].

GLOBAL CONSTRAINTS:
Maintain the character from @Image1 wherever present; follow the storyboard for shots where they are absent. Cross-check face, body, and hair against @Image2. Cross-check wardrobe against @Image3. Cross-check expression range against @Image4. Follow exact panel order from @Image5.
No panel borders, no annotations, no timing brackets, no panel numbers, no grid layout, no on-screen text bleed from any reference image. The final video shows only the cinematic scene.
Consistent lighting, environment, and character identity across all shots. No deformation. Stable proportions. Natural motion physics.

No text overlays. No subtitles. No watermarks.
```

### When to drop `@-tags` from this skeleton

Adjust the SUBJECTS / REFERENCES / STRUCTURAL GUIDE blocks based on which sheets the user actually uploaded:

- Only character + storyboard (minimum viable): keep SUBJECTS (`@Image1`) and STRUCTURAL GUIDE (`@Image2` = storyboard). Drop REFERENCES block.
- Character + turnaround + storyboard: SUBJECTS (`@Image1`), REFERENCES (`@Image2` = turnaround), STRUCTURAL GUIDE (`@Image3` = storyboard).
- Character + turnaround + wardrobe + storyboard: SUBJECTS (`@Image1`), REFERENCES (`@Image2` = turnaround, `@Image3` = wardrobe), STRUCTURAL GUIDE (`@Image4` = storyboard).
- Full bible (character + turnaround + wardrobe + emotion + storyboard): use the canonical skeleton above with all five `@-tags`.

Adjust tag numbers to match actual upload order. The roles are stable; the numbers shift.

### Character preproduction

For requested Stage A hero or Stage B consistency sheets, use the local [character-continuity method](../../methods/character-continuity.md). It owns hero, bible, board and sequence work. A Stage 2 request with supplied assets can stay in this section without regenerating earlier stages.

## Skeleton 2: Seedance 2.0 Chinese Terse Form

Use for: Seedance 2.0 in Chinese-language workflow (Jimeng / Dreamina). Common in observed UISDC variants. Shorter, prompt-engineered to lean on the storyboard reference doing the heavy lifting.

```
根据故事板分镜生成[N]秒视频。参考图：@Image1（分镜脚本）。保持角色一致性，无文字、无字幕。
```

Optional expansions:

```
根据故事板分镜生成[N]秒视频，主题：[topic in Chinese]。
参考图：@Image1（分镜脚本）。[character refs as @Image2, @Image3 if multi-character].
风格：[style], [palette description], 写实电影感, 4K, 超清。
保持角色一致性，按照分镜顺序逐帧生成，无文字、无字幕、无水印。
```

**Worked example: Wuxia 英雄救美 Stage 2 (Chinese)**

```
根据故事板分镜生成15秒视频，主题：英雄救美情节最后反转、邵氏武侠风格。
参考图：@Image1（分镜脚本），@Image2（男主角色参考），@Image3（女主角色参考）。
风格：邵氏武侠暖色调，写实电影感，4K，超清，高级感。
保持角色一致性，按照9张镜号顺序逐帧生成，无文字、无字幕、无水印。
```

The terse Chinese form carries sequence intent through the board reference. It does not provide explicit beat-timing proof. Use the requested language and level of detail; no training-data or superiority claim is made.

## Skeleton 3: Veo 3.1 Structured Clip Format

Use for: Veo 3.1 via Flow, API, or Vertex. Descriptive `Clip N` blocks with `SFX:` and `Music:` labels; verify actual multi-shot/audio support on the selected surface.

```
Storyboard reference: @Image1 (hero frame), @Image2 (panel grid).

Aspect: [aspect ratio]. Duration: [N] seconds total across [panel count] clips.
Lens: [lens choice]. Palette: [color description] throughout all clips.

Clip 1 [0-Xs]: [camera move] as [subject action]. [lighting]. [atmosphere]. SFX: "[sound effect description]". Music: [musical cue if any].

Clip 2 [Xs-Ys]: Cut to [shot type]. [camera move] revealing [subject action]. Environment: [detail]. SFX: "[sound effect]".

Clip 3 [Ys-Zs]: [transition type] to [new framing]. [camera move] following [subject action]. SFX: "[sound effect]". "[dialogue line if present]".

...

Clip N [last block]: [final camera move and action]. [resolution detail]. SFX: "[final sound]".

Style note: [visual style descriptors]. Maintain character identity established in @Image1: [subject description in 1 sentence].

No on-screen text. No subtitles.
```

Use detailed camera prose and requested dialogue/SFX where the selected surface supports them. Mirror source panels or document an ordered compression map; there is no universally safe compression ratio.

## Skeleton 4: Kling 3.0 Multi-Shot with Voice Tokens

Use for: Kling 3.0, especially when the sequence has dialogue or character voice cues.

```
[N]s video. Start image: @Element1 (hero frame). Reference grid: @Element2 (panel storyboard).

Style: [visual style]. [Include a seed setting only when requested and actually supported on the selected surface.]

[0-Xs] Shot 1: [subject] [action] in [environment]. Camera [move], [shot type].
[Xs-Ys] Shot 2: [subject] [next action]. Camera [move]. Environment shifts to [change].
[Ys-Zs] Shot 3: [subject] [final action]. Camera [move], [shot type]. Audio: <<<voice_1>>> [dialogue line in quotes].
...
[last block] Shot N: [final action]. [resolution detail].

Maintain character identity across all shots: [subject description]. Use the supplied identity references and consistent descriptions wherever the character appears. No seed or prompt guarantees identity lock.

No subtitles, no watermark.
```

Keep character descriptions consistent. Verify any element, seed or voice control before inserting it; these examples do not establish native support.

## Skeleton 5: Generic I2V Fallback

Use for: Pika V2.2, Runway Gen-4, Luma Ray 3, or any model without distinctive multi-shot syntax.

```
Animate the storyboard composite (@Image1) into a continuous [N]-second shot.

Opening action: describe the actual observed first sequence panel. Bind a start-frame control only to a separately supplied clean opening-frame asset when supported.

Follow the camera moves and subject actions exactly as shown in the storyboard grid panels, in numbered order:

Beats 1 through [N]: [single flowing paragraph describing the sequence of actions, camera moves, and environmental responses, mirroring the panel order, with phrasing like "first... then... next... finally..."]

Camera language: [list of shot types and moves]. Style: [visual style]. Palette: [color description].

Maintain visual consistency throughout. Exclude unwanted board annotations and grid borders; retain final titles, wordmarks or subtitles requested by the brief.

[Model-specific note line. Pick one:]
- Pika V2.2: Use Pikaframes interpolation between the hero frame and the final panel. Per-transition prompt above.
- Runway Gen-4: Use Story Panels mode if available. Otherwise treat as standard I2V with the grid as a structural reference.
- Luma Ray 3: Use the hero frame as the start image. Motion prose drives the sequence.
```


For Pika V2.2 Pikaframes, the workflow differs: instead of one continuous prompt, the user uploads 3 to 5 keyframe images (sampled from the storyboard panels) and provides a per-transition prompt for each gap. Adapt the skeleton:

```
Pika V2.2 Pikaframes workflow:
- Keyframe 1: Panel 1 from the storyboard composite
- Keyframe 2: Panel [N/4] from the composite
- Keyframe 3: Panel [N/2] from the composite
- Keyframe 4: Panel [3N/4] from the composite
- Keyframe 5: Panel N (final) from the composite

Transition prompts:
1->2: [motion description, e.g. "subject rises from crouch into vertical extension, camera dollies in"]
2->3: [motion description]
3->4: [motion description]
4->5: [motion description]

Style: [visual style]. Maintain character identity across keyframes.
```

## Actual reference handling

Build the mapping from uploaded files and the selected surface. Numeric tags in these templates are examples. With only a storyboard, that asset is the structural reference. With a separate clean opening frame, map it as start-frame. A character sheet remains an identity reference even if cropped; do not call it the opening scene. Multi-reference limits and native attachment syntax require current selected-surface verification.

**Role-aware multi-sheet pattern (Seedance 2.0):** when the user uploads a multi-sheet character bible (turnaround sheet, wardrobe sheet, emotion sheet) alongside the storyboard, use Skeleton 1B (above). The role-aware structure declares each `@-tag` with its role and an explicit do-not-render directive. Default tag mapping: `@Image1` = character hero shot (renders as subject), `@Image2` = character/turnaround sheet (does not render), `@Image3` = wardrobe sheet (does not render), `@Image4` = emotion sheet (does not render), `@Image5` = storyboard composite (does not render). Drop any `@-tag` whose asset is not uploaded. Adjust numbers to actual upload order.

## Compression rules

When the storyboard has more panels than the video model can comfortably handle in beat blocks:

- Group adjacent panels with related action into one beat block. Preserve all requested/observed beats unless compression is justified; there is no universal twelve-beat limit.
- Adjust beat timing to absorb the merged panels. If panels 3 and 4 merge into one beat, that beat's duration spans the original 3+4 time bracket.
- Document the compression in the Stage 2 prompt: "Panels 3-4 combined into Beat 3 for camera continuity."

If a panel contains several actions, preserve them in its beat or make an explicit storyboard revision. The current compression validator accepts ordered grouping only; it does not silently accept split, skipped, duplicated or reordered source panels.

For saved structured handoffs, use the [validation contract](validation-contract.md): `--format reference` for terse prose, `--format keyframes` for transitions, and `--format explicit` for timed blocks. Include the actual rendered-board read record and, when compressing panels, the complete panel-map file. Ordinary copyable prompts need no saved JSON record; actual board inspection and ordered correspondence still apply. Sound is optional unless requested. All explicit timing must be contiguous.
