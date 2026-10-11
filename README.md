# Curiosity Kit

*Independent skills for curious people.*

**[Download for ChatGPT](https://raw.githubusercontent.com/Israelmusondaayliffe/curiosity-kit/main/downloads/curiosity-kit-chatgpt.zip)** · [Upload and install](#chatgpt-web)

Curiosity Kit is a plugin for Codex and Claude Code. It brings together 26 independent skills for researching, writing, making decisions, building software, producing creative work and finishing multi-step projects.

Start with Chief of Staff when you want help choosing an approach. Go straight to a specialist when you know what you need. Each skill includes its own methods and supporting files, so using one doesn't require running the others first.

[Install](#install) · [First task](#your-first-task) · [Skills](#the-26-skills) · [Requirements and limits](#requirements-and-limits) · [Troubleshooting](#troubleshooting)

## Install

### ChatGPT (web)

1. Click **[Download for ChatGPT](https://raw.githubusercontent.com/Israelmusondaayliffe/curiosity-kit/main/downloads/curiosity-kit-chatgpt.zip)** and save the ZIP file. Keep it zipped.
2. On ChatGPT web, open **Plugins > Add > Upload plugin/archive**, when that option is available. Eligible workspace owners and administrators can use **Admin console > select workspace > Plugins > Add > Upload plugin**.
3. Choose `curiosity-kit-chatgpt.zip`, review the plugin, and select **Install** when shown.
4. Open a fresh chat, select **Curiosity Kit**, then choose **Chief of Staff** and describe what you want to do.

Upload requires permission or access as an eligible workspace owner or administrator. Availability varies by account, plan and workspace; not every personal account offers ZIP upload. If the option is missing, check with your workspace administrator. See OpenAI's [Plugins in ChatGPT instructions](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).

Use the ZIP linked above. GitHub's whole-repository **Download ZIP** and attaching a ZIP to an ordinary chat are not plugin installation.

This package has been checked for structure, resources and archive integrity. This exact public Curiosity Kit archive has **not yet been natively installed in ChatGPT**. All 26 skills and existing hooks are included; native hooks are unsupported in ChatGPT Cloud and will not provide local hook behavior there. Other workflows still depend on the tools and permissions available in your host. Read [Data handling](#data-handling) and [Cloud and hooks](#cloud-and-hooks) before use.

### Codex and Claude Code

Clone or download this repository, open a terminal in its root directory, and run the two commands for your host. Use an existing Codex or Claude Code installation. For a published Git marketplace, its repository URL can replace `.`.

### Codex

```sh
codex plugin marketplace add .
codex plugin add curiosity-kit@curiosity-kit
```

### Claude Code

```sh
claude plugin marketplace add .
claude plugin install curiosity-kit@curiosity-kit
```

After installation, check the plugin list and open a fresh session.

```sh
codex plugin list
# or
claude plugin list
claude plugin details curiosity-kit
```

Look for the enabled selector `curiosity-kit@curiosity-kit`. Check the loaded skill inventory as well. A plugin appearing in the list doesn't prove every skill loaded. There are 26 installed entries; Codex's implicit-discovery list may show only 21 because five entries require explicit selection.

No separate Curiosity Kit installer or mandatory setup interview is needed. For removal, use `codex plugin remove curiosity-kit@curiosity-kit` or `claude plugin uninstall curiosity-kit@curiosity-kit`. See [Cloud limits](#cloud-and-hooks) before assuming a local installation is available in a Cloud session.

## Your first task

### Let Chief of Staff choose

[Chief of Staff](skills/chief-of-staff/SKILL.md) is Curiosity Kit's Chief of Staff. Give Chief of Staff the result you need and the material you already have. Chief of Staff chooses the smallest useful method, coordinates work when needed and checks the finished result.

For example:

> Use Chief of Staff to turn these project notes into a one-page update for the team. Separate decisions from open questions, keep the dates exact, and leave anything that needs my choice unresolved. Save a draft here.

Chief of Staff's installed skill ID is `curiosity-kit:chief-of-staff`. In Claude Code, select `/curiosity-kit:chief-of-staff`. In Codex, use the entry available in the installed skill catalog. Use the actual installed entry rather than assuming a short alias.

A simple question can stay a simple answer. Chief of Staff doesn't require a plan file, interview or team of agents for every request.

### Pick a specialist directly

You can select any skill without going through Chief of Staff. Use your host's installed skill entry and describe the task in ordinary language.

These are good starting prompts:

- **Writing Like Me:** "Turn these notes into a 400-word article. Use these two pieces as voice references. Keep the argument mine, flag unsupported claims and return a complete draft."
- **Coding Studio:** "Fix this rounding bug through both callers. Show the failing regression first, preserve my staged changes and verify the repair."
- **Strategy Room:** "Compare these three launch options against our budget and deadline. Challenge the assumptions, explain what would change the recommendation and leave the final choice to me."
- **Data Storytelling Studio:** "Use this checked analysis to make a one-page decision memo and one chart. Keep the definitions and uncertainty visible."
- **Guide Production Studio:** "Turn this process into a workshop a colleague can run without me. Include a worked example, expected results and what to do when a step fails."
- **Continuity Vault:** "Prepare a handoff from these files and this conversation. Include the current state, unresolved effects, evidence links and the next safe action."

A useful brief names the result, source material, constraints and what the agent may change. Add a concrete check when it matters, such as "the test fails before the fix" or "another person can follow the guide without this conversation."

### Keep control of the work

Choosing a skill selects a method. Permission to send, publish, install, schedule or change an account still comes from your request and the host's controls. A request for a draft remains a draft.

Chief of Staff asks before choosing Operating Graph, Gauntlet or the Matt method library unless you've explicitly selected that method for the task. AI Film, ProofLoop and other methods with explicit activation rules keep those rules. Mentioning a method in a quotation or old document doesn't activate it.

## The 26 skills

The links open each skill's full instructions. You don't need to read the whole catalog before starting.

<details>
<summary>Choose a skill by the work you want to do</summary>

### Plan, research and decide

- [Chief of Staff / Chief of Staff](skills/chief-of-staff/SKILL.md): choose and coordinate methods, review agreed commitments, and inspect capability readiness.
- [Strategy Room](skills/strategy-room/SKILL.md): examine assumptions, compare alternatives and work through decisions before committing.
- [Knowledge Work Superpowers](skills/knowledge-work-superpowers/SKILL.md): investigate substantial questions across sources and produce complete, evidence-backed work.
- [Last30Days](skills/last30days/SKILL.md): research recent public evidence and work with selected local research records and briefs.
- [Founder Revenue Engine](skills/founder-revenue-engine/SKILL.md): interpret business signals, clarify customers and offers, and prepare commercial work.
- [Matt method library](skills/matt-pocock-knowledge-work/SKILL.md): explicitly selected Matt Pocock methods for interviews, specifications, engineering, research, teaching and writing. It preserves 39 named methods through 38 local playbooks.

### Write, explain and create

- [Writing Like Me](skills/writing-like-me/SKILL.md): draft and revise in an evidenced voice, develop ideas, check claims and review complete pieces.
- [Explanation Studio](skills/explanation-studio/SKILL.md): explain a specific gap in understanding or teach from what the reader already knows.
- [Guide Production Studio](skills/guide-production-studio/SKILL.md): create practical guides and workshops with examples, checks and recovery steps.
- [Data Storytelling Studio](skills/data-storytelling-studio/SKILL.md): turn checked findings into decision-focused narratives, charts and presentations.
- [Visual Production Studio](skills/visual-production-studio/SKILL.md): develop image and video prompts, references, boards and media deliverables with the required tools.
- [AI Film Studio](skills/ai-film-studio/SKILL.md): explicitly selected film planning and craft, including scenes, shots, acting, geography and compiled prompts.

### Build and improve tools

- [Coding Studio](skills/coding-studio/SKILL.md): explore, implement, debug, refactor, review and verify software.
- [Web Product Studio](skills/web-product-studio/SKILL.md): design and build web products, then check their actual browser behavior.
- [Harness Engineering](skills/harness-engineering/SKILL.md): build and audit assistant instructions, skills, plugins and their tests.
- [Model Prompt Lab](skills/model-prompt-lab/SKILL.md): create, migrate, diagnose and compare prompts and model behavior.
- [Agent Ops](skills/agent-ops/SKILL.md): design or audit reusable agents, tools, roles and handoffs.

### Carry work through and check it

- [Outcome Engine](skills/outcome-engine/SKILL.md): take an accepted direction through checked work and finished deliverables.
- [LoopKit](skills/loopkit/SKILL.md): run bounded feedback loops and resume interrupted work from recorded state.
- [Operating Graph](skills/operating-graph/SKILL.md): explicitly selected execution with dependencies, approvals, joins and one controller.
- [Gauntlet](skills/gauntlet/SKILL.md): explicitly selected improvement or verification against an external standard, with independent review.
- [ProofLoop](skills/proofloop/SKILL.md): explicitly selected work against agreed criteria, with separate approval for reusing lessons.
- [Loop Observatory](skills/loop-observatory/SKILL.md): read and compare selected runs, their evidence and available cost records.

### Preserve and learn from work

- [Continuity Vault](skills/continuity-vault/SKILL.md): create portable handoffs, digests and source-backed continuation records.
- [Memory](skills/memory/SKILL.md): retrieve scoped prior work or diagnose memory readiness through a separately installed Claude Mem engine.
- [Practice Compiler](skills/practice-compiler/SKILL.md): examine a selected, dated body of work and propose improvements supported by recurring evidence.

</details>

## Requirements and limits

Curiosity Kit supplies skill instructions, local support files and host integration. Your host supplies models, permissions, worker tools, filesystem access and any connected services.

- Research needs the relevant sources or available search tools. Private sources need their own authorized connection.
- Browser checks and media production need the actual browser, renderer or provider used by the selected method. Writing a prompt or storyboard doesn't generate the media.
- Memory requires the external Claude Mem engine and a supported host integration. Curiosity Kit doesn't install or configure that engine.
- Independent review needs a separate available reviewer. A second pass in the same context is self-review.
- Monitoring and recurring work need a supported scheduler and your authorization. Installing a skill doesn't start a background service.

Each skill documents its specific prerequisites. Curiosity Kit doesn't supply credentials, connect accounts or override host restrictions. It doesn't pin one model for all work; exact capabilities still depend on the selected model and environment.

### Data handling

The selected skill can read user-authorized files, session exports and memory records, and save local drafts, research records, logs, checkpoints or reviewed learning records. These can contain personal or sensitive information. Local records remain until you or your environment removes them; the plugin provides no universal deletion deadline. Local scripts and two native hooks support these workflows. The package declares no MCP server.

Your Codex or Claude Code host processes task content through its configured model and tools. Requested workflows can send prompts, references or selected content to third parties, including OpenAI Images, Google Gemini and Midjourney, through available host tools, connectors or browser operations. Some caption and motion HTML templates load GSAP from jsDelivr when opened, causing browser requests to that CDN independently of host connectors. Each selected service has its own privacy policy, account controls and retention rules.

Memory uses a separately installed Claude Mem engine. Its capture, local storage, configured model provider and optional cloud sync have their own settings; cloud sync can transmit observations and full prompts. Installing Curiosity Kit does not install that engine or enable cloud sync.

Curiosity Kit has no creator-operated data-collection endpoint or bundled analytics service. Its creator receives no task data through the plugin and therefore holds no developer-service copy to retain. This does not replace your host's or other providers' data policies. Review the selected method and destination before sending sensitive content.

### Cloud and hooks

The source edition was qualified on local Codex and Claude Default Cloud, with local installation/removal checks on both hosts. This depersonalized candidate receives package and privacy checks; those do not establish a fresh native run of every workflow. See [candidate readiness](READINESS.md) for the actual scope and remaining limits.

- Claude Default Cloud evidence covers session-only loading with `--plugin-dir` and an actual SessionStart. Persistent Cloud installation remains unverified.
- Codex Cloud installation and execution remain unverified. The attempted environment was offline and had a read-only installation profile.
- Cloud use requires the host CLI, repository access and an installation location that the environment allows. A local install doesn't establish Cloud loading.
- Codex discovered `sessionStart` and `preCompact` hooks as untrusted. Review and approve them through Codex's normal hook controls before expecting execution. Fresh combined Codex hook execution remains unrun; earlier unchanged LoopKit evidence is documented separately.

These checks support the recorded release scope. They don't establish that every workflow, provider, desktop interaction or production setup has been tested.

## Troubleshooting

**The marketplace can't be added.** Confirm that the selected host can access this repository using its existing authorized GitHub authentication. Check the actual Cloud environment separately from your computer. Don't paste credentials into prompts or files.

**The plugin is listed but a skill seems missing.** Open a fresh session and inspect its loaded skill inventory. Explicit-only skills may be absent from an implicit-discovery list. Use the installed `curiosity-kit:<skill-id>` entry through the host's supported mechanism. Check the host’s installed catalog and exact plugin namespace.

**Chief of Staff or a former method name isn't a command.** Chief of Staff's technical ID is `chief-of-staff`. Many former skill names are now methods inside one skill. Open that skill's instructions for the method map rather than assuming every method has its own slash command.

**A skill reports a missing tool or permission.** Check its prerequisites and the host's actual tool list. Install success doesn't mean a provider, browser or memory engine is available. Keep any useful preparation and resolve the specific blocker before relying on that step.

**A hook doesn't run.** Check registration and trust in the host that should execute it. Registered, trusted and actually executed are different states. Follow the hook guidance above rather than treating plugin installation as proof of execution.

For rollback, preserve your work and existing configuration, remove only this plugin, and reinstall your recorded prior version through the host. Remove the marketplace only if nothing else uses it: `codex plugin marketplace remove curiosity-kit` or `claude plugin marketplace remove curiosity-kit`.

## Build and contribute

The source is in `skills/`; `adapters/` supplies host metadata. Build with Python 3.9 or later:

```sh
python3 -B build/package.py --out build/out
```

The builder validates both combined packages and each standalone skill. It does not install anything. Committed `plugins/` payloads must match the build. See [contributor notes](AGENTS.md) and [readiness](READINESS.md).

## Credits and licenses

Methods draw on multiple sources, including Pstack / Poteto Mode, Matt Pocock, Emil Kowalski and other credited creators. Original contributions use the [MIT License](LICENSE). Third-party material keeps its own terms, including scoped MIT, Apache, CC BY-SA, font and vendor licenses. Keep the skill-local notices and licenses. Names in those credits identify creators, not assumptions about the person using this plugin. Asset-specific rights and external dependencies remain part of each skill’s contract.
