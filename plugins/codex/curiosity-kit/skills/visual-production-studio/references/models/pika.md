# Pika — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## V2.2, Pikaframes original

Surface: Pika legacy app FAQ

### Status
Version-preserved; FAQ latest 2.2 wording is stale against 2.5 catalog

### Source preservation
Explicit Stage-2 target and sparse keyframe-transition templates

### Modes
T2V; I2V; Pikascenes; Pikaframes

### Prompt
Retain original version-labelled motion and ordered-transition templates, with requested timing and start/end identity.

### Controls
- Duration: Legacy T2V/I2V 5/10s
- Resolution: 720p/1080p

### Cautions
FAQ disagrees internally on Pikaframes 10s versus 25s; no universal cap inferred. Pikaswaps/Pikadditions/Pikatwists and separate audio tools are not automatically native 2.2 capabilities.

### Primary evidence
- [Pika FAQ](https://pika.art/faq). primary page body opened Publication/update: not established. Access: 2026-10-09.
- [Pika 2.5 Pikaframes API](https://dev.pika.art/models/pika/pikaframes/image-to-video). primary request schema opened Publication/update: not established. Access: 2026-10-09.

## 2.5, 2.5 Keyframe

Surface: Pika native API

### Status
Current first-party schema

### Source preservation
Current expansion

### Model ids
pika/pika-2.5/image-to-video; pika/pikaframes/image-to-video

### Modes
I2V; ordered keyframe interpolation

### Prompt
Image supplies subject; prose directs motion. Keyframe transitions can share optional motion guidance. Negatives are a dedicated field on these endpoints.

### Controls
- Duration: I2V 5/10s; keyframe transitions 1–10s, >5s only with 2 frames
- References: Pikaframes 2–5 ordered images
- Resolution: 720p/1080p enums; do not infer every combination
- Seed: Dedicated integer
- Negative: negative_prompt

### Cautions
I2V page generic capability text says T2V but required image schema governs this endpoint. Pika API also aggregates other providers; aliases remain wrapper-specific.

### Primary evidence
- [Pika 2.5 I2V API](https://dev.pika.art/models/pika/pika-2.5/image-to-video). primary request schema opened Publication/update: not established. Access: 2026-10-09.
- [Pika 2.5 Pikaframes API](https://dev.pika.art/models/pika/pikaframes/image-to-video). primary request schema opened Publication/update: not established. Access: 2026-10-09.


## Retained V2.2, Pikaframes and current 2.5

Authored V2.2 I2V: “The small robot tilts its head toward the flower, reaches out slowly, and stops with its hand beside the petals. Camera remains steady.” This preserves the original animation route without importing 2.5 fields. For Pikaframes, supply actual ordered keyframes and describe the visual transition; different FAQ duration claims remain unresolved, so do not promise a universal interval.

For a selected Pika 2.5 endpoint that exposes negative_prompt, put relevant user-requested exclusions there rather than grafting the field onto every version. Keyframe generation is a separate schema from basic I2V. A transition between two supplied states needs continuity and feasible motion, not an obligatory generic four-beat story.

For the retained sparse Pikaframes recipe, preserve one transition prompt per adjacent keyframe pair and exactly N−1 transitions for N ordered frames. Sample actual storyboard panels into source images; keep identity/style roles stable and avoid forcing dense timestamps onto sparse anchors.
