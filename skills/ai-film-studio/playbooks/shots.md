# Shots and complete prompts

## Turn the scene into coverage

Read the scene and current bible. Preserve the agreed ending, exact dialogue and active states. Choose the least coverage that makes the changing information legible: an establishing relationship, a consequential action, the person receiving it, and the image that ends the scene. These are functions, not four mandatory shots.

The default scene opening briefly establishes geography, often around one second. A close-up opening or an audio bridge can be a declared artistic choice. Do not impose a wide that contradicts the approved scene. Each cut must preserve positions, eyelines, light and prop ownership or visibly explain their change. Establish a new camera side before crossing an axis. A threshold transition should show the boundary and a motivated change in light rather than a meaningless flourish.

For each shot, write:

- its dramatic purpose and relationship to adjacent shots;
- active asset IDs, current versions and reference roles;
- first-frame occupancy, facing, gaze, landmark-relative positions and prop contact;
- a continuous take or explicit cut sequence;
- framing/optics chosen for the visible result, then camera movement serving the action;
- feasible timed beats with visible end states;
- physics, main light, exact audio, performance and style;
- a short positive constraint for each known failure risk.

Complex action can begin already in progress when that removes an uncontrollable setup. Break a shot when motion, dialogue, handoffs and camera demands compete. Keep about three short sentences per beat; use several beats when the action needs them. Preserve user timing and label estimated timing. The script checks intervals; the filmmaker still checks whether a human could do the action in that time.

For handheld work, describe a physical operator: stance, breathing, a weight shift, the step that follows the subject, and settling after that step. Match the motion to the operator's position and the scene's purpose. Generic digital jitter does not establish handheld movement; a smooth supported move is a different choice.

Prior audio can explain a character's current reaction without being spoken again. Label it as prior audio context in the working notes and translate its effect into present behaviour. Keep it out of the current quoted dialogue ledger and SOUND block unless the director explicitly requests an audible carryover; then mark the actual bridge and timing. Do not let remembered dialogue become a new line or an invented offscreen voice.

## Compile the project formula

Read [formula.md](../references/formula.md) and [cli.md](../references/cli.md). Fill the project input from the actual scene, not from the example's story. Then run compile and check as documented. Deliver the emitted scene, shotlist and complete prompt text. The compiler is a renderer of authored decisions; it does not write a scene or inspect a reference for you.

The project formula owns block order and exact constants. Asset descriptors, approved voice wording, scene geography and style are inserted consistently. Reference roles are explicit; the location inheritance exclusion stays attached to the location. Each shot is self-contained rather than relying on a prior generated clip.

Use the generic target when no provider-specific format is requested. Honor an explicit target. A dated target profile supplies formatting conventions only; inspect its source/date and limits. If the target is unsupported, provide a complete generic draft clearly labeled as such and name the missing target information. Do not silently label generic text as a tested provider prompt.

Before live use, check the real service's available mode, reference labels/slots, duration, aspect ratio, audio, editing controls and cost. Put UI controls in the service's actual controls rather than inventing prompt switches. Never infer access from a model name. No personal sibling is required to construct the prompt.

## Check the actual result

Run the checker on output files. Then inspect them directly for story purpose, usable coverage, physical timing, contradictory spatial or lighting prose, voice/speaker fidelity and reference leakage. A file hash cannot establish those judgments. Compare all emitted dialogue against the approved lines, including fragments and language.

If compilation fails, fix the declared input or obtain the missing decision. If file checking fails, distinguish an edited prompt from a changed approved source. Preserve manual work before replacement. A necessary formula exception must be a disclosed project/target decision, not an after-the-fact exemption made to pass.

For image prompts and edit/extension tasks, use [prompt-modes.md](../references/prompt-modes.md). The structured compiler covers scene-shot generation. Mode-specific prose outputs still require a full preservation/continuity review; do not claim the compiler exercised a mode it does not implement.
