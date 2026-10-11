# Amazon Nova Canvas

Evidence checked 9 October 2026. Guide-backed generation and mask editing. Canvas is separate from Titan and Nova 2 Omni; exact API model ID and account availability must still be resolved.

## Generation
Use a caption-like description of the image. Describe visible objects, arrangement, light and material. Put unwanted objects in the dedicated negativeText field when the selected Canvas API supports it; do not turn the positive prompt into a list of “no” commands. A fixed seed can support controlled comparisons, not a universal determinism guarantee.

Authored generation prompt: “A matte ivory desk lamp on a walnut table beside a closed sage-green notebook, eye-level product photograph, soft light from the left, beige wall.” If explicitly required, negativeText may list “letters, logos”; these exclusions are a separate control, not an automatically added stylistic preference.

## Mask semantics change by operation
- Inpainting: maskPrompt identifies the area to change. Removal omits the positive text. For addition/replacement, describe the whole desired image; mask geometry affects the replacement silhouette.
- Outpainting: maskPrompt identifies the object/area to preserve. Describe the whole desired extended scene, including that unchanged object. Never invert the mask based on habits from another provider.

Authored outpainting intent: extend the selected lamp photograph into a wide composition, retaining the lamp and table while revealing more beige wall to the right. The preservation mask and output canvas are separate inputs; prose alone does not establish a native boundary.

## Sources
[Generation](https://docs.aws.amazon.com/nova/latest/userguide/prompting-image-generation.html), [masks](https://docs.aws.amazon.com/nova/latest/userguide/prompting-image-masks.html), [inpainting](https://docs.aws.amazon.com/nova/latest/userguide/prompting-image-inpainting.html), [outpainting](https://docs.aws.amazon.com/nova/latest/userguide/prompting-image-outpainting.html): substantive guides reviewed in full on 2026-10-09; publication dates not exposed. No generation test.
