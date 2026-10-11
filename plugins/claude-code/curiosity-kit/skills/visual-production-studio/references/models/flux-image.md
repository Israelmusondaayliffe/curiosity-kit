# FLUX — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## FLUX 3 Image, flux-3-image

Surface: BFL API / Playground

### Status
new_current_discovery

### Prompting
Text brief or edit instruction; assign reference roles by position. Optional caption with <id> mentions plus JSON box rows appended inside prompt, not separate box API field.

### Controls
15 fixed ratios orauto; resolution 768sq/1k/1.5k/2k/4k; version currentlylatest only. No n/seed/output_format established in schema.

### Primary evidence
- [FLUX 3 Image overview](https://docs.bfl.ai/flux_3/flux3_image_overview). Full substantive body lines 82–199 of 224. Publication/update: not established. Access: 2026-10-09.
- [FLUX 3 technical prompting](https://docs.bfl.ai/guides/prompting_unified_technical). Full substantive body lines 21–135 of 156. Publication/update: not established. Access: 2026-10-09.
- [FLUX 3 multi-reference prompting](https://docs.bfl.ai/guides/prompting_editing_multi_reference). Full substantive body lines 21–204 of 226. Publication/update: not established. Access: 2026-10-09.
- [FLUX 3 bounding boxes](https://docs.bfl.ai/flux_3/flux3_image_bounding_boxes). Rendered lines 96–372 of 415, layout/edit rows, coordinate order, anchoring and limitations; code read as examples only. Publication/update: not established. Access: 2026-10-09.
- [FLUX 3 Image API](https://docs.bfl.ai/api-reference/utility/generate-an-image-with-flux-3). Request/response body lines 417–580 of 601; selected examples/navigation 29–148. Publication/update: not established. Access: 2026-10-09.

## FLUX.2 max, flux-2-max, FLUX.2 pro, flux-2-pro, flux-2-pro-preview, FLUX.2 flex, flux-2-flex, FLUX.2 dev

Surface: BFL API, Playground and owner open weights differ

### Status
new_current_discovery

### Prompting
Narrative subject/action/style/context; salient constraints early, quoted text, hex codes attached to objects. JSON structure is prompt content, not native top-level schema.

### Controls
Up to 4 MP; multiples of 16; minimum 64². Max has grounding; flex steps/guidance; pro-preview mutable versus fixed pro. Prompt upsampling support differs by variant.

### Guide gap
Shared guide qualified; every variant-specific API output field was not exhaustively reviewed. Do not import FLUX 3 box schema.

### Primary evidence
- [FLUX.2 prompting guide](https://docs.bfl.ai/guides/prompting_guide_flux2). Substantive guide lines 43–603 of 670; prose, color, structured prompting and references. Publication/update: not established. Access: 2026-10-09.
- [BFL available models catalog](https://help.bfl.ai/articles/7655484417-what-flux-models-are-available). Full substantive body lines 8–101 of 118. Publication/update: relative: 1 month ago. Access: 2026-10-09.
- [FLUX.2 overview](https://docs.bfl.ai/flux_2/flux2_overview). Full substantive body lines 21–265 of 290. Publication/update: not established. Access: 2026-10-09.

## FLUX.2 klein4B, flux-2-klein-4b, FLUX.2 klein9B, flux-2-klein-9b, flux-2-klein-9b-preview, FLUX.2 klein Base4B, FLUX.2 klein Base9B

Surface: API versus open-weight base variants

### Status
new_current_discovery

### Prompting
Detailed narrative prompts; no automatic prompt upsampling. Include scene/light/context explicitly.

### Controls
64²–4 MP; multiples of 16. Preview 9B may change; non-preview snapshot fixed. Base variants are undistilled/open-weight-only, not public API. Licensing differs between 4B/9B; no deployment authorized.

### Guide gap
Official usage guide exists for klein; base-specific craft differences beyond detailed narrative not established.

### Primary evidence
- [FLUX.2 klein guide](https://help.bfl.ai/articles/7592221790-how-do-i-generate-quickly-with-flux-2-klein). Full substantive body lines 7–135 of 152. Publication/update: relative: 3 months ago. Access: 2026-10-09.
- [FLUX.2 overview](https://docs.bfl.ai/flux_2/flux2_overview). Full substantive body lines 21–265 of 290. Publication/update: not established. Access: 2026-10-09.

## FLUX.1 Kontext pro, FLUX.1 Kontext max, FLUX.1 Kontext dev

Surface: BFL legacy API / owner open weights

### Status
current_catalog_legacy

### Prompting
Simple precise edit instructions; quoted old/new text for replacement; bright annotation boxes can locate edits. Explicitly preserve identity through sequential changes.

### Guide gap
Pro editing guide read; max/dev-specific full parameter guides not independently read. Catalog identifies dev as editing-only.

### Primary evidence
- [BFL available models catalog](https://help.bfl.ai/articles/7655484417-what-flux-models-are-available). Full substantive body lines 8–101 of 118. Publication/update: relative: 1 month ago. Access: 2026-10-09.
- [FLUX.1 Kontext editing](https://docs.bfl.ai/kontext/kontext_image_editing). Rendered lines 81–178 and 291–293 of 335; editing guidance, text replacement, annotations and single-source endpoint. SDK examples not executed. Publication/update: not established. Access: 2026-10-09.


## Native FLUX 3 boxes versus FLUX.2 prose

Authored FLUX 3 layout prompt: `A yellow mug <mug_1> on a navy background <background_1>. [{"id":"background_1","bbox":[0,0,1000,1000],"desc":"Flat navy backdrop"},{"id":"mug_1","bbox":[300,200,800,700],"desc":"A yellow ceramic mug"}]`

The caption plus array is one prompt string. Boxes use top/left/bottom/right, 0–1000. Editing rows instead use id/from/src_bbox/tgt_bbox/desc: matching source/target boxes anchor; a changed target moves; null source creates; null target removes. `ref_image_0` binds the first actual image. Boxes guide placement, not clipping masks or guaranteed unchanged pixels. [Official box guide](https://docs.bfl.ai/flux_3/flux3_image_bounding_boxes), sections 96–139, 196–323 and 340–372 checked directly again 2026-10-09.

For FLUX.2 max/pro/flex/dev/klein, use narrative or descriptive structured prose without importing FLUX 3 rows: “A yellow ceramic mug occupies the lower-left half of a navy tabletop; high side light reveals its glaze.” Klein needs explicit scene/light/context because it lacks automatic upsampling. Kontext editing instead favors a focused delta such as “Replace ‘COFFEE’ with ‘TEA’; retain the lettering style and cup.” The actual selected variant controls remain separate.

## Supplemental catalog discovery only

These retained names are not fully qualified native adapters. Do not inherit the newer branch's controls or silently upgrade a selected alias. Evidence observed 2026-10-09.

- `FLUX1.1 pro`, `FLUX1.1 pro Ultra`, `FLUX.1 Fill pro`. [Catalog](https://help.bfl.ai/articles/7655484417-what-flux-models-are-available). Dedicated guide missing or not read. Official catalog/index names retained; dedicated generation/fill/expand guide not read, so no inherited FLUX3 or FLUX2 controls. Status: catalog_only_not_execution_qualified.
- `FLUX.1 dev`, `FLUX.1 Expand pro`. [Catalog](https://docs.bfl.ai/api-reference/utility/generate-an-image-with-flux-3). Dedicated guide missing or not read. Official catalog/index names retained; dedicated generation/fill/expand guide not read, so no inherited FLUX3 or FLUX2 controls. Status: catalog_only_not_execution_qualified.
- `FLUX Outpainting`, `FLUX Erase`, `FLUX Deblur`, `FLUX Virtual Try-On`, `FLUX Virtual Try-On v2`. [Catalog](https://docs.bfl.ai/llms.txt). Dedicated guide missing or not read. Official index discovery only; tool-specific API/guide body not read. Status: catalog_only_not_execution_qualified.

FLUX 3 prompting guidance uses positive descriptions and does not provide a generic negative-prompt convention. Do not append another family's negative_prompt field. Exclude an unwanted visual element through a precise desired-state edit when appropriate, while preserving the user's actual intent.
