# Write a focused image edit

Inspect the current base image before describing a change. Start from the latest accepted or supplied image, not an earlier version remembered from the conversation.

## Build the edit

1. Identify the target by visible content and location. Separate the requested change from protected identity, object geometry, copy, surroundings and framing. “Make the mug blue” should not redesign the room.
2. Write the delta first. Follow with the few protected features most likely to drift. For a removal, let removal override preservation of that target and describe the surface or background revealed behind it.
3. Integrate what changes. Match perspective, scale, occlusion, contact shadows, reflections, light direction and material response. A replacement occupies the original object's spatial role. Decide whether a background-only swap must hold foreground pixels or whether a relocation should change reflected light on the subject.
4. Preserve the frame and ratio unless expansion or reframing is part of the request. New camera, pose, expression and cinematic treatment are optional changes, never automatic improvements.
5. Use one clear natural-language instruction for a small edit. Separate changes, preservation and reference roles in JSON only if that makes a complex edit easier to use. Return a complete prompt with its needed attachment descriptions.

For an upload without editing direction, first use the surrounding request. If it only asks what the picture shows, identify it. If it asks for exploration, offer a small set of complete directions grounded in the actual image, such as a lighting change, material change, setting, narrative context or design application. Do not replace its person or world in every option.

## Check the result at the right level

Before delivery, look for conflicting change/keep clauses and missing integration cues. If a rendered edit is supplied, compare the exact target and protected areas. Repair the dominant visible error with a smaller delta or a staged edit; do not certify preservation from prompt wording.

[Targeted edit recipes](../references/image-prompt-edit/gpt-edit.md), [upload exploration](../references/image-prompt-edit/nano-edit.md), [Uni modification](../references/image-prompt-edit/uni-modify.md) and [texture vocabulary](../references/shared/patterns/texture-library.md) cover optional branches. For descriptive architect edits, use the [nested skeleton](../references/shared/architect-prompt-skeleton.json) and [JSON envelope](../references/shared/json-envelope-template.md).. Midjourney-specific editing uses [its edit method](midjourney-edit-architect.md).
