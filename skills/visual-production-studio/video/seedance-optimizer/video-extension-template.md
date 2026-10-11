# Video Extension Template

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

If the user says only "extend" and the direction cannot be determined from context, the direction is high-impact information and must be included in a single consolidated clarification request.

In an extension Prompt, use the user's confirmed name for the subject at the boundary. When the user writes only "person" or "subject," retain that neutral term. Do not infer a profession, performance type, or narrative identity from the subject's actions, posture, or clothing in the source video.

Throughout the extension, the same subject must remain one continuous instance; it must not be duplicated, split, or replaced with a second identical subject. Keep the body structure, number of parts, and topological relationships consistent with the boundary frame. When the subject turns around, becomes occluded, exits the frame, or re-enters, it is still the same continuous object and must not be replaced by a new instance.

The final Prompt must state the single-instance and topology requirements above explicitly; they must not be checked only during internal analysis and then omitted.

### Forward Extension (After the Original Video)

A forward extension continues generation after the source video ends. The first frame of the new segment continues from the source video's final frame.

```text
@Video1 is the source video to extend forward.

Extend @Video1 forward. The first frame of the extended segment directly continues from the final frame of @Video1: maintain continuity in <subject posture and orientation>, <prop positions>, <background and spatial relationships>, <camera position and composition>, <lighting>, <audio state>, and <motion trajectory>.

Then, <new action, event, shot, or sound to add in the extension>.

Throughout the extension, maintain continuity in <character identity and clothing>, <key props>, <background layout>, <camera axis>, and <the original audio environment>.
The same subject must remain the same continuous object throughout, without duplication or splitting; the character's appearance or the number of an object's parts must remain stable.
```

Completed example with additional assets:

```text
@Video1 is the source video to extend forward.
@Image1 is used for the Gardener's facial features, short hair, and light-green work apron; do not use the image background.
@Image2 is used for the structure and material of the woven flower basket; do not use the garden or people from the image.

Extend @Video1 forward. The first frame of the extended segment directly continues from the final frame of @Video1: maintain continuity in the greenhouse workbench, the Gardener's position and orientation, the wooden rack's position, the fixed medium-shot camera position, and the afternoon side lighting. The other reference assets must not replace this boundary frame.

Then, the Gardener picks up the woven flower basket defined by @Image2 from beneath the workbench and places it with both hands on the middle shelf of the wooden rack behind him. At the end, the basket is only on the middle shelf, and the Gardener has released both hands and stepped back half a step.

Throughout the extension, maintain continuity in the Gardener's face and apron, the greenhouse layout, the wooden rack's position, the camera direction, and the greenhouse ambience.
The Gardener and the basket must each remain the same continuous object throughout, without duplication or splitting; the Gardener's body structure and the basket's number of parts must remain stable.
```

### Backward Extension (Before the Original Video)

A backward extension generates content before the source video begins. The final frame of the new segment connects to the source video's first frame.

First describe what happens before the source video begins, and then define the source video's first frame as the explicit end state of the extended segment. Writing only "then connect to the source video" may cause the model to introduce characters, props, or effects from later in the video too early, or to change the image again after reaching the target state.

```text
@Video1 is the source video to extend backward.

Extend @Video1 backward. Before the source video begins, <preceding action, event, shot, or sound>.

The final frame of the extended segment connects naturally to the first frame of @Video1: keep <subject posture and orientation>, <prop positions>, <background and spatial relationships>, <camera position and composition>, <lighting>, <audio state>, and <motion trajectory> consistent.

Throughout the extension, maintain continuity in <character identity and clothing>, <key props>, <background layout>, <camera axis>, and <the original audio environment>.
The same subject must remain the same continuous object throughout, without duplication or splitting; the character's appearance or the number of an object's parts must remain stable.
Characters, props, or effects that belong only to later parts of the source video must not appear early.
```

When additional reference assets are provided, first state each asset's role for characters, clothing, props, or sound, and then state that the source video controls the extension boundary. New assets must not override the source video's control of the boundary image at its final or first frame.

An extension creates only a new segment beyond the boundary; do not edit the source video at the same time. The boundary goal is natural continuity in visuals and sound, not guaranteed pixel-level identity. The volume of the extended segment may differ slightly from that of the source video.
