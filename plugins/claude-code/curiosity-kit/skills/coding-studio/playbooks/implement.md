# Implement an accepted change

Use this method for a clear coding request or an accepted plan. It carries the requested behavior through actual code, tests, integration, and an honest return. It can run directly, with native workers, or as the implementation step owned by another task. No external model, personal sibling skill, commit, PR, or deployment is required.

Read [the host contract](../references/host-contract.md). Use [plan.md](plan.md) only when unresolved scope or design prevents a responsible next step. Use [debug.md](debug.md) for an unexplained failure and [refactor.md](refactor.md) for behavior-preserving structural changes or compatibility migrations.

## Inputs and completion boundary

Identify the current request or plan, project and environment, accepted decisions, allowed edits, protected work, and required observations. Resolve a requested model or tool route before launching work. A strict route that is unavailable blocks that route; it does not authorize a silent substitute.

Set completion at the requested result. Local code and passing checks may be the entire task. A request to prepare a PR can also require a reviewable description. Commit, publish, merge, deploy, and operating health are separate states with their own authority and evidence.

When another task owns review or delivery, return implementation and local-check evidence to that owner. Do not begin a competing shipping workflow or a second watcher.

## 1. Verify the starting state

Inspect the selected checkout and instructions rather than assuming the current directory is the intended repository. Resolve the current revision, relevant tracked changes, staged changes, and untracked files. Record enough of the affected starting state to distinguish your edits from existing work. Include file contents or diffs where needed; a clean-looking status summary is insufficient when the task depends on dirty files.

Preserve unrelated bytes and the index. Do not stash, reset, switch branches over edits, stage everything, or clean generated files merely to obtain a tidy baseline. If isolation is useful, prefer an available native mechanism and verify the actual starting revision and files inside it. A child, worktree, or branch label does not prove that uncommitted prerequisites were copied.

Read the complete relevant unit and its decisions. Trace the real entry points and existing tests. Check whether some work is already present. Verify an existing implementation against the intended behavior before deciding to rebuild it. For external state, inspect the actual outcome; repository state cannot establish whether a previous request, setting, or write took effect.

## 2. Select the next ready unit and its proof

Work in dependency order. A prerequisite is ready when its required result has been inspected and verified, not merely when its author says "done." Reconcile changed source or newly discovered dependencies before starting affected work. Independent work may continue around a blocked decision if its result does not assume the answer.

Find the test home that owns the behavior. Search tests by entry point, caller, imports, naming, and scenario. Choose one evidence strategy before changing production behavior:

| Current situation | Next step |
| --- | --- |
| A test already fails on the accepted behavior | Capture that exact failure and use the existing test. |
| Existing coverage misses the actual chain | Strengthen it at the relevant interface and observe the intended failure. |
| New behavior has no test | Add one concrete behavioral case, observe the intended failure, then implement that case. |
| Structure will change while behavior stays | Capture characterization or equivalence evidence before moving code. |
| An assertion embodies superseded behavior | Identify the actual accepted decision, update only affected expectations, and show the new case rejects the old behavior when practical. |
| An automated test cannot establish this result | State why and choose the nearest meaningful observation, such as a real UI exercise, packaging smoke test, or inspected output artifact. |

Do not change an expectation merely because the current patch fails it. A bug fix restores accepted behavior; a refactor preserves it; an approved feature may intentionally change it. Keep those cases distinct.

Before adding a test, name the behavior it protects, the credible regression it catches, and why existing coverage misses it. Prefer extending an existing scenario table when that is its natural home. A new passing test for a healthy uncovered contract is useful coverage, but it is not evidence that a bug was reproduced.

Before relying on a test, ask what makes it sensitive to the defect. Use an independently specified expected result. Avoid deriving an expected total with the same implementation algorithm, having a fixture return the intended answer, or mocking away the boundary where the defect occurs. Inject time, randomness, and true third-party dependencies when that makes a local check reproducible. A mocked integration establishes only the behavior exercised by that substitute.

A missing dependency, compilation error, or wrong test selector is a setup failure. It is not the red observation for the feature. Fix allowed setup problems or record the blocker before making the behavioral claim.

## 3. Implement one behavior at a time

Make the smallest coherent change that satisfies the current case and existing contracts. Follow useful project conventions and reuse adequate code. Prefer a native capability, then the standard library, then an already suitable dependency. Adding an installation, account, credential, or service is a separate action, not an implied implementation step.

Keep the accepted scope intact. Do not add modes, generic frameworks, retries, validation layers, or fallbacks merely because they might be useful someday. A new mechanism is justified when the requested behavior, an existing contract, or a demonstrated material failure requires it. Choose its smallest adequate form. If it changes a settled decision or needs additional authority, raise that exact conflict before doing the dependent work.

Run the focused check, inspect its result, and repair the cause. Continue through small red-to-green or characterization-preserving steps rather than writing a large test batch and all implementation at once. Capture pre-change evidence when it occurs; it cannot later be reconstructed from a green final diff.

Trace effects beyond changed files. Follow shared callers, middleware, callbacks, caches, hooks, jobs, persistence, and other interfaces that expose the behavior. Expand the check set according to the actual dependency chain. Do not use an arbitrary trace depth to dismiss a known downstream consumer.

For resources acquired by the changed code, exercise release and ownership on failure, cancellation, and teardown as applicable. Check for callbacks or background work using a resource after its owner closes it. Preserve output evidence before cleaning up an owned process or fixture.

For shared writes, test the shared invariant at the boundary where actors really meet. Separate processes may need a database-level test. Check a rejected action leaves no forbidden durable or queued effect. For retryable work, exercise interruption at the meaningful boundary and verify repeat handling. A return code or success banner alone cannot establish those properties.

## 4. Delegate only work with real independence

Native workers are optional. Use them when the available host supports the required environment and the task benefits from separate attention or parallel work. A short serial change can stay with one agent.

Before parallel edits, inspect dependencies and mutable resources. Disjoint filenames are necessary for a shared checkout, but insufficient when units change the same contract, schema, generated output, package lock, test database, port, or browser session. Give a contested invariant or shared resource one owner. Serialize the dependent portion while allowing genuinely independent work to continue.

Give each worker a bounded assignment:

- The requested result, relevant decisions, and exact action authority.
- The intended source revision and any required uncommitted input.
- Owned files and excluded mutable resources.
- Prerequisites and interface contracts it must preserve.
- Focused checks, required pre-change evidence, and the expected handback.
- A stop condition for new overlap, a missing prerequisite, or a needed decision.

Use the host's actual isolation and lifecycle behavior. Have an isolated worker verify its baseline before editing. In a shared checkout, workers must not write the Git index or run a formatter, build, or test that mutates another worker's files or shared state. A focused test is suitable only when its effects fit the worker's owned scope. The integration owner runs authoritative combined checks.

Workers report changed paths, actual checks and results, red or characterization observations, remaining uncertainty, and any partial work. Their report is a lead to evidence, not acceptance. Do not claim a child ran unless the host confirms it. If a launch fails before any child exists, report that state accurately and use only an allowed alternative. A failed or interrupted launch with uncertain state must be reconciled before retry.

## 5. Integrate and check the actual result

Inspect the actual diff and outputs, including added, removed, generated, and untracked files. Compare them with the assignment and starting state. A file inside an owned directory may still contain somebody else's new edit. Attribute changes before reverting or carrying them forward.

Integrate in dependency order. Recheck remaining results against the advancing state. A conflict-free merge does not establish compatible behavior. Resolve a semantic collision explicitly, rebase the affected work under the same intent when authorized, or finish it serially. Repeated broad edits or collisions are a reason to stop further parallel writing and preserve partial work.

Run checks that cover the integrated change. Inspect exit status and the actual output rather than searching only for a success word. Retain failed, blocked, skipped, and unavailable observations as such. If a check failed before the work, cite an actual baseline run on a relevant comparable state. An unchanged test path does not establish a pre-existing failure.

For persistence, cross a boundary that distinguishes saved data from a shared cache, such as a fresh process or an independent readback. For asynchronous work, observe the requested result after acceptance. For a UI change, exercise the real interaction and relevant layout states when available. Code inspection can support a claim when runtime access is blocked, but cannot replace the missing runtime observation.

Bind each check to its actual candidate, including relevant staged, unstaged, and new files, fixtures, runtime parameters, and generated instructions. Matching HEAD alone does not establish unchanged input. Preserve the command, result, time, and evidence location. Reuse a result only when its consumed inputs and dependency boundary remain applicable.

After simplification or review-driven repair, rerun affected verification against the resulting candidate. Do not reuse a previous green result for changed behavior. Use [verify.md](verify.md) for integrated acceptance and [review.md](review.md) for requested independent review. Keep independent review distinct from author tests, and preserve material dissent or missing coverage until the designated acceptance owner resolves it.

## 6. Finish without adding a delivery tail

Read the current request or plan again. Check that every requested behavior is implemented or explicitly blocked. Inspect changed lines for leftover experiments, accidental broad edits, duplicated rules, and unused abstractions. Clean up only owned temporary material, preserving useful evidence and user changes.

Verify that unrelated work and staged content remain intact. If a requested commit or publication follows, pass the exact candidate and evidence to the authorized step in [deliver.md](deliver.md). Otherwise leave the result local. A test run does not authorize Git or account mutations.

Return a compact report containing:

- What changed and where, including the exact candidate identity available in this host.
- Which requested units are complete, incomplete, or blocked.
- Focused pre-change and post-change evidence, plus integrated checks.
- Any deliberate test exception or unavailable acceptance observation.
- A changed decision, unexpected risk, or preserved partial work the next owner needs.
- The actual delivery state, without implying publication, deployment, or health.

## Example handback

This example illustrates the content; its results must be replaced with real observations.

"Implemented the shared reservation check in the service used by both the page and import endpoint. The existing multi-client test failed with two allocations before the repair and now observes one allocation and one conflict. The import and page endpoint tests pass on the integrated tree. A fresh-process read confirms the surviving reservation persists. Browser page acceptance is blocked because this environment has no usable browser session. The unrelated staged documentation change is unchanged. No commit or external action was performed."

This is narrower and more useful than "all tests pass" when one required observation is still missing.

## Resume and recover

Use [learn.md](learn.md) when the next owner needs a durable handoff. After interruption, read the current tree, previous result, active worker state, and any operation identifiers. Determine what already happened before rerunning a command. Preserve completed verified units. Recheck only evidence invalidated by changed code, inputs, environment, or elapsed relevance.

For an uncertain external mutation, read its outcome through a stable identity or the service's supported reconciliation method. An absent local success marker does not prove failure. Retry only when no effect occurred or repeating the exact operation is established safe and authorized. If neither can be established, pause that operation and report the ambiguity.

If a worker stopped after partial edits, inspect those edits and its actual state. Continue the same unit with a verified handoff rather than starting another writer over it. If restoration is needed, restore only attributable changes from a known baseline. Do not erase unknown work to recover a clean checkout.

After repeated failed patches, stop varying the same idea. Name the common assumption and test it through [debug.md](debug.md). A recoverable failure calls for diagnosis; an unresolved user decision or missing authority calls for a specific question.
