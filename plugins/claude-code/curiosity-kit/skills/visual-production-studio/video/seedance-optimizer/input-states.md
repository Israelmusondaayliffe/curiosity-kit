# Input States

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

Determine which of the following states the input falls into before processing its content.

### Text-to-Video Only

The user provides no assets, and the text does not express a need to reference a particular person, product, scene, action, camera movement, or sound. Directly extract the subject, event, scene, visual treatment, camera, and sound, then apply the video generation template. Do not invent asset numbers or suggest that the user provide assets.

### References Needed but Assets Not Provided

Preserve every asset reference already written in the user's original Prompt exactly as provided, including `@ImageN`, `@VideoN`, `@AudioN`, or equivalent labels in the runtime environment. Do not delete them, renumber them, or rewrite the request as generation without references. The fact that the corresponding assets are not attached to the current message or cannot be read by the current Agent must not alter the reference relationships.

Continue optimizing the Prompt normally from the user's original text while preserving its task organization, asset roles, and reference relationships. Do not claim to have inspected the assets, and do not add details that could only be confirmed by inspecting them. If the user did not write any asset references, do not invent them.

Assets that are not attached or cannot be read only limit which facts can be confirmed; they do not block Prompt optimization or require a warning that prevents useful text optimization. State an unverified attachment boundary when it materially affects use. Still evaluate aspect ratio and duration intent using the “Aspect Ratio and Duration Compatibility Gate.”

### Assets Are Readable

Actively inspect the images, videos, and audio provided by the user. Inventory all assets first, then map them in conjunction with the Prompt. Do not guess from filenames alone, and do not force every asset into the Prompt.

### Current Agent Cannot Read the Assets

If the user provides an attachment, path, or URL that the current runtime cannot access, continue optimizing according to “References Needed but Assets Not Provided”: preserve the user's existing asset references, use only information that can be confirmed from the text, do not pretend to have inspected the assets, and do not append a missing-asset warning or a suggestion to provide them.

For damaged or unreadable assets, likewise preserve any reference relationships already written by the user. Do not infer appearance, voice, or content from a filename, path, or URL.

### Asset Specification Preflight

First distinguish hard input limits from stability recommendations:

- Up to 30 images, with each image no larger than 4K.
- Up to 10 videos, with a combined duration of no more than 30 seconds.
- Up to 10 audio clips, with a combined duration of no more than 30 seconds.
- Up to 50 total reference assets across images, videos, and audio.

Recommended ranges are not hard limits. Subject images generally work best with 1 to 8 subjects; subject audio and video generally work best with 1 to 5 subjects and clips of 5 to 10 seconds each; video editing generally works best with an original video of no more than 20 seconds and 1 to 5 reference images. If the input exceeds the recommended range but remains within the hard input limits, continue optimizing rather than blocking because there are many assets. Reduce cross-contamination by assigning a role to every asset, mapping each subject, and activating assets by scene.

When the input exceeds the hard limits, prioritize assets explicitly specified by the user, assets needed to cover required entities, the unique editing master or extension source video, and key action, sound, and boundary-frame assets. Leave all other assets out of the Prompt, then add one `Asset Note:` after the main body explaining that the asset set must be reduced before submission. Do not claim that the input limits can be bypassed through Prompt wording alone.
