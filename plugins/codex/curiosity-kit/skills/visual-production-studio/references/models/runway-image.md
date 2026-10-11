# Runway Gen-4 Image

Evidence checked 9 October 2026. Guide-backed product image prompting. Gen-4 Image and Gen-4 Image Turbo are UI selections; current native API support must be resolved separately. This file is for still images; video I2V uses a different motion-first method.

## Base generation
Use positive visual descriptions: subject, setting, composition, light and visible style. Add details that constrain the picture rather than conversational requests or negative lists. Begin simply, then refine a particular visible attribute. Do not import video instructions that say the source image already establishes the entire appearance into text-to-image creation.

Authored base example: “A red enamel kettle on a brushed steel stove, close-up at counter height. Cool tiled kitchen in the background, steam lit by a narrow shaft of warm morning sun. Muted documentary photograph.”

## References mode
The guide allows up to three references, named reference tags, and conversational instructions. Bind each contribution: subject identity, scene, style or sketch composition. Reuse the actual tag assigned by the UI, not a guessed placeholder. Iterate character and scene separately when combined instructions drift.

Authored instruction after selecting and naming actual references: “Place the character from the character reference in the kitchen from the scene reference. Use the sketch only for camera angle and subject placement; keep the character's face and clothing.” The role labels in this example explain the binding; substitute actual selected UI tags when submitting.

## Sources and limits
[Base prompting guide](https://help.runwayml.com/hc/en-us/articles/35694045317139-Gen-4-Image-Prompting-Guide), [creation guide](https://help.runwayml.com/hc/en-us/articles/37053594806419-Creating-with-Gen-4-Image), [References guide](https://help.runwayml.com/hc/en-us/articles/40042718905875-Creating-with-Gen-4-Image-References): guide bodies reviewed on 2026-10-09; publication dates not established. The reference mode's conversational guidance qualifies the base guide's descriptive style; neither proves output fidelity.
