# Durable hook selection

After initializing or explicitly selecting a run, bind it to the actual workspace. This writes one owned pointer in LoopKit's state directory. An ordinary child-shell command can persist selection for a later startup/resume hook. It changes no host settings, registration, trust or schedule.

```sh
python3 "$LK" bind "$RUN" --workspace "$WORKSPACE" --host codex
python3 "$LK" unbind "$RUN" --workspace "$WORKSPACE" --host codex
```

Use `claude-code` on that host. Bind validates the snapshot's host, canonical workspace and run identity. A different selected run is a conflict; replacement requires `--replace-run OLD_RUN`, naming that exact selection. Rebinding the same run is idempotent. There is no newest-run scan.

## Root and precedence

Explicit `--state-root` wins, then `LOOPKIT_STATE_ROOT`. Without either, use the host's own home: `$CODEX_HOME/loopkit` (or `~/.codex/loopkit`) on Codex, and `$CLAUDE_CONFIG_DIR/loopkit` (or `~/.claude/loopkit`) on Claude Code. Bind from a shell with the same home variables as the host session, and check the `pointer` path that bind returns. CLI and hook must resolve the same root. A child-shell-only override cannot configure a future parent hook; use the documented default or an override already provided to the host/test environment. No cross-host fallback or synchronization occurs.

Pointer: `bindings/HOST/SHA256_OF_CANONICAL_WORKSPACE.json` beneath that root. It records schema, LoopKit ownership, host, workspace, exact canonical run path and run id, with an integrity digest. Bind/unbind serialize pointer changes and publish atomically. Intentional root aliases, including macOS `/tmp` to `/private/tmp`, are canonicalized; symlink substitution inside the binding directory or at the pointer is rejected.

Hook selection order: an explicit `--run` written into the host registration, otherwise this exact workspace pointer. No environment variable selects a run: a stray exported value would otherwise reach every session on the host. A bad explicit selection errors rather than falling back. Pointer identity is checked against the actual snapshot. No pointer or a terminal selected run is inactive. Missing/corrupt runs, changed run identity and malformed/wrong-scope pointers produce a concise visible diagnostic.

## Cleanup

Unbind requires the exact selected run and validates ownership, host and workspace. It removes only that pointer: run state, evidence, other workspaces and host bindings remain. Missing selection is a no-op. Conflicting or malformed pointers are not silently deleted. A valid owned pointer may be removed even if its target run is now missing. Terminal cleanup is explicit, not automatic.

Module API: `bind(run, workspace, host, supplied=None, replace_run=None)`, `resolve(workspace, host, supplied=None)`, `unbind(run, workspace, host, supplied=None)`. `supplied` is the explicit state-root path. Resolve returns the validated nonterminal run or `None`; errors propagate to the hook's visible diagnostic.
