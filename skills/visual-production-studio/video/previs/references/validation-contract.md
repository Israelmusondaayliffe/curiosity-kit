# Applicable checks and rendered-board handoff

Validators check prompt structure and recorded evidence, not creativity, provider capability or actual visual fidelity. Final creative acceptance belongs to the user or the creative reviewer explicitly designated for the current task. They use Python's standard library; the optional grid detector also needs Pillow and NumPy and reports a fallback when unavailable.

## Stage 1

Use `scripts/validate_stage1_prompt.py PROMPT --format FORMAT --duration SECONDS --panels COUNT`.

- `annotated` and `combat` require actual per-panel timing and an arrow legend.
- `grid` permits a clean numbered grid without invented timing or sound.
- `commercial` permits a table with duration/action/transition columns instead of arrows.
- `--audio required` adds a sound-cue check. `optional` is default; `silent` permits silence.
- If concrete timing is present, supply duration and count so coverage and cardinality are checked. A placeholder such as “timing bracket” is not a completed timed prompt.

The keyword checks are helpful lint, not a semantic judge. Fix factual failures. If valid prose escapes a heuristic, inspect the actual requirement and improve the check; do not add meaningless keywords to the user's prompt.

## Stage 2

Use `scripts/validate_stage2_prompt.py PROMPT SECONDS COUNT --format FORMAT --handoff READ.json`.

- `explicit` requires exact ordered contiguous ranges from zero to the full duration. Decimal seconds, `to` ranges, and minute:second ranges are supported. Gaps, overlaps, reversed ranges, reordered beats and zero duration fail.
- `reference` permits terse board-led prose with no timestamps. It does not prove exact timeline execution. If timestamps are included, all of them must pass.
- `keyframes` permits ordered `1->2:` transition prompts without inventing dense beat blocks. It does not prove keyframe-support limits.
- `--audio required` applies only when sound is requested. No native token is mandatory for ordinary prose or silent prompts.
- `--panel-map MAP.json` permits intentional compression. The JSON is one list of source panel IDs per output beat, for example `[[1,2],[3],[4,5]]`. Each source panel must occur exactly once, in order. This is an explicit adaptation, not an off-by-two tolerance. Mention the merging reason in delivery prose.

## Real board-read record

Inspect the rendered board first, then record the actual visible order and upload roles. This is a small test/handoff record, not a saved preferred creative recipe. Only mark observations actually made. Do not fill this example by copying an expected-output description.

```json
{
  "board_read": {
    "source": "actual-board.png",
    "observation": "Two sequential panels beneath the hero inset; inset is not counted.",
    "panels": [
      {"id": 1, "observation": "Wide view: subject enters from left."},
      {"id": 2, "observation": "Close view: hand reaches the door."}
    ]
  },
  "assets": [
    {"tag": "@Image1", "source": "actual-board.png", "role": "storyboard"},
    {"tag": "@Image2", "source": "character.png", "role": "identity"},
    {"tag": "@Image3", "source": "opening-frame.png", "role": "start-frame"}
  ]
}
```

Map tags to actual upload order. Accepted roles are storyboard, start-frame, end-frame, identity, wardrobe, expression, environment, style, motion and audio. Labels may be native tags or explicit stable natural-language upload labels. A single tag cannot be both a sheet and an opening frame. Omit assets not actually present. For surfaces without tags, keep this mapping as the operator's stable reference index and use natural-language labels in the prompt.

The validator checks nonempty panel observations, the recorded count/order, duplicate roles, unknown prompt tags and obvious misuse of a sheet as a start frame. It cannot tell whether a human or assistant actually viewed an image. The source image and direct visual read remain necessary evidence. The optional grid detector never substitutes for them.
