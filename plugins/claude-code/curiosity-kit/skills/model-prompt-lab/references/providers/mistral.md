# Mistral: hosted models and open-weight templates

Checked 2026-10-09 UTC. Official documentary guidance only. Unless stated, no publication/update date was displayed. Choose API/Studio Conversations, Vibe product or the exact self-hosted model/runtime. Mistral hosting a model does not establish Mistral model origin.

## Large 4 identity must be resolved

The [catalog](https://docs.mistral.ai/models) and [Large 4 page](https://docs.mistral.ai/models/mistral-large-4-0), dated 2026-10-06, describe a public-preview text/vision model with tools, structured output and 1M context. The page displays `mistral-large-4`, while [reasoning documentation](https://docs.mistral.ai/studio/conversations/reasoning) uses `mistral-large-4-0`. Retain both as a documented inconsistency; validate the actual endpoint's accepted identifier instead of choosing silently. The [2026-10-06 changelog](https://docs.mistral.ai/resources/changelogs) says weights are coming soon. An open-weight catalog label is not proof a download is available.

No dedicated Large 4 prompt guide was found. Apply the [general prompting guide](https://docs.mistral.ai/inference/prompting): clear purpose, complete relevant context, explicit precedence for overlapping conditions and useful examples. Delimiters can be Markdown or XML; roleplay and long wrappers are optional. User-message placement is a fallback when system access is absent, not equal system priority.

Original example:

> Classify each request as eligible, ineligible or needs-information using the policy below. Apply exclusions before general eligibility. For needs-information, name the missing fact. Return every input ID once, with the policy clause supporting its result.

Test exception collisions and missing facts rather than assuming a longer system prompt fixes them.

## Medium 3.5 and Small 4

[Medium 3.5 model](https://docs.mistral.ai/models/mistral-medium-3-5-26-04), dated 2026-04-28, identifies the 256k multimodal agentic/coding model. Its [official weight card](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) recommends high effort for agentic coding, temperature 0.7/top_p 0.95; none uses task-tuned temperature 0–0.7 without top-p filtering. Use Mistral parsers and processor template. The corrected Transformers long-context configuration matters: degraded context handling may be deployment, not prompting. Its linked SYSTEM_PROMPT.txt was not successfully retrieved in this study; do not fabricate its contents.

[Small 4 weight card](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) similarly uses high versus none and a processor template with appropriate tool/reasoning parsers. High recommends temperature 0.7; none uses 0–0.7 by task. API wording calls none minimal thinking while the card labels it no reasoning; do not promise identical internals. The [published system template](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603/blob/main/SYSTEM_PROMPT.txt) contains replaceable dates, uncertainty and language guidance. Its no-web claim and Le Chat identity are deployment-specific; do not copy them into a tool-enabled agent.

Original coding adjustment:

> Reproduce the supplied pagination bug, inspect the adjacent pagination cases, and make the smallest in-scope repair. Run the existing relevant tests and report their actual results. Preserve the public response shape and leave unrelated refactors untouched.

The weight-card settings are starting hypotheses for that exact local deployment, not universal API tuning or measured gains.

## Hosted state, tools and schemas

[Reasoning](https://docs.mistral.ai/studio/conversations/reasoning) lists adjustable reasoning for small-latest, medium-3-5 and large-4-0; high emits a thinking chunk, none omits it. Magistral native-reasoning entries are deprecated. Hosted `zai-glm-5-3` has a different contract: load [Z.ai](zai.md) plus the Mistral host page. Agent/Conversation placement is `completion_args`; do not transplant another provider's reasoning object.

[Function calling](https://docs.mistral.ai/studio/conversations/function-calling) supports auto/any/none; parallel calls default on. Execute only authorized calls, return every matching result and continue until the bounded task is actually done. One returned tool result is not a completion signal. Keep call/result history intact; this study did not establish portable cross-model reasoning-state replay.

[Structured output](https://docs.mistral.ai/studio/conversations/structured-output) says JSON mode needs an explicit JSON instruction and format. [Custom structure](https://docs.mistral.ai/studio/conversations/structured-output/custom) is the stronger formatting route; validate exact model/schema support and semantics. Do not infer universal schema coverage across hosted and open models.

## Migration and limits

[Migration guidance](https://docs.mistral.ai/resources/migration-guides) distinguishes tokenizers/templates and SDK versions. Old model examples and broad license descriptions cannot resolve the mixed current catalog. [Sampling](https://docs.mistral.ai/inference/sampling) was partially retrieved: some tabs remained hidden, so it does not supply a complete current settings table.

The [help center](https://help.mistral.ai/en/) currently uses Vibe naming; the May 28 changelog distinguishes Vibe Work/Code/Chat and legacy Le Chat. Product controls were not audited. Recheck actual interface, ID, model license/availability, output accounting and client parsers before use. No runtime quality, user access or self-host compatibility has been qualified.
