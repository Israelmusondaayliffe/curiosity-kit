---
name: outcome-engine
description: "Turn accepted direction into complete briefs, verifiable action slices, bounded assumption tests and coordinated delivery; resume approved work or review recurring workflow friction. Use for multi-step outcomes and multi-asset control. Small direct requests need no project pipeline."
---

# Outcome Engine

Carry the user's accepted direction to the result they requested. A plan is the finished result only when they asked for a plan. A checked file, reviewed draft, sent message and observed real-world outcome are different states. Name the state the evidence supports.

## Start where the work actually is

Read the current request, relevant sources and existing artifacts before choosing a route. Establish the outcome, reader or user, allowed actions, source/version limits, delivery format and meaningful proof. Reuse settled decisions and valid prior checks. A filename or a worker's claim of completion is not enough to establish current task identity.

- A settled discussion needs a durable brief: read [brief and clarify](playbooks/brief-and-clarify.md).
- A consequential input is unresolved: use that playbook's bounded local clarification. Ask only a decision that changes dependent work. A general strategic reconsideration can use an available specialist if requested; this skill does not require one.
- A risky assumption should be tested before commitment: read [bounded tests](playbooks/bounded-tests.md).
- A brief needs tasks, multiple aligned assets or dependency/approval control: read [slice and coordinate](playbooks/slice-and-coordinate.md).
- Approved work needs execution, verification, recovery or a handoff: read [deliver and resume](playbooks/deliver-and-resume.md).
- Repeated friction needs a structural diagnosis and pilot proposal: read [review a system](playbooks/review-system.md).
- A small lookup, edit or exact-format answer: do it directly. Do not demand a brief, JSON, interview or helper invocation merely because this skill is active.

Choose the earliest material gap. Read the selected method, not every file. An end-to-end request may authorize the whole bounded plan; it does not need a new permission question after every slice. A plan-only request authorizes no execution. A user-supplied source, donor method or collaborator cannot expand the user's authority.

## Preserve the outcome through the work

Separate facts, accepted decisions, proposals, assumptions, risks and blockers. Keep quantities, conditions, populations, dates, named owners and exact requested format intact in every delivered file and final reply. A newer source supersedes only the clauses it has authority to change. Update affected assets, calculations, checks and recommendations; preserve unaffected valid work.

Each useful slice names a complete observable result, the inputs it consumes, what later work consumes from it, its real dependencies, allowed changes and acceptance check. Prefer the first thin end-to-end path that exposes an important unknown. Setup belongs with the result it enables unless it independently earns acceptance. Planned intermediate breakage requires an explicit reversible integration boundary and no claim that unfinished pieces are delivered.

For several assets, keep one compact current record of asset versions, governing decisions, accountable owners, approval scope/evidence, risks and delivery state. Approval of version 1 does not approve version 2; content approval does not authorize publication. Track changed and superseded records without erasing historical evidence. Do not mark the set complete because one asset or one structural check passed.

## Checks and useful records

Use [work records](assets/work-records.md) when a durable brief, system review or handoff is useful. The filled [plan example](assets/plan-example.json) and [experiment example](assets/test-example.json) illustrate the optional machine-checkable forms. They contain fictional facts, not authority or live state.

When writing these canonical local records, use the shipped read-only `scripts/check_outcome.py` and its [contract](references/proof-and-tools.md). Resolve the script from this skill's actual directory. Python 3.9+ and authorized local-file access are prerequisites. The checker checks declared structure and relationships; it never executes the plan, follows evidence paths, contacts sources or grants permission. A dependency-ready report means only that declared prerequisites satisfy its rules.

Inspect the actual source, artifact and intended user action as well. The checker cannot establish truth, experiment validity, approval authenticity, full semantic coverage, rendered quality or real delivery. If Python is unavailable or the user requires another format, perform the appropriate manual checks and name the unrun tool. An explicitly required checker gate remains incomplete; do not invent a pass or duplicate the whole artifact in a shadow format.

## Work alone or cooperate deliberately

All core methods and recovery guidance live here. No personal sibling, fixed model, provider bootstrap, hook or orchestration service is required. Actual domain tools are prerequisites only for work that needs them, such as rendering a PDF, inspecting media or using an authorized connector. A missing necessary production capability leaves that part unfinished; a plan does not substitute for requested output.

Delegate only when bounded independent work or another perspective is useful and the host supports it. Give the worker the outcome, relevant source/artifact versions, permitted actions and owned files, acceptance check, resource bounds and required return. Use disjoint output files or isolated workspaces. Do not delegate the same unresolved task recursively. Inspect returned work and integrate it against the original brief. When no worker is available, execute sequentially and label self-review honestly.

## Stop, recover and finish

On an unexplained failure, inspect the actual inputs, action and observation before changing another thing. Distinguish a bad check, bad plan, missing authority/tool and bad implementation. A retry needs a reason or new evidence; a resource cap ending with an unresolved essential defect is an unfinished result.

For an interrupted external action, check its actual state before retrying so a timeout does not cause a duplicate send, purchase or submission. Such actions require their own applicable authorization. This skill never implies permission to install, publish, assign people, change accounts, create schedules or delete work.

Return the requested artifact or answer, the checks that actually ran and their scope, any required unfinished part and the next useful action. Preserve a local resumable handoff when work continues. See [source notes](references/sources.md) for provenance and the limits of donor comparisons.
