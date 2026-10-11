# Qwen: hosted, open-weight and Omni contracts

Checked 2026-10-09 UTC. Official documentary guidance; no runtime/account verification. Choose regional Alibaba Model Studio, Qwen Cloud, self-hosted weights, HTTP Omni or Realtime explicitly. Similar names do not establish behavioral or payload parity.

## Hosted Qwen3.8 Max and Flash

[Recommended models](https://www.alibabacloud.com/help/en/model-studio/models), updated 2026-09-28, and [lifecycle log](https://www.alibabacloud.com/help/en/model-studio/newly-released-models), updated 2026-10-08, record models by host/region. Max and Max-0902 are distinct requested identities; a regional release date is not a global publication date. Model Studio also hosts other providers.

[Qwen Cloud Max](https://www.qwencloud.com/models/qwen3.8-max), no displayed update date, supports vision and non-thinking mode. [Model Studio thinking](https://www.alibabacloud.com/help/en/model-studio/deep-thinking), updated 2026-09-28, uses `enable_thinking` and `thinking_budget`; preservation is separate and requires historical `reasoning_content`. Qwen Cloud examples put controls in `extra_body`; self-host examples use `chat_template_kwargs`. Verify the selected route instead of merging these objects. Older Qwen3 `/think` and `/no_think` prompt commands are not established Qwen3.8 controls.

Original prompt adjustment:

> Compare the supplied product records using only their stated specifications. Return one row per ID with compatibility, supporting field and missing information. Mark compatibility unknown when the decisive field is absent. Keep the original IDs and units unchanged.

Add a boundary-case example only if evaluation reveals a recurring ambiguity. A prompt's desired JSON shape is not a verified endpoint schema guarantee. Check the exact hosted structured-output/tool support before adding configuration, and validate complete records, values and failure status outside the model.

## Open Max / Flash-Next

The [Qwen3.8-2.4T-A95B card](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B), citation month 2026-08 (not page update), describes a text-only always-thinking open model, unlike hosted Max. Its low/medium/xhigh effort defaults xhigh. Do not send an image or thinking-off configuration because the API-branded counterpart accepts one. Use the supplied runtime template and preserve supported state fields.

[Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next), no displayed update date, defaults thinking and `preserve_thinking` on; low/medium/xhigh are documented. Suggested temperature/top_p are 1/0.95 thinking and 0.7/0.8 non-thinking. Native context is 262,144; expansion requires serving configuration. These are model-card settings, not proof of every managed Flash option. Lower effort can increase retries and total latency; measure whole-task success/cost rather than assuming cheaper calls win.

## Omni HTTP: text from multimodal input

[Omni overview](https://www.alibabacloud.com/help/en/model-studio/omni), updated 2026-09-28, and [Qwen-Omni guide](https://www.alibabacloud.com/help/en/model-studio/qwen-omni), updated 2026-10-08, distinguish `qwen3.8-omni-flash` HTTP text output from audio-output routes. Put instructions and media in the same user content array. Short requests suit fast review; detailed analysis should specify timestamps, speakers and transcript/narrative distinctions. Effort defaults xhigh; none disables it. Do not combine `reasoning_effort` with `thinking_budget`.

Original example:

> Summarize this clip in timestamp order. For each change of speaker, record the timestamp, speaker label and spoken claim. Separate visible observations from inferred intent. Mark uncertain words rather than inventing a clean transcript.

Validate timestamp ranges, speaker continuity and supplied-media coverage. Hosted support does not establish an open Omni deployment or compatible self-host processor.

## Omni Realtime: session instructions

[Realtime guide](https://www.alibabacloud.com/help/en/model-studio/realtime) and [client events](https://www.alibabacloud.com/help/en/model-studio/client-events), both updated 2026-09-29, place role/objective in `session.update.instructions`, voice separately. `semantic_vad` filters backchannels. Defaults are temperature 0.6/top_p 0.95; tune one. `max_tokens` truncates output, so specify desired speaking length in instructions. Manual mode needs commit then response.create. HTTP thinking fields are not established Realtime controls; web search and tools are mutually exclusive.

Example: "Answer in two short spoken sentences, then pause. If the listener interrupts, follow their new question. Ask one clarification when the request lacks its decisive detail." Session interruption/turn handling must actually support this behavior.

## Coverage and limits

Current flagship/model-host guidance, open Max/Flash-Next and Omni session prompting were read. Qwen blog rendered no content; official host logs/cards supplied evidence. Smaller 3.7-Plus/3.8-27B companions, every regional deployment and a full streaming reference audit are outside this pass. No universal tool-choice/schema enum is inferred. Recheck exact model ID, region, modality, template, context/output accounting and history support before use. No account access, real cost or task-quality result is claimed.
