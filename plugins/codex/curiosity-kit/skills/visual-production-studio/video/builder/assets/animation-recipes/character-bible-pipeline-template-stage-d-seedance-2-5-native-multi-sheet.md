# Character Bible Pipeline Template (Stage D, Seedance 2.5 native multi-sheet)

Selected recipe: use only relevant fields, supplied assets and the exact model profile. Descriptive tags and JSON are not universal native controls; preserve requested count/style/copy.


Use this template for the Character Bible Pipeline sub-mode of ANIMATE. The full A-B-C-D doctrine lives in [character-continuity method](../../../methods/character-continuity.md). This template covers the Stage D Seedance prompt only.

The prompt uses role-aware `@`-tags. `@Image 1` is the persistent identity anchor that renders as the subject whenever that character appears. Additional tags are consistency references (character sheet, wardrobe sheet, emotion sheet) or the structural guide (storyboard). Reference tags do not render. The do-not-render directive is mandatory and must name the specific visual artifact to suppress.

### Stage D Prompt Structure

```
SUBJECTS:
@Image 1 is the main character. [Compact character description: who they are, canonical look, identity markers from the hero shot, build, hair, signature wardrobe.] Use @Image 1 as the persistent visual anchor whenever that character appears. Whenever this character appears, preserve this exact face, build and signature look; keep intended empty cutaways.

REFERENCES (consistency only, never rendered as standalone images):
@Image 2 is the character turnaround sheet. Use it to keep face, head shape, body proportions, and hair consistent across angles. Do not render @Image 2 in the video. Do not show multi-view turnaround layouts, character sheet boxes, view labels, or any sheet-style framing.
@Image 3 is the wardrobe sheet. Use it to keep clothing, materials, colors, and accessories consistent. Do not render @Image 3 in the video. Do not show wardrobe breakdowns, garment labels, fabric swatches, or any catalog-style layout.
@Image 4 is the emotion sheet. Use it to keep facial expressions within the character's emotional range. Do not render @Image 4 in the video. Do not show expression grids, emotion labels, or any expression-sheet framing.

STRUCTURAL GUIDE (do not render, sequence reference only):
@Image 5 is the storyboard composite. Follow the panel-by-panel sequence shown in @Image 5 exactly. Each panel is one full shot in the video timeline. Do not render @Image 5 in the video. The final video does not show panel borders, panel numbers, timing brackets, annotation arrows, grid layout, or any storyboard-style framing.

ENVIRONMENT:
[Setting description: where the action happens, lighting register, atmosphere.]

STYLE:
[Visual style of the FINAL VIDEO. This is the cinematic finish, separate from any reference image's drawing style. A storyboard may be sketchy or polished; preserve its look if requested, otherwise distinguish final style. State the final style explicitly: e.g., "cinematic 3D animation in Pixar / Donotopia register, soft volumetric lighting, warm grade, shallow depth of field," or "live-action cinematic, 35mm anamorphic, film grain, naturalistic color."]

[Shot 1] [0-Xs] [Action mirroring panel 1 of @Image 5]. The character (@Image 1) [specific action]. Camera: [from panel 1: lens, angle, distance, move]. End state: [where things are]. SFX: <[from panel 1]>.
[Shot 2] [Xs-Ys] [Action mirroring panel 2 of @Image 5]. The character (@Image 1) [specific action]. Camera: [from panel 2]. End state: [...]. SFX: <[from panel 2]>.
[Shot 3] [...continued through each panel of the storyboard...]
[...]
[Shot N] [(N-1)t-Nt] [Final shot, mirroring panel N of @Image 5]. The character (@Image 1) [closing action]. Camera: [from panel N]. End state: [...]. SFX: <[from panel N]>.

GLOBAL CONSTRAINTS:
Maintain the exact character from @Image 1 whenever that character appears. Same face, same hairstyle, same outfit, same body type where visible unless the brief changes it. Cross-check face, body, and hair against @Image 2. Cross-check wardrobe against @Image 3. Cross-check expression range against @Image 4. Follow exact panel order from @Image 5.
No panel borders, no annotations, no timing brackets, no panel numbers, no grid layout, no on-screen text bleed from any reference image. The final video shows only the cinematic scene.
Consistent lighting, environment, and character identity across all shots. No deformation. Stable proportions. Natural motion physics. No subtitles.

AUDIO:
[Illustrative audio notation: (music), <sound effects>, {dialogue}. Or ambient-only list, or the [SOUND] foley-only directive.]

Do not change aspect ratio.
```

### REFERENCE MAPPING Block (above the prompt, NOT inside it)

Present the mapping in the response above the prompt code block. This is for the user's reference, not part of the Seedance prompt itself.

```
REFERENCE MAPPING:
@Image 1 = [description of character hero shot, role: persistent identity anchor, RENDERS as subject]
@Image 2 = [description of character sheet / turnaround, role: consistency reference, DOES NOT RENDER]
@Image 3 = [description of wardrobe sheet, role: consistency reference, DOES NOT RENDER]
@Image 4 = [description of emotion sheet, role: consistency reference, DOES NOT RENDER]
@Image 5 = [description of storyboard composite, role: structural guide, DOES NOT RENDER]
```

Drop any tag row whose asset is not in play. Adjust tag numbers to match actual upload order.

### Minimum Viable Variant (character + storyboard only)

When the user has only a character image and a storyboard (no separate bible sheets), collapse to two tags:

```
SUBJECTS:
@Image 1 is the main character. [Compact character description.] Use @Image 1 as the persistent visual anchor whenever that character appears.

STRUCTURAL GUIDE (do not render, sequence reference only):
@Image 2 is the storyboard composite. Follow the panel-by-panel sequence shown in @Image 2 exactly. Each panel is one full shot. Do not render @Image 2 in the video. Do not show panel borders, panel numbers, timing brackets, annotation arrows, grid layout, or any storyboard-style framing.

ENVIRONMENT: [...]
STYLE: [...]

[Shot 1] [0-Xs] [Action mirroring panel 1 of @Image 2]. The character (@Image 1) [action]. Camera: [...]. End state: [...]. SFX: <[...]>.
[...]

GLOBAL CONSTRAINTS:
Maintain the exact character from @Image 1 whenever that character appears. Same face, same hairstyle, same outfit, same body type where visible unless the brief changes it. Follow exact panel order from @Image 2. No panel borders, no annotations, no on-screen text bleed.

AUDIO: [...]
Do not change aspect ratio.
```

### Stage A / B / C Companion Templates (handoff prompts)

When Stages A, B, or C are not yet complete, ship one prompt per missing stage as ADDITIONAL code blocks above the Stage D prompt. Each is a brief the user pastes into the relevant image model.

**Stage A: Character hero shot prompt (target model: Nano Banana / GPT Image 2 / Midjourney)**

```
Create a single character hero shot. [Character: who they are, age, build, ethnicity, key identity markers, wardrobe, accessories.] [Pose: canonical pose that establishes silhouette.] [Lighting: register.] [Background: neutral so the character is the focus, or specific setting if appropriate.] [Style: cinematic 3D / illustrative / photoreal / etc.] [Aspect ratio: 3:4 portrait or 16:9 cinematic.] Render high detail, professional character design. This image becomes the persistent identity anchor for downstream video generation.
```

**Stage B: Character bible composite prompt (target model: GPT Image 2)**

```
PLAN: Single composite character bible sheet for [character name]. Multi-region layout containing: full-body turnaround (front, 3/4, side, back, 3/4 back), expression study (6-8 core emotions: [list]), wardrobe breakdown (key garments with detail callouts), and cinematic portrait (hero pose). All regions share one visual DNA: same face, same build, same wardrobe baseline, same lighting register.

GENERATE: Design a single 16:9 production-board image presenting a complete character bible for [character description]. Layout: clean grid-based design, labeled sections. Include character + styling reference (full-body multiple angles, plus close-ups), wardrobe breakdown with material detail, expression study grid showing emotional range, and one cinematic portrait at hero scale. Style: [cinematic 3D / illustrative / photoreal]. Background: clean white or neutral gray so character work dominates. Professional pre-production aesthetic, like a Pixar / DreamWorks character bible.

VERIFY: Before showing output, verify identity (face, build, hair) is identical across every region. Verify wardrobe is consistent across turnaround views. Verify expressions are distinct and non-repetitive. Verify layout reads cleanly as a designed sheet, not a collage.
```

If the user wants four separate sheets instead of one composite, use the local image-series method for separate sheets instead of this composite Stage B prompt. That skill handles single-axis variation (turnaround alone, expressions alone, wardrobe alone) more cleanly. Choose separate sheets or one composite by actual readability and the selected surface’s available reference budget.

**Stage C: Storyboard composite prompt (target model: GPT Image 2)**

```
PLAN: Single storyboard composite sheet for [project name]. Grid layout, [N: typically 8-12, up to 15] panels in sequence. Each panel shows one beat of the action. Style: minimal stick-figure choreography OR simplified character renders OR ink-wash silhouette (pick one), clean lines. Panels include camera grammar tokens (lens, angle, distance, move), timing brackets, SFX cues, and brief action notes.

GENERATE: Design a single [16:9 or 4:3] storyboard sheet with [N] sequential panels showing the following beats: [beat 1 description, beat 2 description, ... beat N description]. Each panel labeled with number, timing bracket (e.g., 0-2s, 2-4s), camera grammar (e.g., WIDE / HANDHELD 28mm, ECU PUSH IN 85mm), and brief SFX note. Use [stick-figure / simplified render / ink-wash] style for the choreography drawings. Layout: clean grid, panels separated by clear borders. This is a pre-production tool, not the final video aesthetic.

VERIFY: Before showing output, verify panel count matches [N]. Verify each panel has visible timing bracket, camera grammar, and SFX cue. Verify the sequence reads as a coherent narrative arc. Verify panels are styled for legibility (not cluttered).
```

If the user wants the canonical Stage 1 storyboard with full previs grammar (colored motion arrows, distinct camera tokens, SFX cue layering), use the local previs STORYBOARD-FROM-TEXT or STORYBOARD-FROM-IMAGE method. That skill is the deeper authority for Stage 1.
