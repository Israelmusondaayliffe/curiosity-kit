# Keyframe / First & Last Frame Prompt Template

Selected recipe: use only relevant fields, supplied assets and the exact model profile. Descriptive tags and JSON are not universal native controls; preserve requested count/style/copy.


Two reference images: start state and end state. Prompt describes the transformation between them. Bind actual first/last assets through the selected surface’s supported conditioning fields; prose alone is not a hard endpoint lock.

### Variation Format (3-5 variations exploring different interpolation styles)

```
Starting from the uploaded [explicit description of start frame: subject, pose, environment, lighting, mood], transition toward the state shown in the uploaded [explicit description of end frame: what changed, new pose, new environment, new lighting, new mood]. [Transformation style: smooth morph / dramatic shift / physics-based / time-lapse]. [What changes first, what changes last. sequencing the transformation]. [Midpoint description: what the halfway state looks like]. Camera [behavior during transformation]. [Speed/pacing: constant, accelerating, decelerating]. [Duration]. Maintain [persistent elements: what stays constant across both states]. Do not change aspect ratio.
```

### Shot-by-Shot Format (for complex transformations)

```
SHOT 1 ([timestamp]). Anchor Start State
EFFECT: [Subtle motion establishing the start frame is alive]
Starting from the uploaded [explicit start frame description], [minimal motion: breathing, wind, ambient movement]. Camera [static or very subtle]. Maintain [all start-state anchors]. Do not change aspect ratio.

SHOT 2 ([timestamp]). Transformation Begins
EFFECT: [First transformation effect]
[What element begins changing first]. [Direction and speed of change]. Camera [reacts to or reveals the change]. [Start frame anchors still mostly intact]. Do not change aspect ratio.

SHOT N ([timestamp]). Arrive at End State
EFFECT: [Resolution effect]
[Final elements settle into the end state shown in the uploaded end frame description]. Camera [final position]. [All end-state anchors now established]. Do not change aspect ratio.
```
