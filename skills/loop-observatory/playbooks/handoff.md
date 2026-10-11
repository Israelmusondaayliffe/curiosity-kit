# Unresolved repair handoff

Use after intake/report/audit finds a material problem that the execution, judge or evidence owner must resolve. This method completes an analytical handoff; it does not execute the next action. An installed owner skill is optional.

## Build one evidence-bound case

Record:

1. **Owner and request:** the producer/agent/evaluation owner responsible and the smallest check being requested. If ownership is unknown, say so rather than choosing a random available tool.
2. **Immutable target:** producer, namespace, logical run ID, source revision/snapshot ID, artifact hash/version, criterion and rubric/version. Include judgment observation IDs when relevant.
3. **Observed problem:** what the captured evidence actually shows and why it matters. Use exact counts or locations; distinguish it from a causal conclusion.
4. **Evidence:** source and report locations, hashes/field pointers, capture/coherence limits and applicable event/knowledge times. Keep private references within the authorized audience.
5. **Competing explanations:** the plausible alternatives still consistent with the evidence. Include missing/changed artifact, rubric mismatch, reference error or collection defect where relevant.
6. **Discriminating check:** the smallest read or owner-controlled test that would distinguish those alternatives. State the expected observable result for each interpretation.
7. **Permissions and state:** whether the user authorized only this analysis or separately authorized repair. Default handoff state is unresolved; do not start a repair, pause a run, change a rubric or send an external message as an implied side effect.
8. **Resolution evidence:** what new owner receipt, source revision, artifact and judgment would be needed to mark the issue resolved. Old success text or a generic “fixed” message is insufficient.

Preserve the original failed or disputed evidence. A later correction adds a new bound revision/receipt and can change the current view; it does not erase the history or retroactively validate the earlier claim.

## Example: pass-side disagreement

Run `graph / checkout / run-17`, source revision 12, artifact `sha256:61…`, criterion `required-error-state`, rubric `ui-quality@3` has machine observation `judge-17` positive and adjudicated human observation `review-17` negative. Both bind the same artifact and rubric. The supplied screenshot lacks the error-state content named by the criterion.

Observed: one compatible pass-side disagreement and an apparent requirement omission. Unresolved: whether the judge saw the correct screenshot or the reference's requirement interpretation differs. Owner: the Graph execution/evaluation owner. Next check: inspect the judge's bound input attachment and rubric clause. If the attachment hash differs, repair evidence binding; if it matches and the clause is unambiguous, investigate the judge's missed requirement. No prompt or artifact change has been made.

Resolution would require an owner receipt binding any correction to a new artifact/judgment or a documented adjudication of the existing pair. The original pair remains in historical evidence. This example does not authorize contacting the owner or invoking graph-debug.

## When there is no defensible diagnosis

Return the missing evidence and what it prevents. Examples:

- “The labels disagree, but the human label has no artifact version; supply that binding before calibrating this pair.”
- “Two same-ID run revisions conflict and neither supersedes the other; supply the producer's authoritative order.”
- “Known measured spend is USD9, but one run has no billing observation; the cohort cost per accepted outcome cannot yet be calculated.”

Finish with a useful next evidence request, not an invented repair or an unbounded investigation.
