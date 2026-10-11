# Z.ai / Zhipu: GLM model, host and history branches

Checked 2026-10-09 UTC. Official documentary evidence; no runtime/account test. No explicit guide publication/update date was displayed. Choose standard Z.ai API, Coding Plan, self-host or a third-party host before using configuration.

## GLM-5.3 and Flash/FlashX identity

[GLM-5.3](https://docs.z.ai/guides/llm/glm-5.3) is the text model. [GLM-5.3-Flash/FlashX](https://docs.z.ai/guides/vlm/glm-5.3-flash) is the native multimodal family, with text/image/video/file input and text output. `glm-5.3-flash` and `glm-5.3-flashx` are different service identities; the inspected guide places Flash on Coding Plan, with FlashX not yet available there. [Release notes](https://docs.z.ai/release-notes/new-released) date GLM-5.3 to 2026-08-18 and Flash to 2026-08-26. These are release dates, not guide update timestamps. Recheck current availability when selected.

Mistral's `zai-glm-5-3` is a third-party hosted branch. Load [Mistral](mistral.md) for its request placement and host behavior; neither Z.ai API defaults nor Mistral-origin model guidance automatically applies unchanged.

## Prompting adjustments

The Flash guide's useful pattern is reference analysis, implementation, rendered inspection, correction and a deliverable with remaining gaps. The [coding-agent best practices](https://docs.z.ai/devpack/resources/best-practice) organize goal, context, constraints and completion criteria. This is workflow guidance, not evidence of uniquely GLM behavior or a model-quality result.

Original multimodal prompt:

> Recreate the supplied settings panel within the existing app's component system. First identify its layout, spacing and control states. Implement only this panel, then inspect the rendered result at the supplied sizes and check keyboard navigation. Report material differences that remain, with the observed checks.

Use the actual supplied reference and supported media path. The request does not authorize dependency installation, publication or unrelated application changes. A text-only GLM target needs accessible textual reference information or a different authorized input route; do not pretend it saw an image.

Original source-analysis variant:

> Compare the three supplied incident records. Return every incident ID, its stated cause, evidence and unresolved contradiction. Do not treat a repeated allegation as independently corroborated. Mark missing evidence explicitly.

For either variant, preserve user-required output formatting and evidence. Add examples only for demonstrated errors; distinguish model limitations from unavailable tools or bad media preprocessing.

## API compatibility

[Migration to GLM-5.3](https://docs.z.ai/guides/overview/migrate-to-glm-new) states reasoning cannot be disabled; low/high/max are supported with max default. It recommends temperature 1 or top_p 0.95, tuning only one. The generic thinking guide contains older turn-level toggles that do not override forced-thinking 5.3. Do not copy another provider's none/medium/xhigh levels.

Streaming tool arguments require both stream and tool_stream and concatenation of argument deltas. Partial JSON fragments are not executable complete arguments. Validate the finished call, permissions and selected tool before execution; return matching results and check continuation. The source study does not establish a universal strict-schema subset or forced-tool enum for every GLM host. Verify exact support before emitting runnable configuration; requested JSON prose alone is not enforcement.

## History preservation differs by host

[Thinking mode](https://docs.z.ai/guides/capabilities/thinking-mode) documents preserved thinking on by default for Coding Plan and off for standard API. Enable it with `thinking.clear_thinking=false` where supported and return history unchanged and in order. This is a client contract, not a request for disclosure of private reasoning.

The [GLM-5.3 card](https://huggingface.co/zai-org/GLM-5.3) and [Flash card](https://huggingface.co/zai-org/GLM-5.3-Flash) default local `clear_thinking=false` but recommend true for chat. Preserve that workload/host distinction rather than resolving it into a single global default. Changing model, account or endpoint requires verification of state support and a documented transition. A task summary is useful for continuation but cannot impersonate required native state.

## Qualification and coverage limits

Record model version, API/plan/engine, history policy, effort, sampling and response parser in the candidate identity. A failed streamed-call parser or dropped history can look like a prompt failure. Test complete tool batches, interrupted streams, output headroom, semantic values and actual final delivery before drawing a performance conclusion.

Coverage includes model/release, migration, thinking, two open cards and coding/Flash prompting guidance. Serving recipes were linked but not run; mutable cards were not pinned. No host access, retention suitability, strict-schema guarantee, output quality, price or latency has been qualified. Recheck current exact controls and account availability at use; keep a useful prompt deliverable even when runtime acceptance is blocked.
