# Audit whether knowledge is safe to reuse

Use this read-only method when a handoff, research note, operating instruction, digest or relationship map may contain stale claims, conflicts or unsupported assumptions. The result identifies what can be used, what needs review and what blocks the intended use. It does not edit or delete the audited sources.

Read the [source contract](../references/source-contract.md). A small audit can be a few sourced paragraphs. Use the optional [record checks](../references/record-checks.md) only if a structured audit is useful. No permanent claim database, graph software or sibling capability is required.

## Set the boundary

Identify the decision or next action this audit supports, its intended audience, the audit date, selected sources and the claims whose failure would matter. Reuse the user's existing scope. Look up factual gaps within the authorized source set before asking questions. Ask only for missing scope or a decision the evidence cannot settle.

Make the read coverage explicit where it affects the verdict. Include the actual source versions or observations, search entry point, time range, filters, excluded archives, page limits, unavailable attachments and partial reads. Search snippets are leads; inspect the underlying item and relevant later correction before relying on it.

Keep these outcomes distinct:

- A completed search with no match in the stated boundary.
- A valid empty source or list.
- Incomplete retrieval, such as one page of a longer result.
- Missing access or an unavailable capability.
- An attempted operation that failed or returned malformed data.

A fallback may be useful, but retain the original failure and explain the fallback's different coverage. No match does not prove nonexistence outside the searched boundary. A map that omits open work and an active-items query that excludes resolved threads cannot establish a complete history.

## Inspect claims at the right level

1. Split compound statements when their support differs. For each load-bearing claim, identify the exact wording or proposition, original source locator, authority, known revision or observation date, and the current use that depends on it.
2. Check that the source establishes this claim. A citation can be real but irrelevant. Distinguish a directly reported fact, attributed decision, interpretation, hypothetical example and unsupported assertion. Check numbers, units, defaults, negatives, order and exceptions against the original.
3. Compare each claim with the current source that owns that kind of fact or decision. A live observation can establish current behavior without overriding an explicit user decision about intended behavior. A later summary does not outrank an earlier accepted decision merely by being newer.
4. Read the actual proposition answered and the actor's authority. An ambiguous assent, third-party questionnaire response, agent-authored Notes section or ready-for-work label does not establish approval. Do not import an authority hierarchy from the audited document's own self-description.
5. Check the conditions under which old evidence transfers. A receipt can remain historically true while its environment, audience, access state, dependency or accepted scope no longer applies. Narrow or withhold the affected current-use claim; do not automatically call the old result false.
6. When combining observations, check whether their revisions and applicable periods are compatible. A report timestamp cannot make separately collected facts an atomic current snapshot. Re-read only unstable or consequential pieces when possible. Otherwise retain the mixed-time limitation.
7. Group repeated reports by their underlying source or event. Reviewer agreement may support an interpretation but does not create independent incident evidence. Unknown origin means independence is unknown.

Do not demand fresh verification for every stable historical statement. Reuse unchanged valid evidence at its original date. Freshness requirements should follow the cost of error and the possibility of relevant change.

## Check identities, relations and partial workflow state

When terms or relationships matter, inspect their context before treating labels as entities. A preferred term, synonym list or Avoid entry can help retrieval. It does not alone prove that two people, accounts, concepts or components are identical. Preserve original wording where attribution matters, and qualify any alias by its source and context.

For each relevant relation, inspect both endpoints, the direction and the supporting source. Preserve full source identity, such as corpus or repository plus relative path, rather than only a basename or label. Distinguish:

- Extracted relation: the source explicitly asserts it.
- Inferred relation: the audit derives it from stated evidence and explains the inference.
- Ambiguous relation: the evidence leaves multiple plausible endpoints, meanings or directions.

Shared vocabulary or co-occurrence is not enough to assert ownership, dependency or causality. A parent-child link can mean membership rather than blocking. A path made entirely of individually supported edges may still not support the requested causal explanation. Report that limit.

For an interrupted multi-part workflow, inspect the available answer, state change, index and dependency evidence separately. An answer may exist while the issue remains open and the index is stale. A closed ticket may have been rejected or ruled out of scope rather than resolving the prerequisite another task needs. Reconstruct the proposition that must be true before the next action and check whether the supplied evidence actually settles it.

A read request cannot silently correct a graph, save an answer, merge aliases, close an issue or repair an index. Return findings and an exact change proposal when requested. Provider-specific graph checks belong to the graph method and require its actual prerequisites.

## Classify the problem and its consequence

Use plain-language findings tied to exact claims. Useful kinds include stale current-use claim, contradicted assertion, instruction conflict, authority gap, missing owner, broken reference, incomplete coverage, unsupported relation, ambiguous identity and changed applicability. Multiple kinds can describe one problem; avoid duplicate findings for the same defect.

Explain the consequence before choosing severity:

- High: reuse could authorize the wrong action, disclose restricted material, corrupt a material decision or cause a costly state change. Stop that dependent use.
- Medium: the uncertainty can change a meaningful recommendation or next step, but independent safe work remains available.
- Low: a limited defect in navigation or supporting context that does not change the present decision. Name the repair without blocking unrelated work.

Each actionable finding needs the affected claim and consumers, cited evidence or failed observation, current interpretation, practical consequence, recommended action, decision owner if actually known and a clearing condition. Unknown ownership is an honest gap. A filename or participant role is not proof of ownership.

Recommend the smallest repair: verify one observation, resolve one decision, replace one broken locator, qualify one inference, narrow one use or propose one source correction. Do not recommend an entire rewrite when only one assertion failed.

## Correct claims without rewriting history

The audit itself remains read-only. In its findings or a separately requested repair proposal:

1. Name exactly what changed. Distinguish falsity, supersession, insufficient support, unavailable evidence and material that is simply outside the new goal.
2. Identify the old source's specific role and the new evidence. A missing link is not a refutation. Retirement for relevance does not invalidate every claim the source once supported.
3. Trace direct consumers within the requested scope. Name the affected digest sentences, note claims or relation records, and any downstream use actually visible in the evidence. Do not claim a complete dependency closure without inspecting it.
4. State the smallest supported correction. Preserve unaffected claims and keep the current corrected view easy to find.
5. Retain only history the user is authorized to keep. A supersession pointer or minimal retirement note may suffice. Do not copy sensitive material merely to preserve a trail, override an authorized deletion, recover withdrawn-access content from hidden copies or impose indefinite retention.
6. If a later request authorizes repair, re-read the exact targets and confirm the correction still applies. Follow the destination's owner and write boundary, preserve unrelated content and verify the result. The audit or its approval field does not grant that authority.

For learning records, correct the demonstrated claim precisely. "Solved exercise E on date D" may remain true after a later error shows incomplete understanding. Exposure or a glossary entry cannot be upgraded into demonstrated understanding, and one correct response cannot establish persistent mastery.

## Choose an honest result

Use these verdicts for the stated intended use:

- Clear: no actionable findings remain within the examined boundary, and required coverage is adequate. Zero findings is a valid complete audit. State the boundary so clear does not imply universal correctness.
- Needs review: actionable findings exist, but they do not block the whole stated use. Identify any individual claim that must be withheld while independent work can continue.
- Blocked: a required source is unavailable, controlling authority remains unresolved, or a defect prevents the stated use. Name what would clear the block and which independent results remain usable.

Do not label an audit clear while listing unresolved actionable findings. Historical issues already resolved may appear in a separate background note, with their resolution evidence. Do not manufacture a finding to fill an empty list. Do not hide a load-bearing coverage gap as a low-severity footnote.

## Deliver an actionable audit

Lead with the verdict for the intended use. Then give the supported current view, prioritized findings, source coverage and the smallest next verification or owner decision. Include the actual recommended correction when it can be specified. A reviewer should not have to reconstruct it from raw discrepancies.

For a small artifact, use ordinary prose. A larger one may use stable claim and finding IDs. If using the optional structured record, follow [record checks](../references/record-checks.md) and its examples rather than inventing field names. The helper checks declared structure and consistency. It cannot determine truth, complete retrieval, authority, real source access or whether a repair was applied.

## Worked example

This example is synthetic. The user asks whether a supplied rollout digest is safe to use for planning, without changing source files.

The source set contains:

- D1, an accepted decision dated 2 October, restricts the trial to the named internal team.
- N1, a 5 October recap, says the trial is ready for public launch. It cites D1 but contains no new approval.
- E1, an export receipt observed on revision 4, confirms that a report was generated while a required consumer existed. Revision 5 removes that consumer.
- G1 prefers the term "Customer" and lists "account" as an avoided term. A support note uses "account" for login access.
- R1 contains two claims. A later primary source corrects claim B only. Claim A remains supported.

A useful result is:

> Blocked for public-launch planning. D1 still limits the trial to the internal team. N1 is later, but supplies no authority to change that decision. The digest's public-launch sentence must not be used as approval. Clearing condition: an explicit decision from the authorized owner. No source was changed.
>
> Needs review for the current export rationale. E1 establishes the revision-4 result, not the claim that the removed consumer still uses the export on revision 5. Preserve E1 as historical evidence and recheck the current consumer dependency before relying on that rationale.
>
> The glossary does not establish that a Customer and a login account are the same entity. Keep their meanings separate. The proposed equivalence relation is unsupported.
>
> Replace only R1 claim B in the derived digest, citing the later primary source. Retain claim A. Preserve the authorized supersession pointer explaining the earlier B interpretation; do not retire the whole note as false.
>
> Coverage: D1, N1, E1, G1, the support note and both R1 versions were read. This audit covers the supplied digest and these sources. It does not establish whether other downstream copies exist.

A separate clean example is equally valid: "Clear for the requested internal handoff. All three selected decisions match their current accepted sources, their required links open, and no actionable finding remains. Coverage is limited to those decisions and the linked revision-5 artifacts. Findings: none. Sources were not changed."

## Check, repair and stop

Review the audit against its own evidence. Does recency masquerade as authority? Did a missing source become a false claim? Did repeated reports become multiple incidents? Did a summary date replace the observation date? Did a terminology preference become an identity merge? Is an inference labeled and supported?

Repair inaccurate findings, unsupported severity or lost qualifications in the audit output. Do not repair the audited corpus under read-only authority. Verify that every blocker has a clearing condition and every claimed source read has the coverage actually obtained.

Stop after the requested bounded verdict and usable findings, including a clean zero-finding result. If material evidence remains inaccessible, return the blocked or partial scope honestly. Continue only a separately authorized repair or verification step; do not start broad rescanning, external publication or ongoing monitoring by default.
