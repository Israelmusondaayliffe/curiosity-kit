# Long Videos and Time Segments

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

Seedance 2.5 supports videos up to 30 seconds long. The total duration is set through generation parameters; the Prompt is responsible only for organizing events within that duration.

Event time segments explicitly provided by the user are part of the creative content and must be preserved. Parameter separation removes only interface settings such as "generate an N-second video" or "output in a 16:9 aspect ratio." If the user's original numerical time segments conflict with the target total duration on the page or in the API, prioritize preserving event order, relative pacing, and the story outcome, and switch to unnumbered "stages." Preserve the numbers and ask the user to resolve the parameter conflict only when the user explicitly states that the original time segments are hard constraints.

For long videos, prefer "stages." Assign only one major state change to each stage and clearly state its end state:

```text
【Stage 1】
At the start: <initial state>.
Main event: <one main action or event>.
At the end: <observable state>.

【Stage 2】
Continuing from the previous stage: <state that must be maintained>.
Main event: <one main action or event>.
At the end: <observable state>.

【Stage 3】
Main event: <concluding event>.
At the end: <final visual state>.
```

The number of stages is determined by the number of events and may be increased or decreased; it is not fixed at three. When the Prompt is long, prioritize subject mappings, asset roles, events, and end states. Compress repeated style terms, repeated constraints, and inactive assets. Do not impose a fixed word limit.

### Target-Duration Override

When the target duration provided by the generation page or API context is longer than the user's original event timeline, first preserve the characters, event order, causal relationships, and story outcome, and then redistribute the pacing of the existing events. When the target duration is provided only by the page or API, organize the Prompt into stages without numerical timestamps so that the stages collectively cover the narrative capacity of the target duration. Do not create numerical time segments such as `0-8 seconds` or `8-18 seconds` in the Prompt merely to align with that parameter.

You may lengthen only action processes, reactions, pauses, or scene transitions. For example, allow shifts in gaze, changes in breathing, the process of picking something up, and reactions after entering to unfold naturally. Do not add characters, main-plot events, or story outcomes, and do not mechanically fill time with repeated actions or empty shots. The target total duration still must not be written into the Prompt as an interface parameter sentence.

For handoffs, grabs, and placement tasks, state the ownership change of the single object. For example, after handing it over, the original holder no longer has it; at the end, it is only in the recipient's hands.

Use continuous whole-number time segments only when the user has already provided numerical time segments or explicitly requests time-segment control over handoffs, entrances and exits, or beats. When there are fewer events, do not split them merely to reach a segment count. When there are more events, merge secondary events first:

```text
0-5 seconds: <starting state>; <main event>; at the end, <observable state>.
5-10 seconds: Continue from <state> in the previous segment; <main event>; at the end, <observable state>.
10-15 seconds: <concluding event>; at the end, <final state>.
```

When the user requests numerical time segments, the segments must be continuous and non-overlapping. They represent event budgets, not frame-level edit points. Do not claim precision to 0.5 seconds, and do not give an unverified maximum number of time segments. When events are too dense, reduce the number of stages instead of subdividing them further.

The overall output duration is still set through generation parameters. Do not separately write "generate an N-second video."
