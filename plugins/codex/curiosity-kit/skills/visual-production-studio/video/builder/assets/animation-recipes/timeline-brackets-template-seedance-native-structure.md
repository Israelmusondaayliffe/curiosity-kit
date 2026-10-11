# Timeline Brackets Template (Seedance native structure)

Selected recipe: use only relevant fields, supplied assets and the exact model profile. Descriptive tags and JSON are not universal native controls; preserve requested count/style/copy.


Structured format for multi-shot prompts. Cleaner than "SHOT 1 / SHOT 2" labels. Matches the pattern in the highest-engagement Seedance prompts, and timings remain requested budgets rather than proven frame-exact results.

```
Style: [STYLE_FAMILY + cinematic markers: 35mm anamorphic, 24fps, film grain]. Duration: [Ns].
[0-8s] Shot 1: [Shot name]. [Subject + action]. Camera: [movement]. Lighting: [description]. End state: [...]. [Dialogue cue if any].
[8-16s] Shot 2: [Shot name]. [Subject + action]. Camera: [movement]. Lighting: [description]. End state: [...].
[16-24s] Shot 3: [Shot name]. [Subject + action]. Camera: [movement]. Lighting: [description]. End state: [...].
[24-30s] Shot 4: [Shot name]. [Closing beat]. End state: [...].
Constraints: consistent faces and clothing, no deformation, realistic physics, stable proportions. Same face, same hairstyle, same outfit where visible unless the brief changes it. No subtitles, no background music.
Audio: [ambient], [foreground sound], [music or score, or the [SOUND] foley-only directive].
Do not change aspect ratio.
```

Use this when the user requests: precise timing, a single-prompt multi-shot output, Seedance native syntax, or a time-coded script. Scale the bracket count to the duration; the four-beat 30s map (0-6, 6-14, 14-24, 24-30) is the default rhythm when the story has no natural structure.
