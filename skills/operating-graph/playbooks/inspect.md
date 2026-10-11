# Inspect without advancing a run

## Inputs and boundary

Use the exact selected run directory and the user's question: current progress, next work, blocked dependency, evidence lineage, approval, resource use or rewrite history. This method is read-only. It does not initialize, transition, register, approve, recover, apply a rewrite or finalize. A request to “check progress” is not permission to do pending work.

## Read and reconcile

1. Follow [CLI](../references/cli.md) for `resume-check` and `replay`. Establish whether committed history, graph versions, immutable receipts and projections agree. If integrity fails, report the first trustworthy observation and use [Debug](debug.md); do not fix records while inspecting them.
2. Read `status` for the exact run, current graph version, epoch, lifecycle and invocation states. Distinguish proposed work, prepared reservations, issued launches, observed workers, unknown outcomes, returned work, accepted outputs and terminal settlement.
3. Use `ready` or `dispatch-preview` to identify the current frontier without preparing packets. Explain why each important blocked node cannot proceed: exact required producer/input, missing effective approval, occupied capacity, exhausted bound, missing capability, stop state or unresolved operation. A frontier preview is not dispatch authority.
4. Inspect lineage from each disputed deliverable backward through consumed input identities, producing invocation, applicable graph contract and exact independent evaluation. Show historical/superseded/provisional data separately from currently eligible outputs. Report a missing observation as unknown rather than inventing a field.
5. Reconcile concurrency slots with outstanding reservations and observed/uncertain workers; reconcile monotonic launch/execution attempts with remaining budget. Include absolute deadline and epoch/version limits where defined. Do not derive a progress percentage from node counts when nodes have unequal work or uncertain outcomes.
6. Read effective approvals with subject/action scope and the latest trusted decision reference. A decision may be present yet inapplicable to changed content or destination. Imported grants without sufficient provenance remain declarations, not actual user permission.
7. Distinguish draft proposals, persisted proposals, deferred rewrites and applied immutable versions. Show why a rewrite is waiting for quiescence and which live or uncertain obligation holds it. Preserve completed historical facts under their original version; explain explicit carry-forward rather than relabeling them.
8. Render a concise text or Mermaid view when it answers the question. The diagram is a view, not a substitute for typed edges, optionality, approval logic and epoch semantics in the definition. Call out the bottleneck that changes the next step; avoid dumping the entire event log.

## Return

Report the requested fact, relevant exact identities, verified completed work, current blockers and the next permissible action. Separate machine lifecycle from semantic task acceptance. A completed status or conditional-pass does not prove the user received the correct result. Include unresolved worker/effect obligations even when the main deliverable already exists.
