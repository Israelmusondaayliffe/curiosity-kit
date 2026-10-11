# Role-Based Multi-Reference Prompt Template (Model-Agnostic)

Selected recipe: use only relevant fields, supplied assets and the exact model profile. Descriptive tags and JSON are not universal native controls; preserve requested count/style/copy.


For Kling, Veo, and other selected models that accept role-assigned reference images (subject reference, style reference, environment reference, mood reference, and structural-guide for storyboards that direct the sequence without being rendered).

### Shot Prompt Structure

```
SHOT [N] ([timestamp]). [Shot Name]
EFFECT: [Primary effect] + [secondary effects]
Using the subject from the uploaded [explicit description of subject reference: identity, features, clothing, pose], placed in the environment from the uploaded [explicit description of environment reference: space, architecture, lighting, atmosphere], rendered in the visual style of the uploaded [explicit description of style reference: color palette, grain, contrast, mood, photographic quality]. [What moves in this shot]. Camera [behavior]. [Speed/timing]. [How the references integrate: which dominates, where they blend]. Maintain [identity anchors from subject reference]. [Transition to next shot]. Do not change aspect ratio.
```

### With Structural Guide Reference

When one of the uploaded references is a storyboard composite, panel grid, or production board (structural-guide role), use this variant. The structural-guide image is read for sequence structure only and is never rendered in the output.

```
SHOT [N] ([timestamp]). [Shot Name]
EFFECT: [Primary effect] + [secondary effects]
Using the subject from the uploaded [explicit subject description], placed in the environment from the uploaded [explicit environment description], rendered in the visual style of the uploaded [explicit style description], following the panel-by-panel sequence shown in the uploaded [explicit storyboard description].

CRITICAL: Do not render the storyboard image in the final video. Use the storyboard only as a panel-by-panel structural guide. The final video does not show panel borders, panel numbers, timing brackets, annotation arrows, or grid layout.

[Per-shot beat blocks describing what happens. Each mirrors one panel from the storyboard.]

Maintain identity, style, and environment as referenced. Do not change aspect ratio.
```

If only two roles plus structural guide are present (no environment reference, for example), adapt the opening sentence accordingly. The structural guide and do-not-render directive remain mandatory.

If only two references (e.g., subject + style, no separate environment):

```
Using the subject from the uploaded [explicit subject description], rendered in the visual style of the uploaded [explicit style description]. [Environment described in text since no environment reference]. [Motion, camera, effects]. Maintain [identity anchors]. Do not change aspect ratio.
```
