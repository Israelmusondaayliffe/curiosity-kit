# Qwen Image — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## qwen-image-3.0-pro, qwen-image-3.0, qwen-image-2.1-pro, qwen-image-2.1-turbo

Surface: Alibaba Model Studio hosted API

### Status
new_current_discovery

### Prompting
Natural-language generation/edit instructions; number images by array order and state contribution/preservation. OpenAI-compatible wrapper uses vendor extensions and is not OpenAI Images behavior.

### Controls
n = 1–6; PNG output; pixel area 512²–2048²; ratio 1:8–8:1. negative_prompt only on 3.0; 2.1 unsupported. prompt_extend defaults true; direct/agent rewriting distinction, agent T2I only.

### Guide gap
Current API and editing guide qualified; no separate exhaustive 3.0 creative grammar located.

### Primary evidence
- [Qwen unified generation/editing API](https://www.alibabacloud.com/help/en/model-studio/qwen-image-generation-and-editing-api-reference). Body lines 13–359 of 892; model IDs, limits, DashScope/OpenAI-compatible fields and extensions. Publication/update: 2026-10-09. Access: 2026-10-09.
- [Qwen image edit guide](https://www.alibabacloud.com/help/en/model-studio/qwen-image-edit-guide). Body 258–354 of 412; input role/order, edit examples and controls; code example sections inspected, not executed. Publication/update: 2026-09-28. Access: 2026-10-09.
- [Alibaba image catalog](https://www.alibabacloud.com/help/en/model-studio/image-model). Full substantive catalog body lines 14–95 of 98. Publication/update: 2026-09-28. Access: 2026-10-09.

## Qwen/Qwen-Image-2.1, Qwen/Qwen-Image-2.1-PE-T2I, Qwen/Qwen-Image-2.1-PE-I2I

Surface: Official open-weight model card and distinct enhancer models

### Status
new_current_discovery

### Prompting
2.1 unified T2I/edit card; supports instruction editing and reference fusion. Prompt enhancer is a separate component; its rewritten_prompt/wh_ratio output is not generator request schema.

### Controls
Examples use PNG; no universal local output count/reference-fidelity guarantee inferred. Card license is Qwen Research License, not automatically Apache.

### Guide gap
PE-T2I partial instructions read. PE-I2I existence discovered but exact instructions not qualified; no shared T2I grammar imposed on I2I.

### Primary evidence
- [Qwen Image 2.1 owner model card](https://huggingface.co/Qwen/Qwen-Image-2.1). Substantive model and usage sections lines 100–209 of 264. Publication/update: not established. Access: 2026-10-09.
- [Qwen Image 2.1 prompt enhancer instructions](https://huggingface.co/Qwen/Qwen-Image-2.1-PE-T2I/blob/main/system_prompt.txt). Rendered lines 94–173 of 287; separate enhancer instructions, not image-generator API schema. Publication/update: not established. Access: 2026-10-09.


## Ordered references and rewrite awareness

Authored hosted edit: “In Image 1, replace only the bag with the bag from Image 2. Preserve Image 1's person, pose, setting and light. Copy the bag's shape, fastening and blue fabric from Image 2.” Number by actual array order; a role description cannot fix swapped uploads.

With exact copy, preserve the user's wording and record whether prompt_extend or agent rewriting is enabled. Qwen 3.0's negative field does not exist for 2.1; avoid defaulting a common wrapper to the wrong version's controls. For the owner open-weight route, prompt enhancers are separate models. PE-I2I was only discovered, so do not impose PE-T2I's schema or rewrite policy on editing.

## Supplemental catalog discovery only

These retained names are not fully qualified native adapters. Do not inherit the newer branch's controls or silently upgrade a selected alias. Evidence observed 2026-10-09.

- `qwen-image-2.0-pro`, `qwen-image-2.0-pro-2026-06-22`, `qwen-image-2.0-pro-2026-04-22`, `qwen-image-2.0-pro-2026-03-03`, `qwen-image-2.0`, `qwen-image-2.0-2026-03-03`, `qwen-image-max`, `qwen-image-max-2025-12-30`, `qwen-image-plus`, `qwen-image-plus-2026-01-09`, `qwen-image`, `qwen-image-edit-max`, `qwen-image-edit-max-2026-01-16`, `qwen-image-edit-plus`, `qwen-image-edit-plus-2025-12-15`, `qwen-image-edit-plus-2025-10-30`, `qwen-image-edit`. [Catalog](https://www.alibabacloud.com/help/en/model-studio/image-model). Shared [guide](https://www.alibabacloud.com/help/en/model-studio/qwen-image-edit-guide): qualified_shared_guide. Shared older/current edit guide contains some model-specific fields; exact snapshot-level full guides not read. Do not upgrade alias silently. Status: catalog_only_not_execution_qualified.
