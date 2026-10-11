# Recraft — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## Recraft V4, recraftv4, recraftv4_vector, recraftv4_pro, recraftv4_pro_vector

Surface: Recraft Studio vs API

### Status
original_target_confirmed

### Prompting
Global scene to local details; concrete geometry, contours, line weight, fills, palette and typography hierarchy for vectors. Short exploration and detailed control are both valid.

### Controls
Explicit V4 model required because API default is V4.1. Prompt ≤10000 chars; n 1–6; random_seed, colors/background. Unsupported negative_prompt/curated style/text_layout controls must not be inherited from V3.

### Primary evidence
- [Prompting with Recraft V4](https://www.recraft.ai/docs/prompt-engineering-guide/prompting-with-recraft-v4). Rendered lines 19–213 of 445; scene structure, concrete visual description, vector and typography guidance; later examples not fully read. Publication/update: not established. Access: 2026-10-09.
- [Recraft API styles](https://www.recraft.ai/docs/api-reference/styles). Rendered lines 19–69 of 131; model/style compatibility and reference limits. Publication/update: not established. Access: 2026-10-09.
- [Recraft V4 API](https://www.recraft.ai/docs/api-reference/models/recraft-v4). Full substantive model/parameter body of 282 rendered lines. Publication/update: not established. Access: 2026-10-09.
- [Recraft API appendix](https://www.recraft.ai/docs/api-reference/appendix). Full substantive limits body of 133 rendered lines. Publication/update: not established. Access: 2026-10-09.

## Recraft V4.1, recraftv4_1, recraftv4_1_vector, recraftv4_1_pro, recraftv4_1_pro_vector, recraftv4_1_utility, recraftv4_1_utility_vector, recraftv4_1_utility_pro, recraftv4_1_utility_pro_vector

Surface: Recraft Studio vs API

### Status
original_target_confirmed

### Prompting
Use the owner V4-family prompting guide; no independently different V4.1 syntax claimed.

### Controls
API default V4.1; generation prompt ≤10000 chars, n 1–6, random_seed, supported ratios/sizes, palette controls. Negative_prompt, curated style, text_layout, artistic_level and no_text unsupported.

### Guide gap
Shared V4-family guide; no separate V4.1-specific craft grammar verified.

### Primary evidence
- [Recraft V4.1 catalog](https://www.recraft.ai/docs/recraft-models/recraft-v4-1). Substantive page body, 173 rendered lines. Publication/update: 2026-05-14. Access: 2026-10-09.
- [Prompting with Recraft V4](https://www.recraft.ai/docs/prompt-engineering-guide/prompting-with-recraft-v4). Rendered lines 19–213 of 445; scene structure, concrete visual description, vector and typography guidance; later examples not fully read. Publication/update: not established. Access: 2026-10-09.
- [Recraft API styles](https://www.recraft.ai/docs/api-reference/styles). Rendered lines 19–69 of 131; model/style compatibility and reference limits. Publication/update: not established. Access: 2026-10-09.
- [Recraft V4.1 API](https://www.recraft.ai/docs/api-reference/models/recraft-v4-1). Full substantive model/parameter body of 300 rendered lines. Publication/update: not established. Access: 2026-10-09.
- [Recraft API appendix](https://www.recraft.ai/docs/api-reference/appendix). Full substantive limits body of 133 rendered lines. Publication/update: not established. Access: 2026-10-09.

## Recraft V4.1 Flash, recraftv4_1_flash, recraftv4_1_flash_raster

Surface: Recraft API

### Status
new_current_discovery

### Prompting
Natural-language text-to-image; no dedicated Flash-only craft guide beyond model examples.

### Controls
Prompt ≤10000 chars; n 1–6; random_seed; colors/background; response URL/base64/multipart. No image-to-image, styles, negative_prompt, text_layout, vector or Pro variant.

### Guide gap
Dedicated model/API usage page exists; no standalone prompting guide found.

### Primary evidence
- [Recraft V4.1 Flash API](https://www.recraft.ai/docs/api-reference/models/recraft-v4-1-flash). Rendered lines 19–47 and 173–236 of 315; identity, output, request parameters and unsupported operations. Publication/update: 2026-09 (release month only). Access: 2026-10-09.


## Retained studio craft

Do not carry forward the obsolete claim that styles are limited to V3. For supplied styles and controls, check current owner support. [V4.1](https://www.recraft.ai/docs/recraft-models/recraft-v4-1), [V4 prompting](https://www.recraft.ai/docs/prompt-engineering-guide/prompting-with-recraft-v4), [Styles](https://www.recraft.ai/docs/api-reference/styles).

## Raster versus actual vector delivery

Authored V4 vector brief: “A simple side-view bicycle icon. Two equal circular wheels, thin uniform dark-green strokes, a triangular frame, flat cream background, no shading. Keep the handlebar and saddle silhouettes readable at small size.” Select an actual V4 vector variant; writing “vector” alone does not prove SVG or editable paths. Inspect the returned file and stroke geometry.

For V4.1 raster, a brief can instead specify paper texture, painted shading or photographic material. Custom style/reference workflows stay available where current V4/V4.1 support them; Flash cannot replace that workflow because it lacks style, I2I and vector routes. Keep explicit selected version, style source and output type together.

When typography matters, specify literal copy, hierarchy and placement, then inspect lettering and actual file format. Do not add obsolete V3 negative_prompt or text_layout fields to make the request appear more precise.
