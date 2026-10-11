# xAI / SpaceXAI: Grok text and Realtime

Checked 2026-10-09 UTC. Documentary guidance; no account/model call. The official [2026-02-02 announcement](https://x.ai/news/xai-joins-spacex) states SpaceX acquired xAI; the page footer uses SpaceXAI LLC. This verifies the naming relationship, not unspecified legal or technical arrangements.

## Grok 4.7 text/API branch

The [catalog](https://docs.x.ai/developers/models), dated 2026-09-21, lists Grok 4.7 as the primary code/chat model with image input. The [Grok 4.7 guide](https://docs.x.ai/developers/grok-4-7), updated 2026-10-05, favors Responses, preserved encrypted reasoning and stable routing for caching. "Grok 4.7 Fast" is the same model on faster infrastructure in Cursor/Grok Build, not a public API model ID. Preserve dated IDs when reproducibility requires them; do not infer alias immutability.

There is no located separate general text-prompt cookbook beyond model/capability guidance. Use explicit objectives, sources, tools and completion criteria. Current facts require actual retrieval; do not assume native real-time knowledge. Original adjustment:

> Compare the two current release notes using the available search tool. Separate announced changes from verified shipped behavior. Give each material claim a source and date. If release status cannot be established, mark it unresolved rather than inferring from the version number.

For a long tool loop, checkpoint task state and use supported compaction. A readable summary does not replace required encrypted state.

## Configuration and migration

[Reasoning](https://docs.x.ai/developers/model-capabilities/text/reasoning), updated 2026-09-29: 4.7/4.6 use low/medium/high/xhigh, default high, without reasoning-off. 4.5 maps xhigh to high. Historical `grok-4.20-multi-agent` uses effort to alter agent count, not an equivalent depth knob. Reasoning requests reject presence/frequency penalties and stop. Responses supplies encrypted reasoning for replay; Chat Completions has no ciphertext field. Summaries differ from replay state.

[Responses migration](https://docs.x.ai/developers/model-capabilities/text/comparison), updated 2026-09-29: Responses uses input and typed output items, stored continuation and built-ins. Legacy Chat Completions uses client history and function calls only. Replace parsing and state handling, not just the model string. Preserve complete outputs and permitted state unchanged; never request private reasoning text as a workaround.

[Function calling](https://docs.x.ai/developers/tools/function-calling), updated 2026-09-29: built-ins execute server-side; custom functions return for client execution. Auto/required/none/named selection and default parallel calls are documented. Return every result with its matching identity or disable parallelism. A generated call is not proof execution succeeded. Object-root or supported object-variant argument schemas still need permission and value validation before side effects.

[Structured outputs](https://docs.x.ai/developers/model-capabilities/text/structured-outputs), updated 2026-09-29: tool arguments use implicit strict handling, unlike Meta's default false. Some accepted constraints are best effort; oneOf behaves as anyOf and references cannot be circular. Tools plus structured output require a supported Grok 4-family model. Check conditional/size/value constraints in application validation. Schema-valid truncated/refused output is not a successful task.

## Realtime voice branch

Use the [speech-to-speech prompting guide](https://docs.x.ai/developers/model-capabilities/audio/speech-to-speech/prompting-guide), dated 2026-08-17, only for the matching Realtime session. It recommends second-person system instructions organized by role, objective, conversation flow, guardrails and speech style. Specify unclear-input behavior, language, actual tool names, escalation and how numbers should be spoken. Text instructions shape words, not guaranteed vocal acoustics.

Original example:

> You help the caller check an order. Ask for one missing detail at a time. If you cannot hear an identifier clearly, ask them to repeat it. Read the final four characters back before using the lookup tool. Explain a lookup failure briefly and do not claim the order was changed.

The lookup tool must actually exist and be authorized. Transport, interruption and session-state handling require separate client checks.

## Product and coverage limits

[Grok product overview](https://docs.x.ai/grok/overview), updated 2026-10-06, describes Grok on web/mobile, voice, media, files and connectors; Grok Build/Bot/API are separate paths. It does not establish public API settings in the user's chat product. Coverage includes current model/capability/migration and substantive voice prompt guide, not every streaming reference, gateway or media-generation model. Account access, pricing, exact host controls and task performance remain untested.
