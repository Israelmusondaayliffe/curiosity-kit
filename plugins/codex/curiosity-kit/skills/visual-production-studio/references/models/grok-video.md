# Grok Imagine Video — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## 1.5, 1.5 Lite, classic

Surface: xAI native API

### Status
Current catalog with strict mode/version splits

### Source preservation
Current expansion

### Model ids
grok-imagine-video-1.5; grok-imagine-video-1.5-lite; grok-imagine-video

### Modes
All:T2V/I2V; 1.5:references,keyframes; classic:edit/extend

### Prompt
Describe shot/camera/lighting and desired sound. Target one edit and preserved properties. Pin first/last separately; intermediate timestamps must be meaningful within duration.

### Controls
- Duration: 1–15s generation
- Resolution: 1.5 native 1080; Lite 1080 upscaled from 720; classic ≤720; 1.5 reference 720
- References: 1.5 up to 14 images, 3 preset voice references
- Keyframes: 1.5 first/last plus 4 interior anchors on a 1/3s grid
- Audio: Native default;generate_audio=false for silence
- Aspect: Nine listed ratios; I2V follows image
- Editing: Classic source ≤8.7s; extension adds 2–10s
- Seed: Not verified
- Negative: Not verified

### Cautions
Lite has no references/keyframe/edit/extend. Custom voice input is restricted; never infer ordinary preset access grants it.

### Primary evidence
- [xAI video overview](https://docs.x.ai/developers/model-capabilities/video/overview). primary catalog body opened Publication/update: 2026-10-08. Access: 2026-10-09.
- [xAI generation guide](https://docs.x.ai/developers/model-capabilities/video/generation). primary guide body opened Publication/update: not established. Access: 2026-10-09.
- [xAI reference-to-video](https://docs.x.ai/developers/model-capabilities/video/reference-to-video). primary guide body opened Publication/update: not established. Access: 2026-10-09.
- [xAI video editing](https://docs.x.ai/developers/model-capabilities/video/editing). primary guide body opened Publication/update: not established. Access: 2026-10-09.


## Keep the mode matrix in the prompt handoff

Authored 1.5 reference-generation intent: “Use the cyclist reference for the rider's outfit and bicycle. Follow the rider down the quiet street as the camera tracks beside her; maintain the reference colors.” Actual reference/keyframe inputs provide conditioning; prose alone does not create them.

For a classic-model edit, name the source video and local transformation: “Replace the overcast sky with warm sunset light while retaining the cyclist's motion and shot timing.” A 1.5 editing request must surface the classic-only edit/extend restriction and ask for an explicit version choice, not silently route to classic. Lite keeps its own capabilities and limits. Do not merge app and API controls by family name.
