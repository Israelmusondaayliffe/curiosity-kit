# Write a Midjourney creation prompt

Use this method for creation, rewrite, optimization and controlled variation in Midjourney. It produces prompt text. Requested browser submissions belong to [batch operations](midjourney-prompt-batching.md).

## Build the picture

1. Extract the explicit subject, action/state, setting, medium, mood, composition, exact visible copy, ratio and reference strings. Separate locked choices from open ones.
2. Choose medium-native language. Photography needs relevant light, lens behavior and material response; illustration needs marks, edges, fills and surface; graphic design needs hierarchy, shape and spacing. Do not add camera specifications to unrelated media.
3. Lead with what appears in the frame. Describe subject and medium, then the action/state, setting, composition, light/palette and only the technical treatment that changes the picture. Translate abstract emotion into posture, gesture, distance or atmosphere.
4. Create the requested number of alternatives. One settled concept can use one prompt. Exploration may vary moment, framing, light, palette, material, mark or energy while preserving the locks. The original concise/controlled/complex word bands and four-option pack are craft examples, not caps or quotas.
5. Add controls after the visual description, on the same line. Use the selected [Midjourney model/operation guidance](../../references/models/midjourney.md). Version pinning belongs to an explicit version request or reproducibility need; do not automatically pin a historical example's version.
6. Keep every supplied URL, style code, personalization/profile ID and multiple-tag string exact. Image Prompts influence content/composition/color; Style References influence treatment; Personalization and Moodboards apply an aesthetic. Do not interchange their roles or invent codes.
7. Include only supported controls that have a job. Lower stylization and chaos can serve literal work; stronger interpretation belongs to open work. Image weight needs an actual Image Prompt; style weight needs a Style Reference and the selected operation's compatibility. Speed, repeats, privacy and higher-cost options are intentional execution choices.

## Palette and Wada

For a supplied palette contract, preserve color names, values, roles, pairings, proportions and forbidden substitutions. Place colors on visible fields, materials, surfaces and light. If the palette has no role hierarchy, do not claim one was approved.

Use [the complete palette adapter](../references/midjourney-prompt-architect/palette-contract.md) for palette files, palette learning or a named Wada combination. The selected Wada image-reference recipe requires its actual palette JSON, exact combination, colors and prompt recipe, plus the matching canonical PNG. Verify that JSON and PNG use the same number, then place the verified PNG URL before the prompt. Preserve the palette across variations unless color is the requested variable. If the source is unavailable, use exact supplied data and mark what cannot be checked. Never invent a combination or URL. [General color methods](../references/shared/color.md) also supports model-neutral palette work.

## Finish and optionally check a saved pack

Return each independently complete prompt in the requested copyable format. Include a brief direction note only when useful; omit it for prompt-only requests. Keep parameters with their prompt and do not append descriptive prose after the suffix. Check exact copy, source strings, count, distinctness and unresolved placeholders.

The [craft reference](../references/midjourney-prompt-architect/prompt-craft.md) retains full medium-specific methods. The [pack template](../assets/midjourney-prompt-architect/prompt-pack-template.md) is optional.

For saved Markdown packs, run `python3 image/scripts/validate_prompt_pack.py pack.md --count N --expect-reference EXACT_STRING` from the skill root when deterministic structure checks help. `--profile PATH` tests only that supplied snapshot. The retained [historical creation snapshot](../references/midjourney-prompt-architect/current-model-profile.json) is not today's compatibility authority and cannot govern edit or Draft operations. The checker always reports that live support is unverified. It cannot establish render quality or acceptance.
