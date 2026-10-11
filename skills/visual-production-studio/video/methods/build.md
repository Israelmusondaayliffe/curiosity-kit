# Build a video prompt

Use for a new brief, from a quiet single shot to a multi-shot sequence. For existing media motion use [animate](animate.md); for a source breakdown use [remix](remix.md). The [common contract](../../references/contract.md) governs fidelity and execution. No production route JSON or renderer is required for prompt-only work.

## Compose the visual event

1. Extract the subject or product, intended action, setting, medium, mood, duration if given, framing/aspect, exact copy/dialogue, references and forbidden changes. Do not invent a brand claim. If the core subject or requested deliverable is unknowable, ask one focused question; make ordinary unlocked creative choices directly.
2. Resolve a named model/version/surface through its [profile](../../references/models/index.md). If none is named, compose model-neutral direction. Native reference tags, audio fields, seed controls and clip limits require selected-surface evidence. A request for an image prompt stops at its still-image deliverable.
3. Choose one shot or a sequence from the actual brief. Define a visible beginning, meaningful action and ending state. A one-take needs a traversable camera/subject path and visible spatial handoffs; a montage needs intentional cuts. Do not combine incompatible no-cut and hard-cut directions without resolving the brief.
4. Write the visual event first. Tie camera angle, lens character, motion speed, subject movement, light and atmosphere to observable results. State what remains still. Limit simultaneous actions when they compete for a short clip. Use photographic language only for a photographic/cinematic medium.
5. For a multi-shot sequence, map shot duration and transition out/in. Carry identity and wardrobe only where the subject appears. Track props, geography, screen direction and light development across cuts. An intentional cutaway is valid. If timings are explicit, cover the requested duration without accidental gap or overlap; sparse keyframes need not acquire invented timestamp blocks.
6. Specify sound when requested or materially relevant: dialogue verbatim, speaker binding, ambience, music cue, effects or deliberate silence. A surface without audio can receive a separate sound plan, clearly outside native generation. Do not insert music into a silent request.
7. Convert the completed creative direction into the selected model's useful syntax. One native staged request remains one complete prompt; independent submissions each get a complete prompt. Preserve exact supplied reference identifiers and controls. Include brief compatibility notes outside prompt text only when needed.

## Optional depth

For a full effects-led treatment, use the selected portions of [effects vocabulary](../builder/references/effects-vocabulary.md), [creative principles](../builder/references/creative-principles.md) and [genre templates](../builder/assets/build-templates.md). Produce a shot plan, effects inventory with shot/count references, density rhythm and energy arc when those artifacts help the requested treatment. A signature moment is useful only when it serves this concept. Quiet footage may stay low-density throughout; no mandatory three-act arc, contrast quota or 1–4 second shot length applies.

For a named Seedance four-beat treatment or optimizer use [Seedance](seedance.md), retaining its detailed selectable recipes. For camera/physics risk read the relevant [failure patterns](../builder/references/ai-video-failure-modes.md) and [continuity language](../builder/references/consistency-constraints.md); do not load all style/effect libraries by default.

## Finish and recover

Compare the prompt to the original locks, selected model, output count, duration, references and format. Every effect must be visually intelligible; transitions should preserve the intended causal/spatial relationship. Remove synonymous repeated obligations while preserving all distinct requirements. A saved timed pack can use `python3 video/builder/scripts/validate_video_prompt.py FILE`; its result is structural advice, not provider compatibility or visual proof.

If the brief is overloaded, simplify unlocked motion or propose multiple submissions without silently changing requested duration/count. If a feature is unavailable, retain the target and explain the specific limitation before proposing an alternative. Deliver the finished prompt(s); do not start generation from a prompt-only request.
