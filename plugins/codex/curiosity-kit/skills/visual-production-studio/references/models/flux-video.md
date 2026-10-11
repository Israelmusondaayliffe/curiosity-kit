# FLUX 3 Video

Evidence checked 9 October 2026. Official mode and prompting guides reviewed. Keep FLUX 3 Video separate from FLUX 3 Image. Availability, dimensions and quality remain endpoint/account-dependent, not measured here.

## Select the operation before writing
- Text-to-video: establish the shot's visible world, then action, camera, progression and intended sound.
- Image-to-video: the image establishes appearance; describe its motion and camera progression without contradicting it.
- Keyframes: bind the actual ordered/time-indexed image inputs. Describe a continuous transition between them; prose labels do not supply hard frame inputs.
- Continuation: supply the actual start_video input, then describe the new segment and boundary motion. Do not re-create the whole source as a fresh shot.
- Video edit: use the separate editing tool endpoint, not generation mode. Its schema rejects generation-mode fields. Name the target change; preserve timing and performance unless a supported requested edit changes them.

## Authored examples, not output tests
I2V: “The paper sailboat drifts slowly toward camera; small ripples spread from its bow. The camera gently retreats at the same pace, keeping the boat centered.”
Continuation: “Continue the boat's forward drift from the source ending. It passes beneath the low branch and emerges into the sunlight; maintain the same water-level camera and movement direction.”
Edit: “Replace the ceramic mug on the table with a clear glass, maintaining the actor's grip and contact with the tabletop.” Contact surfaces help constrain a relocation/replacement. For dialogue changes, preserve exact approved words and fit them to the existing speaking window; flag impossible timing rather than silently rewriting.

## Controls and limits
Draft-to-enhance lineage is a distinct workflow. High-resolution classes use upsampling, and delivered dimensions can differ from conventional broadcast sizes. Older overview omissions do not override newer mode documentation. Omni Reference is marked coming soon, not an active route. Native audio and keyframe availability must be selected through actual supported inputs. For sequential edits, use the selected previous result as the next source and inspect accumulated drift.

## Sources
[Overview](https://docs.bfl.ai/flux_3/flux3_overview), [earlier help overview](https://help.bfl.ai/articles/7342522296-what-is-flux-3): official overview bodies reviewed. [Video modes](https://docs.bfl.ai/flux_3/flux3_video): mode/control/use-case sections reviewed. [Video prompting](https://docs.bfl.ai/guides/prompting_video_overview), [editing guide](https://docs.bfl.ai/guides/prompting_video_editing): full substantive text reviewed. [Edit endpoint](https://docs.bfl.ai/flux_tools/flux_video_edit): operation restrictions reviewed. Publication dates not established; accessed 2026-10-09. Voice/text fidelity statements are vendor claims requiring review.
