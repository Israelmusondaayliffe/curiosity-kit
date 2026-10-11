# Final Checklist

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

Before output, confirm each item:

- A single Prompt has exactly one primary task: generation, editing, or extension. An explicit hybrid task has been split into two sequential Prompts, each with exactly one primary task.
- The subjects, counts, identities, scene, prop ownership, spatial relationships, and story outcome have not changed.
- Every required character, prop, and scene in the story contract is covered. Two named characters have not been merged, and inferences from assets have not been written as facts about identity, age, relationships, or plot.
- Every asset actually used has one unique and explicit role.
- Asset references already present in the user's original Prompt remain exactly unchanged. None have been deleted, renumbered, translated, or converted into reference-free generation because the assets were not attached or could not be accessed; no asset reference absent from the user's input has been invented.
- When assets are missing, corrupted, or inaccessible, the Agent has not claimed to have reviewed them and has not added appearance, voice, action, or scene details that could be confirmed only by reviewing those assets.
- Irrelevant assets have not been forced into the output. When the complete asset inventory is available, every actually available asset that was not assigned a role is listed individually under `【Unused Assets】`.
- Inaccessible assets have not been treated as understood.
- Different characters, products, and props are mapped individually, not replaced by a range statement.
- A single-character design image has not been used to define two on-screen characters. When multiple individual or group candidates exist, they have first been assigned as one image per person and one image per group.
- Each stage of a long video has only one primary state change and a clear ending state.
- Event time ranges explicitly requested by the user have not been removed without authorization. When only an external target duration exists, the existing events have been redistributed using stages without numeric timestamps, and the parameter has not been written back as new time ranges.
- An editing task includes a sole master, edit scope, target count, content to preserve, and timeline inheritance. Audio editing also specifies the audio to change, audio to preserve, lip-sync timing, and all visuals.
- The current task's automatically locked aspect-ratio and duration rules have been followed. When a conflict exists, only one parameter note is output outside the Prompt.
- The extension direction and boundary-frame role are correct, and the original video is not rewritten at the same time. The boundary visuals, audio state, movement trend, and continuing subjects are all covered.
- The first frame, last frame, and other reference images are defined individually without overwriting one another's roles. A fixed frame uses the standalone exact role statement `Use @ImageN as the first frame.` or `Use @ImageN as the last frame.` and does not weaken it to a composition reference. The aspect ratios of the first and last frames have been checked or handled under the inaccessible-media boundary.
- Multiple keyframes define key states image by image and in order, without promising frame-by-frame replication or a static hold.
- A storyboard grid specifies the reading order, each panel's shot role, and any sketch, annotation, or placeholder content not to adopt.
- A blockout has been identified as coarse or fine, with subject mapping, inherited information, and excluded content specified accordingly.
- Abstract emotion and cinematography terms have observable results when control is needed.
- At every speaking stage, the speaker, speaking state, dialogue, audio role, language, and on-screen or off-screen position match the input. Speech has not been changed to silence, and Mandarin, a dialect, or a regional accent has not been added without instruction.
- Shot numbers, asset reference numbers, chapter numbers, and step numbers remain identifiers; they have not been misinterpreted as camera angles or other cinematography parameters.
- The Prompt contains no output parameters, internal analysis, evaluation metadata, keys, Endpoints, or reasons for modifications.
- Exactly one `Please note that this is not video editing.` is included only when the compatibility gate is triggered for reference-based generation. It is not added automatically for actual video editing, video extension, first-frame generation, first-and-last-frame generation, or ordinary generation without a specification conflict.
- When reference-video specifications cannot be accessed, the compatibility decision follows the explicit aspect-ratio or duration intent in the original Prompt. Existing video references remain intact, and the Agent does not claim to have read or checked the reference-video specifications.
- No negative constraint unrelated to the user's request has been added automatically.
- All placeholders have been replaced. By default, the output contains one complete Prompt body only, without Markdown headings, code fences, or surrounding explanations.
