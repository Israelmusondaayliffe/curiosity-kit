# Failure Modes

Current use: follow [previs method](../../methods/previs.md) and `validation-contract.md` for mode-specific timing, actual upload roles, autonomy and evidence. Version names and provider behavior in imported examples are historical, unverified here; reuse their craft without treating them as current native controls or rankings.
Seven documented failure modes for Previs-to-Sequence. Each has a clear cause, Stage 1 mitigation, Stage 2 mitigation, and model-specific notes. Reference during validation and when iterating after a failed generation.

## Quick-reference table

| Failure | Symptom | Primary mitigation |
|---|---|---|
| Motion discontinuity | Video jumps between panels with hard cuts | Continuous-motion language in Stage 2 |
| Character drift | Subject identity shifts across shots | Character ref sheets as @Image2+ |
| Timing mismatch | Beats don't align with storyboard | Explicit time-stamped blocks summing to total |
| Panel count mismatch | Video compresses more panels than expected | One paragraph per panel in Stage 2 |
| Style drift | Final video looks nothing like storyboard | Accept the limit. Use storyboard for structure only. |
| Hero-frame divergence | Video starts at hero, drifts in 2 seconds | Match the intended opening action to the actual opening reference |
| Text/glyph corruption | Storyboard text bleeds into video | Stage 2 instruction to ignore annotations |

## 1. Motion Discontinuity Between Panels

**Symptom:** Video model treats each panel as an independent shot. Output is choppy. Subject teleports between positions. Camera cuts feel mechanical rather than choreographed.

**Cause:** Stage 2 prompt is structured as discrete shots without bridging language. Video model defaults to treating beat blocks as cuts.

**Stage 1 mitigation:** Ensure adjacent panels share a continuous spatial relationship. Don't jump the subject across the frame between consecutive panels unless the camera does a documented whip-pan or hard cut.

**Stage 2 mitigation:** Write the prompt as one flowing narrative. Use bridging phrases between beat blocks: "as the camera continues to push in", "she rises smoothly from the crouch", "the dolly carries through". For models that support it (the selected supported model), explicitly say "continuous motion, no cuts".

**Model note:** These are possible failure patterns, not provider rankings or guaranteed behavior. Inspect the actual selected model output.

## 2. Character Drift / Identity Shift

**Symptom:** Subject's face, build, costume, or color shifts across shots. Most visible in shots that change distance (CU after WS).

**Cause:** Storyboard composite alone has insufficient character detail. Video model interpolates between panels using its own learned subject priors.

**Stage 1 mitigation:** Build a dedicated character reference sheet as a side column in the composite (front, side, three-quarter back, expression set, costume close-ups, weapon or prop detail). For multi-character work, build one sheet per character.

**Stage 2 mitigation:** Upload character sheets as additional `@Image` references. Use supplied reference roles and stable identity descriptions:

- State the subject and actual identity reference clearly near the start.
- Keep descriptions consistent; a seed, if supported, does not guarantee identity.
- Veo 3.1: explicit phrase "the same [character with detailed description] as shown in @Image1" at each major shot.
- Keep an explicit identity description where useful without claiming stronger model persistence.

**Iteration tip:** If drift happens despite refs, simplify the character. Reduce distinctive features to 3 to 5 strong identifiers. Models lose minor details before major ones.

## 3. Timing Mismatch

**Symptom:** Generated video doesn't match the storyboard's beat structure. Action lands too early or too late. Total duration drifts.

**Cause:** Stage 2 prompt lacks explicit time-stamped blocks, or the model ignores them, or the beat brackets don't sum to the declared total duration.

**Stage 1 mitigation:** Make beat brackets unambiguous in each panel. Write `[0-1.25s]` not `~1s`. Brackets must sum exactly to the total declared duration.

**Stage 2 mitigation:** Use an explicit timing format for timed prompts; descriptive bracket formats below are not proof of native controls.

- Seedance 2.0: `[0-Xs]` square bracket blocks at the start of each beat sentence.
- Veo 3.1: `Clip N [Xs-Ys]:` headers.
- Kling 3.0: `[Xs-Ys] Shot N:` blocks.

Run `validate_stage2_prompt.py` to confirm timing brackets sum to declared duration before shipping.

**Iteration tip:** Inspect the actual timing failure, then change one relevant instruction or clip setting within the authorized retry budget. Do not alter the requested duration based on an unsupported overshoot percentage.

## 4. Panel Count Mismatch

**Symptom:** Video has fewer distinct shots than the storyboard panel count. Fast sequences are compressed; the model dropped beats.

**Cause:** Video model treats dense panel sequences as suggestions rather than discrete shots. Common at 12+ panels for short durations.

**Stage 1 mitigation:** Match panel count to motion register and duration (see pattern-anatomy.md). Don't over-pack 16 panels into 10 seconds. Use 8 panels for slow narrative, 12 for fast, 16 only for combat or rhythm-driven sequences with explicit beat sync.

**Stage 2 mitigation:** Write one full prompt paragraph per panel in Stage 2 even when content is similar. The verbal density signals to the model that each beat is distinct. Avoid running multiple panels into a single sentence.

**Iteration tip:** If the model keeps compressing despite full paragraphs, drop to a lower panel count in Stage 1. Try 8 panels for 15 seconds when 12 keeps collapsing.

## 5. Style Drift Between Storyboard and Video

**Symptom:** Final video looks polished and photoreal even though the storyboard was hand-drawn schematic. Or the opposite, when the user wanted the ink-wash look preserved.

**Cause:** Storyboard aesthetic (low-detail previs, hand-drawn, schematic) is interpreted by the video model as a structural reference, not a style reference. Video model defaults to its trained aesthetic.

**Stage 1 mitigation:** None for the storyboard itself. Keep the board readable. A drawn, polished or final-look treatment can all be useful when requested.

**Stage 2 mitigation:** State the target visual style explicitly and separately from the storyboard reference. Frame the storyboard as "shot structure and timing reference" not "visual style reference". When the user wants the final video to preserve the storyboard's drawn aesthetic (rare, but observed in ink-wash variants), say so explicitly: "Preserve the ink-wash monochrome aesthetic of @Image1." Even then, expect partial migration toward the model's default style.

**Accepted limit:** Style locking across image and video stages is a known unsolved problem. Set user expectations. Tell them: "The storyboard drives shot structure. The video model brings its own aesthetic. Some style migration is normal."

## 6. Hero-Frame Divergence

**Symptom:** Video starts very close to the hero frame for the first 0.5 seconds, then drifts away rapidly. Subject identity loosens after 2 to 3 seconds.

**Cause:** Video model treats the hero frame as a starting suggestion rather than a hard anchor. The model's motion priors override the hero's specific composition after a beat.

**Stage 1 mitigation:** Make the hero frame visually unambiguous. Strong character silhouette, clear pose, recognizable lighting. Avoid hero frames with ambiguous subject orientation.

**Stage 2 mitigation:** Match the actual opening pose, action and camera framing. Request a hold only if the board calls for one. Supply a clean start/end frame only when present and supported; an identity sheet is not a substitute opening scene.

**Model note:** These are possible failure patterns, not provider rankings or guaranteed behavior. Inspect the actual selected model output.

## 7. Text or Glyph Corruption from Storyboard Annotations

**Symptom:** Final video has visible text, arrows, panel borders, or annotation marks bleeding into the rendered scene. Numbers from panel labels appear as floating glyphs.

**Cause:** Storyboard composite contains annotated text (timing brackets, camera notes, panel numbers, arrows). Video model interprets these as visual content to reproduce.

**Stage 1 mitigation:** Keep all annotations outside the panel image area. Use margin labels, footer legend, side columns. Avoid drawing text or numbers inside the panel frame itself. Use a contrasting color for annotations (typically white on dark margins, or black on light margins) so the model can clearly distinguish annotation from content.

**Stage 2 mitigation:** Instruct the video model to ignore the storyboard's annotation overlay. "Ignore panel borders, arrows, timing brackets, and panel numbers visible in @Image2. Use the storyboard only for shot structure and subject pose reference. The final video has no on-screen text, no annotations, no panel borders."

Suppress unwanted annotations. Preserve requested wordmarks, title cards or subtitles; do not contradict them with a blanket no-text directive.

## Iteration cost guidance

When a generation fails, iterate by:

1. **First, identify which failure mode hit.** Usually obvious from the symptom.
2. **Apply the Stage 2 mitigation first.** Cheaper than re-running Stage 1.
3. **If Stage 2 mitigation doesn't resolve it, regenerate Stage 1.** Common cases: panel count was wrong, annotations bled, hero frame was ambiguous.
4. **If the issue persists across multiple Stage 1 + Stage 2 iterations, consider model swap.** Some failure modes are model-specific (style drift varies, character drift varies). The model-pair matrix has alternates.
5. **For long sequences, inspect segmentation needs.** Match editorial segments to actual surface limits and preserve continuity frames; do not impose a universal duration ceiling.

Use only the approved generation/retry budget. Identify a concrete defect before another attempt; no fixed iteration count or success rate is promised.
