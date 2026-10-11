# Moonshot AI / Kimi: K3 and active companion models

Checked 2026-10-09 UTC. Official documentary guidance; no inference/account test. Page publication/update dates were not displayed unless specifically labeled. Choose official API, Kimi product or exact self-host engine before adding controls.

## Resolve model and generation

The [model list](https://platform.kimi.ai/docs/models) lists K3, K2.7 Code and K2.6 as current material branches. It records K2.5/moonshot-v1 retirement on 2026-08-31 and K2-series retirement on 2026-05-25. The [changelog](https://platform.kimi.ai/docs/platform-changelog) gives July 2026 for K3, June for K2.7 Code and April for K2.6; those entries do not supply exact release days. Preserve a requested legacy target while reporting availability unresolved or retired; do not fabricate a compatible replacement.

## K3 prompt and configuration

[K3 quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart) and [thinking-model guide](https://platform.kimi.ai/docs/guide/use-thinking-models) describe always-on thinking, low/high/max effort with max default. Omit fixed sampling fields: temperature 1, top_p 0.95, n=1 and zero penalties. Replay complete assistant messages unchanged, including permitted reasoning and tool fields. Changing model/host requires a fresh state-compatibility check, not rewriting these fields as a natural-language summary.

K3 vision accepts object arrays with base64 or ms file IDs, not public image URLs. Strict JSON schema constrains visible content, not `reasoning_content`. Do not count the existence of reasoning or valid JSON as evidence the task completed. Check refusal, interruption, missing fields, item coverage and semantic values.

The [general prompting guide](https://platform.kimi.ai/docs/guide/prompt-best-practice) supports clear context, delimiters, relevant examples, reference-only answers and measurable output shape. Use that to resolve ambiguity rather than adding generic instructions to think harder. Original example:

> Using the attached contract excerpts only, list each renewal deadline and its governing clause. Preserve exact dates and distinguish notice dates from renewal dates. If an excerpt does not establish a deadline, say "not established" and identify the missing clause. Do not infer legal effects outside the supplied text.

This is a source-extraction example, not legal advice or a schema guarantee. Test a no-deadline excerpt and conflicting amendments explicitly.

## K3 large tool library

The [K3 tool-calling guide](https://platform.kimi.ai/docs/guide/kimi-k3-tool-calling-best-practice) starts with `search_tools` and core tools, identifies searchable domains in the system prompt, forces initial retrieval where needed and appends complete declarations in system messages. This is a host/tool workflow, not permission to call unavailable tools or execute side effects. Verify actual selected-tool forcing support before using the guide's workflow on another model.

Original adjustment for an available search-tools host:

> The tool catalog contains read-only inventory and shipment lookups. Retrieve the relevant declaration before calling an unfamiliar tool. Use shipment lookup only for the supplied order IDs. Retain blocked IDs in the final result and stop before any write operation.

The host must enforce permissions, retain declaration/history integrity, return all matching tool results and bound discovery/continuation. Do not put invented schemas into a conversation and imply they are implemented.

Search readiness is unresolved: K3 quickstart retains a near-term web-search warning, while the September changelog announces standalone Search APIs. Built-in search, Formula tools and standalone search are distinct paths. Verify the chosen path; the existence of one does not establish the others.

## K2.7 Code and K2.6 migration

[K2.7 Code quickstart](https://platform.kimi.ai/docs/guide/kimi-k2-7-code-quickstart) specifies always-on thinking, fixed temperature 1/top_p 0.95 and tool_choice auto/none. [K2.6 quickstart](https://platform.kimi.ai/docs/guide/kimi-k2-6-quickstart) permits disabling thinking, with temperature 0.6 then; thinking-mode tool choice is also auto/none. Therefore K3's forced first-tool workflow cannot be copied unchanged. K2.6's web-search discussion explicitly warns it is outdated.

For a coding request, preserve repository context, exact change boundaries and observed checks in the prompt. Tune prompt and effort separately from mandatory compatibility changes. Example: "Repair the reproduced test failure, preserve the public interface, and report the command and observed result of each relevant check. Mark unavailable checks; do not call them passed."

## Open K3 and gaps

The [official K3 card](https://huggingface.co/moonshotai/Kimi-K3) says training used preserved thinking history; return `reasoning_content` and `tool_calls` intact. Linked serving recipes were not installed or exercised. An arbitrary compatible endpoint may drop these fields. Card prose includes video while its modality summary lists text/image: verify self-host video preprocessing with the exact engine before promising it.

Coverage includes current catalog, general prompting, K3 tool/history/vision/structure and active companion differences. It is not every deployment recipe or product setting. Mutable cards were not revision-pinned. Exact IDs exposed by the selected host, access, data retention, budgets, actual schema subset and end-to-end performance remain to be checked.
