# Verification

Verify the requested result without repairing it during the verdict pass. This method belongs to Harness Engineering and works without a sibling skill or main mode.

## Inputs and boundary

Read the approved profile and plan yourself. Obtain the candidate revision, target hosts, required outcomes, operation manifest, before/after hashes, permissions, backups and previous evidence. Missing required inputs block their dependent checks.

Start with the actual target-state change and unresolved required work. Validators, reports and check counts cannot outweigh an unfinished outcome. Use the task owner's qualitative rubric, threshold and evidence surface; do not replace it with a generic harness score.

For a small change, run relevant checks and report inline. Reserve durable evidence packets for installation, release or consequential changes. Do not invent checks for unchanged surfaces.

## Executable interface

Use this package's local CLI, `scripts/hectl.py`, for structure, resource closure and source-to-loaded-payload comparison: `skill-check DIR --host claude-code|codex`, `plugin-check DIR --host claude-code|codex`, `parity SOURCE INSTALLED`, `listing-budget PATH --context-tokens N`, `audit` for the instruction chain and inventory, `selfcheck` for this skill's own files, and `unslop verify` for a prose repair. Inspect `python3 scripts/hectl.py <command> --help` when options are uncertain. Supply explicit roots, host, expected hashes and evidence destinations where the command requires them. Record invocation, exit status, diagnostics and actual outputs. Missing tools, unsupported flags, malformed output and timeouts are failures, not empty passes.

A helper validates what it measures. Parsing a receipt cannot establish that its claims are true. Discover actual host configuration and installation locations rather than using another host's paths.

## Procedure

1. Freeze candidate identity. Inspect current files, instruction precedence, manifests, permissions and backup evidence. Verify operation scope, protected material and recovery coverage. Reject placeholders, unintended private data and unexpected files.
2. Validate changed skills and packaging with the target host's supported tools. Check current availability and flags. Resolve Claude Code's CLAUDE.md and settings behavior separately from Codex's AGENTS.md and configuration behavior.
3. Check every declared local reference, asset and script dependency, including nested paths, case sensitivity and interpreter requirements. Resolve paths from their documented owning file or package root, not an accidental working directory.
4. Inspect each host's installed/enabled listing (Claude Code: `~/.claude/plugins/installed_plugins.json` and `enabledPlugins`, or the session's own skill and plugin catalog; Codex: `codex plugin list --json`) and compare the complete managed source payload with the actual loaded installation using `hectl parity`. Record missing, extra and changed files and justified generated-file exclusions. If no cache exists, identify the loaded payload. Version labels alone cannot prove parity.
5. Start a fresh task through the real host. Prove discovery and invocation of the intended entry, activation boundaries and access to retained workflows. Demonstrate a supporting-file read with a task whose answer depends on content found only there. Remove siblings and main mode for independence checks.
6. Exercise each required workflow through its relevant surface: CLI, browser, native UI, connector, artifact or hook. Launch an isolated instance, check readiness and ownership, perform the user action, inspect resulting state and side effects, preserve evidence, then clean only owned scratch processes and data. Confirm evidence survives cleanup. Hook configuration is not hook execution; honor existing trust requirements.
7. Include negative activation, missing tools/resources, malformed inputs and permission stops where applicable. Observe dry-run side effects instead of trusting the label. A mocked external boundary remains unqualified for real execution.
8. For context changes, compare affected sections and actual loaded context, routes, visible entries and selected methods. Rerun affected frozen behavior cases after installation or task-start context changes. Entry count is not token savings.
9. Inspect current qualitative output separately. When independent review is required, use a fresh reviewer on the integrated candidate; otherwise identify the actual review method honestly.

## Operational acceptance

Registration is not execution. Before calling hooks or routines operational on a host, run this bounded sequence once per host and candidate. Reuse the current receipt template rather than adding a framework.

1. Discover the current install, version and enabled state from the host's own listing.
2. Review hook trust or enablement through the host's supported surface. Where no supported reader exists, record the state as unknown rather than parsing private app storage. `hectl audit --readiness` reports these checks as pass, fail or unknown; add `--native-hooks` on Codex to query `codex app-server`, `--registry` for a runtime registry and `--routine-state` for a routine's receipt proof.
3. On an isolated, disposable fixture with its own state root and a bound run, trigger native startup and pre-compaction events through the real host. Accept evidence only from the host's own event records, such as hook responses or transcript lines naming the hook. A direct script invocation proves the script, not native delivery. Remove the fixture binding afterwards.
4. Run each routine twice by hand, then observe one native scheduled or run-now occurrence, and reopen the artifact it actually produced.
5. Record the host version, permission mode as observed (not assumed after an edit), scope, timezone, failure and stop behavior, output identity and recovery. Treat a run marked successful without its required artifact as a failure. Preserve any classifier or permission denial verbatim.

An unattended routine that keeps state must fail closed on invalid state, write it atomically, bound each subprocess, and read the exact receipt path the tool reports. Keep each host's evidence separate; one host's pass is not another host's qualification.

## Verdict and recovery

Return one compact receipt (for a bounded run, in the shape of `assets/templates/verifier-receipt.json`, which `hectl run stop --as completed` checks): candidate identity, host/version, target-state change, unresolved count, each required check's action, expected and observed result, evidence and status; separate functional and qualitative results; and recovery state.

A required missing, skipped, stale, stubbed, renamed or failed check prevents completion. Missing, blocked, stale, failed or below-threshold qualitative evidence also prevents completion. Explain the blocker without editing the artifact or weakening acceptance. Return findings for repair within existing authority, then verify the newly frozen revision.

Both hosts must pass the same candidate contract before claiming dual-host qualification. Cleanup failure remains unresolved even if functional checks succeed.
