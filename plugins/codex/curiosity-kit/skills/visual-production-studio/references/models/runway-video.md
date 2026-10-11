# Runway — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## Gen-4, Gen-4 Turbo

Surface: Runway app; Turbo API separately cataloged

### Status
Original Gen-4 guide marked older; preserve its authoring branch

### Source preservation
Explicit Stage-2 Gen-4 and generic I2V template

### Model ids
gen4_turbo

### Modes
I2V

### Prompt
Image supplies appearance; prompt motion with simple positive language. Use positional subject labels, a coherent scene and one-variable iteration; avoid negatives and repeating image detail.

### Controls
- Duration: 5/10s
- Prompt: 1000 characters
- Aspect: 16:9,9:16,1:1,4:3,3:4,21:9
- Fps: 24
- Seed: Fixed seed gives similar motion, not exact guarantee
- Resolution: 4K upscale is separate

### Cautions
T2V and newer Gen-4.5 controls must not be attributed to Gen-4. Audio/performance tools are distinct.

### Primary evidence
- [Runway Gen-4 prompting](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide). primary guide body opened Publication/update: not established. Access: 2026-10-09.
- [Creating with Runway Gen-4](https://help.runwayml.com/hc/en-us/articles/37327109429011-Creating-with-Gen-4-Video). primary guide body opened Publication/update: not established. Access: 2026-10-09.
- [Runway available models](https://docs.dev.runwayml.com/guides/models/). primary catalog body opened Publication/update: not established. Access: 2026-10-09.

## Gen-4.5

Surface: Runway app/API

### Status
Current catalog

### Source preservation
Current expansion

### Model ids
gen4.5

### Modes
T2V; I2V

### Prompt
T2V needs visual setting plus motion; I2V emphasizes what changes. Natural sequencing or timestamps must fit available screen time.

### Controls
- Duration: 2–10s
- Resolution: App720p
- Fps: 24/25
- Aspect: App T2V table16:9; I2V six conventional ratios
- Seed: Not established by inspected app guide
- Audio: Not established as native

### Cautions
Professional output/upscale controls are separate from base native generation.

### Primary evidence
- [Creating with Runway Gen-4.5](https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5). primary guide body opened Publication/update: not established. Access: 2026-10-09.
- [Runway text-to-video prompting](https://help.runwayml.com/hc/en-us/articles/42460036199443-Text-to-Video-Prompting-Guide). primary guide body opened Publication/update: not established. Access: 2026-10-09.
- [Runway available models](https://docs.dev.runwayml.com/guides/models/). primary catalog body opened Publication/update: not established. Access: 2026-10-09.

## Aleph2.0, Act-Two, Characters

Surface: Runway apps/API catalog

### Status
Documented; Characters only catalog-level coverage

### Source preservation
Current editing/performance expansion

### Model ids
aleph2; act_two; gwm1_avatars

### Modes
Aleph in-context video edit; Act-Two driving-performance transfer; Characters talking-avatar

### Prompt
Aleph: short edit description on a representative keyframe; optional reference image, optional extra motion only when needed. Act-Two: driving performance plus character image/video, rather than a T2V prompt.

### Controls
- Aleph: Source longer than 2s and shorter than 30s; 480–1080p, 24–30 fps, ≤10 cuts; Single Edit available, Multi-edit/Expand coming soon
- Act two: Up to 30s, 24 fps; gestures with character image, not character-video input

### Cautions
Do not expose planned Aleph modes as active. Characters API prompting guide not deeply inspected.

### Primary evidence
- [Runway Edit Studio](https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio). primary guide body opened Publication/update: not established. Access: 2026-10-09.
- [Runway Act-Two performance capture](https://help.runwayml.com/hc/en-us/articles/42311337895827-Performance-Capture-with-Act-Two). primary guide body opened Publication/update: not established. Access: 2026-10-09.
- [Runway available models](https://docs.dev.runwayml.com/guides/models/). primary catalog body opened Publication/update: not established. Access: 2026-10-09.


## Different prompts for different Runway operations

Authored Gen-4 I2V: “The dancer slowly raises both arms and turns toward the window. The camera makes a gentle push-in.” Keep the supplied frame's appearance; this motion-first prompt uses positive language and a feasible action chain. Do not add a generic negative block or call Gen-4 a text-to-video model.

For Gen-4.5 T2V, establish the missing scene: “A dancer in a loose white shirt stands in an empty sunlit studio. She raises both arms and turns toward the window as the camera gently pushes in.” Keep the exact selected version and fit changes to available duration.

For Aleph2.0, a representative-keyframe edit can say “Replace the painted wall with exposed red brick; preserve the dancer and her performance.” Act-Two instead requires an actual driving performance and character input; a textual acting description does not replace recorded performance. Characters remains catalog-only for detailed prompting. The Seedance model exposed through Runway is a wrapper with its own fields, not authority to add its seed control to BytePlus native Seedance.

Retain the original storyboard-to-sequence, mood-reference and adjacent Story Panels comparison patterns. Select a real clean opening frame for each I2V submission; a structural storyboard grid is not automatically a suitable input frame and must not be rendered as tiled footage by accident.
