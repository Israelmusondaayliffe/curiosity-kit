# Vidu — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## Q3 Pro, Q3 Turbo, Q3 Pro Fast, Q3 Mix/Drama/Ad, Q2, Q1, 2.0

Surface: Vidu native API

### Status
Current Q3 catalog/schema; older families cataloged without full mode guide audit

### Source preservation
Original Vidu mention-only model-pair example; current expanded family

### Model ids
viduq3-pro; viduq3-turbo; viduq3-pro-fast; viduq3-mix; viduq3-drama; viduq3-ad

### Modes
Q3 T2V; I2V; start/end; reference-to-video

### Prompt
Specify subject movement and camera evolution. Audio dialogue/SFX are native when enabled. Set mode and exact version before applying constraints.

### Controls
- Duration: Q3 1–16s
- Aspect: T2V16:9,9:16,3:4,4:3,1:1
- Resolution: T2V Pro/Turbo 540p/720p/1080p; per-mode variants differ
- Seed: 0/unset random; manual override
- Audio: Boolean default true
- Prompt: Pro T2V 20k characters; Turbo text section 5000; start/end 20k
- Frames: Two ordered images; boundary resolution ratio 0.8–1.25

### Cautions
Legacy short docs URLs were shells; new nested URLs are readable. Q3 reference endpoint failed to open; complete reference limits unverified. Q2 supports some editing, not proof Q3 is a general editor.

### Primary evidence
- [Vidu Q3 text-to-video](https://platform.vidu.com/docs/api-reference/video-models/vidu-q3/text-to-video). primary schema body opened Publication/update: not established. Access: 2026-10-09.
- [Vidu Q3 start-end-to-video](https://platform.vidu.com/docs/api-reference/video-models/vidu-q3/start-end-to-video). primary schema body opened Publication/update: not established. Access: 2026-10-09.
- [Vidu model map](https://platform.vidu.com/docs/overview/model-map). primary page body opened Publication/update: not established. Access: 2026-10-09.

## Q4 Preview

Surface: Vidu native API

### Status
Preview

### Source preservation
Current expansion

### Model ids
viduq4-preview

### Modes
I2V; reference-to-video

### Prompt
Manual prompting requires is_rec=false; default true replaces user text with a recommendation. Preserve exact dialogue intent and explicit camera transitions.

### Controls
- Duration: I2V 3–16s; model map says 1–16s, unresolved
- Resolution: 540p/720p/1080p/2K/4K
- Image: One start frame <=50MB
- Prompt: 20k characters
- Seed: 0/unset random
- Audio: Boolean default true
- References: R2V 1–15 images; up to 3 audio references, each 3–12s; five aspect ratios

### Cautions
images typed string in schema but array in example; validate contract before execution. R2V note says subject invocation unavailable, while prompt field specifies [@subjects_name]; mapping mechanism unresolved.

### Primary evidence
- [Vidu Q4 Preview I2V](https://platform.vidu.com/docs/api-reference/video-models/vidu-q4-preview/image-to-video). primary schema body opened Publication/update: not established. Access: 2026-10-09.
- [Vidu model map](https://platform.vidu.com/docs/overview/model-map). primary page body opened Publication/update: not established. Access: 2026-10-09.
- [Vidu Q4 Preview reference-to-video](https://platform.vidu.com/docs/api-reference/video-models/vidu-q4-preview/reference-to-video). primary page body opened; relevant model/mode sections inspected Publication/update: not established. Access: 2026-10-09.


## Creation versus reference composition

Authored Q3 I2V: “The wooden toy boat gently rocks once, then drifts to the right; the camera holds the source framing.” For Q4 reference generation, identify the actual referenced subjects and their contribution, keeping names and media order aligned with the chosen endpoint. Do not invent a universal subject-invocation token while the owner examples conflict.

If the user has supplied exact dialogue, text or shot instructions, automatic recommendation/rewrite must not silently replace them. Record the selected behavior and verify the returned output. A model-map duration claim cannot resolve the conflicting Q4 I2V minimum; validate that exact endpoint. Older Q2/Q1/2.0 entries remain discoverable without inheriting Q4 controls.
