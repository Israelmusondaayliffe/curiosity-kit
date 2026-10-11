# Verify without repairing

Read the contract independently of the actor's account. Inspect the actual deliverable and fresh workspace state. The snapshot and captured output establish what ran; they do not establish whether the checks measured the right thing.

1. Confirm contract identity, intended host/workspace, current generation and unit coverage. Check that required checks were not deleted, renamed, narrowed or replaced by stubs. Confirm declared input files include the code/data determining each check.
2. Execute the relevant recorded checks when safe and authorized. Capture invocation, resolved executable, cwd, input hashes, exit or timeout, output and current artifact binding. Treat spawn errors, skipped checks, output limits and unavailable dependencies as failures/blocks, not empty success.
3. Inspect the check itself: does it drive the user's real path and test the exact symptom? File existence, a screenshot without action context, a green typecheck or a model's assurance cannot substitute for required behavior. For a UI/service, inspect both the visible result and material side effects. A mock or dry run proves only what it actually exercised.
4. Assess each judgment criterion separately against the artifact: correctness, usefulness, quality or other contracted outcome. Record criterion, verdict, reviewer, actual evidence and reason. If independence is required, use a genuinely separate reviewer/context and preserve its provenance. Missing/failed reviewers are unavailable; self-review must be labeled accurately.
5. Confirm evidence still matches the current contract, scripts/inputs and relevant artifact bytes. Later edits invalidate affected checks/reviews. Recheck affected earlier units through the supported integrated CLI rather than silently reopening or hand-editing state. If that path is unavailable, block completion and report the concrete repair needed.
6. Finish only when every required check and judgment is satisfied. Otherwise give precise findings and the smallest next action. Repair is a separate operation followed by fresh verification.

## Adversarial checks

Look for constant success, swallowed errors, missing required branches, stale captures, artifact mutation during checking, evidence referring to another run, unsafe effects outside scope, optional help misrepresented as an independent review, and blocked access presented as a no-op. Ask whether the check can actually go red on the fault. Verify the real value or process, not an mtime or cached narrative.

Hashes protect a binding from unnoticed drift; they are neither domain-quality grades nor protection against an adversary who can rewrite the run and recompute every hash. Report proof at the level actually established. Host hook or scheduler behavior requires that actual host surface, not direct script invocation alone.
