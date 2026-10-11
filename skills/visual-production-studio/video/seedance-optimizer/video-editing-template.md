# Video Editing Template

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

An editing task must define one source video as the sole editing master. It cannot merely describe the target visuals and thereby turn into a regeneration task.

For visual edits, first inventory every category of visible subject in the source video, including user-named and unnamed characters, real people, models, animals, props, foreground objects, and background subjects. Explicitly specify whether each category is to be replaced, removed, or kept unchanged. Do not overlook real people, models, props, or background subjects that the user did not name. Objects the user has not requested to modify remain unchanged by default. Include an entire group in the removal or replacement scope only when the user explicitly requests replacing the whole group or asks that the target video retain only specified objects.

If the current Agent cannot view the entire source video or has access only to sparse previews, it must not claim to have exhaustively inventoried every object. After explicitly stating all user-specified replacements, removals, and preserved objects, add this fallback sentence: `Except for the objects explicitly modified above, all other visible characters, props, and background elements in @Video1 remain unchanged and are not to be replaced or removed.` If the user explicitly requests that the target video retain only specified objects, replace this fallback with an instruction to remove all remaining objects as requested.

Every video-editing Prompt must include one of the following two scope-closure statements. The scope closure must not be omitted:

- Local modification: `Except for the objects explicitly modified above, all other visible characters, props, and background elements in @Video1 remain unchanged and are not to be replaced or removed.`
- The user explicitly requests retaining only the target objects: `Except for the objects explicitly retained above, remove all other visible subjects from @Video1; do not add any unspecified objects.`

The source-video subject inventory determines only which objects are replaced, removed, or preserved; it must not be used to change the target asset set already specified by the user. If the user has explicitly assigned @Image3 to an edit object, do not add an unnamed image as an appearance, clothing, group, or auxiliary reference for that object, even if the other image is clearer or contains similar content. Continue to list those assets in `【Unused Assets】`.

```text
【Editing Goal】
Edit @Video1, changing only <original object or region> to <target content>.

【Role of the Source Video】
@Video1 is the sole editing master and governs the original scene, camera position, camera movement, action trajectories, occlusion relationships, and event order.

【Role of the Target Material】
@Image1 is used for the <appearance, structure, or material> of <the target subject, background, or product>; do not use <irrelevant background, characters, or composition>.

【Edit Objects and Scope】
Modify only <explicit objects and regions>. The number of target objects throughout the video is <count>. Do not modify <content that must be preserved>.
Except for the objects explicitly modified above, all other visible characters, props, and background elements in @Video1 remain unchanged and are not to be replaced or removed.

【Timeline Inheritance】
<Target object> inherits the timing, duration, path, and speed changes of every appearance, movement, occlusion, and exit of <original object>.
All other character actions, camera movement, shot changes, and event order remain as in @Video1.
```

When replacing a subject, specify the original and target subjects. When replacing a background, make clear that only the background outside the subject's outline changes. For a local edit, specify the region, attribute, and content to preserve. When adding or removing an object, state its quantity, position, appearance timing, and affected scope.

Completed example of dynamic-subject replacement:

```text
【Editing Goal】
Edit @Video1, replacing only the red bicycle and its rider passing in front of the bench with the dark-gray electric patrol vehicle from @Image1.

【Role of the Source Video】
@Video1 is the sole editing master and governs the park road, the two people on the bench, the camera position, camera movement, the original rider's motion slot, occlusion relationships, and event order.

【Role of the Target Material】
@Image1 is used only for the body structure, color, and transparent windshield of the dark-gray electric patrol vehicle; do not use the image background or driver.

【Edit Objects and Scope】
Remove the red bicycle and its rider from the source video. There must be exactly one electric patrol vehicle throughout the video. The two people on the bench, the trees, the road, and the background remain as in @Video1.

【Timeline Inheritance】
The electric patrol vehicle fills the original rider's motion slot with exactly the same appearance timing, movement path, speed, and occlusion positions. The red bicycle and rider must no longer appear in the final video. All other character actions, camera movement, shot changes, and event order remain as in @Video1.
```

For cross-category dynamic-subject replacement, prefer "motion-slot replacement": explicitly remove the original subject, have the target subject inherit the original subject's exact appearance timing, movement path, speed, and occlusion positions, and state that the original subject no longer appears in the final video. The preservation list should include only areas adjacent to the target that genuinely cannot change. Avoid diluting the editing goal with an overly long list.

```text
Remove <original moving subject> that passes in front of <foreground subject> in @Video1, and replace it with <target moving subject> defined by @Image1 at exactly the same appearance timing, movement path, speed, and occlusion positions. <Original moving subject> must no longer appear in the final video.
```

Use the global master-inheritance requirement by default. Add a small number of observable event conditions only when grabs, handoffs, placements, or entrances and exits in the source video can be observed accurately:

```text
Only after <observable completion state of Event A> occurs may <Event B> begin.
Only after <observable completion state of Event B> occurs may <Event C> begin.
```

Do not rewrite the source video into time segments from memory, and do not invent event conditions from incomplete frame samples. A Prompt can increase the probability that key events follow the original timeline, but it cannot guarantee frame-by-frame alignment after editing.

### Audio Editing

When modifying only dialogue, language, voice timbre, background music, ambience, or action sound effects, still define the source video as the sole editing master. Specify separately the speaker or sound category to modify, the target change, the time range, and whether all other audio and all visuals remain unchanged. Do not redesign character actions, lip-sync timing, shots, or editing rhythm because of an audio edit.

```text
【Editing Goal】
Edit @Video1, applying <removal, replacement, or adjustment> only to <speaker or sound category> in <the entire video or an explicit time segment>.

【Role of the Source Video】
@Video1 is the sole editing master and governs the original visuals, character actions, lip-sync timing, shots, editing rhythm, all other audio, and event order.

【Role of the Target Audio】
@Audio1 is used for the <voice timbre, dialogue, ambience, sound effects, or music> of <target speaker or sound category>; do not use <irrelevant audio>.

【Audio Edit Scope】
Modify only <explicit speaker, sound category, or time segment>.

【Content to Preserve】
Keep <all other dialogue, lip-sync timing, ambience, action sound effects, visuals, shots, and editing rhythm> from @Video1 unchanged.
```

When the user asks only to remove the original background music, do not fabricate a target audio material. State directly that the background music is to be removed while character dialogue, lip-sync, ambience, action sound effects, and all visuals are preserved. When changing the dialogue language or voice timbre, preserve the dialogue content and speaking times from the source video by default unless the user explicitly requests rewriting them as well.
