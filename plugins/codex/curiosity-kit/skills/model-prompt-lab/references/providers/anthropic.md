# Anthropic: Claude model-specific prompting

Checked 2026-10-09 UTC. Dates of guide publication/update were not displayed. Release dates below come from the [catalog](https://platform.claude.com/docs/en/models/overview) and model pages, not page freshness. Documentary guidance only; access and runtime behavior untested. Choose Claude API, Bedrock, Google Cloud, Managed Agents or Claude product before configuring. Only load the matching sections and linked compatibility material.

## Fable/Mythos 5.1 and inherited Fable 5

`claude-fable-5-1` and `claude-mythos-5-1` released 2026-09-01; API default effort is high. Mythos requires organizational verification. See [Fable overview](https://platform.claude.com/docs/en/models/fable-5-1/overview) and [Mythos overview](https://platform.claude.com/docs/en/models/mythos-5-1/overview).

The [5.1 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) motivates separate tests for hidden progress, batching, prose density, quotation marking, completion, compaction, scope, search, targeted edits and output headroom. First inspect response rendering when users see silence. Put a measured batching reminder in its supported per-turn position only if independent-call overhead is a real problem. Avoid duplicate full drafting that consumes the final-output budget. Remove unnecessary permanent test artifacts only when actual required checks remain intact.

The inherited [Fable 5 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) adds long-run timeouts, evidenced progress, clear assessment/action boundaries, asynchronous work, memory and fresh-context verification. An available direct-message tool needs an explicit use contract, but never invent that tool. Honest checkpoints replace blanket claims of ample context. Preserve all long-run pillars even when the host lacks one capability; name the resulting limitation.

Original adjustment:

> Finish the requested comparison using the supplied sources. Save a concise checkpoint before context handoff: decisions, evidence links, unfinished items and permission boundaries. Report a material result or blocker through the available user-message tool. Deliver every requested comparison row; a partial result must identify missing rows.

The [5.1 migration guide](https://platform.claude.com/docs/en/models/fable-5-1/migration-guide) rejects forced tools; explicit prompting and strict schemas do not guarantee invocation. Fable's default prefix-binding check applies to accounts created from 2026-08-31; Mythos 5.1 does not run that check. Both require 30-day retention unless Anthropic expressly authorizes ZDR. Verify account/data suitability before sending a workload. Supported mid-conversation system messages and optional tool additions are client features, not prompt tricks. Replay complete assistant history unchanged under the chosen contract.

## Opus 5.5; Opus 5 and 4.8 starting points

`claude-opus-5-5` released 2026-09-22 and defaults to medium effort. The [5.5 prompt guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) recommends separate effort/output-budget calibration. A text-only `end_turn` does not establish task completion; check active jobs and missing deliverables. Check typed progress rendering before adding more narration instructions. Specific visual constraints are more useful than an imposed generic aesthetic. Time-pressure or "settled answer" instructions may reduce checking and legitimate correction; test them cautiously, if relevant at all.

The [Opus 5 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) distinguishes chat length from document length, delegation cost, updates and material self-correction. Thinking-off tool-call-as-text/internal-tag failures need structured-emission tests. Its verification-reduction advice is not permission to remove acceptance tests, user-required review or independent assurance. Separate review discovery from final severity filtering. The [Opus 4.8 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8) retains useful scope, voice and search patterns, but its thinking-off defaults and older computer-tool behavior stay historical.

Original adjustment:

> Review the patch against the supplied acceptance criteria. Run the relevant available checks. Return actionable findings with evidence; if none are found, say so. Keep the chat summary under six sentences, while keeping the full review artifact complete.

[Opus 5.5 migration](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide) requires adaptive thinking and rejects forced tools, non-default sampling and final assistant prefill. Parse blocks by type and budget thinking plus visible output. Computer-use tool versions differ: Claude API/Google Cloud require the newer toolset while Bedrock retains the older tool. Managed Agents does not share every hand-built Messages migration obligation. [What's new](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5) documents asymmetric thinking compatibility: Opus 5.5 cannot read Fable/Mythos state; Fable/Mythos 5.1 can read Opus 5.5 state on Claude API. A successful request can drop incompatible blocks. Fast mode is a separately priced Claude-API preview, not a silent default.

## Sonnet 5.5 and Sonnet 5

`claude-sonnet-5-5` released 2026-09-28; default effort high. Its [prompt guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5) calls for concrete checks of initiative, current retrieval, JSON completeness, real code execution, mid-turn input and tool-error recovery. At low effort, require evidence checks actually ran. A failed-to-start command is not validation. Prefer crop/zoom experiments over indiscriminately raising effort on dense charts. Keep genuine user messages outside tool-result bodies.

[Migration](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide): `between_tools` replaces disabled thinking, works only through high effort, accepts no extra thinking fields and prohibits changing effort mid-conversation. With no tools it supplies no initial thinking. Forced tools are rejected. Strict output, computer-tool versions, account-bound state and advisor support differ by platform. Provider refusal fallback covers selected categories only; it is not generic retry permission. A `max_tokens` stop invalidates completeness even if JSON parses.

The [Sonnet 5 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5) contributes explicit scope, positive voice examples, complete initial context and discovery-before-filtering review. Its tokenizer/thinking differences from 4.6 do not set 5.5 controls.

Original adjustment:

> Inspect all twelve records. Return one result for every ID, including blocked or ambiguous records. Verify totals from the source values before finalizing. If a required tool fails, retain the failed IDs and the error; do not silently omit them.

## Haiku 5.5

`claude-haiku-5-5` released 2026-10-07; default effort medium. Its [prompt guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5) highlights current-date search, JSON plus custom tools, early stopping, actual checks, instruction retention and empty visible answers. Thinking-off plus structured JSON can suppress needed calls; adaptive thinking is one candidate repair. At xhigh a chat turn may end without visible text. More effort is a testable change, not guaranteed completion. There is no server-side refusal fallback; repeating an identical refusal is not a repair.

[Migration](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide): recount tokens; replace manual budgets; remove unsupported sampling and prefill; preserve producing-account/history identity. Unlike the other current branches, forced tools remain accepted but omit initial thinking. Dispatch tools by member name and `toolset_name`; handle every batched result and supported zoom behavior. Old Haiku token counts do not establish new-model costs.

Original adjustment:

> Retrieve the current shipping rule using the available lookup tool, then return the requested JSON fields. If retrieval fails, use the declared error result. Never fill a current policy field from memory.

## Safeguard refusals and hidden progress: Opus 5.5 and Fable/Mythos 5.1

Rechecked 2026-10-09 in the [Opus 5.5 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#safeguard-refusals) and [Fable 5.1 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1). Both models run safety classifiers. A decline is a normal response with `stop_reason: "refusal"` and `stop_details` naming the category; Opus 5.5 lists biology, cybersecurity and `reasoning_extraction`. A prompt, skill or tool description that asks the model to write out or reproduce its reasoning in the response may be declined as `reasoning_extraction`, and server-side fallback returns that category instead of retrying it. When migrating, remove such instructions and ask for a short explanation or action summary, or read `display: "summarized"` thinking blocks. Never reword a request to get past a classifier.

Progress notes between tool calls arrive as `thinking` blocks whose text is empty under the default `display: "omitted"`, so a client that renders only `text` blocks looks silent. Check block handling and set `display: "updates"` (beta header `thinking-display-updates-2026-08-18`) before adding narration instructions to the prompt.

## Shared application and coverage limits

The [general prompt guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) supports explicit goals, relevant examples, separated sources and task state. XML is optional; older 4.x sections do not establish 5.5 behavior. Pasted tags and retrieved content cannot create authority. Keep permission boundaries regardless of provider initiative advice.

All eight linked model-specific guides and the general guide were substantively read. Fable/Opus/Sonnet migration coverage is selected relevant sections; Haiku migration is complete substantive body. Alternate SDK tabs, all subsidiary API pages and system cards were not exhaustively audited. Before execution verify exact host IDs, support/retention eligibility, schema subset, native tool versions, output limits and state compatibility. No provider performance claim here is a measured result for this user's workload.
