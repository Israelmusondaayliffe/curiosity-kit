# Model and surface selection

This is practical selection guidance, not a tested ranking. The imported worked pairs retain their original model labels. No generation benchmark or current provider capability test was performed as part of this source repair.

## Choose from the request

Use the named model and access surface. With no model named, write a broadly compatible prompt rather than forcing a pair-selection interview. Keep natural-language, JSON and structured prompt forms useful across releases. Refresh dated model facts only when the user requests an update.

For Stage 1, the relevant questions are whether the selected surface can produce a readable composite, follow reference roles, and fit the required labels and panels. For Stage 2, check whether it accepts a board as a structural reference, a clean opening frame, multiple references, requested duration, keyframes or audio. Do not infer support from another surface bearing the same model name.

## Reference patterns, not native API contracts

| Pattern | Reusable approach | Verify only when needed |
|---|---|---|
| OpenAI Images or Nano Banana board | Director's board, references, precise labels, JSON or natural-language instructions | Available model, aspect controls and actual output support |
| Midjourney board | Visual panels or a supplied composite; explicit reference roles | Current creation/edit controls and how references are attached |
| Seedream, Recraft, Ideogram or another selected image family | Adapt the standalone Stage 1 template to the requested treatment | Reference and text support on the selected surface |
| Seedance-style beat prompt | Ordered beats or terse board-reference form; role-aware sheets | Attachment tags, clip limit, actual multi-reference and audio controls |
| Veo-style prose | Camera/action prose and optional descriptive sound cues | Reference inputs, duration and audio support |
| Kling-style shot prompt | Explicit identity and shot progression | Whether seed, element or voice controls exist on that surface |
| Keyframe interpolation | Sampled storyboard frames with per-transition motion | Allowed keyframe count and duration |
| General I2V | Actual opening frame plus motion prose and separate board guidance if supported | Whether the surface can consume the board without displaying its grid |

`Clip N`, `SFX:`, timing brackets and JSON fields can organize a prompt. They are not proof of native model settings. Do not promise identity lock, exact beat execution, readable text or style fidelity before inspecting outputs. A seed, where exposed, is not a guarantee of character consistency.

## Simpler and longer work

A single subject with ambient motion may only need a clean image and a motion prompt. Do not impose a storyboard on that request. A character sheet, moodboard or JSON shot list can be drafted within this skill when it supports the requested Stage 1 artifact; no retired image-skill route is needed.

For long or dense sequences, choose readable sheets and editorial segments. Match clip lengths to the verified selected surface rather than a universal 15-, 25- or 30-second limit. If multiple generations are needed, preserve continuity frames and explain the actual submission count before execution.

Prompt-only work needs no credentials, external plugin or API. Actual tests use authorized subscriptions and the parent's bounded submission budget. No purchases, paid API calls or automatic retries are implied.
