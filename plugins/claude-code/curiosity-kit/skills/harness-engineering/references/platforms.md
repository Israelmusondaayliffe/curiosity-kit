# Platforms

The dated material below is compatibility guidance carried from source review, not proof of the current user's installation. Platforms change; confirm against the live environment or official documentation before a change depends on one, and treat anything not listed as unknown.

The dated sections below are compatibility notes, not a live capability catalog. Discover whether the selected environment supplies Codex, Claude Code, connected-folder Chat/Cowork, or another supported surface. Retain useful connected-folder/cloud methods without assuming CLI access or claiming independent qualification from a product name. `cowork` remains a legacy CLI/schema value for compatibility.

Invocation is host-specific: distinguish the user's ability to invoke a method from model-initiated discovery. Claude Code documents both `disable-model-invocation` and `user-invocable`; Codex uses its own policy metadata. Read current official contracts and inspect actual loading before changing either. No donor claim that hidden methods are universally unreachable substitutes for that check.

## Detection

`python3 scripts/hectl.py detect` reports its signals and a verdict: Cowork when the sandbox paths exist; Claude Code when running inside a Claude Code session (`CLAUDECODE=1`); otherwise the only installed host, or `ambiguous` when both Claude Code and Codex are installed. Installation alone never decides which host is running. On `ambiguous`, ask or pass `--platform`; an explicit `--platform` always wins. Each platform a user runs is its own harness scope.

## Claude Code (source compatibility notes dated 2026-10-03; recheck the selected CLI/Desktop version)

- **Instruction chain**, broadest first: managed policy (`/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS, `/etc/claude-code/CLAUDE.md` on Linux), `~/.claude/CLAUDE.md`, project `CLAUDE.md` or `.claude/CLAUDE.md`, `CLAUDE.local.md`, then nested `CLAUDE.md` files loaded when their directory is read. `@path` imports expand at launch, up to four levels deep.
- **Home and settings**: `~/.claude/`, or `CLAUDE_CONFIG_DIR`. `settings.json` (user), `.claude/settings.json` (project), `.claude/settings.local.json` (local). Settings hold permissions, hooks, env, model, `enabledPlugins` and `skillOverrides`.
- **Skills**: `~/.claude/skills/`, `.claude/skills/`, plugin skills namespaced `plugin:skill`. Frontmatter adds `disable-model-invocation` (hides the skill from the model, from subagent preload and from scheduled firing; the user can still type `/name`), `user-invocable`, `when_to_use` and others.
- **Skill listing**: every skill name is listed; descriptions share a budget of 1% of the context window (at 4 characters per token: about 8,000 characters at 200K, 40,000 at 1M). Each description plus `when_to_use` is cut at 1,536 characters. Over budget, descriptions survive by recent use and the rest become bare names. `skillOverrides` can hide or shorten personal and project skills but not plugin skills.
- **Plugins**: `.claude-plugin/plugin.json`; skills, agents, commands, `hooks/hooks.json`, `.mcp.json`. `claude --plugin-dir PATH` loads a plugin for one session without installing it. `claude plugin validate PATH`. Marketplace installs cache under `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` and register in `~/.claude/plugins/installed_plugins.json`.
- **Desktop app**: Code-tab sessions load plugins from the app's own store fed by claude.ai uploads and marketplaces, together with the CLI set. Store rows are not enabled plugins. Prove desktop behavior in the app.
- **Hooks**: events include SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop and SessionEnd; types command, prompt and agent; exit code 2 blocks. Plugin hooks fire in every session where the plugin is enabled.
- **Health**: `claude doctor` and `/doctor`.
- **Session isolation for tests**: `--setting-sources` limits which settings files load, `--plugin-dir` adds a plugin, `--no-session-persistence` keeps no transcript, `--strict-mcp-config` with an empty config drops MCP servers. `--bare` skips hooks, plugins sync and CLAUDE.md but needs an API key rather than a subscription login.

## Claude Cowork (source compatibility notes dated 2026-07; recheck the selected surface)

- Tasks run in a managed sandbox or local VM; the session filesystem disappears afterwards. Durable state lives in a connected folder, app-level instructions, or an external system.
- **Instruction layer**: global instructions in app settings, plus contract files at a connected-folder root. The global instructions must tell Claude to read the folder contract, because folder files do not load themselves.
- Uploads appear read-only under `/mnt/user-data/uploads/`. A file reaches the user only through explicit delivery or by committing it to a connected folder.
- **Plugins**: a ZIP with `.claude-plugin/plugin.json` at the root, uploaded through the app or a configured marketplace; cached into sessions under `~/.claude/plugins/synced/`. Namespaced plugin skills outrank loose copies.
- **Enforcement**: validator scripts stored in the connected folder and run by contract; lifecycle hooks are effectively unavailable. **Automation**: scheduled tasks created in a session.
- **Proof**: structure in the sandbox, behavior in the live app (plugin list, a fresh task's inventory, the session actually reading the contract).

## Codex (source compatibility notes dated 2026-10-03; recheck the selected host)

- **Instruction chain**: the home's `AGENTS.override.md` when it has content, otherwise its `AGENTS.md`; then, for each directory from the project root (nearest ancestor with a root marker, `.git` by default, set by `project_root_markers`) down to the working directory, the first file found among `AGENTS.override.md`, `AGENTS.md` and any `project_doc_fallback_filenames`. Without a root marker only the working directory is read. Source: `codex-rs/codex-home/src/instructions/mod.rs` and `codex-rs/core/src/agents_md.rs` in openai/codex, read 2026-10-03.
- **Home**: `CODEX_HOME`, default `~/.codex/`; `config.toml` holds configuration (audit key names only).
- **Skills**: `~/.codex/skills/`, system skills under `~/.codex/skills/.system/` (skill-creator with `init_skill.py` and `quick_validate.py`). The validator accepts only `name`, `description`, `license`, `allowed-tools` and `metadata` in frontmatter, requires a hyphen-case name up to 64 characters, and caps the description at 1,024 characters with no angle brackets. Per-skill `agents/openai.yaml` carries the display name, default prompt and `policy.allow_implicit_invocation`.
- **Plugins**: `.codex-plugin/plugin.json` with an `interface` block. `codex plugin marketplace add`, `codex plugin add`, `codex plugin list --json`. Cache under `~/.codex/plugins/cache/<marketplace>/<name>/<version>/`. Local development versions take a `+codex.<digits>` suffix to refresh the cache. A system `plugin-creator` skill may or may not be installed; check before relying on it.
- **Autonomy and enforcement**: Goals, Automations, rules and hooks (hooks need explicit trust). Browser and Computer Use are optional bundles; test them only when the harness depends on them.
- **Proof**: skill validator, installed listing, source-cache parity (`hectl parity`), and discovery in a new task.
