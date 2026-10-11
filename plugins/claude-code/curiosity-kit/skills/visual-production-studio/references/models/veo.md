# Veo — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## 3.0, 3.0 Fast, 2 historical adjacent example

Surface: Gemini API / Google enterprise API

### Status
Veo3 aliases retired 2026-06-30

### Source preservation
Original builder targets Veo3; Veo2 adjacent pair retained as provenance

### Model ids
veo-3.0-generate-001; veo-3.0-fast-generate-001

### Modes
Historical T2V/I2V audiovisual authoring

### Prompt
Retain version-labelled historical prompt patterns without an active execution promise.

### Controls
- Execution: Disabled for retired IDs; no silent substitution

### Cautions
Veo2 edit or silent-video features must not be relabelled Veo3/3.1. Veo2 complete current status not independently audited here.

### Primary evidence
- [Gemini API deprecations](https://ai.google.dev/gemini-api/docs/deprecations). primary lifecycle table opened Publication/update: not established. Access: 2026-10-09.
- [Google enterprise Veo 3 model](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-0-generate). primary model page opened Publication/update: not established. Access: 2026-10-09.
- [Gemini API Veo guide](https://ai.google.dev/gemini-api/docs/veo). primary guide body opened; mode and limit sections inspected Publication/update: not established. Access: 2026-10-09.

## 3.1, 3.1 Fast, 3.1 Lite

Surface: Gemini API

### Status
Preview IDs; earliest shutdown 2026-10-22; recommended successor is a different family

### Source preservation
Explicit Stage-2 Veo3.1 target

### Model ids
veo-3.1-generate-preview; veo-3.1-fast-generate-preview; veo-3.1-lite-generate-preview

### Modes
T2V; I2V; first+last; asset-reference generation; Veo-output extension

### Prompt
Subject, action, context, style and cinematography; separately describe dialogue, ambience and SFX. Negative field should list excluded elements rather than imperative no/don't sentences.

### Controls
- Duration: 4/6/8s; reference/extension/high-resolution combinations require8s
- References: Up to 3 asset images; first+last separately
- Resolution: Standard/Fast 720p/1080p/4K, extension 720p; Lite limits differ
- Aspect: 16:9 or9:16
- Extension: Existing Veo outputs; +7s, up to 20 extensions, maximum 148s
- Seed: Available, not deterministic guarantee
- Audio: Native synchronized audio

### Cautions
Lite support differs between Gemini and enterprise docs; verify selected route. Arbitrary video reference/edit is not established by Veo extension support. Two-day output retention in guide; downloading is a distinct authorized action.

### Primary evidence
- [Gemini API Veo guide](https://ai.google.dev/gemini-api/docs/veo). primary guide body opened; mode and limit sections inspected Publication/update: not established. Access: 2026-10-09.
- [Gemini API deprecations](https://ai.google.dev/gemini-api/docs/deprecations). primary lifecycle table opened Publication/update: not established. Access: 2026-10-09.
- [Google video prompt guide](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide). primary page body opened Publication/update: not established. Access: 2026-10-09.
- [DeepMind Veo prompt guide](https://deepmind.google/models/veo/prompt-guide/). primary page body opened Publication/update: not established. Access: 2026-10-09.

## 3.1 GA, 3.1 Fast GA

Surface: Google enterprise API

### Status
GA; retirement date November 17 2026 or later shown on model page

### Source preservation
Surface-specific counterpart, never merged with preview aliases

### Model ids
veo-3.1-generate-001; veo-3.1-fast-generate-001

### Modes
T2V; I2V; first+last; asset reference; extension; audio

### Prompt
Apply model-specific Google video prompt guide, then validate enterprise controls.

### Controls
- Duration: 4/6/8s; reference 8s
- Aspect: 16:9,9:16
- Outputs: Up to 4
- Resolution: Standard720p/1080p/4K; Fast720p/1080p in model table
- Input: Image 20 MB; 24 fps

### Cautions
Enterprise lifecycle is independent of Gemini preview retirement. Model-page internal Lite modality/extension inconsistencies unresolved.

### Primary evidence
- [Google enterprise Veo 3.1 model](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate). primary model page opened Publication/update: 2026-10-09. Access: 2026-10-09.
- [Google video prompt guide](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide). primary page body opened Publication/update: not established. Access: 2026-10-09.


## Version-specific authoring examples

Authored retained Veo 2 visual brief: “A locked wide shot of a greenhouse at dawn. Condensation glints on the glass as a gardener opens a roof vent; faint mist moves through the plants.” This preserves the historical visual recipe without assigning Veo 3 audio or Veo 3.1 controls. Current Veo 2 execution remains unqualified here.

Authored Veo 3 historical audiovisual brief: “A medium shot of a baker setting a tray on a wooden counter. She says, ‘Fresh from the oven.’ Quiet room tone and a soft tray tap.” Keep this as version-labelled authoring because inspected Gemini API 3.0 aliases are retired. Do not turn enterprise evidence into a claim about those aliases.

For selected Veo 3.1 on a verified live route, organize subject/action/setting/cinematography and separately name dialogue, ambience and SFX. Use an actual asset-reference input for identity, actual first/last inputs for boundaries, and an actual eligible Veo output for extension. Authored extension: “Continue the baker's motion as she slides the tray toward camera, maintaining the counter-level framing and room ambience.” Arbitrary video editing is not established by extension support.

Check duration/reference/resolution combinations rather than assuming every 4/6/8-second mode accepts the same inputs. If a negative field is needed, list unwanted elements, not commands. Do not add exclusions the user never requested merely to fill a template.

The original storyboard branch also retains structured Clip blocks, dialogue/SFX prose, multi-sheet role adaptation, JSON planning, DECONSTRUCT and REMIX. Clip/SFX labels and arbitrary storyboard JSON are organizational authoring formats until the exact Flow, Gemini API or enterprise schema establishes native fields.
