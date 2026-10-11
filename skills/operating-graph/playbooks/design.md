# Design a useful operating graph

## Inputs and decision

Use after explicit Operating Graph selection for a new or revised design. Obtain the intended outcome, source material, required deliverables, observable acceptance criteria, permitted actions, actual decision authority and finite resource limits. Existing approved directions need no generic re-interview. A design request authorizes design artifacts; it does not start workers, initialize a run or perform the proposed actions.

Decide whether a graph improves the work. Use real dependencies, genuinely independent lanes, independent evaluation, consequential approvals or bounded feedback as reasons. For an ordinary serial task, keep an inline path. Do not add a planner, skeptic or arbitrator merely because the node kind exists. Keep knowledge indexing with its source-owning method.

## Build the contracts

1. Freeze the original goal, typed deliverables, stable criterion strings and authority. Make each criterion observable: what output must exist, which fact/behavior it must demonstrate, how it will be checked and who can judge it. “High quality” alone is not a check. Separate task success from optional improvement and from authority to publish or otherwise act externally.
2. Choose exactly one authority and one controller. Separate production from evaluation of that production. Assign every node one bounded outcome, execution mode, owner, input identities, output types, success criteria, allowed write scope and finite budget. Workers receive enough source/context to finish without the parent transcript; inaccessible pointers are missing inputs.
3. Add only genuine prerequisite edges. A dependency carries exact upstream outputs and the context needed to use them, not just order. Independent lanes should run concurrently within real capacity. A downstream join waits for all required, current inputs. Optional work cannot accidentally become a mandatory global barrier.
4. Separate data readiness, shared-write conflicts and approval gates. Prefer independently owned output/patch artifacts and one integration writer. If two tasks must edit the same canonical file, serialize them or redesign the outputs. A shared base revision must be explicit. Conflicts need a resolution step; last-writer-wins is not a policy.
5. Give every required deliverable an independent evaluator path. The evaluator receives its exact digest, original criteria and appropriate raw sources. A separate role label is not sufficient if the same invocation produced and approved its output. Integration needs its own whole-result check; passing branches do not prove the assembled result.
6. Mark external actions and their exact authorization scope: action, destination, content/data version, authority and any required moment-of-action confirmation. An APPROVE edge is mandatory even under ordinary ANY activation. Authority-node success is never consent. Use inert sample effects for a design demonstration.
7. Mark optional nodes and explain their omission rule. Define what happens on failed input, missing capability, malformed return, exhausted retry, deadline, cancellation and unknown external outcome. Choose partition, race or mixed topology only when useful. A race needs a predeclared selection rule and full loser accounting; do not silently accept the first answer.
8. Bound total work, concurrency, launches/retries, graph versions, epochs and any node-local loop. Leave capacity for the controller and actual host constraints. Distinguish runtime-measured counters from worker-declared effort. Do not treat a packet's suggested effort as enforced host measurement.
9. Encode cycles only with explicit next-epoch feedback and a finite epoch limit. Declare the epoch-one seed, barrier, exact previous-epoch feedback and exit rule. Same-epoch execution stays acyclic. Historical successful invocations survive recurrence; a new epoch creates fresh work rather than overwriting the old attempt.
10. Use [graph-contract.md](../references/graph-contract.md) for actual fields and [templates](../assets/templates/graph.json) as concrete starting data. For a useful checked fan-out, consult the [diamond](../assets/templates/diamond-graph.json): independent specialists, integration and final evaluation. A skeptic before synthesis is useful when competing evidence needs challenge, not a compulsory stage for every job.

## Validate and explain

Save the definition in the agreed design location and give a compact diagram that labels meaningful data, approval and feedback relationships. The JSON contract is authoritative; an unlabeled Mermaid arrow cannot explain all execution semantics.

Run the local `validate` command from [CLI](../references/cli.md). Inspect every reported violation and repair the design, preserving the original goal and authority. Check the prospective frontier by reasoning from actual prerequisites and capacities; do not initialize a run merely to produce a design preview. Check resource references and write ownership, not only acyclicity.

Walk through one ordinary path and one consequential failure: which node becomes ready, which exact evidence arrives, which gate blocks, and what the controller does next. If the intended job cannot be expressed safely, name the missing capability rather than inventing an executable condition or quietly dropping it.

## Return and handoff

Return the graph definition, readable topology, criterion/evaluator mapping, bounded execution assumptions, validation result and unresolved decisions. State clearly that no run has started. If execution was separately requested and authorized, hand the definition and current authority to [Run](run.md); otherwise stop at the design. Material external actions retain their own confirmation requirements.
