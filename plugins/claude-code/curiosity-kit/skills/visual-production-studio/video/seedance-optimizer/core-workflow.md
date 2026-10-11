# Core Workflow

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

### 1. Parse the User's Goal

Build a “story contract” from the user's text before inspecting the assets. Extract and lock:

- Subjects and their counts.
- Actions, events, and causal sequence.
- Scene, time, weather, and spatial relationships.
- Prop ownership, transfers, and final states.
- Visual style, camera, sound, dialogue, and subtitle requirements.
- Content the user explicitly requires to preserve or exclude.
- Whether the task is generation, editing, or extension; whether a generation task uses keyframes, a storyboard grid, or a blockout; and whether an editing task modifies only sound.

The story contract defines the factual boundary for all later rewriting. Do not replace, merge, or remove characters or events from the story contract merely because a more visually prominent person, outfit, prop, or scene appears in an asset.

Preserve the semantics of the user's notation. Forms such as `Shot #45`, `Shot No. 45`, and `Shot 45` indicate a shot number by default, not a `45-degree camera angle`. Interpret a number as a camera angle only when the user explicitly writes “45 degrees” or an equivalent photographic angle. Do not rewrite shot numbers, asset numbers, chapter numbers, or step numbers as camera parameters.

Whenever the input includes speech, dialogue, narration, or an audio role, create an internal “dialogue ledger” for every time segment. Record the speaker, whether that person speaks, the exact dialogue, the audio role, the language, and whether the voice is on-screen or off-screen. Do not turn a segment with specified speech or an audio role into silence, and do not swap speakers or audio. If the user explicitly asks a character to speak with assigned audio but provides no dialogue text, or if the current environment cannot transcribe it reliably, preserve that character's role of speaking with the corresponding audio and do not invent specific dialogue.

When the user provides only a quoted dialogue fragment, keyword, or short phrase, treat only that fragment as the exact words that may be spoken. You may add the speaker's expression, actions, and delivery, but do not invent a complete sentence around the fragment. When the user describes only a speaking intention such as “use status to pressure the other person” or “continue arguing” without providing any exact words, do not invent dialogue. Express the intention through observable lip movement, pauses, posture, and the other person's reaction instead.

For example, if the input only says that she should convey status-based pressure when saying “You're an outsider,” the final dialogue may only be `{You're an outsider}`. Do not splice narrative explanations such as “mother-son relationship” or “status-based pressure” into the dialogue, and do not rewrite it as “You're an outsider. What right do you have...” or any other complete sentence.

Create a “required entity list” for the story contract, with a separate slot for every explicitly mentioned person, group, key prop, and scene. Use this list only for internal checks; do not output it to the user. Later, record each slot's narrative role, adopted asset, and observable features, then confirm before output that every slot appears in the Prompt.

Convert internal thoughts into visible actions, expressions, dialogue, or narration, but do not add events that change the story.

For a causal reveal shot in which a character changes expression or behavior only after the cause appears, show the trigger clearly before showing the character's reaction. When the cause and reaction are far apart, establish their relationship with one explicit eyeline or camera shift. When they can share the frame, keep the cause and reaction visible within the same composition. Do not push into a face-only close-up before the audience can clearly see the trigger, and do not show only the reaction close-up while omitting the trigger.

When the story explicitly involves pretending to be injured, simulating an injury, or nearly being injured, clearly preserve an observable uninjured state in any potentially ambiguous shot; for example, keep skin, clothing, and props intact. Do not rewrite a performance or an event that did not occur as a real wound, bleeding, or damage.

### 2. Compile Novels and Long Text

First convert the text into filmable events:

- When the user requests a trailer, overview, or ensemble presentation, choose a montage structure that summarizes the theme.
- When the user requests one scene, preserve the core events that occur continuously within that scene.
- When the user does not specify a scope, choose one causally complete primary event that can work within the target video, and briefly explain the selection outside the Prompt.
- Ask one consolidated question only when multiple mutually exclusive main storylines are equally important and choosing among them would change the core story.

Compress repetitive description and information that cannot be visualized, while preserving character relationships, key dialogue, trigger events, and the ending state.

### 3. Inventory and Understand the Assets

When there are many assets, inspect them in two passes:

1. In the first pass, lightly inventory all assets and identify candidates for people, products, props, scenes, actions, camera movement, pacing, sound, and style.
2. In the second pass, inspect in depth only the assets that match the story, conflict with it, serve as keyframes, or will be used by the current scene.

When inspecting a video, confirm at least the subjects, principal actions, shot changes, start state, and end state. When inspecting audio, confirm at least the sound type, voice quality, language, dialogue content, or intended use as ambient sound.

Distinguish between two kinds of information:

- **Story Assignment**: A character's name, age, and relationships; which event they perform; who owns a prop; and how the story ends. These come from the user's text.
- **Asset Observation**: Facial features, hairstyle, clothing, material, color, spatial layout, actions, camera movement, voice quality, and other features that can be directly seen or heard.

Use assets only to add features that can be observed directly. Do not infer from an asset's appearance or rewrite identities, ages, relationships, or plot points stated in the text. Likewise, do not invent brands, colors, occupations, personalities, or prop functions that cannot be confirmed from the assets.

When the user refers only to a “person” or “subject,” keep that neutral term. Do not relabel the subject as a dancer, actor, worker, or any other identity based on actions, posture, or clothing. Continue using a character name or identity only when the user has provided it.

Forms of address, rank, occupation, and relationships define only narrative slots; do not automatically turn them into appearance or personality traits such as young, old, delicate, or commanding. Include such attributes only when the user's text states them explicitly or the corresponding expression is directly observable in the assets.

For a character asset, describe facial features, hairstyle, clothing, accessories, and directly observable posture by default. Do not replace visible details with summary labels such as “girlish,” “mature,” “delicate,” or “commanding.” When the user explicitly requests these performance directions, rewrite them as expressions, posture, and actions.

The mapping priority is fixed:

```text
User's explicit specification > Prompt description > Asset content > Filename and metadata > Upload order
```

When the user's explicit mapping already covers all required entities, do not activate other available assets that the user did not name. Do not add them as a second person, second scene, or auxiliary reference merely because their content is similar, and do not add unnamed assets to reinforce the same role. Generic background guests, furniture, decor, or environmental elements do not create an asset gap; cover them through the designated scene asset and the text description. Evaluate unnamed assets only when the user explicitly requests selection from all assets, asks to combine multiple references, or a core character, prop, scene, action, or sound explicitly required by the user still lacks a source. List every number that remains inactive by default under `【Unused Assets】` in the Prompt.

Upload order is not semantic evidence of identity or role and should generally be used only to establish stable numbering. Only when the user requests an immediate answer, the candidates are equally reasonable, and the number of slots equals the number of candidates may upload order be used as the final stable tie-breaker: assign candidates one-to-one by the order in which story slots first appear and by asset order. This ordering only makes the assignment deterministic; it does not prove true identity and must not be used to add unconfirmed age, relationships, or personality.

If the input is JSON or long text containing Asset IDs, create the `@ImageN`, `@VideoN`, and `@AudioN` mappings in the order each asset appears in the input, then replace Asset IDs in the text with the corresponding references. The final Prompt must not expose raw Asset IDs.

If there are only local paths and no reference labels, create stable aliases separately by media type and in the order provided by the user, then list each path and alias under “Asset Understanding.” Use those aliases in the final Prompt and remind the downstream workflow to preserve the same upload order.

### 4. Assign Asset Roles and Subject Mappings

Every used asset must have one explicit role:

- Images: character appearance and clothing, product structure and material, props, scene layout, lighting, or keyframes.
- Videos: action, camera movement, pacing, or timeline; or the unique editing master or extension source video.
- Audio: a designated speaker's voice and dialogue, ambient sound, sound effects, or music.

Before creating mappings, check every character, prop, and scene required by the story. Then perform the following steps in order:

1. Take each unassigned character, group, prop, and scene from the required entity list one by one.
2. Review all candidate assets and compare headcount, clothing hierarchy, silhouette, structure, props, and scene role. Do not stop searching after finding the first usable asset.
3. Select the best-matching asset for the current slot, then proceed to the next slot. Different named characters or groups should use different best candidates by default.
4. After mapping is complete, run an omission audit: every required entity must perform exactly one explicit role in the Prompt, and every activated asset must perform only its declared role.
5. Subtract the assigned assets from the complete list of available assets to obtain the unused set. Whenever this set is nonempty, add `【Unused Assets】` after the asset roles in the Prompt, list each unused number by media type, and explicitly state that the assets are not used for people, scenes, props, actions, camera, or sound. Do not explain this only outside the Prompt, and do not replace specific numbers with “other assets.”

Do not merge two named characters into one subject, and do not omit a character merely because that character's asset is less visually prominent. When distinguishable candidate assets are available, do not reuse one asset for multiple named characters or groups. Reuse is allowed only when the asset itself contains those characters together and no better independent candidates exist. When multiple assets jointly define the same entity, state this explicitly. Assets not called for by the story may be left unused.

In the final asset roles, each line must define only one subject, group, prop, or scene and its primary reference asset. Do not compress multiple subjects and assets into one range mapping, such as “Character A and Character B reference @Image1 and @Image2.” Split it into “Character A references @Image1” and “Character B references @Image2.”

If two core identities have no appearance clues in the text and the candidate assets are equally reasonable, do not pretend that a hidden answer can be inferred from the images. Ask one consolidated question according to “Handle Mapping Confidence.” If the user requests an immediate answer based on reasonable assumptions, use the stable tie-breaker above for a conservative one-to-one mapping and avoid adding unconfirmed distinctions such as age or personality.

When one subject has multiple references, state the view or attribute contributed by each asset and declare that they jointly define one entity rather than generating multiple copies.

Bind different subjects one by one, for example:

```text
<Character A> maps to @Image1; use only facial features, hairstyle, and clothing.
<Character B> maps to @Image2; use only facial features, hairstyle, and clothing.
<Prop A> maps to @Image3; use only structure, material, and color.
<Scene A> references @Image4; use only spatial layout, architecture, and lighting, and do not use the people in the image.

【Unused Assets】
@Image5 and @Image6 do not participate in this task and are not used for people, scenes, props, actions, or camera.
@Audio2 does not participate in this task and is not used for dialogue, voice quality, ambient sound, sound effects, or music.
```

Do not replace one-to-one mappings for multiple characters with a single range statement.

When the role of a reference video is unspecified, choose the dimensions relevant to the task from action, camera movement, pacing, scene, and sound. In a generation task, do not inherit character identity, clothing, or the entire scene from a reference video by default. When the reference video already provides the action, camera movement, and sequence accurately, state only which dimensions to inherit; there is no need to restate every action, as repetitive rewriting may conflict with the asset itself.

When written dialogue conflicts with the content of reference audio, use the user's text to determine the dialogue. By default, the audio provides only voice quality, accent, speaking rate, and emotion. The exception is when the user explicitly asks to reuse the dialogue in the audio.

When multiple references for the same subject conflict, follow the user's explicit specification first. If the user has not specified, assign appearance, clothing, structure, or material to the most suitable asset based on clarity and story fit. Clarify only when the core identity remains indeterminate.

### 5. Handle Mapping Confidence

- **High confidence**: Map automatically and continue.
- **Medium confidence**: Use the most reasonable mapping and disclose the key assumption outside the Prompt under “Asset Understanding.”
- **Low confidence, but no effect on the core result**: Do not use the asset and do not ask the user.
- **Low confidence, and affects core identity, count, prop ownership, front/back or left/right, facing direction, editing target, unique master, extension direction, or keyframe role**: Consolidate all related ambiguity into one brief question.

If an explicit user mapping clearly conflicts with the asset content, still follow the user's mapping. Confirm once only when the conflict is almost certain to produce an incorrect result.

Do not interrupt the user over missing style, lighting, routine camera movement, image quality, or anything else that can be resolved conservatively from context.

When clarification is necessary, ask only one consolidated question and stop to wait. Do not simultaneously output a provisional Prompt that might mislead downstream submission. Continue from mapping and task routing after the user responds. Only when the user explicitly requests a version based on reasonable assumptions may you proceed with assumptions and disclose them outside the Prompt.

If the user provides only assets without any generation, editing, or extension goal, ask once for the minimum creative objective. Do not invent a story from the asset content.

### 6. Select One Primary Task

#### Aspect Ratio and Duration Compatibility Gate

Run this gate proactively while parsing the user's original Prompt and before constructing any API request. Do not wait for an API error, and do not rely on `TaskTypeConstraint` before adding the declaration. First read the reference video's actual aspect ratio and duration, then compare them with the user's explicitly requested target output specifications:

- If the target aspect ratio differs from the reference video, do not classify the task as video editing; handle it as regular video generation.
- If the target duration differs from the reference video by more than approximately 0.3 seconds, do not classify the task as video editing. When the user explicitly asks to continue the video before or after the original, handle it as video extension; handle other duration changes as regular video generation.
- If a reference video has been provided but its specifications cannot be read, or the user asks to reference the original video without providing it, first determine the task from the explicit intent in the original Prompt. If the user clearly requests a relative change such as “landscape to portrait,” “portrait to landscape,” “shorten it to 8 seconds,” “change it to 20 seconds,” or “expand it to 20 seconds” without an extension direction, conservatively determine that there is an aspect ratio or target total duration conflict, avoid video editing, and handle the task as regular video generation. When the user provides only a target ratio or duration without expressing a relative change, do not claim that a conflict has been confirmed. Explicit extension intent such as “extend before,” “extend after,” or “continue” must still be handled as video extension.
- Classify the task as video editing only when the target aspect ratio and approximate duration match the reference video or are both unspecified, and the user asks to modify a specific object, region, or sound in the original video.

Verbs such as “convert,” “adjust,” “modify,” “change to,” and “reconstruct” do not by themselves constitute video editing. Do not trigger the declaration solely because the original Prompt uses words such as “convert,” “adjust,” “modify,” or “keep unchanged.” When incompatible specifications route the task to regular video generation, use the reference video only as a reference for content, characters, scenes, actions, timing, camera, and sound. Treat aspect ratio and total duration only as page or API parameters. Do not use phrases such as “edit,” “modify,” or “convert the original video” in the final Prompt, and do not promise exact frame-level or pixel-level consistency.

Only when the aspect ratio or duration conflict above is confirmed or conservatively determined may the optimized final Prompt proactively include this complete sentence: `Please note that this is not video editing.` In a structured Prompt, place this sentence immediately after the goal sentence under `【Generation Goal】`, without starting a new paragraph. This is a routing-disambiguation declaration, not a negative constraint on visual content. Do not add it to genuine video editing, video extension, first-frame or first-and-last-frame generation, or regular generation tasks without a specification conflict. If the user already wrote the same or an equivalent declaration, keep it only once and do not repeat it.

For example, `Convert Video1 into a 9:16 vertical frame, keeping the original content completely unchanged and adjusting only the frame composition` should be classified as regular video generation. Video1 serves only as a reference, while 9:16 is set as a generation parameter.

Placement example:

```text
【Generation Goal】
Generate a video using @Video1 as the complete content reference, keeping the original content unchanged and only adapting the composition. Please note that this is not video editing.

【Reference Asset Roles】
@Video1 is used as a reference for visible subjects, scenes, actions, event timing, camera, and sound.

【Event Script】
Preserve the complete event sequence, motion paths, shot changes, and start and end states from @Video1. Do not add, remove, or rewrite any original event.

【Maintain Consistency】
Keep the visible subjects and their count, scene, props, spatial relationships, action order, relationship between camera and sound, and outcome state consistent with @Video1. Adjust only the composition.
```

Set the target aspect ratio through the page or API parameters; do not write it into the final Prompt.

Choose exactly one of the three primary tasks. First determine whether the user wants to modify an existing video, then whether the user wants to add new content before or after an existing video; only otherwise choose generation:

1. **Video Editing**: Use one original video as the unique master and modify only the specified object, region, or sound.
2. **Video Extension**: Generate a new continuous segment before or after the original video without rewriting the original segment.
3. **Video Generation**: Generate a new video from text and optional reference assets.

Multi-asset inputs, long-form video, time ranges, keyframes, storyboard grids, blockouts, sound, emotion, and cinematography are composable modules, not additional primary tasks. When a blockout video is re-rendered as a reference for action, space, or complete structure, the task is video generation; the mere presence of a video input does not automatically route it to video editing.

When the user asks both to edit the original video and extend it, do not discard either operation and do not force them into one Prompt:

- If the replacement content must continue from the original video into the new segment, edit the original video first to produce a new master, then extend the newly edited master.
- If a new subject appears only in the extension and the original video is not modified, perform only the extension and describe the new asset as a reference for the extended segment.
- If multiple operation orders remain equally valid, ask one consolidated question.

When two sequential operations are clearly required, output a two-step execution Prompt. These are consecutive steps in one task, not alternative versions.

### 7. Apply Task Parameter Rules

Use these rules only for planning and guidance; do not write them into the final Prompt:

- **Regular Video Generation**: Set aspect ratio and total duration on the page or through the API. They may guide composition and event density.
- **Video Editing**: Video editing automatically locks the input video's aspect ratio and approximate duration, so neither can be set separately. Because of input-frame processing, the output duration may differ from the original video by up to approximately 0.3 seconds.
- **First-Frame or First-and-Last-Frame Generation**: The first image's aspect ratio locks the output ratio, while duration remains configurable. The first and last images should have the same aspect ratio. When the current Agent can read the images, verify this proactively; when it cannot, do not pretend that it has.
- **Video Extension**: Video extension automatically locks the input video's aspect ratio, while the extension duration remains configurable.

When the user requests a parameter that the selected task locks automatically, do not ask about it, write it into the Prompt, or use it for incorrect planning. Still output the best Prompt first, then append at most one `Parameter Note:` after the main body. When the first and last images have different aspect ratios, likewise use one parameter note explaining that they should be adjusted to the same ratio before submission to avoid stretching the last frame. Output no parameter note when there is no conflict.

### 8. Apply the Template and Clean the Prompt

Choose the corresponding template below and retain only the sections needed for the current task. Replace every `<placeholder>` with concrete content. Do not leave template instructions in the final Prompt.

After completing the Prompt, perform the “Final Self-Check,” then deliver it according to the “Output Contract.”
