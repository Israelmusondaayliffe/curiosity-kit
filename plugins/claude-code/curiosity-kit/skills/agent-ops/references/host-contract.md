# Host, identity and ownership

Agent Ops supplies local methods and deterministic support, not a hosted execution service. Discover the actual host's child creation, messaging, status, cancellation and continuation tools before use. A source example naming create_thread, Agent or a model alias is not proof that this session supports it. Missing native delegation blocks the advisor's dispatch phase; design, audit and preparation can still return useful results.

## Artifacts and tools

Current official shape examples, checked 5 October 2026; confirm against the installed host before claiming loadability:

Claude project file `.claude/agents/scoped-reader.md`:
```yaml
---
name: scoped-reader
description: Inspect the assigned source and return evidence without artifact edits.
tools: Read, Glob, Grep
disallowedTools: Agent, Write, Edit
maxTurns: 12
---
Read only the assigned paths. Return cited findings and unresolved questions.
Stop when the assigned question is answered or required evidence is unavailable.
```
Adapt the task-specific limit and minimal tools. `effort` is optional and model-dependent; omitting a model pin preserves role selection. A turn-limit result can be partial, not completed. See [Claude subagent fields](https://code.claude.com/docs/en/sub-agents).

Codex project file `.codex/agents/release-notes-reviewer.toml` (filename stem and name match):
```toml
name = "release-notes-reviewer"
description = "Inspect assigned sources and return cited findings."
sandbox_mode = "read-only"
developer_instructions = "Read only the assigned sources. Report evidence and uncertainty. Do not edit artifacts or expand the task. Stop at the stated assignment boundary."
```
Current custom-agent files require name, description and developer instructions. Optional model settings use `model` and `model_reasoning_effort`; fill them only from the user's selection and observed host support. See [OpenAI subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents). Verify discovery in the actual isolated host; parsing alone is insufficient.

Claude Code commonly accepts Markdown agent definitions in an authorized project `.claude/agents/` or plugin `agents/` directory. Verify current frontmatter fields, tools and native dispatch behavior before claiming the artifact works. Codex reusable role configuration is version-dependent: inspect the installed supported schema before emitting TOML. Never copy historical `default_model`, `reasoning` or `instructions` fields solely because an old plugin contains them. A complete inline role brief can use supported native delegation without persistent global config.

Model and effort are requested settings; observed model/effort may be absent or differ. Preserve explicit selections, stop on a material contradiction and record unknown telemetry honestly. A host-issued child/session ID plus its actual result is evidence of the observed operation, not cryptographic proof of all settings. The local checker validates consistency; the parent must inspect real host records. Do not write invented create_thread attestations to satisfy a schema.

Read-only role restrictions reduce authority but do not establish an OS sandbox. Record actual accessible tools and permission boundaries. Reviewer receipt writes need their own narrow path grant. Output, raw evidence and state paths must remain within the approved workspace; private credentials and unrelated logs are not packaged.

## Explicit workflows and peers

Advisor activation requires the user's current explicit selection, not complexity or a route label. Quoted, conditional, revoked and negated requests do not activate it. Recheck before launch, continuation and integration. Native children remain under the parent; child instructions cannot expand authority.

Preserve the Claude source's Fable/Gauntlet mutual exclusion: an active mutually exclusive artifact-review workflow blocks this advisor activation. Check disclosed current workflow ownership and supported status before creating state. Unknown ownership blocks activation; do not encode unknown as peer_active=false. Supply actual disclosed peer paths, which the CLI protects from outputs. Do not infer `.gauntlet/state.json`, scan private sibling trees or require a sibling installation. Gauntlet can use arbitrary run directories, so no single guessed path establishes absence.

Optional Codex composition is permitted only when explicitly selected by the owning workflow. That outer owner retains approval, budget, state, integration, final answer and terminal verdict. Agent Ops contributes bounded assignments/evidence without becoming a second controller. Missing peers are normal standalone operation; no `.gauntlet` paths or private sibling validators are required.

## Context and recovery

Use native observed context metrics where available and retain their units. Do not invent a percentage or carry a historical threshold across models. Sparse status checks should follow meaningful events or blockers, not tight polling. Collect only terminal results; a launch acknowledgement is not completion. Continue only trusted same-or-narrower work with verified lineage and remaining budget; otherwise prepare a fresh bounded attempt after accounting for the previous child.

Source reading, local deterministic fixtures and actual host qualification are separate proof levels. Cowork handoff preparation does not qualify Cowork execution. No automatic installation, external service, account change or schedule is included.

## Method sources

Reauthored from the Codex and Claude Agent Ops editions, with methods from Lauren Tan's Pstack, Matt Pocock's skills and DietrichGebert's Ponytail. Anthropic's [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) supplies the simple-pattern design foundation; its dated examples do not establish current host APIs. Pstack's separate-writes/context principles and Matt's source-linked handoff method inform narrow ownership and continuity. Source study is not host qualification. No external method is a runtime dependency.
