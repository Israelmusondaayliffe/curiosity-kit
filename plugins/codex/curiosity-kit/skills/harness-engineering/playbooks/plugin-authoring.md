# Plugin authoring

Create, update, validate, package or install a plugin the approved architecture calls for. Manifests and install paths differ per host, so resolve the host first with [platforms](../references/platforms.md). Track each reviewed source revision. Use a new release version when distributing a changed package or when the current host requires it for cache refresh; ordinary unpublished edits can share a working version.

For a single `.skill` archive, use the declared-file [standalone packaging method](skill-authoring.md#package-a-standalone-skill). Do not wrap a plugin manifest into that format or infer native installation from archive validity.

## Shared steps

1. Confirm a plugin is justified rather than a standalone skill: several related skills, lifecycle components, or distribution.
2. Define the owned skills, the front door, external tools, hooks, agents and explicit exclusions. Include only manifest component fields backed by real files.
3. Validate every skill with [skill authoring](skill-authoring.md) rules, then the plugin:

```text
python3 scripts/hectl.py plugin-check PLUGIN_DIR --host claude-code|codex
python3 scripts/hectl.py listing-budget PLUGIN_DIR --namespace PLUGIN --context-tokens N
```

4. Bind the package to its exact source revision and choose the release version before distribution. Verify the current host's cache/update rules.
5. Prove visibility in a fresh session after install, not from files on disk.

## Claude Code

- Manifest at `.claude-plugin/plugin.json`; skills under `skills/`, optional `agents/`, `commands/`, `hooks/hooks.json`, `.mcp.json`.
- Try it without installing: `claude --plugin-dir PATH`. Validate with `claude plugin validate PATH`.
- Install through `/plugin` or `claude plugin install` from a marketplace; marketplace installs cache under `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`. Compare source and cache with `hectl parity SOURCE CACHE_DIR`.
- A plugin hook runs in every session where the plugin is enabled. Make a plugin hook act only when its own workflow is active.
- The Claude desktop app loads plugins from its own store, separate from the CLI cache. Prove desktop behavior in the app itself.

## Claude Cowork

- Package the plugin directory as a deterministic ZIP with `.claude-plugin/plugin.json` at the archive root, then upload it through the app's custom-plugin flow or a configured marketplace.
- Static archive checks prove structure only. Claim installation or discovery only after seeing it in the current app.

## Codex

- Manifest at `.codex-plugin/plugin.json` with an `interface` block; each skill carries `agents/openai.yaml`. Local development versions may take a `+codex.<digits>` suffix to refresh the cache.
- Use the system `plugin-creator` skill when installed; if it is absent, author the manifest directly and say so.
- Install with `codex plugin marketplace add` and `codex plugin add`; inventory with `codex plugin list --json`; cache under `~/.codex/plugins/cache/<marketplace>/<name>/<version>/`. Compare with `hectl parity`.

## Visibility policy

Use implicit discovery only for workflows intended to start from ordinary requests. Preserve explicit-only boundaries for governed workflows. Before reducing an owned specialist's visibility, distinguish user invocation, model invocation and direct resource loading under the actual host contract. Prove the intended front-door route and explicit route separately; a local playbook can provide the method without a foreign-skill dependency. Roll visibility changes out in reversible waves and capture the actual model-facing listing, including truncation. Details are in [subtraction protocol](../references/subtraction-protocol.md).

Creating a public repository or submitting to a marketplace is a separate external action with its own approval.
