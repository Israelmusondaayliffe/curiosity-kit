# Decision Wayfinder

Use when explicitly asked to wayfind, map an uncertain effort, find the next blocking decision, or determine what must be settled before planning. Deliver a decision map and one useful next edge, not a complete execution plan. Read the [common evidence/choice contract](../references/evidence-and-choice.md). For durable output use the [map template](../assets/decision-map.md).

## Establish the destination

State the observable successful end state, owner, horizon, evidence of arrival and exclusions. Read existing map/conversation and closest authorized sources before asking known facts. Preserve accepted decisions and their provenance; distinguish a current proposal from a settled record. If success cannot yet be defined, make that the first unresolved node rather than inventing a destination.

## Build and inspect the map

Give each material decision a stable ID and precise question. Record prerequisites and what it unlocks. Include options, owner, source evidence, recommendation if justified, acceptance test, and actual decision record when settled. Classify:
- **settled**: an accepted decision exists with rationale and provenance.
- **frontier**: prerequisites are satisfied and the remaining question can be decided from available evidence/user judgment.
- **fog**: the shape of the uncertainty is not yet understood; first define what must be learned.
- **blocked**: the question is precise but a named prerequisite, owner, source or authority is missing.
- **deferred**: deliberately postponed, with reason and revisit condition.

A precise unanswered question is not vague fog. An option with an unresolved hard prerequisite is not ready. Trace prerequisite IDs, missing references and cycles; surface a cycle and the evidence/choice needed to break it instead of arbitrarily declaring a frontier. Do not require code or a graph engine for a small map.

## Work one edge

Compare ready frontier nodes by downstream unlocking effect and the consequence of delay, respecting user priority. Choose one; explain what it blocks and what evidence or user judgment would resolve it. Recommend a default only when supported and label it as such.

If that branch needs an actual full interview, read [Grill Me](grill-me.md) and hand it only the current question, relevant settled prerequisites, options/constraints, evidence and acceptance test. If a factual check or one clarification suffices, use that directly. Do not launch a whole-plan interview.

Bring back the actual accepted branch result, rationale and source/choice provenance. Update that node and affected dependencies, preserving history rather than rewriting older choices as if they never existed. Recalculate the frontier. Stop once the next blocking edge is named unless the user asks to continue one edge at a time. An unaccepted recommendation cannot settle the node.

## Persist and resume

Keep the map in a user-authorized file when useful, or return it in the conversation. Save only the compact current map plus relevant decision history and source locators. A fresh reader must find the destination, statuses, dependencies, unresolved evidence and exact next edge without the whole chat. On resume check whether evidence/prerequisites changed; reopen only affected nodes and explain why. If persistence is unavailable, provide the complete map and explicitly say it was not saved.

Before returning, reconcile each status with its recorded prerequisites, owner and decisive inputs: a missing material requirement stays blocked, and a conditional next edge is not a ready frontier. Return destination, fog, frontier, next edge/why it blocks, any decision just settled and recommended next action. A settled direction can be handed to the requested execution workflow; optional Outcome Engine handles action slices, optional Continuity Vault preserves the map. Neither is required or replaces Wayfinder ownership. No scheduling, tracker mutation or execution is implied.
