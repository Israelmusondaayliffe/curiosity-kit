# OpenAI: model and surface branches

Checked 2026-10-09 UTC. Official documentary guidance; no account or model execution test. Publication/update dates were not displayed unless noted. Select the exact API model or product interface before applying settings. ChatGPT, Codex and a hand-built Responses client do not expose interchangeable controls.

## Current GPT-6 family

The [catalog](https://developers.openai.com/api/docs/models) identifies [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) and [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna). All link to the [current family guide](https://developers.openai.com/api/docs/guides/latest-model). Load that guide's matching version section; it also retains GPT-5.6 text. Astra's inspected API page lists low, medium, high, xhigh and max; this is not a universal enum or a guarantee the selected host exposes every value. The Sol/Luna model pages were reopened on 2026-10-09 to verify these distinctions:

- Sol supports low/medium/high/xhigh/max, defaults medium and rejects none/minimal. Tools require Responses; Chat Completions supports tool-free requests.
- Luna supports none/low/medium/high/xhigh/max, default medium. Responses supports built-ins and function calls; Chat Completions function calls require reasoning_effort none. Both model pages list structured output support, which still requires a compatible schema and completion checks.

The shared guide documents asynchronous tools with original call IDs and explicit configuration-update items for supported mid-conversation effort changes. The client must track pending work; an async call is not completed work. Verify exact interface support instead of inserting an undocumented per-turn prompt instruction.

Start from a concise outcome and complete constraints, then tune clarification, writing, delegation and testing against the actual workload. Remove a coherent obsolete compensation group at a time; keep authority, evidence and required tests. The [Astra instruction-design article](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), published 2026-09-11, supports narrow discovery descriptions and task-specific resource loading. Its autonomy recommendations do not grant new permissions.

Original prompt adjustment for a bounded UI task:

> Repair the overlapping search controls in the supplied app. Preserve its existing layout and design tokens. Check keyboard access and the two supplied viewport sizes. Deliver the patch and observed checks; report any check that could not run. Do not add a landing page or unrelated controls.

This replaces generic "make it impressive" scaffolding with task-specific restraint. It is a candidate to test, not a claim Astra always overbuilds. Historical specialist field observations about Astra's writing, visual work, computer control and high-effort excess are hypotheses with a bounded original context. Earlier acceptance records were not independently recovered here. "Astro" remains unresolved unless the user's surface identifies it as Astra.

## Historical GPT-5.6 and GPT-5.4 migration

Retain the useful method while checking current compatibility:

- GPT-5.6: consolidate duplicated instructions without deleting distinct host requirements; separate voice, autonomy and output length. Give short answers explicit must-include facts. Distinguish direct judgment calls from predictable bulk reduction. Preserve stable cached prefixes only where the selected endpoint supports them; compaction, continuation and output phases are separate concerns.
- GPT-5.4: discover prerequisites, account for every requested item, specify missing-value behavior and cite source anchors. For dense documents use a page/section map; for screenshots record coordinate conventions and verify observations after acting. For code, actual tests and rendered inspection outrank promises of testing.
- These are retained task techniques, not proof of support for a historical mode, alias, image setting, price or cache key. Recheck the requested version instead of replacing it with GPT-6. A model/configuration migration and prompt subtraction are separate experimental changes.

GPT-5.6 request surfaces. On 2026-10-09 the current family guide's migration section confirmed only that `prompt_cache_retention` becomes `prompt_cache_options.ttl` (its example uses `"30m"`) and that cache boundaries and cache-write billing changed. The rest of this paragraph comes from the original GPT-5.6 specialist's dated extracts and was not on the current page; confirm each against the selected endpoint before relying on it. Explicit cache breakpoints or `prompt_cache_options.mode: "explicit"` control which prefixes are cached, with writes billed at 1.25x uncached input, so volatile prefixes can cost more cached than uncached. `reasoning.context` takes `auto` (default; read the effective value from the response), `all_turns` or `current_turn`; continue with `previous_response_id`, or under `store: false` or Zero Data Retention request `include: ["reasoning.encrypted_content"]` and replay the returned items. Pro mode is `reasoning.mode: "pro"` on the selected 5.6 model, not a separate model slug, and is independent of effort; do not coach it with "think harder" or draft-several-candidates instructions. Each is a configuration change to test separately from prompt subtraction.

The older [reasoning best-practices page](https://developers.openai.com/api/docs/guides/reasoning-best-practices) and [generic prompt guide](https://developers.openai.com/api/docs/guides/prompt-engineering) contain older GPT-versus-o-series framing. Do not apply that dichotomy to Astra. The generic page's reusable-prompt deprecation notice also makes a hosted prompt-object dependency inappropriate without a current support check.

## Tools, structure and state

The [programmatic tool guide](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling) supports bounded predictable processing. Use direct calls where judgment or authorization is required; a programmatic stage needs typed inputs/results, error handling, coverage, retry/stop bounds and a final-answer contract. A top-20 result cannot prove fifty inputs were processed. Preserve per-item status and source references separately from the selected twenty. Citation and native-artifact survival require actual host verification.

[Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) distinguish schema output and refusals. Put nullable fields, ambiguity and error channels into the actual schema. Validate semantics, required artifacts and completion status as well as parseability. Do not assume JSON mode has strict-schema guarantees.

Use the [deployment checklist](https://developers.openai.com/api/docs/guides/deployment-checklist) for exact endpoint/tool/configuration compatibility. Verify output headroom and the selected client's state contract; do not flatten response items into text or transplant another provider's reasoning fields. The [changelog](https://developers.openai.com/api/docs/changelog) records September model releases and Sol/Luna image-encoding fixes, so a model label alone does not freeze visual behavior.

## Qualification and limits

Freeze cases and source prompt; compare correctness, completion, restraint, authority preservation and measured total cost/latency. For Astra migration include matched voice-preservation, bounded computer-control and UI-restraint probes when relevant. Apply [evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices) with human-calibrated grading and judge-bias checks. Its inspected notice schedules hosted Evals read-only transition for 2026-10-31 and shutdown for 2026-11-30; the lab does not require that service.

Coverage: complete substantive current family and retained GPT-5.6 guide sections, model support pages, Astra article and selected operational guides. No separate Sol/Luna prompt guide was located. Dedicated media generation, transcription/speech and restricted-domain services are outside this profile. Current access, continued validity of these controls, product UI settings, retention and runtime results must be verified when selected.
