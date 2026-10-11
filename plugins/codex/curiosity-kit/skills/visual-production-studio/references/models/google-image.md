# Google Gemini — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## Nano Banana 2, gemini-3.1-flash-image, Nano Banana 2 Lite, gemini-3.1-flash-lite-image, Nano Banana Pro, gemini-3-pro-image

Surface: Gemini API, with current main guide using Interactions API

### Status
original_targets_confirmed

### Prompting
Describe a coherent scene with purpose and camera language. Assign each reference a role; use small iterative edits and positive alternatives to vague negations. No universal 120-word cap or required ratio tail.

### Multioutput
Guide explicitly warns requested output counts may not be followed. Count returned images, not prose intentions.

### Guide gap
No arbitrary cross-surface parameter translation; resolve conflicting quotas before execution.

### Primary evidence
- [Gemini image generation](https://ai.google.dev/gemini-api/docs/image-generation). Selected model selection 121–129; editing 458–460; reference table 784–803; grounding 1248–1252; video 1385–1389; identity 5112–5114; best practices 5155–5179; limitations/output 5288 onward; page date. Examples not all read. Publication/update: 2026-10-09. Access: 2026-10-09.
- [gemini-3.1-flash-image model card](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image). Rendered model card lines 88–123; full model specification section. Publication/update: 2026-10-09. Access: 2026-10-09.
- [gemini-3.1-flash-lite-image model card](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-image). Rendered model card lines 88–123; full model specification section. Publication/update: 2026-09-03. Access: 2026-10-09.
- [gemini-3-pro-image model card](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image). Rendered model card lines 88–112; full model specification section. Publication/update: 2026-09-03. Access: 2026-10-09.

## Nano Banana 2.1, gemini-nano-banana-2.1

Surface: Gemini API / AI Studio

### Status
new_current_discovery

### Prompting
Use the current shared image guide; detailed scene and reference-role instructions, conversational edits.

### Controls
1K default,2K,4K; thinking minimal/medium(default)/high; web+image search. Stable model, October2026 update.

### Primary evidence
- [gemini-nano-banana-2.1 model card](https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1). Rendered model card lines 88–119; full model specification section. Publication/update: 2026-10-06. Access: 2026-10-09.
- [Gemini image generation](https://ai.google.dev/gemini-api/docs/image-generation). Selected model selection 121–129; editing 458–460; reference table 784–803; grounding 1248–1252; video 1385–1389; identity 5112–5114; best practices 5155–5179; limitations/output 5288 onward; page date. Examples not all read. Publication/update: 2026-10-09. Access: 2026-10-09.


## Retained studio craft

Use the same detailed creative briefs and JSON/system formats when useful. Identify each reference's contribution and distinguish scene changes from identity. Keep coherent material, contact and light response. Do not impose a 120-word cap, ten outputs, mandatory pose change or aspect-ratio tail. State the intended ratio where relevant and verify the rendered result. Structured prompt fields do not automatically become Gemini API parameters. Exact output counts and flawless lettering are not guarantees.

## Reference construction and version-faithful example

For selected Nano Banana Pro, bind Image 1 to subject identity and Image 2 to the room: “Place the ceramic rabbit from Image 1 on the window ledge in Image 2. Preserve its ear shape, green glaze and small crack on the left side. Match the room's daylight and perspective.” This authored example follows the shared reference-role guide, not a guarantee that every supplied detail survives. A later edit should name one change and reuse the actual returned image.

Nano Banana 2 and 2 Lite keep their own model identities and capability tables. Do not choose Lite for a reference-heavy task merely because it accepts an image. The guide's Pro reference count conflicts between sections, and Lite's listed ratio count conflicts with its enumerated ratios; resolve selected-route limits before execution.

For camera studies, distinguish “same moment, camera moves to the right” from “a later moment, subject turns right.” Retain source NL, descriptive JSON and system-style recipes. The optional Nano Banana → Midjourney logo-retexture pipeline remains a deliberate two-stage choice; export an actual accepted image between stages and preserve both model selections.
