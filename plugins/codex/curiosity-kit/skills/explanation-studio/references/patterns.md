# Choose the explanatory pattern

Use the pattern that answers the real question. Combine patterns only when they carry different necessary relationships. These are method choices, not mandatory output headings.

## How something works

Start with purpose, then a concrete input, the important transformation and the result. Show who triggers the process and who uses its output. Introduce supporting systems only when they explain that path. Avoid a function-by-function inventory.

Check: can the reader predict what happens to one input? If a downstream connection is unseen, label it unknown instead of drawing an invented arrow.

## Code or a change

Read the entry point, relevant calls, data and state changes, configuration, external effects, error branches and supporting tests. For a change, distinguish before from after at the actual revision. Preserve named symbols and conditions. Explain behavior before showing the source fragment that makes it precise.

Check: use an input that takes the main path and one that takes an important branch. A comment about intent is not proof the branch works. Do not execute state-changing code merely to explain it.

## Tradeoff or decision

Use the same desired outcome and constraints for the compared options. State each useful benefit, cost, limiting condition and accepted downside. A priority-based choice is not proof one option is universally better.

Separate a recorded decision reason from your current assessment. If history is missing, explain the present tradeoff and label proposed rationale as inference. Do not manufacture an alternatives-considered section from plausible options.

Check: could a different stated priority reasonably favor another option? If so, show that condition rather than hiding it.

## Incident

Lay out the prior state, observed trigger, failure path, impact and recovery. Distinguish initiating trigger, contributing factors, observed symptom, root cause and failed safeguards. The component showing an error may not have caused it.

Use timestamps and units as supplied. Do not convert order into causation. When evidence supports several causes, use clearly labeled possible branches and state what observation would distinguish them. A recovery that coincided with improvement is not automatically a proven fix.

Check: does every causal arrow have evidence or an uncertainty label? Keep important missing telemetry visible.

## Failure or blocked action

Compare expected and observed behavior. Identify the smallest established difference that explains the mismatch. If the cause is not established, describe what is known and the next safe diagnostic step rather than declaring a fix.

For a status, say what completed, what is blocked, practical impact and required next action. Explain whether a human decision is needed. Missing evidence is not passing evidence. Do not infer prior system effects from a read-only explanation call.

Check: can the reader act without mistaking an unknown or proposed action for something already completed?

## Architecture

Show one important end-to-end path, its boundaries and the responsibilities needed to understand it. Add supporting systems in a second layer. Use containment for ownership and arrows for a named flow; do not conflate them.

Keep a small source-location map only when it helps the reader find the real implementation. A neat architecture picture must not hide a known exception or dependency.

Check: can the reader locate the entry, transformation and outcome without reading every component?

## Algorithm

Choose a small concrete input that exposes the important decision. Show the state before each operation, the condition, the transformation and the next state. Keep indices, units and representation consistent. State stopping conditions and relevant assumptions, such as sorted input.

Example, binary search for 6 in `[2, 4, 6, 8, 10]`: with zero-based inclusive bounds 0 and 4, midpoint 2 contains 6, so return 2. A second target, 7, needs successive bounds `[0,4]`, `[3,4]`, then `[3,2]`; the last range is empty, so the target is absent. Do not silently change from inclusive to exclusive bounds to make a trace fit.

Check: run the steps by hand, including a missing or boundary input. Animation frames must agree with the trace. Complexity claims need the algorithm's assumptions, not just its name.

## Abstract concept

Use a concrete instance or structural analogy. Name the relationship that transfers, explain the concept without the analogy and mark the mismatch. A metaphor that only shares vocabulary is not enough.

Check: does a counterexample reveal a false implication? Narrow or replace the metaphor before making it memorable.

## Before and after

Keep content, scale, orientation and comparison conditions consistent. Highlight the actual difference. If time, sample, denominator or environment changes, label that difference. An attractive after image is not evidence that a measured outcome improved.

Check: can the reader distinguish a changed mechanism from a changed presentation?

## Procedure, tutorial or reference alongside explanation

A procedure starts with the goal and prerequisites, then gives actions, conditions, observable results and recovery. A tutorial guides a novice to one visible success with only necessary supporting theory. A reference gives exact lookup facts and limits. Split substantial mixed purposes, but do not force four files or forbid a useful small table inside an explanation.

A step that cannot be verified is not automatically wrong; name the uncertainty. Never invent a command, UI control, successful run or user permission to complete the form of a guide.
