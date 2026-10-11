# Color exploration and Wada

Use a supplied palette or reference first. Otherwise choose color for the subject, mood, medium and legibility. Explore freely; Wada is a rich optional source, not the default for every image or a required brand dependency.

When Wada is requested, use the exact supplied combination or select a suitable one from a user-supplied palette source. Use the base URL supplied in the current task or its approved palette contract as `{source}`; there is no bundled default. Do not assume an adopter owns a particular palette service or invent a public replacement. The selected source must expose the following compatible layout (join the base URL without a trailing slash to each path):

- Library: `{source}`
- All combinations: `{source}/data/palettes.json`
- Combination data: `{source}/data/palettes/{NNN}.json`
- Reference image: `{source}/references/palettes/{NNN}.png`
- AI-use guide: `{source}/llms.txt`

These are templates, not verified URLs. A supplied local export can provide the same JSON/image pair. Verify the selected source and its JSON before naming colors or numbers; use the [palette contract](../midjourney-prompt-architect/palette-contract.md) for exact fields and the optional image-reference recipe. If no source is supplied, request it only when that specific Wada lookup is needed; other color work can continue from supplied colors or a clearly proposed direction.

Replace `{NNN}` with the verified three-digit combination number. Keep names, values, relationships and source together. Assign visual roles such as dominant field, supporting material and small accent. For a generation request, attach the matching palette PNG if the surface permits; URLs alone may not be read. If inaccessible, use exact supplied palette information or say the source could not be checked. Do not invent a Wada number.

In NL, name the colors and their roles. JSON can use `palette_contract` with `combination`, `colors`, `reference_image`, `authority` and relevant `forbidden_hues`. System prompts can carry a shared `<palette_contract>`. Hold the palette across a set only when continuity calls for it; if color exploration is requested, vary it deliberately. Judge rendered relationships rather than promising exact pixel color from a text prompt.
