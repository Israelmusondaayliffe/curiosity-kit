# Video Generation Templates

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

### Basic Generation

Suitable for text-only generation or tasks with few references and a simple event:

```text
<Subject> <performs the main action or event> in <scene and environment>.
The visuals present <visual style or mood>.
The camera uses <shot size, camera position, camera movement, or cuts>.
The sound includes <dialogue, ambient sound, sound effects, or music>.
```

Delete any unnecessary visual, camera, or sound line, but the subject and main action or event must be explicit.

Completed example:

```text
A young ceramicist shapes clay on a pottery wheel in a studio at dawn, holding the spinning clay steady with both hands until it forms a narrow-necked vase.
Soft morning light enters through the window on the left, keeping the wooden table and clay in natural warm tones.
The camera begins in a medium shot observing the hand movements, then slowly pushes in toward the mouth of the vase.
The sound preserves the low hum of the wheel, palms rubbing against wet clay, and distant birdsong outside the window.
```

### Generation with Reference Assets

```text
【Generation Goal】
Generate <video type or core event>. The core subject is <subject>, and the principal event is <summary>.

【Reference Asset Roles】
@Image1 is used for <subject>'s <appearance, clothing, structure, or material>.
@Video1 is used for <action, camera movement, or pacing>; do not use <identity, clothing, or scene that could be unintentionally carried over>.
@Audio1 is used for <character or sound type>'s <voice quality, dialogue, ambient sound, or music>.

【Unused Assets】
@Image2, @Video2, and @Audio2 are not used in this task or for people, scenes, props, actions, camera, or sound.

【Subjects and Relationships】
<Subject A> maps to @Image1 and always retains <fixed features>.
The spatial, prop, or identity relationship between <Subject A> and <Subject B> is <relationship>.

【Event Script】
At the start: <state of people, props, and scene>.
Principal event: <continuous action or event>.
At the end: <character positions, prop ownership, or final visual state>.

【Maintain Consistency】
Keep <character identities and count, clothing, prop ownership, spatial directions, and sound relationships> stable.
```

Do not invent a visual style, camera movement, or sound merely to fill the template when the user did not request it. Simple tasks may merge adjacent sections, but must not omit the roles of assets that are actually used.

Completed example:

```text
【Generation Goal】
Generate a video of an old wooden chair being repaired. A carpenter first inspects the loose backrest, then applies wood glue and secures the joint. At the end, the chair is stable again.

【Reference Asset Roles】
@Image1 is used for the carpenter's facial features, short hair, and dark blue work apron; do not use the image background.
@Image2 is used for the old chair's curved backrest, dark wood grain, and worn areas; do not use the person in the image.
@Video1 is used for the hand movements when applying glue and pressing the joint together; do not use the character identity, clothing, or workbench from the video.

【Subjects and Relationships】
The carpenter always wears the dark blue apron defined by @Image1. There is only one old wooden chair, defined by @Image2, throughout the video. The tools remain on the right side of the wooden table.

【Event Script】
At the start, the chair is centered on the wooden table and the backrest joint is loose. The carpenter inspects the joint, applies wood glue, and uses both hands to press the backrest into place and secure it. At the end, the carpenter releases the chair, the backrest remains stable, and the chair's count and appearance remain unchanged.

【Maintain Consistency】
Keep the carpenter's identity and clothing, the chair's structure and count, the tool positions, and the studio's spatial orientation stable.
```
