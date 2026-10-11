# Resume or pause safely

Use the explicitly named run and workspace, or the validated [durable workspace binding](../references/binding.md). If neither is available, ask for the run or show bounded candidates for selection; never silently take the newest. Do not search unrelated host homes or import another host's state. Read [state schema](../references/schemas.md) and [host bindings](../references/hosts.md) when needed.

## Restore

1. Read the authoritative snapshot and validate its integrity, contract hash, run identity, workspace/host and generation. A checkpoint is only a bounded pointer. Never act from checkpoint prose alone.
2. Inspect committed units, captured checks/reviews, pending intent and fresh artifacts. Preserve user edits. A mismatched generation means another writer won; reread and reconsider the action, rather than retrying with a guessed larger number.
3. If an action is pending, establish executor/process liveness and inspect actual effects before replay. A missing response does not mean the action failed. Use the exact pending batch and a fresh inspection artifact for reconciliation. Confirm the original executor and owned children stopped. Unknown outcome stays blocked; never replay an uncertain message, purchase, deployment or other external effect automatically.
4. If state/artifacts disagree, diagnose the precise mismatch. Do not overwrite current artifacts from an old checkpoint or mark a stale result fresh. Use the integrated recovery/recheck path only after inspecting the change. If no safe recovery operation exists, stop and hand back that fault.
5. Resolve the named blocked/waiting prerequisite, then use a generation-checked resume. Terminal runs stay terminal. A budget remains consumed after restart; changing it needs the relevant approval and an explicit new/revised run.
6. Choose the next action from current evidence. Previously committed units remain recorded; rerun only what relevant changes invalidate. Return the restored location, verified work, limits and next action.

## Requested pause

Stop at a safe boundary: finish the current atomic step or reconcile it. Start nothing new. Stop only task-owned workers/processes through supported controls and preserve evidence. Write a bounded checkpoint pointing to the contract, current generation, verified units, uncertainty, next action and useful artifacts. Do not push, commit, delete or change global instructions merely to pause unless separately authorized.

This adapts safe-pause/context-preservation methods without importing their source host's automatic commit convention. Do not pause just because the user is absent when they asked you to continue. Conversely, do not conceal a hard budget or safety stop to appear autonomous.

Hooks must use explicit run/workspace binding. A hook with no selected run is inactive. Startup, resume and compact restoration must be exercised on the actual host; a script test cannot prove trust/registration. Visible hook errors mean checkpoint restoration was unavailable and require direct state inspection.

When changing the selected run, bind it explicitly and verify the returned pointer. When requested cleanup ends its hook selection, unbind that exact owned pointer; retain run evidence and unrelated bindings. Terminal runs become inactive without automatically deleting their pointer.
