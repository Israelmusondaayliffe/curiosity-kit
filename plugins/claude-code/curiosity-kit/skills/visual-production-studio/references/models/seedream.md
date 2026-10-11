# Seedream — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## Seedream 5.0 Lite, seedream-5-0-260128, seedream-5-0-lite-260128

Surface: ByteDance product release / BytePlus ModelArk API

### Status
original_target_confirmed

### Prompting
Release/tutorial support explicit reference roles and localized changes. API recommends ≤600 English words or 300 Chinese characters; recommendation, not a hard prompt cap.

### Multioutput
sequential_image_generation auto lets model choose actual count, capped by max_images 1–15; disabled gives one. Streaming supported.

### Guide gap
URL named 4-0-5-0-prompt-guide actually documents4.0/4.5 only. Keep its craft advice version-qualified. Lite-specific evidence is release, tutorial and API; product web-search claim does not establish BytePlus parameter availability.

### Primary evidence
- [Introducing Seedream 5.0 Lite](https://seed.bytedance.com/en/blog/deeper-thinking-more-accurate-generation-introducing-seedream-5-0-lite). Substantive rendered body lines 11–106 of 183. Publication/update: 2026-02-13. Access: 2026-10-09.
- [Image generation API](https://docs.byteplus.com/en/docs/modelark/image-generation-api?redirect=1). Extracted Markdown lines 1–500 and 555–890; request schema, variant capability summary and output schema. Lines 501–554 older-model size examples and 891 onward layer response/stream examples not fully read. Publication/update: 2026-10-06T04:55:21Z. Access: 2026-10-09.
- [Image generation tutorial](https://docs.byteplus.com/en/docs/modelark/seedream-4-0-5-0?redirect=1). Extracted Markdown lines 1–84 of 2259, plus searched variant IDs and batch section headings. Not full SDK examples. Publication/update: 2026-10-06T04:56:15Z. Access: 2026-10-09.
- [Seedream 4.0-4.5 prompt guide](https://docs.byteplus.com/en/docs/modelark/seedream-4-0-5-0-prompt-guide?redirect=1). Extracted Markdown lines 1–125 of 209; title and actual applicability explicitly 4.0–4.5, despite URL. Publication/update: 2026-09-28T05:31:10Z. Access: 2026-10-09.

## Seedream 5.0 Pro, Dola Seedream 5.0 pro, dola-seedream-5-0-pro-260628

Surface: ByteDance product / BytePlus API

### Status
original_target_confirmed

### Prompting
Use explicit subject and change/preserve instructions; point/bbox or freeform annotations identify edit regions. Coordinate tags are in prompt text, not arbitrary API keys.

### Controls
No sequence/web-search/streaming on this API. Prompt optimization standard/fast. No native negative field verified.

### Multioutput
Single-image generation only. Separate layer_decomposition=true uses one source and returns a base plus up to 16 PNG-alpha layers, not a batch of separate scenes.

### Primary evidence
- [Introducing Seedream 5.0 Pro](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro). Substantive rendered body lines 11–148 of 216. Publication/update: 2026-07-08. Access: 2026-10-09.
- [Image generation API](https://docs.byteplus.com/en/docs/modelark/image-generation-api?redirect=1). Extracted Markdown lines 1–500 and 555–890; request schema, variant capability summary and output schema. Lines 501–554 older-model size examples and 891 onward layer response/stream examples not fully read. Publication/update: 2026-10-06T04:55:21Z. Access: 2026-10-09.
- [Seedream 5.0 pro / flash interactive editing guide](https://docs.byteplus.com/en/docs/modelark/seedream-5-0-pro-editing-guide?redirect=1). Extracted Markdown lines 1–185, coordinate clamp snippets 201–221, and 495–524. UI implementation code between 185 and 494 was searched, not executed or fully reviewed. Publication/update: 2026-10-06T04:56:00Z. Access: 2026-10-09.
- [Seedream 5.0 pro / flash tutorial](https://docs.byteplus.com/en/docs/modelark/seedream-5-0-pro?redirect=1). Extracted Markdown lines 1–66, capability/interactive/layer sections via heading search, exact model IDs. SDK examples not reviewed. Publication/update: 2026-10-06T04:56:00Z. Access: 2026-10-09.

## Seedream 5.0 Flash, Dola Seedream 5.0 flash, dola-seedream-5-0-flash-260915

Surface: BytePlus ModelArk API

### Status
new_current_discovery

### Prompting
Shares Pro interactive editing guide and coordinate semantics.

### Controls
Shares Pro 10-reference/single-output/layer modes, but prompt optimization standard only. No API search, sequence or streaming.

### Primary evidence
- [Seedream 5.0 pro / flash tutorial](https://docs.byteplus.com/en/docs/modelark/seedream-5-0-pro?redirect=1). Extracted Markdown lines 1–66, capability/interactive/layer sections via heading search, exact model IDs. SDK examples not reviewed. Publication/update: 2026-10-06T04:56:00Z. Access: 2026-10-09.
- [Seedream 5.0 pro / flash interactive editing guide](https://docs.byteplus.com/en/docs/modelark/seedream-5-0-pro-editing-guide?redirect=1). Extracted Markdown lines 1–185, coordinate clamp snippets 201–221, and 495–524. UI implementation code between 185 and 494 was searched, not executed or fully reviewed. Publication/update: 2026-10-06T04:56:00Z. Access: 2026-10-09.
- [Image generation API](https://docs.byteplus.com/en/docs/modelark/image-generation-api?redirect=1). Extracted Markdown lines 1–500 and 555–890; request schema, variant capability summary and output schema. Lines 501–554 older-model size examples and 891 onward layer response/stream examples not fully read. Publication/update: 2026-10-06T04:55:21Z. Access: 2026-10-09.


## Retained studio craft

Start with the shared prompt and tighten redundant prose when useful. Keep subject, action, layout, material, light, exact copy and the few preservation constraints that matter. This concise adaptation is a studio heuristic, not a universal word limit. Attach the actual reference and state the requested change. Preserve requested JSON if the user uses it; do not claim arbitrary JSON is a native provider schema. Verify search/edit/reference features on the chosen host.

## Interactive coordinates and differentiated examples

For Pro/Flash interactive edits, coordinates are relative to each selected image, not the browser canvas: x/y order, top-left origin, range 0–999. Normalize displayed pixel positions by width/height, multiply by 1000, round and clamp to 999 after undoing zoom/pan. Native prompt tags are `<point>x y</point>` and `<bbox>x1 y1 x2 y2</bbox>`. Keep image identity beside every tag.

Authored Pro/Flash edit: “In Image 1, replace the vase at <bbox>120 180 460 820</bbox> with the vase from Image 2. Preserve the table, lighting and camera position.” The image bindings and bounds must match real inputs; these illustrative numbers are not inferred from an unseen image. The tags are prompt text, not extra JSON request keys. Source: the interactive editing guide above; cached guide coordinate sections reviewed again on 2026-10-09.

Lite authoring example: “Create a coordinated sequence showing the same small ceramic vase at dawn, midday and dusk, fixed camera and unchanged shape; only light and background atmosphere change.” Use Lite's sequence controls only if selected and supported. Pro/Flash single-image and layer-decomposition modes cannot inherit that sequence request as a promise of separate returned scenes. Preserve the requested count as an acceptance criterion.

## Supplemental catalog discovery only

These retained names are not fully qualified native adapters. Do not inherit the newer branch's controls or silently upgrade a selected alias. Evidence observed 2026-10-09.

- `Seedream4.5`, `seedream-4-5-251128`, `Seedream4.0`, `seedream-4-0-250828`. [Catalog](https://docs.byteplus.com/en/docs/modelark/seedream-4-0-5-0?redirect=1). Shared [guide](https://docs.byteplus.com/en/docs/modelark/seedream-4-0-5-0-prompt-guide?redirect=1): qualified_shared_guide. Own shared4.0/4.5 prompting guide read; older API differences only partially surveyed. Not original mandatory targets. Status: catalog_only_not_execution_qualified.
