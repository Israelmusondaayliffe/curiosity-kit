# Matt: loop-me

Source status: beta / experimental. Use only inside the explicitly selected Matt library. Before first action, apply [the host contract](../references/host-contract.md).

Run a stateful [grilling](grilling.md) interview whose output is a complete workflow specification, not a running automation. Load the full interview engine. Work across sessions by rereading the workspace, not by assuming remembered state is current.

## Loop lens

A **loop** is a recurring pattern in the user's career, week, morning or repeated activity. Look for loops within loops and propose useful patterns the user has not noticed. A **workflow** is the specification of one such pattern; its running instantiation is a loop. Recurrence may make work worth delegating, but does not require AI or automation.

## Workspace and discovery

- `NOTES.md` holds facts about the user's world, tools, channels and canonical terminology. When missing or thin, interview about those before specifying a workflow. Sharpen fuzzy terms as they emerge, retaining the user's intended meaning.
- `workflows/*.md` holds one authoritative spec per workflow. Inspect existing names/content before choosing a path. Re-read before updates; reconcile user edits. Create or edit only within the requested workspace and scope. Retiring a spec requires the applicable recoverable-deletion approval or a non-destructive supersession; never silently remove one.

## Interview and spec

Ask the ready frontier with recommendations, or honor requested sequential mode. Research available facts yourself. Establish what the user wants to delegate, why, what starts and ends a run, inputs and source access, outputs and recipients, success evidence, failure/retry/cancellation behavior and any required authorization. Use existing answers; do not ask the user to fabricate knowledge about unavailable APIs. Preserve unresolved questions until answered.

Use this vocabulary only when it helps; it is not a mandatory structure:

- **Trigger:** an event, such as a new email, or a schedule. Event-triggering can avoid unnecessary polling; the actual source capability decides what is possible.
- **Checkpoint:** a human decision/verification point. Some workflows need none; some use no AI.
- **Push right:** prepare as much as allowed before asking the human, so they can decide once with evidence. Required safety/authorization checkpoints remain before their governed actions.
- **Brief:** a compact decision-ready summary of what was produced, why it matters and a link to the full asset. It should make review fast without concealing information material to consent or correctness.

Write the resolved spec in the user's natural vocabulary. Include only sections the workflow needs, but cover every operating path an implementer must handle, including exceptional outcomes, recipients and permission boundaries. A workflow needs no AI, checkpoint or schedule merely because this method has named them.

## Completion

Walk a normal run and each relevant failure/decision path against the spec. It is done when an implementer can build it without guessing an unresolved requirement or asking another design question. Confirm shared understanding using the interview engine, then report the spec path and remaining real capability checks, if any. Do not start a loop, install tooling, subscribe to events or create a schedule from a specification request. Cancellation ends the interview.
