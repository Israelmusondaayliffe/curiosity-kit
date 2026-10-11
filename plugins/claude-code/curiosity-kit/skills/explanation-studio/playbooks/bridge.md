# Build a truthful bridge

Use when the reader supplies a familiar system, asks to draw on what they know, requests a different analogy or challenges a mental model. The result must remain accurate after the analogy is removed.

## Establish the known side

Prefer an explicitly named familiar system, then understanding demonstrated in this task, then relevant context already available and appropriate to reuse. Use earlier private material only within the user's requested scope. Do not search unrelated history or infer an identity to make the explanation feel personal.

Separate claimed familiarity from demonstrated ability when the distinction matters. Knowing a word does not establish the underlying mechanism. If no useful bridge exists, explain plainly or ask one concise question whose answer would materially improve the mapping. A generic accurate explanation is better than forced personalization.

## Choose by structure

Identify the target's inputs, outputs, steps, constraints, state and feedback. Compare relationships with the familiar system, not just similar labels. Relevant matches include sequence, capacity, ownership, hierarchy, composition, abstraction and handoffs.

Choose the strongest small match. Two analogies are useful only if they explain different necessary relationships without contradicting one another. Do not mix them into an incoherent system.

Test the proposed bridge on a concrete normal case and one boundary. If the bridge predicts a false property of the target, narrow it, replace it or explain without it. Do not repair a fundamentally wrong comparison by adding a long disclaimer.

## Teach known, connection, actual mechanism, limit

Start with the familiar behavior. Map the useful relationship to the new concept. Explain the new concept in its own terms and introduce its correct vocabulary. State the material mismatch before the reader is likely to act on a false inference. Finish with a practical implication or a compact memorable model if useful.

Explicit mappings help when several correspondences carry real meaning. Use a table only when the requested medium and the number of useful correspondences justify it. Do not add weak rows to fill a template.

### Example

Reader: “I understand ordering from a restaurant menu. Explain an API.”

“The menu tells you which orders the kitchen accepts. An API similarly defines requests another program accepts. Your program sends a request in the required format, and the other program returns data or an error.

The menu is like the API documentation. The order is the request; options in the order are parameters. The result is the response.

The comparison helps with the agreed request format. It does not mean the program interprets a request as flexibly as a waiter, or that every request is safe to repeat. Some requests change stored data.”

The final limitation matters if the next topic is retries. A familiar story must not imply that duplicated requests are harmless.

## Follow-ups

- Deeper: keep the useful bridge and reveal the next mechanism or constraint. Do not restart the whole introduction.
- Technical version: connect familiar labels to exact terms, data structures and interfaces, then use the real vocabulary.
- Different analogy: choose a different verified familiar system, explain why it fits this relationship better, and state its new limit.
- Where am I wrong: identify the specific false inference, show the counterexample and replace only the broken part of the model.
- ELI5: reduce simultaneous moving parts and vocabulary, not truth or uncertainty. Write for an intelligent reader, not a caricature of a child.
- Connect to my work: use supported task context and a real consequence. Do not invent a workflow or private preference.

For a combined visual request, pass the mapping, true mechanism and important limit into [visual](visual.md). Keep one answer. The mismatch must survive in the picture or its adjacent text; a confident diagram must not erase a qualified analogy.

## Check and recover

Can the reader follow the real mechanism without the analogy? Are causal direction and constraints preserved? Does the normal case work? Does the boundary expose the stated limit? Are familiarity and personalization supported?

If the reader rejects the familiar side, accept the correction and choose another explanation. If the target itself is uncertain, carry that uncertainty through the mapping. Do not claim that an analogy or a user's “got it” proves understanding. Use [teach and repair](teach-and-repair.md) for a requested application check.
