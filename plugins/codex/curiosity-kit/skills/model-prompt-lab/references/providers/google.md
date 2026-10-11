# Google Gemini: text, tool and Live branches

Checked 2026-10-09 UTC; documentary evidence, no runtime/account test. Choose Gemini Apps/Gems, Gemini API Interactions, legacy Generate Content or Live before using controls. The [catalog](https://ai.google.dev/gemini-api/docs/models), updated 2026-10-06, lists stable Gemini 3.8 Flash and preview Gemini 3.1 Pro separately.

## Gemini 3.8 Flash

[Model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash), dated 2026-09-02: `gemini-3.8-flash` accepts text, image, video, audio and PDF input, with text output. Thinking levels are low/medium/high; minimal errors. The [current guide](https://ai.google.dev/gemini-api/docs/latest-model), updated 2026-10-07, sets medium default, removes deprecated sampling controls, candidate count and model prefills, and favors stateful continuation. Do not carry older low-temperature or minimal-effort examples forward.

Use a direct task, explicit answer length and concrete completion requirements. For long documents place source context before the final question, while keeping critical behavior in the system/initial instruction. Simplify obsolete reasoning scaffolds rather than requesting hidden reasoning. Lower effort may reduce redundant verification, but required checks remain. Original adjustment:

> Using the supplied report, identify the three largest year-over-year changes. For each, give the value, comparison period and page reference. If a denominator is absent, mark the percentage unavailable. Keep the answer under 200 words.

This is a prompt candidate; arithmetic and citations still need validation.

## Gemini 3.1 Pro and historical Flash migrations

[Pro model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview), dated 2026-08-18: `gemini-3.1-pro-preview-customtools` prioritizes custom tools over bash and may fluctuate on unrelated tasks. Preserve the requested variant. Do not apply 3.8 controls merely because both names begin with Gemini 3.

The [legacy Gemini 3 guide](https://ai.google.dev/gemini-api/docs/gemini-3), updated 2026-09-23, remains linked from Pro but is deprecated. Its family-wide preview/control assertions yield to current exact-model pages. [3.6 migration](https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.6), updated 2026-10-07, says sampling fields are ignored from those releases and may be rejected later; a nonempty ending model turn gives 400. [3.5 guidance](https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5), updated 2026-10-09, retains concise instructions, explicit verbosity, signatures and media-result migration. Earlier minimal effort is not 3.8 support. Flash-Lite premature tool-loop stopping calls for a matched medium/high test, not a blanket effort rule.

## Interactions tools, schemas and history

[Thinking](https://ai.google.dev/gemini-api/docs/thinking), updated 2026-09-25: stateful `store: true` plus `previous_interaction_id` retains thought blocks/signatures; stateless clients must replay them unchanged, including built-in-tool signatures. `max_output_tokens` includes thinking, so tiny limits can leave empty or truncated visible output. Keep state out of prompt prose and never transplant another model's opaque blocks.

[Function calling](https://ai.google.dev/gemini-api/docs/function-calling), updated 2026-09-23, documents Interactions modes auto/any/none/validated. Use descriptive typed tools, preserve IDs/results, validate arguments and permission before execution. Mandatory structured XML/JSON/YAML immediately before calls can cause `Malformed_Function_Call`; use an actual progress function, supported prose transport or no mandatory pre-call text. Do not remove required user communication or invent a function. [Legacy Generate Content calling](https://ai.google.dev/gemini-api/docs/generate-content/function-calling) needs its own syntax check.

[Structured output](https://ai.google.dev/gemini-api/docs/structured-output), updated 2026-09-23, supports a JSON Schema subset; large/deep schemas may fail. Validate semantic values and completeness outside the schema. [General prompting](https://ai.google.dev/gemini-api/docs/prompting-strategies), updated 2026-09-17, mixes older examples with newer advice. Its broad few-shot recommendation is a technique to test, not a requirement for every request.

## Live and Apps

[Live best practices](https://ai.google.dev/gemini-api/docs/live-api/best-practices), updated 2026-09-15: load only for `gemini-3.8-live` or extended-thinking voice. Specify persona, conversation flow, guardrails, language and real tool conditions; distinguish one-time intake from the conversational loop. Example: "Ask for the destination once, then ask one missing trip detail at a time. Repeat the proposed booking details before any authorized booking step." The client owns interruptions, resumption and compression. Proactive audio stays enabled on 3.8 Live and affects listening cost.

[Gems help](https://support.google.com/gemini/answer/15236405?hl=en), no displayed update date, establishes reusable product instructions, not API effort/schema or fixed-model guarantees. Check actual account controls.

Coverage includes current catalog/model guides, relevant inherited migration, schemas/tools/state and Live prompting. Full streaming protocol, every SDK tab and account access were not tested. Runtime controls, model rollout and actual cost/quality remain verification work.
