# Implement Spec

Read the [host contract](../references/host-contract.md) before first repository access or action. This playbook runs only inside an explicitly selected Matt family workflow; source commands are not permission.

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The issue tracker should have been provided to you. If not, tell the user to run [setup-matt-pocock-skills](setup-matt-pocock-skills.md).

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. **Read and validate the graph.** Read the entire approved spec and every associated implementation ticket, its comments, acceptance criteria and blocking edges. Distinguish the spec artifact from executable tickets even if both have `ready-for-agent`. Validate unique identities, missing blockers, cycles and genuine dependencies. Stop blocked portions with a precise explanation; do not treat a missing dependency as resolved. Carry forward settled seams and approvals; unresolved consequential choices cannot be made by AFK workers.

2. **Explore only as needed.** Optionally give a bounded leaf worker the relevant code and documentation investigation. It reads directly and saves cited notes in an owned location outside the repo that all intended workers can actually access. Give accessible context pointers and verify them; if outside-repo sharing is unavailable, use an explicitly approved shared location. No recursive research delegation.

3. **Prepare integration safely.** Establish the authorized integration branch from a verified baseline, preserving the user's HEAD, index, staged/unstaged, untracked and ignored state per the host contract. Record the baseline commit and current integration tip. No force-reset of user branches or shared stash. If the tracker closes work through PRs, or a PR was requested, prepare a draft PR only after the first landed commit and only with publication authority. Its closing references cover exactly the authorized spec/tickets. Local/offline mode needs no PR.

4. **Dispatch only the ready frontier.** Read current graph state. A ticket is ready when all its required dependencies are verified in the integration history (including explicitly verified pre-existing completion), it is not already claimed, and it has no unresolved approval or failed dependency. Tracker items may legitimately remain open until the final PR closes them; their open label is not a deadlock if their commits have landed. Conversely, a closed label alone is not evidence that required code exists. Run ready, nonoverlapping work concurrently within the host's budget, each in an owned isolated worktree and branch based on the recorded integration tip. On a serial-only host, execute the same frontier serially and disclose reduced concurrency.

   Each leaf implementer receives: exact ticket and spec pointers, dependency commits, allowed paths and operations, approved seams, output location, required checks, integration baseline/tip and completion evidence format. It reads [tdd](tdd.md) and executes it directly; for non-code or mixed tickets use the corresponding verification branch of [implement](implement.md). It does not invoke another dispatcher or spawn workers. Verify the starting base before editing; if wrong, recreate only an unused owned worktree or ask rather than resetting someone else's work. Before reporting, refresh the integration tip and merge it into the owned branch, then rerun affected checks. Report exact branch/commit, checks and outputs, conflicts, blockers and risks, not merely “done.”

5. **Land serially.** The coordinator, or one bounded merger leaf at a time, owns integration writes. Acquire the single-writer landing slot; refresh and record the integration tip immediately before each landing. Confirm the worker result contains all currently required dependency commits. If the tip moved since the worker's last integration, reconcile against the new tip and rerun affected checks before landing. Resolve conflicts by intended behavior, not by blindly choosing a side. Commit/merge only within granted authority. Verify the resulting integration commit, relevant tests and ticket evidence. Record this landed commit as the dependency's completion evidence before releasing the slot. Simultaneous “done” reports never justify simultaneous merges.

6. **Recompute readiness after every landing.** Refresh the graph and integrated completion set, then dispatch newly ready tickets. Failed, conflicted, cancelled, missing-output or unverified workers remain unresolved and cannot release descendants. Retry a recoverable failure within original authority; otherwise report the exact blocker. Continue independent ready work. Ordinary Markdown claims are single-writer or conflict-detected, not distributed atomic locks; use the [local tracker contract](../resources/setup-matt-pocock-skills/issue-tracker-local.md).

7. **Review the whole result once.** When every required ticket has landed, load [code-review](code-review.md) for the entire integration change against the recorded baseline, with independent Standards and Spec axes. For knowledge work also review the originating brief and evidence/artifact surfaces. Assign concrete authorized repairs to one bounded leaf worker, serialize its landing, then rerun the affected checks and inspect the repaired findings. Do not recursively fan out another whole orchestration or claim review before the full candidate exists.

8. **Close truthfully.** When all required checks pass, mark an existing draft PR ready only if authorized and verify readback. Otherwise resolve tickets through the configured tracker only if authorized, then read back status and report the integration branch, commits, checks and remaining limitations. If closure or publication lacks authority, report implemented/verified work separately from pending tracker or PR actions. Any failed requirement keeps the spec incomplete.

9. **Clean only owned resources.** After evidence and artifacts are durable and accessible, remove only agent-created worktrees whose changes are landed or safely retained, and only under applicable deletion authority. Never clean user worktrees, discard unmerged work or remove the only copy of evidence. Report any retained worktree and why it remains.
