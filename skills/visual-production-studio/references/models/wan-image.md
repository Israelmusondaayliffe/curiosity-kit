# Wan Image — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## wan2.7-image-pro, wan2.7-image

Surface: Alibaba Model Studio image API, separate from Wan video

### Status
new_current_discovery

### Prompting
Scene content/style/light/composition; image roles use array numbering. Precise edits use native bbox_list, absolute pixel[x1,y1,x2,y2],maximum 2 boxes/image; not Seedream or FLUX coordinates.

### Multioutput
Standard up to 4; enable_sequential true permits n 1–12 ceiling, actual count ≤n; thinking/color palette unavailable in sequence mode.

### Guide gap
Official T2I/edit usage guides qualified; standalone linked prompt guide not opened. Current 2.7-specific exceptions override older-model generic controls.

### Primary evidence
- [Alibaba image catalog](https://www.alibabacloud.com/help/en/model-studio/image-model). Full substantive catalog body lines 14–95 of 98. Publication/update: 2026-09-28. Access: 2026-10-09.
- [Wan image editing guide](https://www.alibabacloud.com/help/en/model-studio/wan-image-edit). Introduction 14–28; input/specification/prompting/edit controls 1532–1673 of 1866. Publication/update: 2026-09-28. Access: 2026-10-09.
- [Alibaba text-to-image guide](https://www.alibabacloud.com/help/en/model-studio/text-to-image). Introduction 13–21 and key controls 563–640 of 719. Publication/update: 2026-09-28. Access: 2026-10-09.


## Precise region binding

For Wan 2.7 precise editing, bbox_list belongs to the native request and uses absolute pixel [x1,y1,x2,y2], at most two boxes per image. Record source image width/height and image identity before translating any normalized annotation. Never paste Seedream tags or FLUX 3 row arrays into this field.

Authored edit intent: “Replace the selected vase in Image 1 with a small cobalt bowl; retain the table, wall, camera and lighting.” On an illustrative 1200×800 input, pixel box [240,160,720,640] describes a particular region; it is not an automatically detected vase. Keep the actual native container/schema verified separately. Sequence mode and ordinary multi-output generation have different count behavior and incompatible thinking/palette controls.

## Supplemental catalog discovery only

These retained names are not fully qualified native adapters. Do not inherit the newer branch's controls or silently upgrade a selected alias. Evidence observed 2026-10-09.

- `wan2.6-t2i`, `wan2.6-image`, `wan2.5-t2i-preview`, `wan2.5-i2i-preview`, `wan2.2-t2i-plus`, `wan2.2-t2i-flash`, `wan2.1-t2i-plus`, `wan2.1-t2i-turbo`, `wanx2.1-imageedit`. [Catalog](https://www.alibabacloud.com/help/en/model-studio/image-model). Shared [guide](https://www.alibabacloud.com/help/en/model-studio/text-to-image): qualified_shared_guide. Shared generation guide covers older versions partially;2.5/2.6 editing rows read inW1. Full variant API schemas not qualified;legacywanxBeijing-only percatalog. Status: catalog_only_not_execution_qualified.
