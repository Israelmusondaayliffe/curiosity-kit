# Gemini Omni — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## 1.1 Flash, Flash Preview

Surface: Gemini API

### Status
Stable 1.1 and preview separately documented

### Source preservation
Current expansion; not automatic Veo substitute

### Model ids
gemini-omni-1.1-flash; gemini-omni-flash-preview

### Modes
T2V; I2V; reference-to-video; video editing; extension; first+last interpolation

### Prompt
State single continuous shot if cuts are unwanted. Use targeted edit plus preserved properties. Reference tags are zero-indexed IMAGE_REF_N/VIDEO_REF_N; boundary tags FIRST_FRAME/LAST_FRAME differ. Audio may be generated unless suppressed.

### Controls
- Duration: 3–10s
- Input video: Up to 10s for edit/extend
- Extension: +10s, total up to 40s, last 10s context; timing relative to new segment
- Resolution: 360p/720p/1080p/4K listed; native/upscale distinction must be checked
- Task: video_config.task can disambiguate but imposes constraints
- Seed: Not verified

### Cautions
Do not silently use Google’s successor recommendation when user named Veo. Exact asset count and all resolution/mode combinations need schema recheck before execution.

### Primary evidence
- [Gemini Omni API guide](https://ai.google.dev/gemini-api/docs/omni). primary guide body opened; modes and controls inspected Publication/update: not established. Access: 2026-10-09.
- [Gemini Omni Flash model](https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash). primary page body opened Publication/update: not established. Access: 2026-10-09.
- [DeepMind Omni prompt guide](https://deepmind.google/models/gemini-omni/prompt-guide/). primary page body opened Publication/update: not established. Access: 2026-10-09.


## Multimodal authoring without Veo substitution

Authored audiovisual brief: “A ceramic artist lifts a blue bowl from the wheel and sets it on a wooden shelf. The camera follows her hands. Soft studio ambience and a single ceramic tap when the bowl meets the shelf.” Bind image/video/audio inputs through the actual Omni content roles when present.

Preserve the chosen Omni model and surface. A Google migration recommendation does not authorize substituting Omni for a user's Veo 3 or 3.1 request. Conversational multimodal creation and editing require the corresponding route; verify its limits rather than borrowing Veo reference quotas, duration combinations or negative-field advice.
