# DeepSeek: V4.1 Flash and active V4 Pro

Checked 2026-10-09 UTC. Official documentary evidence only; no inference/account test. No explicit page update date was displayed unless noted. Choose official API versus a pinned open-weight encoder/runtime; an OpenAI-compatible transport does not make the contracts identical.

## Identity and retirement correction

The [current catalog](https://api-docs.deepseek.com/quick_start/pricing/) maps `deepseek-flash` to V4.1 Flash, accepting text/image input, and `deepseek-v4-pro` to text-only V4-Pro-0813. The [changelog](https://api-docs.deepseek.com/updates/) records the 2026-09-10 Flash release and 2026-08-13 Pro GA. It explicitly continues Pro. The [September 10 launch article](https://www.deepseek.com/en/news/deepseek-v4-1-flash/) still contains a planned September 14 Pro redirect: that retirement plan is superseded, not a reason to silently migrate a requested Pro workload. Recheck current alias mappings at use.

## Official API prompting and controls

The official [Chinese thinking guide](https://api-docs.deepseek.com/zh-cn/guides/thinking_mode/) was read directly after the English counterpart repeatedly failed retrieval. Thinking defaults on at high; native levels are low/high/max. Temperature and penalties are ignored while thinking, with top_p clamped to 0.95–1.0. Do not use a temperature edit as the sole experiment for a thinking-mode failure.

When tools are present, return every historical `reasoning_content`, including assistant turns without tool calls; missing content can cause 400. Preserve the permitted response fields exactly in the client, rather than asking the model to restate internal reasoning. This is an API continuation requirement, not a portable reasoning-transcript format. Verify mode-specific rules on the chosen endpoint before implementing a transition.

[JSON output](https://api-docs.deepseek.com/guides/json_mode/) requires `response_format=json_object`, an explicit JSON instruction and target shape. It acknowledges occasional empty content; leave sufficient output budget and detect it. JSON mode does not establish strict schema or semantic accuracy.

Original prompt adjustment:

> Return JSON containing status, records and ambiguities. Extract each supplied invoice's ID and total without calculating absent values. Use null for missing fields. Include every input filename once, and record unreadable or conflicting values in ambiguities. Do not add commentary outside JSON.

Define the actual field types and success/error envelope in the application; the sample prose does not enforce them. Test missing fields, conflicting totals, empty content and interrupted output separately. This is a useful output contract, not a claim of unique DeepSeek performance.

For tools, describe the authorized lookup and stopping condition explicitly. Example: "Look up each supplied issue ID once; return its status and evidence link. If access is denied, retain that ID as blocked." The client validates call arguments and permissions, returns every call result and checks final item coverage. The source study did not establish a universal forced-tool or strict-schema enum; verify those before proposing API syntax.

## V4.1 Flash self-host branch

Use the [official model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) and [text/vision encoding guide](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/encoding/README.md). Use its encoder rather than assuming a generic Jinja template. V4.1 changes DSML spacing, permits mid-conversation system messages and has numeric local effort 1–100, with low/high/max mapped to 50/75/100. Those numeric controls are not established hosted API inputs. Feed media through the supported encoder; wording alone cannot supply image data.

## V4 Pro self-host branch

Use the [V4-Pro-0813 card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) and [V4 encoding](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813/blob/main/encoding/README.md), not V4.1 formatting. Local recommendations are temperature 1, top_p 0.95 for agents or 1 otherwise, and 384K output for high/max. These are local model guidance, not verified API limits or permission to spend that budget. The local developer role is internal-only and not accepted by the official API.

## Qualification and gaps

Keep model, encoder revision, serving engine, mode and tool-history policy in the experiment identity. A formatting/state error must not be misdiagnosed as weak reasoning. Compare actual complete task cost, not merely one call's token count.

Coverage includes catalog/changelog, thinking/JSON guidance and both official model/encoding branches. Dedicated vision API guidance remained inaccessible; multimodal existence and native encoder handling are supported, but exact hosted payload details need a fresh check. Mutable cards/encoder files were not pinned to full revisions in the source study. Account availability, real serving compatibility, output quality and prices remain untested.
