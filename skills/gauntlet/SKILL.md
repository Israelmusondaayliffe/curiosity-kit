---
name: gauntlet
description: "Use only when the user explicitly invokes Gauntlet or Gauntlet Loop. Plan approved work, improve artifacts against an inspectable bar with blind critics, or independently verify finished work. Includes dependency-ready execution, durable recovery and evidence reports. Never activate for ordinary review or quality requests."
disable-model-invocation: true
---

# Gauntlet

Own the selected Gauntlet job through inspectable evidence. This skill works without another personal skill or a main mode. Local scripts perform validation and bookkeeping; the actual host supplies agents, tools and execution. Scripts do not impersonate agents.

## Entry and outcome

An explicit Gauntlet request authorizes this method only within the user's stated scope. A request for "more reviewers", "maximum quality" or a large project is not an invocation. Do not initialize state or fan out helpers for those requests. Continue an authorized run when the user explicitly resumes it; an approval response within its current planning conversation can release the approved work.

Choose the route before any write:

- **Plan/build:** [plan](playbooks/plan.md), then [execute](playbooks/execute.md) after approval.
- **Finished artifact, verify only:** [verify](playbooks/verify.md). Do not launch builders, rewrite the artifact or run an improvement loop.
- **Resume/interruption:** [resume](playbooks/resume.md) before dispatch. A terminal run does not restart merely because a prompt exists.
- **Status/evidence:** generate a report from saved state. Missing or failing evidence is an honest report, never a completion claim.

Read [runtime contract](references/runtime.md) before the first command. Use `python3 <skill-dir>/scripts/gauntlet.py --help` for current command arguments and [CLI examples](references/cli.md) for payloads. Read only the selected [domain](references/domains/code.md), substituting visual, prose, research, deck, strategy, prompt-system or brand as appropriate. Mixed jobs declare a primary domain and explicit per-piece exceptions.

## Readiness and authority

Discover actual filesystem, command, artifact-inspection and fresh-agent support. Record missing capabilities honestly. A briefing can be prepared without those capabilities, but do not simulate execution or fresh review. Unsupported execution stops; degraded execution carries its limitation into every handoff/report.

Before creating state, enforce the Claude Fable peer gate described in [runtime](references/runtime.md). Both workflows named for one job requires a choice even if no files exist. The optional read-only probe tolerates absent files; no peer plugin is a required dependency. Optional explicitly invoked Codex advisor composition follows [advisor](references/advisor.md), with local validation and Gauntlet as sole owner. Never discover private sibling internals to make a required function work.

Reuse a settled brief and existing scoped approval. Ask only for material missing decisions. Execution needs an approved plan, inspectable external bar, independently checkable criteria, file ownership and a finite runtime budget. Additional account actions, publication, destructive operations or external task creation retain their separate authorization requirements. An approval field in a file is not user authority; the coordinator checks it against the actual conversation.

Respect explicit model and effort choices through supported host controls. If the available helper mechanism cannot select an effort, use an authorized supported process route where available or record it as unselectable. Never report a default as the requested effort. Without an explicit choice, select the strongest suitable available coordinator, economical capable routine workers and strong reviewers where the judgment requires them. Record actual model/effort observations, not assumptions. No model is a permanent runtime dependency.

## Invariants

1. Freeze the external bar, all acceptance criteria, reader questions and source bytes before judging. Changed targets invalidate prior approval/evidence.
2. Builders never grade themselves. Critics and verifiers receive fresh bounded contexts, not inherited conversations or builder summaries.
3. Inspect actual behavior, source evidence, readable artifacts or rendered pixels. Existence of a file is not a successful result.
4. Quality and integrity are separate mandates. Final verification covers acceptance/scope, evidence/correctness and integration/adversarial failure.
5. Scripts compute consensus and counters from records. Cannot-verify, dissent, gaps and budget exhaustion survive every report.
6. Canonical local state, not chat memory, owns progress. Persist each material event and never replay an interrupted operation blindly.
7. Runtime budgets are finite. A cap pauses work; it never certifies it. Project-worker allocation policies do not remove a user's runtime limits.

## Return

Return the actual artifact locations, exact terminal status, evidence/workbench/handoff paths, reproducible commands and material limitations. A verified result requires current artifact hashes, passed checks, independent evidence and resolved required criteria. Failed, unverifiable, paused and exhausted are useful truthful outcomes. Do not soften them into "done".
