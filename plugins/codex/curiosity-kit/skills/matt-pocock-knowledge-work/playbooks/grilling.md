# Matt: grilling

Source status: promoted. Use only inside the explicitly selected Matt library. Before first action, apply [the host contract](../references/host-contract.md).

## Interview engine

Interview until the design tree is resolved to shared understanding. A design tree records each decision and the decisions or researched facts it depends on. Start with the user's goal, supplied decisions and unresolved branches; do not make them answer settled questions again. It works for software, knowledge work and mixed projects.

1. Establish the decision tree from current context. Find facts in authorized files, sources and tools rather than asking the user to do lookup work. Where the host supports delegation, give a bounded leaf researcher the specific factual question and source/output scope; it researches directly rather than starting another interview. A running lookup is an unsettled prerequisite. Continue independent branches while it runs.
2. Compute the **frontier**: all unresolved decisions whose prerequisites are settled. Ask the whole frontier in one numbered round. Keep dependent questions for a later round. For each question include a concise title, necessary context, genuine alternatives and your recommended answer with its reason. Phrase it so “yes” accepts that recommendation.
3. Wait for the user's answers. Ambiguous or partial answers resolve only what they actually settle. Recompute the tree after each round: answers may remove branches, reveal new ones, or invalidate earlier assumptions. A missing factual answer delays only its descendants.
4. Continue until every in-scope branch is visited and resolved. An empty frontier caused by blocked lookups or unresolved prerequisites is **blocked**, not done. Surface the remaining blocker rather than inventing an answer.
5. Summarize the settled design, relevant exclusions and any explicitly accepted uncertainty. Ask the user to confirm shared understanding before acting on the design. This confirmation is distinct from permission for external actions; apply the host contract to the actual next action.

Example round (adapt presentation to the conversation channel):

Q1 — Audience: Should the guide assume first-time users? Recommended: yes, because the supplied audience has no prior experience.

Q2 — Delivery: Should the agreed deliverable be a printable reference? Recommended: yes, because it will be used offline.

If Q3 asks which advanced concepts to omit, and depends on Q1, hold it for the next round. If only the printing capability is being researched, Q1 can proceed while Q2 waits.

## Sequential preference

The original private method asks one question at a time. Honor an explicit sequential preference: choose one ready frontier decision, recommend an answer and wait, then recompute. Retain the same dependency and exhaustion requirements. Default current behavior is frontier rounds; switching presentation does not transfer decisions to the agent.

## Grill-me

`grill-me` is the explicit wrapper for this complete engine. Run the procedure above; it is not a separate interview implementation. A mention or quotation of its name is not activation. If another Matt method composes grilling, apply that caller's subject/output scope while retaining this interview discipline.
