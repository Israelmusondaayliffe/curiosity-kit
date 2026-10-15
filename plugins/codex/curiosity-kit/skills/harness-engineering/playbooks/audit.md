# Audit

Read the current harness and report what is true, what is risky and what needs a decision. Change nothing.

## Steps

1. Resolve the platform and read its section of [platforms](../references/platforms.md). On Cowork the harness lives in the connected folder, not the sandbox home.
2. If the harness has its own trusted, already-authorized deterministic check script (a smoke or validation script the workspace contract names), inspect its scope and side effects, then run it when permitted. A source README does not authorize unfamiliar code execution. Each failure is a verified finding with the script output as evidence; do not re-derive by hand what it already proves.
3. Run the inventory:

```text
python3 scripts/hectl.py audit --platform claude-code|cowork|codex [--home PATH] [--workspace PATH] --output AUDIT.json
```

It records the instruction files in load order, each marked `effective` or not (Codex uses one file per directory, `AGENTS.override.md` first; Claude Code loads every `CLAUDE.md` from the filesystem root down to the workspace), with imports; settings and config key names (secret-like names redacted, values never read into the report); hooks and MCP servers, each with the sources it inspected and the ones it did not; skills, plugins with enabled state, agents, commands, scheduled tasks and memory presence. An empty `found` list means nothing was found in the inspected sources, not that the surface is absent; read `not_inspected` before saying so. Its `verified_findings` cover dead imports, dead path references, placeholders, duplicate skill names, a missing folder contract and an empty chain. Date or named path templates (`YYYY-MM-DD`, `{name}`) are not reported as missing files. A single-segment reference such as `/contract-check` is resolved against the host's commands and skills; an unknown one is an `unverified-command-reference`, not a dead path. With `--platform auto`, the command refuses to guess when both Claude Code and Codex are installed and nothing says which one is running.

   Static audit reports configuration, not runtime. Add `--readiness` for opt-in runtime checks, each reported as pass, fail or unknown:
   - **Native hooks.** With `--native-hooks` on Codex, it reads `codex app-server` hooks/list for the selected home only. An enabled, unmanaged hook that is not trusted fails. Enabled hooks that are byte-identical, or that come from the same plugin installed from two sources, fail. Hooks from different sources sharing an event are unknown, because overlapping purpose cannot be ruled out. A malformed or unavailable listing is unknown. Claude Code has no supported trust reader, so its hook status is always unknown.
   - **Registry.** `--registry FILE` checks for repeated section headings. On Claude Code it also lists scheduled-task folders the registry does not name. That listing is inventory only (unknown), because a folder may be paused history. Native enabled, paused and permission-mode state stays unknown.
   - **Routine.** `--routine-state FILE` passes only when the last run completed with zero failures and its receipt matches this host and home: dry-run mode, complete status, no stop reason, no unverified checks, and an empty `deleted` list. A success without that receipt fails.

   Output is allowlisted and the native listing is time-bounded (`--readiness-timeout`). A readiness pass is evidence about the selected home at that moment, not proof of native event delivery; that needs the acceptance sequence in [verification](verification.md).
4. Read instruction files and prose directly, but take settings, config, env and credential files only from the report: never print their raw contents. Then read what the script cannot judge: conflicting instructions between layers, duplicated ownership of one job, stale paths described in prose, hooks or permissions nobody reviewed, assumptions ported from another platform, and claims with no evidence behind them.
5. Run the over-constraint pass from [context subtraction](context-subtraction.md) on the chain. Prioritize findings by source-backed impact and risk, not scanner category or model-generation claims.
6. Classify each finding by layer (information, execution, feedback; see [architecture](../references/architecture.md)) and by kind: verified fact, inferred risk, or decision for the user.

Stay read-only for the whole audit. Do not run `hectl cleanup`, `apply` or `run` here, even as a dry run: a cleanup dry run writes its receipt inside the home. Record stale data as a finding and leave the dry run to [maintenance](maintenance.md).

Before a new build, use [research](research.md) to resolve design-changing uncertainty and [interview](interview.md) to confirm the remaining user decisions. A settled narrow change can reuse those answers; a broad build cannot skip its substantive discovery.

## Output

`AUDIT.json` plus a short gap summary: verified facts first, then risks, then decisions needed. Never include credential values or private connector content.

## Promote repeats

A finding class seen in two or more audits belongs in the harness's own check script, not in a longer checklist. When the fix is deterministically checkable (registry parity, scope drift, version drift, dead references, output hygiene), propose the script addition as the fix. A harness with no check script gets one as its first proposed fix.
