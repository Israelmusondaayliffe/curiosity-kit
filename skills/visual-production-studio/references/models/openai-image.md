# OpenAI — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## ChatGPT Images 2.5

Surface: ChatGPT / Work / Codex product

### Status
original_target_confirmed

### Prompting
References, sketch input and focused image comments are product controls. Preserve source NL, JSON and system-style recipes as authoring formats.

### Controls
Do not translate API edition names or API parameter availability into the product UI. Inspect selected product controls.

### Identity
Vendor claims improved precision and iterative consistency; no exact preservation guarantee tested.

### Multioutput
The source eight-image recipe remains a recipe, not delivery-count evidence.

### Primary evidence
- [Introducing ChatGPT Images 2.5](https://openai.com/index/introducing-chatgpt-images-2-5/). The 2026-10-09 source audit reviewed the complete product body, lines 13–130; this profile reuses that evidence. Publication/update: 2026-09-08. Access: 2026-10-09.
- [ChatGPT image generation product guide](https://learn.chatgpt.com/docs/image-generation). Rendered lines 923–948 of 1027; Focused/Canvas views, references and image comments. Publication/update: not established. Access: 2026-10-09.

## gpt-image-2.5-flare, gpt-image-2.5-flare-2026-09-08, gpt-image-2.5-sunburst, gpt-image-2.5-sunburst-2026-09-08

Surface: OpenAI Images API

### Status
original_editions_confirmed

### Prompting
Natural language, labeled sections and JSON-like prose are supported ways to express intent. State composition, exact quoted copy, visible materials/light, and change-versus-preserve priorities. Iterate one variable; inspect drift.

### Controls
Quality auto/low/medium/high/xhigh/max. Custom WIDTHxHEIGHT: each edge ≤3840, multiples of 16, ratio ≤3:1, 655360–8294400 pixels; above 3686400 pixels experimental.

### Multioutput
Images API n=1–10; distinguish a batch parameter from collage/panel instructions and actual delivered files.

### Primary evidence
- [Image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting). Rendered lines 927–982, 1214–1410, 1737–1783 of ~1801; model selection, prompting/editing, supported sizes, GPT Image 2 migration; examples outside these ranges not fully read. Publication/update: not established. Access: 2026-10-09.
- [Images generate API](https://developers.openai.com/api/reference/resources/images/methods/generate). Rendered request body approximately lines 522–700 of 924; model aliases and parameter schema. Publication/update: not established. Access: 2026-10-09.
- [Images edit API](https://developers.openai.com/api/reference/resources/images/methods/edit). Rendered request body from line 529; images, prompt, mask, fidelity and output fields; not every SDK example. Publication/update: not established. Access: 2026-10-09.

## GPT Image 2, gpt-image-2, gpt-image-2-2026-04-21

Surface: OpenAI Images API / retained recipe target

### Status
original_historical_target_still_documented

### Prompting
Keep GPT Image 2 recipes intact. Current migration guidance asks for baseline comparisons rather than automatic upgrades.

### Controls
Omit input_fidelity for GPT Image 2, which always uses high fidelity. Transparency is listed as preview for this version. Do not apply all 2.5 quality/size settings without exact-version schema validation.

### Guide gap
Current shared prompting guide retains a GPT Image 2 section, but no separate full-version guide was needed or assumed.

### Primary evidence
- [Image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting). Rendered lines 927–982, 1214–1410, 1737–1783 of ~1801; model selection, prompting/editing, supported sizes, GPT Image 2 migration; examples outside these ranges not fully read. Publication/update: not established. Access: 2026-10-09.
- [Images generate API](https://developers.openai.com/api/reference/resources/images/methods/generate). Rendered request body approximately lines 522–700 of 924; model aliases and parameter schema. Publication/update: not established. Access: 2026-10-09.
- [Images edit API](https://developers.openai.com/api/reference/resources/images/methods/edit). Rendered request body from line 529; images, prompt, mask, fidelity and output fields; not every SDK example. Publication/update: not established. Access: 2026-10-09.


## Retained studio craft

Keep the user's detailed NL, JSON envelope and system-style prompt recipes. Clearly separate what changes from preserved identity/composition. For iterative editing, ground each new instruction in the actual latest image. One prompt requesting eight separate images is a supported studio recipe to test on the selected surface; do not infer actual delivery count from the prose. No forced Thinking label, fixed seven-prompt quota, invented latency guarantee or claim that only OpenAI can research.

## Apply the selected version: creation, edit and layout

Authored GPT Image 2 example: “Create an editorial still life of a green pear on a white plate, top-down view, the plate in the lower-left quadrant, warm grey tabletop, soft window shadow toward the right. Leave the upper half clear for the exact heading ‘A QUIET MORNING’ in small black serif lettering.” Retain the GPT Image 2 target and exact text; the current 2.5 API settings above do not belong in this older model's prompt.

For selected ChatGPT Images 2.5, a focused follow-up can be: “Change only the plate to cobalt blue. Keep the pear, heading, object positions and light direction.” Bind the actual latest image and any focused image comment. For an API Flare/Sunburst edit, convey the same delta through that edition's supported image/edit inputs, not a claim that product comment controls exist in the API.

A user-requested JSON envelope can group scene, typography and preservation priorities as prompt content. It does not create new request fields. Search-grounded content remains a research-plus-authoring workflow using actual sources, not proof that every Images endpoint browses. For one-submission eight-image recipes, preserve the requested count and inspect returned files; a collage and eight separate files are different outcomes.
