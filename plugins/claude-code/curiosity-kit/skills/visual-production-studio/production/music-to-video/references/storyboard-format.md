# Storyboard: frames and groups

The plan is Markdown with simple frontmatter. Every machine-read array/object uses strict JSON, including quoted object keys. It is not a general YAML parser. Keep explanatory prose outside those values; end-of-line comments are allowed after whitespace outside JSON strings. Frames use `## Frame N — id` (`:` or `-` separators also work). Top-level metadata is unindented; group metadata is indented. The heading id is a human treatment label, while the source filename stem is the engine composition ID.

```markdown
---
compositionId: music-video
duration_s: 8
canvas: {"w":1080,"h":1920,"fps":29.97}
style: restrained editorial / supplied brand
assets: false
---

## Frame 1 — opening
- src: compositions/frames/01-opening.html
- duration: 4s
- span_sec: [0,4]
- pacing: beat_cut
- mood: energetic
- feel: four strong onsets resolve into a clean hold

### Groups
- **g1** — template: `intro-kinetic-cascade`
  - span_sec: [0,4]
  - params: {"theme":"light","icon":"bolt"}
  - role_bindings: {"phrase":{"times":[0,1,2]},"climax":{"in":3}}
  - copy: "Build with intention"

## Frame 2 — hold
- src: compositions/frames/02-hold.html
- duration: 4s
- span_sec: [4,8]
- pacing: phrase_flow
- mood: spacious
- feel: sustained tail with no reliable transient grid

### Groups
- **g1** — free_design
  - span_sec: [4,8]
  - free_design: {"dominant_system":"held wordmark","primitives":["negative-space-hold"],"density_topology":"remove"}
  - anchors: [4,8]
  - copy: "Make it matter"
```

This example requires a matching audiomap whose duration is eight seconds and whose supplied/measured/manual anchors include 0,1,2,3,4,8. It does not invent real audio evidence. A manual anchor must include its source and reason. A beat-cut frame needs actual rhythmic support even when a syntactic validator accepts the numeric map.

## Fields

Frontmatter requires positive `duration_s` and JSON `canvas` with positive integer `w`/`h` and finite positive `fps`. Keep source music identity and analysis provenance in the audiomap/project record. Optional style/assets/build notes remain readable authoring context.

Every frame requires `src`, positive `duration`, two-value `span_sec`, `pacing` (`beat_cut` or `phrase_flow`) and filled groups. Mood/feel describe the musical interpretation. Duration equals span length. Frames begin at zero, proceed contiguously in document order and end at track duration. Each filename stem becomes its exact frame composition ID and timeline key.

A group has one kind, `template`, `free_design` or `asset`, and its own track-time span. Groups tile the frame without gaps/overlap. Template IDs must exist. `params` binds actual declared variables; `role_bindings` records real anchor roles, not GSAP tweens. Free design includes dominant_system and nonempty primitive IDs; `anchors` names the real times. Asset JSON includes treatment (`beat_cut`, `ken_burns`, `bg_under_text`), nonempty local `clips`, optional anchor array and overlay copy. Never use beat_cut in phrase_flow.

All group boundaries and named anchor arrays refer to canonical audiomap seconds, within the group and sorted. The builder converts to frame-local time. A role's `hold` or font `size` is a duration/value, not automatically an absolute musical timestamp. Do not place a boundary inside a roll simply to satisfy a preferred duration. Dense sub-phases belong within a coherent group when that better follows the music.

## Validation and edits

Run `../scripts/validate-plan.mjs` before building and assembly. Unknown references, missing audio map, malformed JSON, invalid paths, impossible intervals and absent anchors are failures. The helper checks numeric membership; it does not prove that an inferred downbeat is musically correct. Review anchor provenance and actual source evidence separately. A skeleton intentionally fails until groups are filled. After changing the source track or analysis, revalidate affected timing and compositions.
