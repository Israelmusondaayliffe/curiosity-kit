# Ideogram — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## Ideogram 4, Ideogram 4.0

Surface: Owner JSON prompting / v2 generate / v2 remix

### Status
original_target_confirmed

### Prompting
Native structured JSON differs from arbitrary JSON prose. Guide schema separates high-level intent, style and compositional background/elements. Bboxes use [ymin,xmin,ymax,xmax]0–1000. Exact text, hierarchy and uppercase hex colors belong in intended elements.

### Controls
v2 generate prompt 1–10000 chars,n 1–8,seed 0–2147483647,rendering_speed turbo/default/quality. Magic Prompt auto/on rewrites; off keeps wording while structuring; valid JSON bypasses except on.

### Primary evidence
- [Ideogram 4 JSON prompting introduction](https://ideogram.ai/blog/ideogram-4-json-prompting/). Substantive schema, ordering and controls sections approximately lines 142–312 of 366; introduction read. Publication/update: 2026-06-18. Access: 2026-10-09.
- [Ideogram owner prompting guide](https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md). Rendered lines 192–310 of 438; schema and prompt-processing distinction. Remaining detailed fields not fully reviewed. Publication/update: not established. Access: 2026-10-09.
- [Ideogram 4 generate v2](https://developer.ideogram.ai/api-reference/images/generate/ideogram-4). Rendered body lines 11–159 of 342; request and response fields. Publication/update: not established. Access: 2026-10-09.
- [Ideogram 4 remix v2](https://developer.ideogram.ai/api-reference/images/remix/ideogram-4). Rendered body lines 11–142 of 334; request and response fields. Publication/update: not established. Access: 2026-10-09.
- [The Ideogram 4.0 prompt guide](https://ideogram.ai/blog/claude-mcp/). Rendered lines68–191 of323; verbose/JSON modes, key ordering, palettes, reference-style extraction. Installation directions read as source content only; no installation performed. Publication/update: 2026-06-12. Access: 2026-10-09.

## Ideogram 4.5

Surface: v2 generate and separate precise-edit endpoint

### Status
new_current_discovery

### Prompting
Accepts natural language or Ideogram4 structured JSON. Generate route may rewrite according to Magic Prompt; precise-edit converts NL but uses valid JSON directly.

### Controls
n 1–8; quality very_low/low/medium/high with operation-dependent defaults. Black mask edits, white preserves. Precise-edit returns source dimensions subject to size downscaling; unmeaningfully changed pixels are copied according to API claim.

### Guide gap
Current endpoint explicitly reuses 4.0 JSON schema; standalone 4.5 craft guide not found.

### Primary evidence
- [Ideogram 4.5 generate v2](https://developer.ideogram.ai/api-reference/images/generate/ideogram-4-5). Rendered body lines 11–155 of 338; request/response and source-image rules. Publication/update: not established. Access: 2026-10-09.
- [Ideogram 4.5 precise edit v2](https://developer.ideogram.ai/api-reference/images/precise-edit/ideogram-4-5). Official canonical page and endpoint verified; substantive body 76–145 of 328. Publication/update: not established. Access: 2026-10-09.
- [Ideogram 4 JSON prompting introduction](https://ideogram.ai/blog/ideogram-4-json-prompting/). Substantive schema, ordering and controls sections approximately lines 142–312 of 366; introduction read. Publication/update: 2026-06-18. Access: 2026-10-09.


## Retained studio craft

For typography and layout, state exact quoted copy, reading order, hierarchy, composition, medium and background. Check whether Magic Prompt or another rewrite feature is active when exact prompt fidelity matters; preserve the user's choice and do not silently change settings. Inspect rendered lettering and file type rather than assuming the brand promise establishes accuracy.

## Native caption example and runtime boundary

Authored Ideogram 4 caption example, not model-tested:

```json
{"high_level_description":"A cream exhibition poster with a blue circle below its title.","compositional_deconstruction":{"background":"Solid cream paper","elements":[{"type":"text","bbox":[100,100,250,900],"text":"OPEN STUDIO","desc":"Large black sans-serif title"},{"type":"obj","bbox":[400,300,800,700],"desc":"Flat cobalt-blue circle"}]}}
```

The owner runtime expects serialized caption JSON; hosted generation endpoints can convert natural language. Keep those surfaces distinct. Preserve ordered keys: background before elements; object rows type/bbox/desc; text rows type/bbox/text/desc. Boxes are optional y/x/y/x values on 0–1000. A style_description, if used, requires its documented photographic or art branch and key order; do not mix both. Uppercase full hex colors are supported palette values. [Owner schema](https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md), sections 192–341 checked directly again 2026-10-09; later examples were not needed for this construction.

Ideogram 4.5 precise-edit is a separate operation with its own mask and source rules. Do not turn its pixel-preservation claims into a guarantee for ordinary generate/remix.

## Supplemental catalog discovery only

These retained names are not fully qualified native adapters. Do not inherit the newer branch's controls or silently upgrade a selected alias. Evidence observed 2026-10-09.

- `Ideogram3.0`, `Ideogram2a`, `Ideogram2.0`. [Catalog](https://developer.ideogram.ai/api-reference/images/generate/ideogram-4). Dedicated guide missing or not read. Official navigation/catalog presence only; older exact model guide not read. Status: catalog_only_not_execution_qualified.
