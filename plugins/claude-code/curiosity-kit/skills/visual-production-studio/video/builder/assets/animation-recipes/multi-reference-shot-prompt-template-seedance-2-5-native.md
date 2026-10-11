# Multi-Reference Shot Prompt Template (Seedance 2.5 Native)

Selected recipe: use only relevant fields, supplied assets and the exact model profile. Descriptive tags and JSON are not universal native controls; preserve requested count/style/copy.


This optional staged recipe binds each actual reference by role. Verify current capacity, duration and syntax in the selected Seedance profile; no universal working-set sweet spot is established.

### Structure

```
[Reference-binding block: one role line plus one exclusion line per tag.]
@Image 1 defines <CharacterName>'s face, hairstyle, and [garment]. Do not use the background.
@Image 2 defines [element]. Do not use [what it must not contribute].
@Video 1 defines only the [motion type] motion. Do not use the person's identity, clothing, or scene from the video.
@Audio 1 is the background music.

[Style and world preamble: visual style, era, setting, lighting register, filmic markers.]

[0-6s] [Stage 1: one primary change, referencing tags as they appear.] End state: [where things are].
[6-14s] [Stage 2.] End state: [...].
[14-24s] [Stage 3, the turn.] End state: [...].
[24-30s] [Stage 4, resolution.] End state: [...].

[Consistency clause: same face, same hairstyle, same outfit, same body type where visible unless the brief changes it.] No subtitles, no background music[, adjust when music is directed via @Audio or (music)].
[Audio line: native syntax (music), <sound effects>, {dialogue}, or ambient-only list.]
Do not change aspect ratio.
```

### Reference Example (Seedance 2.5 idiomatic)

```
@Image 1 defines <Chef>, a small husky in a white chef hat. Do not use the background.
@Image 2 defines the copper-pot kitchen set. Do not use any characters from it.
@Audio 1 is the warm jazz piano score.

Cinematic 3D render, warm golden-hour restaurant kitchen, shallow depth of field, 24fps.

[0-6s] <Chef> stirs a copper pot on the stove, steam rising. End state: he lifts the spoon to taste.
[6-14s] He tastes, eyes widen, and barks one command toward the pass. End state: three plates lined up on the counter.
[14-24s] A waiter sweeps past collecting the plates; the camera tracks the plates through the kitchen bustle. End state: the last plate lands on the pass under warm light.
[24-30s] <Chef> leans into frame, looks straight into the lens, and gives one approving nod. End state: hold on his face, steam drifting.

Same face, same fur pattern, same chef hat where visible unless the brief changes it. No subtitles.
(music: @Audio 1 warm jazz piano) <kitchen clatter, sizzling, soft laughter>
Do not change aspect ratio.
```

### Rules

- One prompt in one code block. Not N prompts.
- Every tag gets a role line AND an exclusion line. The exclusion line stops reference leaks.
- Tag numbering follows upload order. Retain actual selected-version reference syntax; do not infer parser compatibility across versions.
- One primary change per stage, an explicit end state per stage. Time ranges are budgets.
- Preamble carries style, world, and filmic markers.
- Audio uses the source illustrative notation: `(music)`, `<sound effects>`, `{dialogue}`. For clean footage: `[SOUND] Strictly only naturally occurring sound and foley, no music allowed.`
- Always close with "Do not change aspect ratio."
- Do NOT use the "Using the uploaded [description]..." prefix. That convention is for other sub-modes.

### Reference Mapping Block (shown in the response, NOT in the prompt)

Above the prompt code block, present a mapping so the user knows which upload corresponds to which tag:

```
REFERENCE MAPPING:
@Image 1 = [description of first uploaded image] (role: ..., excludes: ...)
@Image 2 = [description of second uploaded image] (role: ..., excludes: ...)
@Video 1 = [uploaded video description] (role: motion reference)
@Audio 1 = [uploaded audio description] (role: score / beat sync)
```

This mapping is for the user's reference. It is not part of the Seedance prompt itself.
