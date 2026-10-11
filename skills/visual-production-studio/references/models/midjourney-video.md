# Midjourney Video — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## Video family; source label V1, V7 is image version

Surface: Midjourney web/Discord

### Status
Documented I2V workflow

### Source preservation
Mention-only video-duration example, retain distinction

### Modes
I2V; extension; loop; end-frame

### Prompt
Start image anchors appearance; optional text guides motion. Only video-supported parameters survive animation; image style/reference parameters do not transfer.

### Controls
- Duration: Initial 5s; extend by 4s up to 4 times, total 21s
- Resolution: 480p SD / 720p HD
- Aspect: Approximately source image
- Parameters: --motion low/high; --raw; --loop; --end; --bs 1/2/4
- Audio: Not documented
- Seed: Not documented

### Cautions
--v 7 selects image generation, not a video model. No native public API established by this guide.

### Primary evidence
- [Midjourney Video](https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video). primary guide body opened Publication/update: not established. Access: 2026-10-09.


## Animate the actual image with the video grammar

Authored manual-motion prompt: “The paper fox slowly unfolds its ears and looks toward camera; leaves drift across the foreground. A gentle camera push brings the fox closer.” Start with the actual selected image and choose the documented manual/automatic motion path. Image V7/V8 selection is not a video model version.

Retain source Video Model V1 as a historical label, with loop, end-frame and extension behavior governed by the selected current video controls. Do not carry image-only --sref, --p, --v or Edit flags into an assumed video API. Inspect generated motion and source identity instead of promising continuity from the prompt alone.
