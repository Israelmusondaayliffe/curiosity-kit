# Kling — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## 3.0, 3.0 Omni

Surface: Kling app guides; API schema only shell

### Status
App documented; exact native API IDs provisional

### Source preservation
Dedicated builder plus Stage-2 target

### Modes
T2V; I2V; first/last; multi-shot; Elements identity/voice; Omni reference/edit workflows

### Prompt
Use one coherent shot or explicit per-shot content and duration. Custom Multi-Shot requires Multi-Shot enabled. Bind named subjects and speaker dialogue; describe reference roles rather than re-explaining bound voices.

### Controls
- Duration: 3–15 seconds
- Audio: 3.0 native audio; early guide covers Chinese/English/Japanese/Korean/Spanish
- References: 3.0 Omni February guide: 7 images without video; with video 4 image/element refs and one 3–10s video
- Resolution: February 720p/1080p list superseded by later 4K announcement
- Seed: Unknown native API contract
- Negative: Unknown native API field

### Cautions
September comparison increases video-reference allowance; do not combine old/new limits without surface/version check. Early Omni video-input/native-audio limitation needs current recheck. App Elements, Motion Control and native API are not interchangeable.

### Primary evidence
- [Kling Video 3.0 guide](https://kling.ai/quickstart/klingai-video-3-model-user-guide). primary guide body opened Publication/update: 2026-02-06. Access: 2026-10-09.
- [Kling Video 3.0 Omni guide](https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide). primary guide body opened Publication/update: not established. Access: 2026-10-09.
- [Kling native 4K announcement](https://kling.ai/blog/kling-ai-introduces-native-4k-video-model). primary article body opened Publication/update: 2026-05-20. Access: 2026-10-09.
- [Kling 4.0 versus 3.0](https://kling.ai/blog/kling-4-vs-3). primary comparison body opened Publication/update: 2026-09-30. Access: 2026-10-09.
- [Kling API capability map](https://kling.ai/document-api/guides/capability-map/video). JS shell only; indexed snippet not a verified schema Publication/update: not established. Access: 2026-10-09.

## 4.0, 4.0 Flash

Surface: Kling app early-access announcement

### Status
September 28 staged early access; full model planned October 2026, general availability unconfirmed

### Source preservation
Current catalog expansion, separate from requested 3.0

### Modes
generation; multimodal reference; keyframe sequencing; targeted video editing

### Prompt
Use a short concept or explicit camera/action/dialogue/timing instructions. Give each reference its specific identity, motion, camera, pacing or style role; name primary edit footage and changes.

### Controls
- Duration: 3–30 seconds announced
- References: Combined 15 assets; up to10 images,5 videos totaling30s,7 subjects with3 video-based
- Keyframes: Up to10
- Resolution: 720p/1080p/4K;21:9;10-bit HDR described as coming soon
- Audio: Stereo announced
- Seed: Unverified
- Negative: Unverified

### Cautions
Do not advertise HDR or full rollout as available merely because October has begun. No verified exact native API alias.

### Primary evidence
- [Kling 4.0 versus 3.0](https://kling.ai/blog/kling-4-vs-3). primary comparison body opened Publication/update: 2026-09-30. Access: 2026-10-09.
- [Inside Kling 4.0 complete guide](https://kling.ai/blog/kling-4-ai-video-model). primary guide body opened Publication/update: 2026-09-30. Access: 2026-10-09.


## Versioned shot and reference construction

Authored 3.0 I2V: “The cyclist coasts to a stop beside the wall, plants one foot, and looks toward the street. The camera tracks gently left to keep the cyclist centered.” The source supplies appearance; use one feasible motion chain rather than an unrelated new scene.

For 3.0 Custom Multi-Shot, enable the actual UI operation and provide explicit per-shot content/duration. Keep subject and speaker names stable; bind Elements and voice references through their selected controls. For 3.0 Omni editing, identify master footage and requested borrowed dimensions. A reference video's camera path does not automatically transfer its actor or costume.

For selected 4.0/Flash authoring, a reference brief may distinguish image identity, motion footage, pacing and audio. Keep staged-access and announced features visible. Do not invent native API @ tags, seed, negative fields or JSON from readable app instructions. Retain original Stage-2 board/reference and Chinese/English forms through [previs](../../video/methods/previs.md).

Retain the original BUILD, ANIMATE, DECONSTRUCT and REMIX pathways, including role-aware multi-sheet/storyboard translation and the adjacent Smart Storyboard pattern. Descriptive roles remain the fallback when native tags are unverified; an adjacent pattern does not prove a dedicated API operation.
