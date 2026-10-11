# Execute bounded work

Read the contract and fresh authoritative snapshot, not a builder's summary. Confirm the selected run, workspace, host, generation, current unit, remaining budget and authority. Inspect fresh artifacts and preserve unrelated changes. Resolve blocked/waiting prerequisites before resuming.

## One useful iteration

1. Observe the latest result and choose the smallest in-scope action that addresses the highest-value failure. Use the current unit's declared commands where they are adequate. `run-unit` executes its action/check sequence; `check` is verification-only. See [CLI](../references/cli.md).
2. Before `--execute`, inspect the exact argv, cwd, declared input scripts/data and possible side effects. No shell-string interpolation is used, but an interpreter or executable can still perform arbitrary effects. Use the host sandbox/permissions and isolation required by the task. Never treat a contract's authority text as permission supplied by the file itself.
3. Record intent before external or host-tool work as well. If the available CLI cannot faithfully represent an action, do not fabricate a captured command result. Keep the real host tool response and effect evidence, and record the unsupported integration clearly; it cannot become a machine pass merely by writing a receipt.
4. Inspect captured exit/timeout/output and artifacts. Failed actions do not proceed as though their effects succeeded. Checks that mutate the inspected artifacts do not qualify as read-only verification. Required judgments use the actual output and explicit criteria.
5. Commit a unit only through the verified completion operation. Final completion must still satisfy every essential unit after all later changes. An earlier verified unit is history, not permanent immunity from regression.
6. Continue while authority, prerequisites and caps allow useful progress. Progress means a relevant failure resolved or an evidenced unit/milestone reached. Rewording the same plan or changing an unrelated file is not progress. Diagnose repeated equivalent actions rather than adding more attempts blindly.

## Stops and handoffs

- Completed: all required fresh machine and judgment evidence supports the requested result
- Waiting input: a named decision is genuinely required
- Blocked: a named tool, access, authority or other prerequisite is unavailable
- Exhausted: the agreed iteration, no-progress or time budget is consumed
- Failed: the contract/state is invalid or the fault cannot be repaired within scope
- Cancelled: the user stops the task

Keep the distinction visible. Do not enlarge caps or shrink requirements to manufacture completion. Report partial work and evidence at a stop. On interruption use [resume](resume.md); on repetition or confusing signals use [diagnose](diagnose.md). A budget stop cannot be cured by restarting the process or changing a model.

Optional workers receive one bounded unit, its input identities and limits; the parent integrates and verifies their artifacts. No compulsory delegation or background service. Native Goals are optional and explicit-request-only. “Keep going” authorizes continued work only inside the task's established boundaries.
