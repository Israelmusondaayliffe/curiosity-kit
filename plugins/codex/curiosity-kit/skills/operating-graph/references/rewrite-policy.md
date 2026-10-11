# Rewrite decisions and preserved boundaries

Load for graph changes. [Rewrite](../playbooks/rewrite.md) owns the complete operational method; [CLI](cli.md) supplies the actual proposal/application interface. A proposal cannot grant its own authority.

## Diagnose a reason to change topology

Look for an observed failure that the current node contract cannot resolve within its local budget: repeated failure, material contradiction, a genuinely unsatisfiable dependency, a conflicting shared writer, costly unnecessary fan-out or a terminal evaluator's specific rejection. Resource use at roughly half, three quarters or near exhaustion can prompt inspection; those thresholds are advisory, not an automatic permission to mutate.

A simple local correction does not require a rewrite. Conversely, retries that repeatedly expose the same ownership/dependency error call for a new shape. State the concrete triggering event, expected improvement, regression risk and affected verification before choosing an operation. A deadline or exhausted budget stops work; it does not expand the budget.

## Primitive operations

- `add_node`: add one complete, distinct node contract and connect it lawfully. Do not add a second authority/controller.
- `update_node`: change allowed contract fields; semantic changes invalidate affected successful work and descendants. Protected authority/permission/goal boundaries remain fixed.
- `disable_node`: remove its future eligibility, never its history. Repair or explicitly disposition affected edges; do not eliminate essential work to manufacture completion.
- `add_edge`: add a real dependency/relationship with valid endpoints, typed data and temporal semantics. Recheck the whole same-epoch graph.
- `disable_edge`: remove only a permitted relationship. Effective required approval/evaluation cannot be weakened by toggling a flag or ANY mode.
- `set_priority`: alter deterministic frontier ordering. Unchanged semantic evidence can remain valid through explicit carry-forward; priority is not authority.

The engine applies operations in order to an owned graph copy. Validate each operation against its actual intermediate context and the complete result against the immutable original contract.

## Nine patterns, without hidden privileges

| Pattern | Use | Required judgment |
|---|---|---|
| `split_node` | One task has separable outcomes or overloaded context. | Keep every original required output; connect children and repair old edges. |
| `merge_nodes` | Artificial separation creates handoff cost or inseparable checks. | Preserve distinct requirements, ownership and evaluation; no self-approval. |
| `replace_node` | A node's approach/capability is unsuitable after bounded evidence. | Preserve old attempts, source inputs and downstream obligations. |
| `add_reviewer` | A deliverable needs a missing independent check. | Reviewer receives exact artifact/criteria and is genuinely separate. |
| `reroute_edge` | The original prerequisite is wrong or unavailable. | Substitute equivalent current evidence, not an easier acceptance target. |
| `collapse_fanout` | Optional decomposition adds no useful independent work. | Account for every child before disabling; retain necessary outcomes. |
| `serialize_branch` | Writers conflict or one result really depends on another. | Add genuine order without inventing a global barrier. |
| `create_arbitration_node` | Material conflicting evidence needs a reasoned decision. | Supply both sources and a selection criterion; arbitration cannot grant authority. |
| `promote_successful_pattern` | Better ordering is supported by the current job's evidence. | Changes priority only; no global learning, policy installation or cross-run memory. |

These patterns compile to the primitives. The compiler is not proof the final graph is connected, acyclic, complete or authorized. In particular, disabling an old node does not automatically repair all its incoming/outgoing edges.

## Risk and policy

Use the runtime's calculated risk as a floor. A proposal may declare more risk, never less. The highest applicable operation risk controls the proposal, including context introduced by earlier operations. The graph's `automaticRiskLevels`, `approvalRiskLevels` and `prohibitedMutations` restrict application; unsupported or contradictory policy declarations must not be silently ignored.

Typically priority-only adjustments and harmless unstarted optional work are low risk. Worker/contract changes, necessary rerouting and changes that invalidate accepted artifacts need stronger review; external effects or removal of required evaluation are especially consequential. Labels do not override actual policy or the immutable safety floor. Do not call an evaluator addition safe just because its purpose includes a reassuring word.

Some operations remain forbidden even with a granted proposal: changing the original goal/criteria, weakening required approvals, changing authority, expanding existing permission scope, increasing frozen hard limits, erasing history, rewriting immutable versions or allowing self-evaluation. If those are truly needed, stop and design a separately authorized new run.

## Apply at a safe boundary

Persisted submission requires the exact run/base version, safe proposal ID, existing evidence references, full operations, reason, predicted effect, risk and rollback reference. Application also requires current authority and the run's finite rewrite/version allowance.

Drain to quiescence before version mutation. This includes prepared reservations, unknown launches, live workers/reviewers, pending returns, partial commits and unacknowledged cancellations. Ordinary independent work can run concurrently; quiescence is a version-mutation boundary, not a barrier after every batch. A blocked drain leaves the proposal unapplied and records the precise obligation.

At apply time, revalidate version, policy, scoped approval, budgets and quiescence under the single-writer guard. Commit one immutable new version, affected-set invalidation and explicit carry-forward. Prior successful invocations stay under their original contracts. New semantic work gets a new invocation; old reviewer success does not certify its result.

## Rollback and corruption

A rollback reference identifies an immutable earlier version. Restoring its shape is a new proposed/validated version within current authority; it never rewinds event history, refunds attempts, revives denied approval or undoes an external effect. Validate the current evidence and affected closure again.

Event corruption is not a high-risk rewrite that becomes safe through approval. Stop automatic mutations and use the supported diagnostic/recovery contract. Recover only from trustworthy committed records; retain unknown external obligations. Do not edit a hash until a previously failing verifier says pass.
