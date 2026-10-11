# Luma — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## Ray3, Ray3 Modify

Surface: Dream Machine app

### Status
Original version documentation retained alongside later releases

### Source preservation
Explicit Stage-2 Ray3 plus generic I2V template

### Modes
T2V; I2V; keyframes; extend; loop; visual annotation; Modify

### Prompt
Preserve visual-reference and keyframe conditioning; articulate desired motion and continuity. Modify specifies transformation versus retained performance. Draft/Reasoning/HDR are workflow controls, not decorative prompt terms.

### Controls
- Quality: HDR and EXR workflows; Hi-Fi 4K mastering separate
- Exact alias: App label Ray3 is not ray-3.2 API

### Cautions
Do not migrate the original Ray3 branch to Ray3.2 silently. Native audio not established by these sources.

### Primary evidence
- [Luma Ray3 guide](https://lumalabs.ai/learning-hub/ray3-user-guide). primary guide body opened Publication/update: 2025-09-06. Access: 2026-10-09.
- [Luma Ray3 FAQ](https://lumalabs.ai/learning-hub/ray3-faqs). primary page body opened Publication/update: not established. Access: 2026-10-09.
- [Luma Ray3 Modify guide](https://lumalabs.ai/learning-hub/ray3-modify-user-guide). primary guide body opened Publication/update: not established. Access: 2026-10-09.
- [Luma keyframes guide](https://lumalabs.ai/learning-hub/how-to-use-keyframes). primary guide body opened Publication/update: not established. Access: 2026-10-09.

## Ray3.2

Surface: Luma Agents API

### Status
Public API documented; access-dependent HDR/reframe features

### Source preservation
Current expansion

### Model ids
ray-3.2

### Modes
T2V; I2V; video_edit; video_reframe; extension chaining

### Prompt
Describe desired result while using actual frame anchors and preservation controls; source-video editing is distinct from image interpolation.

### Controls
- Duration: Generation5/10s; edit source ≤18s, duration inherited
- Keyframes: 1–64 output-frame anchors; edit anchors use separate video.edit fields; mutually exclusive with legacy start/end/loop
- Resolution: 360p draft, 540p,720p,1080p; reframe1080p rolling out
- Edit: Depth,face,normals,pose,trajectory controls and adhere/flex/reimagine strengths
- Hdr: Access required; EXR requires HDR
- Loop: No 10s or HDR

### Cautions
Indexed launch20s/16-keyframe claims differ from current API; use selected surface. Seed/negative/audio fields not established.

### Primary evidence
- [Luma create generation API](https://docs.agents.lumalabs.ai/api/resources/generations/methods/create/). primary API body opened Publication/update: not established. Access: 2026-10-09.
- [Luma Ray3.2 announcement](https://lumalabs.ai/news/introducing-ray-3-2). search-index body only; direct open failed Publication/update: 2026-06-09. Access: 2026-10-09.


## Preserve Ray3 operations while adding Ray3.2

Authored Ray3 I2V: “The hanging lantern sways gently as fog passes behind it. Keep the camera close and let the lantern settle near center.” For Ray3 Modify: “Make the lantern look carved from translucent amber; preserve its motion, framing and the source performance.” Use actual image, keyframe or video inputs for the intended mode.

Ray3 keyframes, extension, loop, visual annotations, Draft/Reasoning and HDR/EXR workflows remain distinct selected operations. Their historical app recipes do not become Ray3.2 API requests. For Ray3.2 video_edit, specify change/preserve intent and use its explicit edit controls; for reframe, preserve the action while changing the canvas through the supported operation.

A 64-anchor API limit does not prove 64 independent cuts or exact temporal fidelity. Frame anchors, start/end, loop and edit-anchor namespaces must be validated against the selected API; do not mix mutually exclusive fields. HDR/EXR and Hi-Fi mastering are output/workflow decisions, not descriptive adjectives.

For the retained storyboard-sequence adaptation, use the actual approved hero/start image. Do not claim to have cropped or uploaded a clean opening frame until that artifact exists.
