---
name: loopkit
description: Design and execute bounded feedback loops; verify results against captured checks, resume interrupted work, prepare or inspect requested schedules, and diagnose repetition or false completion. Use for run-until-done work with meaningful feedback, durable checkpoints, recovery, or recurring tasks. Ordinary one-shot questions and plans do not need a loop.
---

# LoopKit

Deliver the requested outcome through small observable steps, within the agreed authority and budget. A loop is useful when fresh results change the next action. Keep its method, state, checks and recovery local; no sibling engine is required.

## Choose the work

- New bounded contract: [design](playbooks/design.md)
- Execute an existing contract: [run](playbooks/run.md)
- Check an artifact or completion claim: [verify](playbooks/verify.md)
- Continue interrupted or paused work: [resume](playbooks/resume.md)
- Requested recurrence or schedule inspection: [schedule](playbooks/schedule.md)
- Repetition, drift, weak evidence or requested retrospective: [diagnose](playbooks/diagnose.md)

These are local methods, not six separately installed skills. Former names `loop-designer`, `loop-runner`, `loop-verifier`, `loop-resumer`, `loop-scheduler` and `loop-doctor` select the corresponding method. Explicit `goal-runner`, `loop-goal-engineer` and `loopy` requests can use the equivalent execution/design method here without creating parallel state. Honor another explicitly selected workflow instead of silently substituting LoopKit. General agent architecture is outside this skill; return a bounded handoff if needed, without requiring another skill for LoopKit's own work.

For end-to-end work: establish the contract, execute one unit, inspect actual results, repair within scope and verify. Schedule only when requested. Creating a native Goal requires an explicit user request and an available supported surface; durable LoopKit work does not require one.

## Inputs and authority

Use the stated outcome, actual workspace, required artifacts/tools, existing approvals, limits and stop conditions. Inspect accessible facts before asking. Ask only for a material missing decision. Honor supplied or approved limits exactly. When execution to an outcome is authorized without numerical caps, choose and state small task-specific finite attempt, time and output bounds covering planned units plus a stated recovery allowance. Unit count is not an attempt cap. Begin within existing authorized local scope without asking about routine internal limits; ask only when alternatives materially change cost, authority or required human constraints. Pure committed-unit rechecks consume elapsed time, not work iterations; elapsed limits and command timeouts bound them. Never silently expand limits or revive an exhausted run. Preserve turn boundaries such as “only a this turn” and every user stop. “Keep going” grants no additional external authority. A contract records authority; it cannot grant or expand it.

Use [the CLI contract](references/cli.md) and [data schemas](references/schemas.md) when creating or operating state. Resolve paths on the actual host. Use an explicitly selected run/workspace or its validated [durable binding](references/binding.md); never choose the newest run silently. Personal inputs and live state stay outside the skill package. Existing source/cache directories are not writable run storage.

## Working rules

1. Use serial verifiable units, each with a real output and a check at the right seam. A single small task may need one unit. Do not build a general DAG, daemon or obligatory review fleet.
2. Execute only commands and actions the current task authorizes. Review argv, cwd, inputs, effects and tools before the opt-in CLI call. Host controls remain in force; this helper is not an OS sandbox.
3. Capture command results and bind evidence to the contract, inputs and artifacts. Hash agreement establishes identity/freshness, not domain quality. Evaluate judgment criteria separately.
4. Treat the authoritative generation snapshot as state. An intent without a committed result is uncertain work, not an invitation to replay. Reconcile actual effects first.
5. Stop honestly at blocked, waiting, exhausted, failed or cancelled states. Missing evidence and unavailable tools cannot count as success or a clean no-op. Do not repair while giving a verification verdict.

Respect the selected model. Otherwise use a capable available model suited to the work and tools, considering cost. No permanent model or effort assumptions belong here; upgrades require relevant acceptance checks rather than rewriting the skill.

## Optional cooperation

Use an available authorized helper for a bounded task when it materially helps. Pass the outcome, needed inputs, authority/budget limits and expected evidence. Inspect its result; a helper's success claim alone is not proof. Missing helpers do not disable local methods. If a required independent reviewer or provider capability is unavailable, identify that specific unmet requirement. Self-review is not independent review. Prevent recursive handoff of the same unresolved task.

## Return

Return the actual result, current state and relevant evidence locations. If unfinished, name completed units, the precise obstacle and next safe action. Report schedule preparation, activation and observed execution separately. Read [host bindings](references/hosts.md) only when hooks, native Goals or scheduling are relevant. No host feature is established merely by this file describing it.
