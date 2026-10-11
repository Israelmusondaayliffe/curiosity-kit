# Slice and coordinate

Turn an accepted brief into small complete results and manage their dependencies without inventing a second project-management system. Read the brief and its governing sources in full before declaring work ready.

## Cut by observable result

Choose a first thin path that reaches the user and exposes an important unknown. A research slice supports one material claim and adds the usable finding; a writing slice completes a reader action; an operational slice takes one permitted sample from intake through confirmation; a software slice proves one behavior through its public interface. Separate database, prose and test chores are not automatically independently useful slices.

Fold setup, source reconciliation and documentation into the outcome they enable unless they can genuinely be accepted independently. Split when a reviewer could reject one result while accepting its neighbor, or when the inputs no longer fit a fresh working context. Do not split by an arbitrary number of files or tasks.

Each slice needs:

- A stable ID, outcome, owner and allowed output location.
- The relevant brief/source versions and exact constraints inherited from them.
- Inputs it consumes and what later work expects from it. Resolve mismatched quantities, names, formats or versions before dependent work begins.
- A real proof method and observable acceptance checks tied to requirement IDs where useful.
- Only dependencies that actually prevent this work, including the needed predecessor output version.
- Permitted changes, action scope and exclusions.
- State, actual evidence after execution and any open blocker.

Plan checks before implementation. Derive expected results from the brief, an independent worked example or a known baseline, not by repeating the same calculation being tested. A requirement with no slice/check remains uncovered, even when the graph is valid.

## Use the dependency frontier

A slice can be considered dependency-ready when its required predecessor versions have verified evidence and its local blockers are clear. That says nothing by itself about permission to execute. Check current user authority, required content approval and real tools before starting.

Work in dependency order, but do not stop unrelated authorized work merely because one branch is blocked. Parallelize only when outputs are disjoint or workspaces genuinely isolate writes. Name one writer per shared file. A common brief, source change or shared interface may require coordination even when the dependency graph has no edge. Reconcile integrated outputs before marking the whole result complete.

A worker receives its outcome, exact relevant inputs, owns specified files, inherits action/resource limits and returns the artifact, checks and open findings. It does not rediscover the whole project, recursively delegate the same task or assume that another worker's summary proves a dependency. The parent reads the work and retains responsibility.

No worker support is required for sequential execution. Do not invent a successful dispatch when the host cannot perform it.

## Wide changes and integration

When a coordinated migration cannot be safely divided into independent complete paths:

1. Expand with the new form while current users can still use the old form, if compatibility is required.
2. Migrate bounded consumer groups, accounting for docs, string references, tests, exports and external consumers as well as obvious callers.
3. Contract only when every required consumer has moved and the relevant compatibility commitment permits retirement.

Some authorized isolated migrations cannot remain valid after each small edit. Declare where intermediate breakage is allowed, how it is contained/reversed, which high-signal checks remain active and the final integration check required before handoff. Do not call broken intermediate batches independently complete or expose them as a release. Nor should temporary compatibility code be added without a real consumer need.

Changing, deleting, merging or publishing remains subject to the user's scope and applicable permissions. A migration plan alone authorizes none of those actions.

## Multi-asset control

Keep a single current source of coordination facts. The optional control section of the [plan example](../assets/plan-example.json) holds assets, decisions, approvals and risks; slices hold the only execution dependency graph. Owners can be named inline rather than maintained in a redundant directory.

For every asset, preserve the current version, owner, governing accepted decisions, risk/recovery links and state. Use the exact asset states in the [schema](../references/checker.md), and report blocked work through its slice blockers. Distinguish draft, verification, content approval and actual delivery. A recorded delivery location and authority statement are still declarations that must be checked against real evidence.

Approval records name the asset, exact version, scope, approver, status and actual evidence. Keep pending/rejected approval visible. An old approval can remain valid for its old version without satisfying the current gate. Approval of content is not permission to publish; sending to a new audience is not covered merely because an earlier recipient approved the draft.

Only attach approval dependencies to the work that needs them. Creating a private draft may proceed while publication approval is pending. A review packet depends on the checked drafts, not on sending them first. A requirement for all assets cannot be satisfied by presenting the best one.

When a shared fact or source changes, identify its consumers. Update affected briefs, assets, checks and recommendations, mark prior evidence stale where it no longer applies, and obtain renewed approval only for the changed scope that needs it. Preserve unchanged valid results. Avoid rewriting every record merely to give it a new timestamp.

## Machine check and human check

Use `check_outcome.py plan FILE` for the canonical JSON plan. It validates structure/references and reports dependency-ready work from declared state, plus blockers. It does not observe actual predecessor artifacts, decide whether a requirement is semantically covered, authenticate approvals or execute anything. Inspect the actual source/artifact/evidence before acting on its output.

For a simple human-readable plan, apply the same dependency and coverage reasoning manually. Do not require JSON for a direct one-step request. An explicit machine-check gate still needs the actual tool result; missing Python is a named unrun check, not a pass.

Before handing off, verify the whole plan covers accepted requirements, each task is useful and correctly sized, consumed/produced contracts match, there is no cycle or invented dependency, and all approvals/actions stay distinct. Return the requested plan without creating external tickets, assigning people or changing trackers unless separately authorized. For already authorized execution, continue with [deliver and resume](deliver-and-resume.md).
