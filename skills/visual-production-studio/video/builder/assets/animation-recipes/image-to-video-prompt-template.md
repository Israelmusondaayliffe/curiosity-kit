# Image-to-Video Prompt Template

Selected recipe: use only relevant fields, supplied assets and the exact model profile. Descriptive tags and JSON are not universal native controls; preserve requested count/style/copy.


Single reference image animated. Focus on motion, not description.

### Short Clip (single shot, 3-8 seconds)

```
Using the uploaded [explicit description of subject, pose, setting, lighting, and notable details], [describe the primary motion: what moves, in which direction, at what speed]. Camera [camera behavior: push-in, orbit, static, tracking]. [Secondary motion: environmental elements, atmospheric effects, fabric, hair]. [Speed/timing: normal speed, slow-motion percentage, speed ramp]. [Lighting shifts if any]. Maintain [identity anchors: specific features, outfit, expression foundation that must not change]. [Duration]. Do not change aspect ratio.
```

### Multi-Shot Sequence (4+ shots)

Each shot follows this structure:

```
SHOT [N] ([timestamp]). [Shot Name]
EFFECT: [Primary effect] + [secondary effects]
Using the uploaded [explicit description], [what moves in this shot]. Camera [behavior]. [Speed/timing]. [Subject identity anchors repeated]. [Transition to next shot]. Do not change aspect ratio.
```
