# Keyframe Anchors

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

Keyframe images are still provided as ordinary reference images; assign each image a specific role in the Prompt. Do not combine the first-frame and last-frame roles into a single range statement.

When fixing the first frame, write `Use @ImageN as the first frame.` as a standalone sentence. When fixing the last frame, write `Use @ImageN as the last frame.` as a standalone sentence. Do not weaken these statements to "use only as a first-frame reference," "reference the opening composition," or "first-frame composition reference." Do not compress the role statement and the subsequent action into the same sentence. The exact role statement must remain verbatim in the final Prompt. Add a separate sentence describing the composition, subject positions, poses, prop states, scene, and camera direction defined by that frame.

The first frame locks the output aspect ratio. The first and last frames should use the same aspect ratio to avoid stretching the last frame; duration is still set on the generation page or through the API. This rule is only for input preflight and must not be written into the Prompt as an output parameter.

### First Frame Plus Other References

```text
Use @Image1 as the first frame.
This first frame defines the composition at the start of the video, subject positions, poses, prop states, scene, and camera direction.
Use @Image2 for the <appearance, clothing, structure, or material> of <the subject> without changing the first-frame composition defined by @Image1.
Use @Image3 for <the scene, props, or lighting> without changing the first-frame composition defined by @Image1.

The shot begins naturally from the first frame defined by @Image1, followed by <a continuous action or event>.
Maintain continuity in <character identities, prop ownership, spatial relationships, and visual style>.
```

### First Frame, Last Frame, and Other References

```text
Use @Image1 as the first frame.
This first frame defines the composition at the start of the video, subject positions, poses, prop states, scene, and camera direction.
Use @Image2 as the last frame.
This last frame defines the composition at the end of the video, subject positions, poses, prop states, scene, and camera direction.
Use @Image3 for <Subject A>'s <appearance, clothing, structure, or material> without changing the first-frame composition in @Image1 or the last-frame composition in @Image2.
Use @Image4 for <the specified attributes> of <Subject B, a prop, or the scene> without changing the first-frame composition in @Image1 or the last-frame composition in @Image2.

<One continuous action or event>.
The shot begins naturally from the first frame defined by @Image1 and, after a continuous action, arrives at the last frame defined by @Image2.
Maintain continuity from first to last in <character identities, prop structure and ownership, scene layout, and camera direction>.
```

Completed example:

```text
Use @Image1 as the first frame.
This first frame defines the baking station, the cake decorator's position, the undecorated cake, tool placement, and a frontal medium-shot camera position.
Use @Image2 as the last frame.
This last frame defines the decorated cake centered on the turntable, the cake decorator's hands away from the cake, and the same frontal medium-shot camera position.
Use @Image3 for the cake decorator's facial features, updo, and white uniform without changing the first-frame composition in @Image1 or the last-frame composition in @Image2.
Use @Image4 for the cake's two-tier structure, white frosting texture, and blueberry decorations without changing the first-frame composition in @Image1 or the last-frame composition in @Image2.

The shot begins naturally from the first frame defined by @Image1. The cake decorator rotates the cake turntable, continuously pipes even cream patterns along the edges of both tiers, and then places the blueberries one by one. Finally, the decorator moves both hands away from the cake and naturally arrives at the last frame defined by @Image2.
Maintain continuity from first to last in the cake decorator's identity and clothing, the number and two-tier structure of the cake, tool positions, the baking-station layout, and camera direction.
```

When the user explicitly requests an intermediate key state, an additional image may define the characters, actions, props, and spatial relationships that must appear at that moment; describe the shot as naturally reaching that state around the specified time. It is a semantic anchor, not a static hold or a pixel-locked frame. When the first-frame and last-frame boundaries take priority, reduce other assets unrelated to the current event.

### Controlling the Order of Multiple Keyframes

When multiple independent images define separate process stages, use the first sentence to declare the keyframe order, then describe each key state image by image. Keyframes control stage order and visible states; they do not promise frame-by-frame replication or require a static hold at any key state.

```text
Use @Image1 through @ImageN as keyframes in that order.

Use @Image1 as the first frame.
This first frame defines <the starting composition, subject positions, poses, prop states, and camera direction>.
@Image2 defines the second keyframe: <the visible state at the end of the first stage>.
@Image3 defines the third keyframe: <the visible state at the end of the second stage>.
Use @ImageN as the last frame.
This last frame defines <the ending composition, subject positions, poses, prop states, and camera direction>.

The shot passes through the states defined by @Image1, @Image2, @Image3, and onward to @ImageN in order, using continuous action to transition naturally between stages.
Throughout the process, maintain continuity in <subject identities, prop structure and ownership, scene layout, lighting, and the camera axis>.
```

### Storyboard Grids and Storyboards

A storyboard grid defines the overall story, shot order, and approximate composition; it does not require strict replication of every panel's details. Prefer clean storyboards with no more than 15 panels and minimal text annotations. Specify the reading order, the shot structure to adopt, and any sketch style, annotations, or placeholder characters not to adopt.

```text
@Image1 provides the shot order and approximate compositions for an <N-panel storyboard grid>. Read it <from left to right and from top to bottom>; do not adopt <the sketch style, text annotations, or placeholder characters> shown in the image.
@Image2 defines <Subject A>'s <appearance and clothing>.
@Image3 defines <the structure, material, or lighting> of <a key prop or scene>.

Shot 1: <shot size, subject action, and scene state>.
Shot 2: <shot size, subject action, and camera movement or transition>.
...
Shot N: <ending action and final visual state>.

The final visuals use <visual style>. The audio includes <dialogue, ambience, action sound effects, or music>.
```

### Blockout References and Rendering

First determine whether the blockout video provides a motion skeleton or a complete structure:

- **Coarse blockout**: Simple geometry mainly provides action paths, direction of movement, subject blocking, entrances and exits, camera position, camera movement, cuts, lighting changes, audio rhythm, or spatial relationships. Map every geometric object individually to a final subject or prop.
- **Fine blockout**: The structure of the subjects, props, or scene is already complete. It is mainly used to replace character appearance, materials, colors, the scene, or the visual style. Preserve the existing structure, actions, spatial relationships, and camera work.

A blockout video is a generation reference; it does not automatically become the editing master merely because it is a video. If the blockout contains trajectory lines, coordinate axes, controllers, camera frustums, or text markers, explicitly exclude those production markers.

#### Coarse Blockout

```text
@Video1 is a coarse-blockout reference. Use it only for <action paths, subject blocking, camera position, camera movement, cuts, lighting changes, audio rhythm, or spatial relationships>; do not adopt its blockout appearance, materials, or scene.
<Blockout Subject A> in @Video1 corresponds to <Subject A>.
<Blockout Subject B or geometric prop> in @Video1 corresponds to <Subject B or a key prop>.
@Image1 defines <Subject A>'s <appearance, clothing, or structure>.
@Image2 defines <the specified attributes> of <Subject B, a key prop, or the scene>.

<The subject> completes <the primary action or event> in <the scene>.
Preserve <the action paths, blocking, camera movement, cuts, lighting, or audio rhythm> from @Video1.
The final visuals use <the characters, scene, materials, and visual style>. The audio includes <dialogue, ambience, or action sound effects>.
```

#### Fine Blockout

```text
@Video1 is a fine-blockout reference. Preserve <subject structure, actions, spatial layout, camera position, camera movement, and cuts>; do not adopt its original gray-blockout materials, blank background, or production markers.
@Image1 defines <the character appearance, material, color, or surface details> of <the subject>.
@Image2 defines <the space, materials, lighting, or visual style> of <the scene>.

Rerender <the subject> in @Video1 as <the final subject>, and rerender the scene as <the final scene>.
Preserve <the structure, actions, camera work, and spatial relationships> from @Video1. The visuals present <materials, colors, and style>. The audio includes <ambience, sound effects, or music>.
```
