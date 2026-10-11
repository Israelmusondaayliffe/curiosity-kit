# Select a dated provider reference

Documentation snapshot: 2026-10-09 UTC. These references are original working summaries of official sources, not provider manuals, runtime qualification or a model ranking. Load only the chosen provider and relevant model/interface sections. A prompt can be drafted while API access is unresolved; label configuration and live acceptance pending.

## First resolve the target

Record the user's model name verbatim, resolved provider/model ID (or unresolved UI label), version/snapshot, host/product, endpoint, region/tier where relevant, available tools, and check date. Do not convert "Astro" into Astra or invent an API slug. Preserve a named older target instead of upgrading it. Resolve an ambiguous alias through the actual selected interface, or ask the smallest necessary question.

Keep goal, evidence, output, authority, verification and stopping conditions in the common prompt. Add only the applicable model adjustment. API fields belong in a separate configuration artifact. Prose cannot enable tools, enforce schemas, preserve encrypted state, enlarge context, or grant permission. A model on another provider's host needs both its model guidance and the actual host contract.

## Branch directory and coverage

- [OpenAI](providers/openai.md): GPT-6 Astra, GPT-6.1 Sol, GPT-6 Luna; historical GPT-5.6/5.4 and Astra migration distinctions. Current catalog routes flagships to a shared family guide, with separate model support pages. No additional dedicated Sol/Luna prompting guide was found.
- [Anthropic](providers/anthropic.md): Fable/Mythos 5.1, Opus/Sonnet/Haiku 5.5; retained Fable 5, Opus 5/4.8 and Sonnet 5 guide differences. General guide and all eight model-specific guides linked from it were substantively read; selected migration sections, not all subsidiary references, were covered.
- [Google](providers/google.md): Gemini 3.8 Flash, 3.1 Pro and customtools, inherited 3.5/3.6 migration, Live. Interactions and legacy Generate Content are different branches.
- [Mistral](providers/mistral.md): Large 4, Medium 3.5, Small 4; API/Studio versus open-weight deployment. No dedicated Large 4 prompting guide located; generic sampling tabs and Medium's system-template fetch were incomplete.
- [Meta](providers/meta.md): Spark API, Glimmer self-host and Llama 4 remain separate. Spark protocol/task cookbooks are covered; no standalone general Spark prompt guide located. Cookbook version labels and effort tables contain conflicts.
- [xAI/SpaceXAI](providers/xai.md): Grok 4.7, historical 4.6/4.5/multi-agent distinctions, Realtime. Model/capability guides supply text guidance; voice has its own prompt guide.
- [DeepSeek](providers/deepseek.md): V4.1 Flash and still-active V4 Pro; official API versus native encoders. Chinese thinking guide read; English equivalent and dedicated vision guide were inaccessible.
- [Qwen](providers/qwen.md): 3.8 Max, Flash/Flash-Next, Omni HTTP and Realtime; regional Model Studio/Qwen Cloud versus open weights. Open/API parity is not assumed; smaller companion variants and open Omni deployment are outside this bounded pass.
- [Moonshot/Kimi](providers/kimi.md): K3, K2.7 Code, K2.6; API and K3 open model. Search-path readiness and self-host video preprocessing remain unresolved.
- [Z.ai](providers/zai.md): GLM-5.3 and Flash/FlashX; standard API, Coding Plan, self-host, and third-party host differences.

Coverage means a catalog-to-applicable-guide study of general text, reasoning, coding, multimodal understanding and selected conversational audio. It does not mean every official page, every SDK tab, deployment, model variant, fine-tuning recipe or standalone image/video/music generator. The eight supplemental providers contributed 85 official source records, including catalogs and operational pages, not 85 distinct prompting guides. OpenAI and Anthropic have separate coverage. Source dates below are access dates unless explicitly labeled publication, update or release.

## Verify before applying

1. Reopen the current catalog, exact model page and applicable migration page for mutable names or controls. Prefer exact current model/interface guidance over older generic examples. Keep contradictions visible until resolved.
2. Distinguish a mandatory compatibility repair from a prompt hypothesis. Record whether evidence is documentary, manually inspected, synthetic or observed through the actual host.
3. Check parameter placement and allowed values, tool selection, schema subset/refusal/truncation behavior, output accounting, history/state replay, retention/access requirements and renderer behavior. Equal effort words do not mean equal compute.
4. Preserve full permitted response/tool identities and opaque state only as documented. Do not ask for private reasoning or synthesize missing state. A readable handoff summary is not a substitute for a required opaque block.
5. Test the actual failure: semantic correctness, complete item coverage, real tool execution, visible delivery, interruptions, permission boundaries and total cost/latency. A valid JSON object or HTTP success is insufficient.

No reference establishes this user's model access, measured quality, current prices, retention eligibility or native integration. If unavailable, deliver the useful prompt and explicit unresolved checks without claiming success or substituting a favored model.
