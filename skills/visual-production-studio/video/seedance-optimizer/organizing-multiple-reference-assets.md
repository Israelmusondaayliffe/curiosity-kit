# Organizing Multiple Reference Assets

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

Organize multiple reference assets in the following order:

```text
role of each asset → subject mapping → grouping by type → subject definitions → scene-by-scene activation
```

Having many reference assets does not mean that all of them should be included in the Prompt. Use only the assets relevant to the current story and scene. Put assets that are available but have not been assigned a role in `【Unused Assets】` within the Prompt, list every unused reference number, and prohibit their activation. Unused assets may be consolidated into one compact line for images, one for videos, and one for audio, but no reference number may be omitted or expressed as a subject-range mapping.

Seedance 2.5 accepts up to 50 reference assets. Even when approaching this limit, classify every asset individually by character, prop, scene, action, or sound, and activate it scene by scene. Do not use a catch-all sentence that leaves allocation to the model, and do not make all assets appear simultaneously merely to demonstrate their quantity.

### Grouping by Type

```text
【Characters】
<Character A> corresponds to @Image1; use only the appearance, hairstyle, and clothing.
<Character B> corresponds to @Image2; use only the appearance, hairstyle, and clothing.
Do not swap the two characters' appearances, clothing, actions, positions, or dialogue.

【Props】
<Prop A> corresponds to @Image3 and belongs only to <Character A>.
<Prop B> corresponds to @Image4 and belongs only to <Character B>.

【Scenes】
<Scene A> references @Image5; use only the space, materials, and lighting.
<Scene B> references @Image6; use only the space, materials, and lighting.

【Actions and Sound】
@Video1 is used for <Character A>'s <action or camera movement>; do not use the characters or scene from the video.
@Audio1 is used for <Character B>'s <voice timbre and specified dialogue>.
```

### Subject Definitions and Scene-by-Scene Activation

```text
【Subject Definition: Character A】
Appearance and clothing: @Image1.
Fixed prop: <Prop A> from @Image3.
Allowed scenes: <Scene A> and <Scene B>.
Action reference: <action> from @Video1.
Do not use: <another subject's clothing, props, or voice>.

Scene 1 | <Scene Name>
Use: <the subjects, props, scene, actions, and sounds activated for this scene>.
Event: <one main event>.
At the end: <observable state>.

Scene 2 | <Scene Name>
Use: <the subjects, props, scene, actions, and sounds activated for this scene>.
Event: <one main event>.
At the end: <observable state>.
```

Multi-angle references for the same subject should assign a role to each image. For example, front, left-side, right-side, and back views jointly define the same entity, and the number of entities in the final video must be stated explicitly.

### Spatial Relationships and Positions

Describe inside/outside, front/back, orientation, distance, and separation relative to stable objects such as doors, tables, vehicles, counters, and roads. Do not rely only on screen-left or screen-right. For example:

```text
The <Clerk> always stands on the inside of the glass display counter, facing outward. <Customer A> and <Customer B> stand side by side on the outside of the counter and speak with the <Clerk> across it.
```

When the user provides a clean blocking diagram, use it for composition, character positions, orientation, and spatial relationships. Do not treat arrows, annotation boxes, or explanatory text in the image as content for the final video.

Completed example with multiple assets:

```text
【Characters】
The Inspector corresponds to @Image1; use only the facial features, short hair, and orange windbreaker.
The Archivist corresponds to @Image2; use only the facial features, glasses, and gray knit cardigan.
Do not swap the two characters' appearances, clothing, actions, or dialogue.

【Props】
The portable recorder corresponds to @Image3, belongs only to the Inspector, and remains the only one throughout.

【Scenes】
The mountaintop observation station references @Image4; use only the building structure, metal platform, and overcast lighting.
The records room references @Image5; use only the bookshelf layout, wooden table, and warm indoor lighting.

【Actions and Sound】
@Video1 is used for the Inspector's action of opening the equipment bay and removing the memory card; do not use the characters or scene from the video.
@Audio1 is used for the Inspector's voice timbre and dialogue.

【Event Script】
Stage 1: The Inspector stands alone in front of the equipment bay at the mountaintop observation station, with the portable recorder hanging at his waist. He opens the equipment bay and removes the single memory card. At the end, the memory card is only in the Inspector's right hand.
Stage 2: Inside the observation station, the Inspector inserts the memory card into the portable recorder. At the end, the recorder's screen shows that data reading is complete, and the memory card remains inside the device.
Stage 3: The shot cuts to the records room. The Archivist stands on the inner side of the wooden table, and the Inspector stands on the outer side. The Inspector places the recorder at the center of the table and says naturally in Mandarin: {This week's observation data has been exported.}
Stage 4: The Archivist picks up the recorder to inspect the data, while the Inspector naturally closes his mouth and waits. At the end, the recorder is only in the Archivist's hands.
Stage 5: The Archivist places the recorder back on the table, and both characters look at the completed status on its screen. End on a medium shot that clearly shows their identities, the number of props, and their positions.

【Maintain Consistency】
Keep both characters' identities and clothing, the recorder's quantity and ownership, the spatial orientation of both scenes, and the speaker relationship consistent.
```
