# Write a Midjourney edit

Build the edit around its base image, precise delta, protected anchors and integration. Preserve the selected Midjourney version and operation through prompt writing and any authorized execution.

## Inspect and choose the route

1. Inspect the latest base and each reference. Identify visible identity, geometry, text, wardrobe, composition and style that must survive. Ask for a missing critical reference before calling the prompt ready for execution.
2. Assign reference roles. Edit references carry source content, identity or composition. A Style Reference carries palette, medium, texture, light or grain. An Image Prompt influences broader content/composition/color. Personalization and Moodboards express an aesthetic. Reference order is a working convention, not an influence-weight guarantee.
3. Choose the smallest viable route. A local removal, prop/color replacement or simple retexture can use one pass. A meaningful viewpoint, garment transfer, environment change, expansion or identity-preserving style change needs stronger anchors and a useful fallback. Combined identity, major action, environment, geometry, wide expansion and strong styling usually benefit from staged passes rather than an ever-longer prompt.
4. Use Quick Edit or attached Edit references for a global semantic change or reference composition. Use the full Editor for local masks, protected regions, background isolation, canvas expansion or layer-assisted work when the actual selected tool exposes them.

## Construct the prompt

Put the direct instruction first, then the target/reference relationship, protected anchors, spatial requirements, integration, necessary style cues, relevant exclusions and supported parameters. Use frame-left/viewer-left for the image plane and the subject's own left/right for anatomy. Name visible anchors rather than “keep everything the same.”

Use the [full edit craft](../references/midjourney-edit-architect/edit-methods.md) when reference architecture, risk or editor routing needs more detail. Select the matching [complete recipe](../references/midjourney-edit-architect/edit-patterns.md):

1. Direct delta: replace the identified target while preserving its spatial role.
2. Removal/reconstruction: remove it completely and rebuild the revealed surface; do not add a replacement.
3. Character/object consistency: keep the stated identity or geometry while changing only the specified state.
4. Viewpoint: reveal new surfaces coherently without redesigning the subject.
5. Background-only replacement: protect foreground pose, crop, perspective and existing subject light.
6. Integrated relocation: retain identity while matching the new environment's light, atmosphere, reflections and contact.
7. Reference composite: transfer assigned attributes without exchanging faces, clothing or architecture between sources.
8. Retexture: translate the whole image's medium while preserving composition, silhouette, proportions and camera.
9. Aspect expansion: generate on named sides while retaining original scale and proportions; do not stretch or recenter protected content.
10. Inpainting: select one target region with enough blending context, protect unrelated areas and make one local change. Separate passes when exact object count matters.
11. Layer-assisted composite: place the object at the required scale, clean its edges, integrate it, then add a style-cohesion pass only if needed.

Background-only preservation and full relighting are different briefs. Do not combine them accidentally. Match light, scale, perspective, contact, occlusion and material response only where relevant. Drawn work needs consistent marks, line weight, fill, grain and palette rather than automatic photographic detail.

## Stage difficult changes

The identity/action/environment chain first changes pose, gaze or viewpoint, then uses the inspected selected result as the base for relocation, then adds a cohesion pass only if required. The geometry/style chain first establishes object or architectural geometry, then retextures that inspected result while preserving its silhouette and layout. Local text, edge or placement cleanup can follow either chain.

Each pass is a separate submission. State which actual selected result becomes the next base and what must be inspected before continuing. Do not describe imagined intermediate images as approved outputs.

## Compile for the actual tool

Load the selected [Midjourney profile](../../references/models/midjourney.md) for current operation controls. [Historical edit boundaries](../references/midjourney-edit-architect/current-model-boundaries.md) preserves the V8.1/V8.2 source syntax and reference distinctions, not current verification.

For web prompts, describe attachment roles and use the tool's observed attachment controls; do not add Discord edit-URL syntax. For a complete Discord edit prompt, place visual instructions before trailing parameters and the required `--edit` URLs. If no tool is named, an attachment-based web prompt is a useful prompt-only form; identify it rather than claiming an executable Discord command. Never treat `--iw` as edit strength or `--sw` as identity/preservation strength. Do not invent edit-weight controls.

## Diagnose and repair

When an output is supplied, identify the dominant visible failure, likely competing control or missing anchor, smallest change and revised prompt. The [full recovery library](../references/midjourney-edit-architect/failure-recovery.md) preserves thirteen repairs: identity; style/texture; floating contact; count/placement; reference leakage; ignored change; collateral edits; ratio deformation; anatomy; environment integration; mutated text; product/logo geometry; architecture. Do not run unchanged retries to avoid diagnosis.

Precision-delta, anchor-rich, cohesion-controlled and production-fallback variants are available when alternatives help. Four alternatives are optional. Keep every route aimed at the same requested outcome. The [MIT notice](../LICENSE-MIDJOURNEY-EDIT) covers the retained edit library.
