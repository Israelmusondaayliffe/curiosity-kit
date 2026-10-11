# Meta: Spark, Glimmer and Llama are distinct targets

Checked 2026-10-09 UTC. Official documentary evidence only; no model/API/account test. Source publication/update dates were not displayed unless noted. Resolve "Meta" or "Muse" to a model and interface before applying a branch.

## Muse Spark API and agent products

The [developer overview](https://dev.meta.ai/docs/overview) lists `muse-spark-1.3` Standard and separate Contributor IDs, older 1.2/1.1, Responses/Chat Completions/Messages interfaces and Muse Code. The [Muse product announcement](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) displays September 8 and September 30, 2026 without clearly labeling publication versus update in the inspected body. It describes a personal agent powered by Spark. Neither that agent nor Muse Code proves the user can configure public API fields. Spark's internals are not established by product marketing.

There is no located standalone general Spark prompting guide. Use the official task cookbooks as conditional techniques:

- [Computer use](https://dev.meta.ai/docs/cookbook/computer-use): explicit goal, distinguish sandbox tools from host shell, inspect after actions.
- [Iterative game work](https://dev.meta.ai/docs/cookbook/iterative-game-dev): actual asset inventory, browser play-tests, console evidence and small repairs. A still screenshot cannot establish correct motion.
- [macOS computer use](https://dev.meta.ai/docs/cookbook/computer-use-macos): narrow reversible goals, serial actions and fresh screenshots. Its coordinates are normalized 0–1000, not pixels; typing does not submit. Only use this contract with the matching tool.

Original prompt:

> Locate the draft in the supplied sandbox and fix the clipped modal using the existing component styles. After each meaningful UI change, inspect a fresh render. Check open, close and keyboard focus behavior. Stop before any publish action and report observed results.

Some cookbook headers name 1.3 while body steps retain 1.1. Their verification patterns are useful guidance, not evidence of version-equivalent performance.

### Spark protocol contract

[Tool calling](https://dev.meta.ai/docs/tool-calling) accepts only auto; none/required/named choices return 400. Custom free-text tools are Responses-only. `max_tool_calls` bounds built-ins, not client functions. Keep full calls/results and IDs; large libraries can use documented tool search, not invented tool availability.

[Chat Completions](https://dev.meta.ai/docs/protocols/chat-completions) is positioned for simple exchanges; Responses is preferred for reasoning continuity, tools, grounding and files. Chat uses `response_format`, Responses uses `text.format`. Chat does not support several familiar OpenAI options, including stop, verbosity and n greater than one. Built-in web search is a Responses tool, not `web_search_options`.

[Reasoning](https://dev.meta.ai/docs/reasoning): none is rejected; minimal/low/medium/high/xhigh are listed, with max for Standard Spark 1.3. The Chat parameter table omits that max extension; verify exact endpoint/tier rather than merging the tables. Responses supports stored continuation or encrypted replay; Chat's redacted `reasoning_content` cannot carry private state. Summaries are not opaque replay. Thinking consumes output/cost headroom.

[Structured output](https://dev.meta.ai/docs/structured-output): strict defaults false on both outputs and function tools. The strict subset requires an object root, all properties required and `additionalProperties: false`; oneOf/allOf are unavailable, nested anyOf is allowed. Recursive/complex schemas can fail. Nullable fields provide a missing-value channel only if the schema permits them. Validate semantic accuracy independently.

## Muse Glimmer self-host

[Glimmer overview](https://dev.meta.ai/docs/muse-glimmer) describes a 30B dense text/image model with 128K default context. Its [actual prompt guide](https://dev.meta.ai/docs/muse-glimmer/prompting) requires the tokenizer chat template and generation prompt; images use AutoProcessor. Native recipient-tagged turns and ATEM tools differ from Llama. Only one tool call per turn is supported. `reasoning_strength` supports low/medium/high/xhigh, default high; recommended sampling is 1.0/0.95/64 for temperature/top_p/top_k. These are Glimmer-local facts, not Spark API settings.

Put task behavior and output constraints upfront; avoid directions about private internal operation. Example: "Compare the two supplied screenshots. Report only visible differences, with image label and approximate region; mark unreadable text rather than guessing." Feed actual images through the processor and test visibility at the chosen resolution.

## Llama 4 self-host or third-party host

The [official repository catalog](https://github.com/meta-llama/llama-models/blob/main/README.md) identifies Scout and Maverick as the latest Llama generation; its Llama 4 launch is dated 2025-04-05. This does not make Llama the current Muse/Spark flagship. Select base versus Instruct and the correct tokenizer. The [Llama 4 format](https://github.com/meta-llama/llama-models/blob/main/models/llama4/prompt_format.md) uses its own role headers, turn endings and image tokens. Never paste Glimmer's recipient syntax into it. API tool/schema guarantees depend on the actual serving host.

## Limits

The Llama website retrieval failed; official repo and Meta developer docs were accessible. Mutable repo references were not commit-pinned here. Coverage includes catalog, Spark protocol/task guidance, Glimmer prompting and Llama format, not every serving recipe. Exact account support, Messages differences not detailed above, retention, runtime/template version and output quality need verification when selected.
