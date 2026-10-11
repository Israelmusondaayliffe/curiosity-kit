# Health and supported recovery

## Diagnose the failing layer

Use the [host contract](../references/host-contract.md). Keep checks read-only. Check the installed public diagnostic first; do not run an installer through a package runner merely to obtain a status command.

Separate:
1. Host registration and native hook availability.
2. Worker reachability/version and MCP tool availability, recorded independently.
3. Existing storage/schema and historical inventory.
4. Observer provider readiness, as reported by its supported non-secret interface.
5. Fresh event capture, generated observation, scoped retrieval and actual fresh-session injection.

A healthy process or historical count only addresses its own layer. Tool skew can coexist with a healthy worker. No minimum version replaces a current tool-presence check.

## Local read-only diagnostic

Python 3.11+ is required for the packaged standard-library diagnostic. Consult its actual arguments:

```sh
python3 <skill-dir>/scripts/memory_health.py --help
```

For a caller-selected isolated Codex configuration and data directory:

```sh
python3 <skill-dir>/scripts/memory_health.py --platform codex --config "$HOST_CONFIG" --data-dir "$MEMORY_DATA" --plugin-id "$MEMORY_PLUGIN_ID" --port "$MEMORY_PORT" --json
```

Use `--platform claude` with the selected Claude JSON settings file. `--plugin-id` selects the exact engine alias discovered in the current host registration. Omitting it uses documented compatibility fallbacks, not an inferred installation identity. `--skip-worker` makes no HTTP probe and leaves readiness incomplete, exit 2. With no explicit paths, the command uses the host's normal configuration and `CLAUDE_MEM_DATA_DIR` or `~/.claude-mem`; qualification must always supply isolated paths.

Host configuration and engine settings are different. `--config` takes the actual host configuration used for registration; never pass the engine's `settings.json` as registration evidence. For CLI/plugin-dir-only registration or inaccessible host settings, report registration as unknown and use observed tools and the actual native profile to describe what is available. Do not fabricate settings or diagnose an engine failure from the wrong input. Missing exact registration in a supplied real host configuration remains a failure.

The script checks specified configuration, storage and local worker readiness. It does not read observation bodies, credentials or transcripts, start services, scan for test markers, repair state, or make model calls. Its status vocabulary is pass/fail/unknown/skipped. Exit 0 means the requested readiness checks passed, not that capture or MCP delivery works; 1 means an observed failure; 2 means invalid, unsupported or incomplete diagnosis. Skipping a requested check leaves incomplete evidence.

Use explicit disposable data/config paths during qualification. Do not fall back to production if isolated host configuration is missing. A read-only storage limitation, including unsafe-to-inspect WAL state, is unknown rather than a corrupt-engine finding. Do not add snapshot or restore machinery to get a green status.

## Recovery boundaries

Identify whether an event reached the hook spool, the worker's in-memory processing, committed SQLite or the search index. Spool acknowledgment is not a generated observation. A restart may lose in-flight RAM work; a raw-spool replay is not automatically safe or authorized.

Use only a recovery operation verified for the installed engine and current task. Do not copy old pending-queue commands from upstream documentation when the installed architecture differs. If the supported route is unknown, return that precise gap.

Do not infer an installed general backup/restore command from historical source notes. Discover a supported version-correct route; offer no fabricated restore operation. Backup, export, import, service restart, updates, cloud sync, log clearing, project merging and configuration changes are engine administration; obtain the required explicit authority and version-correct procedure first. Never apply a historical migration's copy-back hint as a general restore.

When asked whether capture works now, readiness alone leaves it unproven. Reuse a harmless event from the user's authorized real task, or obtain scope for one small uniquely marked workspace event. Through available supported interfaces, observe its native handoff and generated record, then use scoped search and selected detail to confirm the event's project, host and freshness. A spool acknowledgment alone is insufficient; report any stage you cannot observe. Fresh-session injection requires observed delivery in a real subsequent host session, not a context preview or an assumed fresh subagent. If you cannot open that session within current authority, report injection specifically unverified and request only the necessary host step. Do not add a scanner, runner, state store, invented job tool or extra model call.

## Return

Report the failed or unproven layer, observed identities, check scope and next smallest supported action. Do not claim recovery or production isolation from source inspection alone.
