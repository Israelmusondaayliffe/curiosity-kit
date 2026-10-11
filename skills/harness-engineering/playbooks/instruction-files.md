# Instruction files

Design, rewrite, split or check agent instruction files: the CLAUDE.md chain on Claude Code, folder contract files on Cowork, the AGENTS.md chain on Codex. The discipline is the same everywhere; file names, load order and import rules are not, so read the platform's section of [platforms](../references/platforms.md) first.

## What belongs where

| Content | Home |
| --- | --- |
| Stable personal policy explicitly intended across workflows: identity, voice, fabrication boundaries and universal authority rules | Global layer (`~/.claude/CLAUDE.md`, Cowork app instructions, Codex home `AGENTS.md`) |
| Writable zones, output paths, project loading, workspace verification entry points | Workspace layer, as a delta only |
| Project commands, constraints, acceptance | Project or nested layer |
| Detailed workflows and conditional detail | A skill or a linked reference |
| Exact paths, formats, validations | A script, hook, rule or template |

Place each rule in the smallest scope that serves its consumers. Never promote workflow-specific authority into global policy merely to remove duplication. Avoid repeating rules already inherited reliably. Independently executed prompts and skills must retain essential rules unless loading a shared contract is guaranteed and verified in each execution path. Duplication across independent consumers may therefore be necessary; remove it only after proving that scope, access and behavior remain intact. Spend tokens on gotchas that cost time when missed; cut what the file system already shows and what testing shows the selected model handles without the rule. Keep user policy and taste even when it reads like a rule. See [context doctrine](../references/context-doctrine.md).

## Workflow

1. Resolve the chain with `python3 scripts/hectl.py audit`; it lists files in load order with their imports and flags dead imports and paths.
2. Use [context subtraction](context-subtraction.md) to identify evidenced duplication and obsolete guidance. Add a missing load-bearing requirement when needed; deletion is not a prerequisite or a quota.
3. Keep only repeated behavior that truly needs persistent instruction. Move workflows into skills or references and exact checks into mechanisms.
4. Separate global personal policy from workspace layout and project commands.
5. Preserve load-bearing rules and show a diff. Name every removal and its reason; an unexplained cut gets reverted.
6. Check that closer files refine rather than silently contradict broader ones. On Cowork, check that the global instructions tell Claude to read the folder contract, since folder files do not load themselves.

Templates live in `assets/templates/`: `claude-global.md`, `claude-project.md` and `cowork-contract.md` for Claude platforms, `agents-global.md`, `agents-workspace.md` and `agents-project.md` for Codex. Replace every bracketed field; `hectl skill-check` and `hectl audit` flag leftover placeholders.

Treat size as a diagnostic. Accept a reduction only against the behavior cases in [subtraction protocol](../references/subtraction-protocol.md). Apply the result through [plan](plan.md) and [build](build.md).
