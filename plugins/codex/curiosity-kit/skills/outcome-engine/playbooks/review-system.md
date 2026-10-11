# Review a system

Review a recurring workflow, project or operating process when its structure causes repeated friction. Do not turn proofreading, one isolated error or a named small repair into an architecture program. This method produces an evidenced recommendation and bounded pilot proposal; it does not implement live changes unless separately authorized.

## Understand the current system

Name its user, recurring trigger, intended result, frequency or volume and acceptable failure. Read relevant contracts, decisions, process notes, artifacts and observed incidents. Mark unavailable evidence and estimates. A single anecdote can justify a question, but not a claimed recurring baseline or quantified savings.

Map the path from trigger to completion: inputs, steps, decisions, accountable owners, handoffs, waiting, rework, approvals, observations, exceptions and failure points. Use a small diagram when it clarifies the relationships. Capture the actual path, including off-system work, without inventing steps from a generic template.

Separate process, training, authority, data, incentives and tooling causes. For example, missing approval authority cannot be fixed by another automation; an unclear source document may require an owner decision rather than a new dashboard. State which cause is observed, inferred or unknown and what would distinguish competing explanations.

## Find useful structural changes

Focus on demonstrated friction and areas that actually change. Look for a decision scattered across many places, repeated data entry, unclear ownership, repeated interpretation at a handoff or proof separated from the work. Respect settled decisions. Reopen one only when new evidence warrants it, and name the conflict.

A responsibility should expose a small understandable interface while owning substantial useful work. Related decisions should change together. Apply the deletion test: if a wrapper or step disappears, does required complexity become simpler in a better home, or merely spread across its callers? Deleting an approval or recovery step because it looks slow can remove a necessary control.

Compare a small evidence-backed set of alternatives, including the current process, consolidation or removal where useful. Two to five can fit a complex review; do not invent extra candidates to reach a count. For each viable change, state:

- Observed friction and source, current responsibility/interface and proposed change.
- Before and after path, who would own it and which facts or decisions move.
- Expected locality, reader/operator effort or proof benefit, with measured baseline or explicitly unmeasured hypothesis.
- Risks, affected consumers and compatibility/authority constraints.
- Recommendation strength and what would weaken it.

Recommend the best evidence-to-risk choice. A neat diagram, fewer lines or a claimed AI capability is not itself an outcome improvement.

## Allocate work and controls

For each proposed future step, choose human judgment, AI assistance, deterministic automation or removal, with an owner and reason. Keep consequential authority, relationships and accountability with the appropriate person. Use AI for bounded interpretation/drafting with relevant checking. Automate stable, permissioned repetition only when inputs and failure behavior are understood. Remove work only when no necessary function or control is lost.

Define controls before selecting tools. Name the input preconditions, approval gate, exception path, failure signal, what the user sees, recovery owner/action and rollback. Include silent failures: a report generated from stale data, a notification never delivered or a record marked done while its artifact is missing. Where concurrent changes matter, account for competing completion orders or the actual locking/ownership mechanism; do not invent a distributed-state system for a small manual process.

State actual tool prerequisites and unavailable surfaces. An account integration described in a plan is not installed. Review agreement is not permission to change settings, create credentials, send messages or replace a live process.

## Design a right-sized pilot

Preserve these fields in the [system-review record](../assets/work-records.md): scope, owner, baseline, success signal, stop rule, rollback path, review date and exclusions. Add the actual evidence collection method and post-pilot proof. A missing required owner/date remains a named decision, not an invented assignment.

Choose a reversible pilot narrow enough to distinguish the main hypothesis. Keep one necessary success measure and countermeasure that catches the likely harmful tradeoff. For example, reduced handoff time is not success if required approvals disappear. A trial in synthetic records proves only that workflow, not production performance or customer benefit.

Use [bounded tests](bounded-tests.md) when the pilot needs precommitted prediction, sample rules and a durable observation ledger. Do not create a second ledger or scorecard with conflicting definitions. For a migration, use the slice method's consumer inventory and final integration gate.

## Review and return

Check that all source-backed claims, causes, proposed changes and unmeasured benefits are distinguishable. Preserve exact counts and conditions. Inspect whether every necessary old function has a future owner and proof, including exception handling and recovery. A reduced interface must not hide an essential missing capability.

For a canonical local review, run `check_outcome.py review FILE` under the [checker contract](../references/checker.md). Its section/pilot checks do not prove the diagnosis, feasibility or real pilot results. Use the requested format when different and disclose any unavailable check.

Return the actual review, the recommendation and pilot, decisions genuinely needed and remaining evidence gaps. If the user then authorizes implementation, carry the accepted scope into briefing/slicing without repeating the entire interview. Until then, keep the current system unchanged.
