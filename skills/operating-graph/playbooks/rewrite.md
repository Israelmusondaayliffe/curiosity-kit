# Rewrite only the inadequate part of a graph

## Select the operation

A design proposal, a persisted proposal and an applied rewrite are three different actions. A draft outside the run leaves canonical state unchanged. Persisted submission writes a controller record. Application changes the graph version and active work/evidence. Establish which action was requested; do not promote a review comment into permission to apply it.

Read [rewrite-policy.md](../references/rewrite-policy.md), the exact run's policy and the relevant [CLI](../references/cli.md) operations. Use [Debug](debug.md) first when the cause is unclear. Corruption cannot be fixed by loosening graph rules.

## Diagnose and choose

1. Cite the triggering events and concrete inadequate behavior. Distinguish a bad node result, missing input or temporary host failure from a topology problem. A bounded local retry belongs inside a node when its contract remains correct; the graph changes only when relationships, responsibilities or checking need to change.
2. Consider the smallest complete change using the existing primitives: `add_node`, `update_node`, `disable_node`, `add_edge`, `disable_edge`, `set_priority`. The nine available patterns compile into those primitives; they are design conveniences, not exemptions from validation.
3. Identify affected contracts, producers, consumed/produced artifacts, descendants and evaluator receipts. Preserve unaffected completed results only through a deliberate carry-forward rule. Unknown impact invalidates dependent claims. A scheduling-only priority change need not discard valid semantic work.
4. State predicted benefit, possible regressions, risk, required approval and rollback reference. Check interactions across the sequential operations in the proposal; an individually harmless operation can become unsafe after another operation changes the same node.
5. Preserve the original goal, criterion meanings, required deliverables, authority, permissions, hard limits and effective approval boundaries. Policy can restrict the engine's safety floor, not override it. A changed goal or broader authority is a new authorized task/run, not a rewrite that quietly moves the acceptance target.

## Submit and apply

When persisted submission is requested, bind the proposal to the exact run/base version, valid evidence events and safe proposal identity. Validate the complete proposed graph, not only the edited node. Honor the policy's automatic, approval and prohibited mutation rules. A low-risk label never grants user authority that the workflow lacks.

Before applying, stop new dispatch and reach a genuine quiescent boundary: no outstanding prepared reservations, uncertain launches, live workers/reviewers, pending return ingestion, partial operations or unacknowledged cancellation. Settle existing work with its current contract. Do not hold a filesystem lock while waiting for a worker. If a child cannot be observed or stopped, leave the rewrite deferred with that exact blocker.

At commit, recheck current base version, effective scoped approval, policy, remaining version/rewrite budget and quiescence under the runtime's writer guard. Apply once, preserve old versions and invocation history, and record the affected-set invalidations. A semantic change creates explicit fresh work; never erase a successful historical attempt or activate its stale outputs under a new meaning.

After application, inspect the new immutable version and replay consistency. Check affected prerequisites, outputs, criteria and nearby positive behavior before continuing. Prior independent evaluation of changed output is stale. Reuse unchanged completed evidence only through the recorded carry-forward binding.

## Failure and rollback

Reject stale proposals, unsafe paths, unsupported policies, nonexistent evidence, missing permission and changes to protected boundaries. Missing quiescence is a resumable deferral, not a reason to strand packets by incrementing the version anyway. If persistence is interrupted, use supported recovery; do not manually delete an immutable version and retry.

Rollback is an explicit new version restoring an eligible prior topology through the permitted operation contract. It never erases history, refunds consumed attempts, restores revoked consent or pretends intervening external actions did not happen. Re-evaluate evidence eligibility and required approvals after rollback.

## Return

Return draft/submitted/deferred/applied status, exact proposal/base/new version, causal evidence, risk/approval decision, affected and preserved work, checks and next action. A submitted proposal is not an applied fix, and an applied fix is not a newly verified task outcome.
