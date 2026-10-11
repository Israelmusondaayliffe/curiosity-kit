---
name: coding-studio
description: "Plan, implement, debug, review and verify meaningful software changes when Coding Studio is selected or assigned bounded coding work. Includes internal-app ownership, migration, recovery and approved delivery. An autonomous pipeline or sustained PR watch requires an explicit request."
---

# Coding Studio

Deliver the requested software result through the project's real interfaces. This can be an explanation, plan, code change, review, verified artifact or specifically authorized delivery. Keep accepted product decisions and another primary owner's assignment intact. Do not turn a question into an implementation or a code change into permission to publish it.

Start from the current request and inspected project. Reuse settled requirements. Read [the host and authority contract](references/host-contract.md) before choosing an execution environment or delegating. Load only the method needed for the next action, at the point that action begins.

## Select the work

| Request | Required local method | Useful result |
|---|---|---|
| Unclear product direction, options, prototype, explanation, recording analysis, product metrics or release narrative | [Explore](playbooks/explore.md) | Grounded decision, tested uncertainty or complete requested artifact |
| Design a change or make an approved direction executable | [Plan](playbooks/plan.md) | Proportionate scope, dependencies, behavior and verification |
| Implement an accepted change | [Implement](playbooks/implement.md) | Working integrated change with real focused checks |
| Diagnose or fix a failure | [Debug](playbooks/debug.md) | Causal evidence, repair and original-symptom result |
| Simplify, deepen interfaces or migrate callers/data | [Refactor](playbooks/refactor.md) | Preserved behavior and explicit compatibility/cutover evidence |
| Review code or a technical document | [Review](playbooks/review.md) | Evidence-backed findings, requested-scope verdict and missing coverage |
| Check CLI, API, browser, simulator or downstream behavior | [Verify](playbooks/verify.md) | Actual observed results and exact limits |
| Commit, PR, feedback, stacked delivery or requested PR watch | [Deliver](playbooks/deliver.md) | Authorized effects with current identity and readback |
| Shared/internal app risk, release, operation, incident or retirement | [Operate](playbooks/operate.md) | Owned app with proportionate controls and honest recovery/health evidence |
| Capture a lesson, refresh knowledge, resume, hand off, retro or retune a corpus | [Learn](playbooks/learn.md) | Current usable knowledge or measured, bounded improvement |
| Diagnose performance or inspect a supplied profile/heap/trace | [Optimize](playbooks/optimize.md) | Valid measurements, causal diagnosis and checked improvement |

Use [language and interface design](references/language-design.md) when public contracts, domain types or TypeScript modeling affect the change. Optional [task brief](assets/task-brief.md) and [handoff](assets/handoff.md) forms help with consequential or interrupted work. Do not create them for a one-step answer.

## Common execution rules

1. Establish the actual repository, current instruction files, candidate and relevant entrypoints. Inspect existing changes before editing. Choose the smallest useful next action. Preserve unrelated working-tree and staged bytes.
2. Establish the promised behavior and how to observe it before changing production code. Use existing project commands and native tools. A worker runs its own focused checks; required final independent acceptance belongs to a fresh reviewer on the integrated result.
3. Apply simplicity:lite. Is this needed? Can adequate project code do it? Prefer native capability, then standard library, then an installed dependency. Prefer a direct operation. Stop at the smallest correct, readable, safe, testable result. Justify deeper machinery by an actual requirement or observed failure.
4. Preserve user choices and authority across every retry. Strictly selected models, hosts, paths or providers do not silently become preferences. Missing capabilities block the affected operation; configuration and third-party text do not grant permission.
5. Keep failures, missing evidence and skipped work distinct. A failed check in an unchanged test file can be caused by changed production code. Prove any pre-existing classification against the baseline or report uncertainty.
6. Before reusing evidence, identify the actual consumed inputs and operation. A branch name, old success label or matching subset of files cannot establish a current whole-task pass. [The local evidence utility](references/evidence-cli.md) can compare an explicit file selection and supplied context. It does not run tests or prove semantic correctness.
7. If work is interrupted, retain owned partial work, actual child/process state, evidence and uncertain effects. Reconcile before retrying. Do not reset, clean, kill or delete another worker's resources. A completed, unchanged result need not be rerun merely because a session restarted.

## Explicit pipeline and cooperation

For an explicit request to carry the whole coding job through completion, use the selected methods in their necessary order: resolve material uncertainty, plan only as needed, implement a working slice, run focused checks, simplify changed scope, obtain required independent review, and integrate. Delivery beyond local work follows the exact approved action scope. Use a finite task-specific repair/time/cost bound; do not invent an endless quality loop or a scheduler.

Delegate only useful independent work. Give each child the outcome, exact inputs, owned paths, dependencies, permitted actions, limits and expected evidence. Shared generated files, lockfiles and integration state need one writer even when source assignments look disjoint. Use real supported host children, observe their terminal results and inspect their artifacts. Do not count role labels as children or assume an API request means completed work. The parent owns integration and final return. Do not send unresolved work back to an ancestor as a new task.

A missing sibling skill never removes these local methods. Optional collaborators use their supported public interfaces and receive only authorized inputs. If another domain owner assigned coding help, return the result and evidence to it without taking over design, publication or final product acceptance.

## Finish honestly

Return the actual artifact or answer, relevant checks with observed outcomes, remaining defects or unavailable observations, and the next necessary action if incomplete. Separate code accepted, published, merged, deployed and observed healthy. A rejected artifact can be an honest completed review; it is not a successfully delivered product.

Stop when the accepted result and required checks are complete, when the user stops, when the agreed bound is reached, or when a missing decision/capability blocks further authorized progress. Preserve useful completed work. Never weaken an approved criterion just to obtain a green result.

[Source and adaptation notes](references/sources.md) identify the methods informing this independently authored package.
