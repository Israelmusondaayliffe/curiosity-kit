# Output Contract

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

Match the user's output language. Retain the user's existing asset-reference syntax, such as `@Image1`, `@Image 1`, or an equivalent label in the runtime environment. Do not translate or renumber any reference the user has explicitly established.

### Default Delivery

By default, output only the optimized Prompt body. Do not add Markdown headings, code fences, prefaces, or closing explanations, and do not add outer wrappers such as "Optimized Prompt," "Asset Understanding," or "Optimization Notes." Do not instruct the model to wrap the final result in a code fence.

When the Prompt itself needs structure, it may retain task-internal labels such as `【Generation Goal】`, `【Reference Asset Roles】`, `【Event Script】`, and `【Maintain Consistency】`. These labels are part of the directly submittable Prompt body, not response wrappers.

When the Agent infers asset mappings automatically, do not output a separate reasoning table. Write the final mappings directly into the Prompt's reference-asset-roles section, specifying the adopted scope of every asset actually used. When the Agent can access the complete asset inventory, it must append `【Unused Assets】` inside the Prompt and individually list the reference number of every actually available asset that was not assigned a role; do not describe them only outside the Prompt. When the complete asset inventory is unavailable in the current environment, do not fabricate unused reference numbers.

### Asset Reference Fidelity

When the user's original Prompt already contains explicit asset references, retain the same reference syntax and numbers in the final Prompt, regardless of whether the current Agent can access the corresponding assets. Do not delete or renumber a reference, translate its label, or convert the task into reference-free generation merely because the asset is not attached to the current message, is corrupted, or cannot be accessed.

Inaccessible assets limit only the facts the Agent can confirm and add. They do not alter the asset roles or reference relationships the user has already established, and they do not trigger any missing-asset explanation or supplementary advice outside the Prompt.

### Input and Parameter Notices

When the input assets exceed a hard limit, first output a complete Prompt based on the selected assets, then append one `Asset Note:` listing the asset types or reference numbers that must be reduced before submission. Recommended ranges are not hard limits and do not trigger an asset note.

When the user requests parameters that are automatically locked by video editing, first-frame generation, first-and-last-frame generation, or video extension, or when the first and last frames have mismatched aspect ratios, first output the complete Prompt, then append one `Parameter Note:`. The parameter note states only the conflicting rule and the action required before submission. It does not repeat the Prompt, expand into API documentation, or write the parameters back into the Prompt.

Example: `Parameter Note: Video editing automatically preserves the input video's aspect ratio and basic duration, so these cannot be set separately to 16:9 and 20 seconds. The Prompt above has been written to follow the original video's timeline.`

### Required Capability Boundaries

Exact subtitles, formulas, signs, product parameters, or frame-level timestamps cannot be fully guaranteed by the Prompt alone. Still output the best possible Prompt first. When genuinely necessary, append at most one line beginning with `Additional Note:` after the Prompt, stating that prepared assets or post-production are required. When unnecessary, output no note.

For a hybrid task containing two sequential operations, output separate, submittable Prompts labeled `Step 1:` and `Step 2:`, and state that Step 2 uses the output from Step 1 as its new master. Otherwise, output only one Prompt by default.

In an ordinary generation task, a user-provided duration, aspect ratio, or other generation parameter may guide event density and composition, but must not be written into the Prompt. For video editing, first-frame generation, first-and-last-frame generation, or video extension, apply the task's automatically locked rules first and do not use conflicting parameters to plan the Prompt. List configurable parameters outside the Prompt only when the user asks for an invocation example.

### Complete Input-to-Output Example

User input: `Have the barista from the reference image perform a pour-over in the reference cafe, following the actions in the uploaded video, and finally hand the coffee to the customer.`

After reviewing the three assets, the Agent directly outputs the following Prompt body:

【Generation Goal】
Generate a continuous video of the barista completing a pour-over and handing the coffee to the customer.

【Reference Asset Roles】
Use @Image1 for the barista's facial features, short hair, and brown apron; do not adopt the image's background.
Use @Image2 for the cafe's wooden counter, glass windows, and warm afternoon light; do not adopt the people in the image.
Use @Video1 for the pouring rhythm and wrist movements during the pour-over; do not adopt the identities, clothing, or scene from the video.

【Event Script】
At the start, the barista stands on the inner side of the counter, the customer stands on the outer side, and the dripper and serving carafe are between them. Following the action rhythm in @Video1, the barista slowly pours the water. After finishing the pour, the barista returns the dripper to its holder, then uses both hands to hand the only cup of coffee to the customer. At the end, the coffee is held only by the customer, and both of the barista's hands have moved away from the cup.

【Maintain Consistency】
Maintain the barista's identity and apron, the cafe layout, the positions on the inner and outer sides of the counter, and the number of coffee cups.
