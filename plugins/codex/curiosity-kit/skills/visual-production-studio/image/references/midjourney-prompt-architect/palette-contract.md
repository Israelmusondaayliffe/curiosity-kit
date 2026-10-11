# Palette contract intake

Use this adapter only when the user supplies a palette contract, a contract file, or a canonical pointer owned by the relevant project.

## Accepted input

Read JSON, YAML, Markdown, or structured text that identifies some or all of:

- palette or collection name;
- named colors and exact values;
- roles such as dominant, support, highlight, shadow, neutral, or accent;
- approved pairings, proportions, contrast rules, materials, or lighting behavior;
- forbidden substitutions or combinations;
- provenance and the contract's authority level.

Treat explicitly approved fields as locked. Preserve exact color names and values. If the contract has no role mapping, use the colors without inventing a hierarchy and state the assumption outside the prompt only when consequential.

## Prompt mapping

Translate the contract into observable color behavior:

- name the dominant field or material;
- assign supporting colors to surfaces, wardrobe, environment, or light;
- reserve accents at the stated scale;
- preserve approved contrast and temperature relationships;
- vary placement, balance, atmosphere, or material response without leaving the palette.

Prefer meaningful color language over dumping a sequence of hex codes. Include exact values only when the user or contract requires them.

## User-supplied Wada palette source

Use the palette source supplied by the user or the project's approved palette contract. `{source}` below means that source's base URL. No hosted endpoint is bundled or assumed. Do not infer ownership, invent a public replacement, or treat this placeholder as a URL ready to submit. For a compatible source, join its base URL without a trailing slash to these paths:

- Repository: `{source}`
- All palettes: `{source}/data/palettes.json`
- One palette contract: `{source}/data/palettes/{NNN}.json`
- One palette reference image: `{source}/references/palettes/{NNN}.png`
- AI-use guide: `{source}/llms.txt`

`{NNN}` is the verified three-digit combination number from `001` through `348` for the retained Wada collection contract. A source claiming a different catalog must identify it; do not silently reinterpret its numbers as this collection. A supplied local export with the same JSON/image pairing is also usable. Preserve the combination number, exact color names, hex values, `prompt_recipe`, source/provenance and authority; accept additional relationship/role fields without changing their meaning. Verify the JSON and image against the selected source rather than deriving color values from the number.

For the original Wada image-reference recipe, when explicitly selected:

1. Read the palette JSON and preserve its exact number, color names, hex values, and `prompt_recipe`.
2. Put the corresponding reference PNG URL before the Midjourney text prompt as an Image Prompt.
3. Translate the named colors into observable materials, surfaces, atmosphere, and light without adding unrelated hues.
4. Keep the same palette across prompt variations unless the user explicitly chooses palette as the variation axis.
5. Validate that the JSON and PNG use the same combination number.

Use a supplied source when the user asks for Wada, palette learning or that reference recipe. It is an optional resource alongside current supplied brand colors and free color exploration. State a selected combination number only after it is verified.

If no source is supplied or the selected source cannot be read, use any exact supplied palette data and identify unverified fields. A prompt that does not need that specific combination can continue with its supplied or openly proposed color direction. Never invent a combination or URL.
