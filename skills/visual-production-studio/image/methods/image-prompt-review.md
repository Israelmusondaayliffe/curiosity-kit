# Review prompts or supplied images

Review the artifact the user actually supplied. A prompt, prompt set, shot list or rendered image is enough; no preceding generation workflow is required.

1. Read the brief and relevant references. Establish intended count, file/composite form, named model and tool if any, exact copy, protected features and allowed changes.
2. Check the written artifact for missing instructions, contradictions and unsupported claims. Look for ambiguous reference roles, competing change/keep clauses, wrong format or ratio, accidental substitutions, nonexistent controls and recipe defaults that erase the source's character.
3. For a set, review coverage, meaningful variation and continuity. Preserve intentional repeats, cutaways and absent subjects. Do not impose old ten-shot photoshoot rules on unrelated work.
4. Inspect material and spatial behavior where the medium calls for it: weight, contact, scale, reflection, occlusion, light direction, marks and texture. Use [material review](../references/image-prompt-review/material-review.md) only when these details matter.
5. If images are present, compare visible output with the actual source and prompt. Separate observed drift from potential prompt risks. Without images, label the work prompt review only.
6. Report defects tied to specific prompts, clauses or visible regions. Recommend the smallest repair. If revisions are requested, return complete corrected prompts while retaining useful wording, exact strings, format and unaffected choices. A shared structural defect can receive one shared correction rather than a creative rewrite of every frame.

The optional [JSON checker](../scripts/validate_prompt_payload.py) accepts objects, arrays, fenced JSON, directories and stdin. Use requested count and required/equal dotted paths only when derived from the brief. For example, `python3 image/scripts/validate_prompt_payload.py prompts.md --expect-count 2 --require-path subject --equal-path palette` from the skill root. It checks JSON structure and explicit constraints, not a provider schema, visual quality or creative acceptance.

[Review methods](../references/image-prompt-review/review-methods.md) retains the full review taxonomy. [Midjourney prompt checks](midjourney-prompt-architect.md) covers that syntax separately. User selection determines acceptance and preferred reusable recipes.
