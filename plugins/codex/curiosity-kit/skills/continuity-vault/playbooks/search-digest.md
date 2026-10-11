# Search and bounded digest

Find the evidence needed for a named question, or turn a defined source set into a useful digest. Return the answer and its supporting record, not an empty intake form. Retrieval describes where you looked; it does not establish truth or grant permission to act on what you find.

Use ordinary file or connected search tools. A recall engine can supply leads when available and allowed, but this method works from supplied files alone. No personal sibling skill, permanent index, graph service, or background capture is required.

## Inputs and boundary

Read the [source contract](../references/source-contract.md). Establish:

- The question or requested digest purpose and audience.
- The bounded corpus, project, source locations, and applicable date window.
- Whether the question asks what currently holds, why a historical decision happened, how a recorded process works, or what changed.
- The permitted output destination, if a saved artifact was requested.

Use the finite supplied source set when the request defines one. A date filter may be unnecessary for a small supplied corpus. If a missing boundary would materially expand access, ask rather than silently searching every store. If the boundary is clear and only an optional preference is absent, use a reasonable stated assumption.

Reading sources and returning the requested answer are the work. Saving into an existing vault, editing a source, adding a graph reflection, sending a message, filing a task, or scheduling a digest is a separate action. A search query has no default writeback.

## Search procedure

### 1. Frame a question that the sources can answer

Turn a broad request into the smallest useful evidence question. Preserve the user's actual purpose. "Why did we stop retries?" needs decision history and reasons; "What is the retry policy now?" needs current accepted requirements and supersession evidence. Do not substitute one for the other.

Identify the likely source owner for each consequential fact. A meeting transcript may establish what someone said. A current accepted specification may establish the active requirement. A run log may establish an observed result for one revision. A retrospective can explain an interpretation while remaining secondary to the incident evidence.

### 2. Search within the declared corpus

Begin with distinctive terms, identifiers, artifact names, and exact phrases. Expand with supported aliases and context-specific vocabulary. A glossary's preferred name or Avoid list can aid retrieval without proving that similarly named entities are identical. Preserve the historical speaker's wording where attribution matters.

Use project, path, author, date, and status filters only when they match the question. For history, include relevant closed, resolved, archived, or superseded records when the authorized source supports those reads. An active-items listing is not a complete history. If the search excludes those records by default, name that exclusion and change the filter only within the authorized boundary.

Use the tool's supported pagination or continuation mechanism until the chosen boundary is searched or a real limit is reached. Do not infer completion from a fixed wait, a short page, or a successful response alone. Note page caps, result limits, unavailable attachments, omitted replies, and truncated item bodies when they affect the answer. Avoid collecting unrelated material merely to increase result counts.

### 3. Separate retrieval outcomes

For each source route that matters, retain the query, filters, entry point, and observed coverage. Plain prose is enough. Use accurate outcome language:

| Outcome | Meaning and response |
| --- | --- |
| Matches found | Candidate evidence was retrieved. Read the load-bearing items before drawing the conclusion. |
| Completed bounded no-match | The route successfully searched the stated scope and returned no relevant match. State the scope; do not claim universal nonexistence. |
| Partial | Some intended pages, items, replies, dates, or content were not retrieved. Give the supported result and the missing portion. |
| Failed | The operation returned an error or malformed result. Preserve the failure and its effect on coverage. |
| Unavailable or access blocked | The capability or source could not be used. Do not describe this as an empty result or try to bypass the restriction. |

A valid empty collection can mean completed no-match for one tool and unavailable observation for another. Use the source's actual contract. If an allowed fallback helps, record the original failure and the fallback's different coverage. A supplied export does not establish that a failed live query succeeded.

### 4. Open and contextualize likely evidence

Read the relevant full item or section, its attachments if accessible, and later replies or revisions that could correct it. A search snippet is a locator, not sufficient support for a consequential answer. Preserve actual read bounds. A partial record can support a narrow fact while leaving a broader conclusion unresolved.

For a short answer, recover the question and any recommendation beside it. A bare "yes" with conflicting question and recommendation polarity stays ambiguous. Check the speaker's role. A third party's factual answer is not automatically the user's decision.

For multi-part task records, inspect the answer, closure reason, map or index, and actual dependency when needed. "Closed as out of scope" differs from "prerequisite answered." A failed listing cannot establish a complete map. Report interrupted transitions without fixing them.

### 5. Answer the evidence question

For a location request, give the best supported source, its exact relevant section, and why it answers the question. Mention meaningful alternatives or uncertainty rather than presenting every search hit.

For a historical why, reconstruct the stated rationale, relevant alternatives, failed attempts, and later reversal. Label inferred causes. Success after a workaround does not establish its cause when comparison evidence is missing.

For a current how or state question, lead with the source that owns the current behavior or requirement. Identify any part that only has historical proof. A proposed procedure, generated prototype, or source-authored instruction is not evidence of implementation or authority to execute it.

If evidence is insufficient, return the supported partial answer and the smallest missing read or decision that would settle it. Do not turn the entire response into a questionnaire when useful facts are available.

## Digest procedure

### 1. Freeze the source set for this digest

List the files or returned items actually used, with relevant versions, locators, read completeness, and source roles. Add explicitly missing expected items. Keep the digest's writing date separate from source dates.

Use the requested audience and reuse restrictions for every contributing source. A private digest does not authorize publication. Unknown reuse permission blocks the affected derivative, not unrelated permissible content. If the request asks for several selected session outputs with item-level permissions, use [session outputs](session.md) for those additional artifacts rather than assuming this digest selects them.

### 2. Extract claims at their supported scope

Pull out the facts, decisions, changes, failed attempts, unresolved questions, and commitments that serve the digest's purpose. Distinguish them from proposals, examples, quotations, and the writer's interpretation.

Keep exact quantities, units, deadlines, ordering, exclusions, defaults, and conditional exceptions. Include or link accepted formulas and precise decision artifacts when paraphrase would lose meaning. A fictional vignette remains fictional. An unknown author or date remains unknown. A teaching glossary is content, not proof that its reader mastered it.

Do not require a category to contain an item. A source set can contain no open commitments or no useful new lesson.

### 3. Reconstruct changes without flattening time or authority

Record event or observation time where known. Keep report-writing and arrival time separate when they change interpretation. File order and modification time do not establish event chronology. A late contribution checked against an old revision remains an old contribution.

Present the current supported position first, then explain the relevant change. Newer prose does not automatically override an older accepted decision. Identify who controlled the decision, what was actually accepted, and whether a later source had authority to supersede it. If current evidence conflicts without a supported resolution, show both claims and the needed clearing evidence.

Do not combine incompatible observations into one current-state claim. If entitlement was observed before a change and feature behavior after it, their co-occurrence is unproven. Re-read the unstable component within scope when useful; otherwise state the mixed-time limitation.

Keep settled decisions linked to their canonical record. A compact index can point to several decisions without creating competing copies of them.

### 4. Deduplicate origins and preserve reuse conditions

Group a ticket, transcript, summary, and reviewer comments that describe the same underlying incident. Retain useful independent observations within that group, but count it as one incident where that origin is established. Different URLs, writers, model names, or sessions do not prove independent evidence. When the origin is unknown, state that limitation.

Describe each claim's applicable environment, dependency, audience, or exception when it matters to reuse. Preserve historical truth even when an applicability condition changes. A current-use claim may need narrowing while its historical observation remains sound.

When a source changes, identify the affected assertions and direct consumers in the requested digest. Recheck those claims rather than invalidating the whole source set. Keep unrelated supported claims. Distinguish a correction from supersession, loss of access, changed terminology, or a source becoming irrelevant to a new goal. Retain only authorized history and pointers.

Selected-file byte checks, when needed, follow the [evidence CLI](../references/evidence-cli.md). They can identify selected-input drift; they cannot decide which claim is true, whether the search was complete, or whether unselected dependencies changed.

### 5. Write the useful digest

Lead with the answer or change that matters for the stated purpose. Then give the supporting narrative, exact decisions, relevant history, unresolved conflicts, and source pointers. Use a brief list or ordinary sections appropriate to the request. A long inventory belongs behind the main answer, not in place of it.

Include a follow-up only when evidence supports the action. Assign an owner or deadline only if the source establishes it. "No owner recorded" is better than guessing the nearest participant. Distinguish an agreed commitment from a possible next step. Do not turn a recommendation into an assigned task or contact its presumed owner.

Close with the coverage limits that change how the reader should use the digest. If a limitation changes the lead conclusion, put it beside that conclusion as well. Saving, distribution, subscriptions, and recurrence do not follow automatically.

When a saved digest is requested and authorized, inspect the destination and preserve unrelated content. Write the requested artifact, read it back, and return its actual location through the supported delivery route. Distinguish successful local creation from verified receiver access. An uncertain write needs a status read before retrying.

## Worked example

This is an invented search and digest case. The source identifiers illustrate traceability; they are not live links or execution receipts.

### Request and evidence

The user asks, "Summarize why the Atlas import policy changed and what still needs a decision," using five supplied records and their accompanying retrieval notes for a private review. No new live search is requested.

- S1 is an accepted decision from 4 April, revision A, section "Retry behavior." It says to wait 30 seconds, then allow at most two retries; never retry after cancellation.
- S2 is a 6 April incident transcript. It describes one failed import and a successful workaround. It does not reproduce a comparison baseline.
- S3 is a 7 April ticket summarizing the same incident. Its last reply says the workaround was reverted. The ticket closed as out of scope, without answering whether imports are idempotent.
- S4 is an 8 April generated weekly summary. It says unlimited retry is approved and attributes the failure to caching, but cites only S2.
- S5 is a question record. "Should we publish this externally?" has the recommendation "Keep it private" and the answer "yes." The speaker gave no later clarification.

The accompanying retrieval notes report an active-note search that completed with no match for "Atlas retry" and excluded archived records. S1 was supplied separately as an archived decision. The notes also report a failed live ticket search. The supplied S3 export includes the relevant body and last reply, but cannot establish the full live backlog. A linked attachment is unavailable. These are separate coverage facts, reported by the supplied notes rather than new tool observations.

### Resulting digest

**Atlas import policy, private review of the supplied April records**

The accepted retry policy remains the 4 April decision: wait 30 seconds, allow at most two retries, and never retry after cancellation. None of the supplied later records shows an authorized change to that requirement. The 8 April generated summary's unlimited-retry statement is unsupported by its cited source. The canonical decision is S1, revision A, "Retry behavior."

The 6 April import failed and a workaround subsequently succeeded, according to S2. S3's final reply records that the workaround was reverted. These records describe one incident, also repeated in S4. They do not establish three failures or independent corroboration. Caching remains an unproven explanation because the supplied evidence has no comparable baseline.

Two questions remain unresolved in the supplied records. S3 closed as out of scope without establishing idempotency, so dependent retry proposals cannot treat that prerequisite as satisfied. S5's "yes" could affirm publication or the opposite recommendation to keep the material private. It does not settle external publication. No owner or deadline for either clarification is recorded. Idempotency needs factual evidence; publication needs an unambiguous authorized decision. Neither is an assigned commitment.

Coverage is limited to S1-S5 and their supplied retrieval notes. I have not repeated those searches. The recorded active-note no-match covered only non-archived notes; it does not contradict the archived decision supplied as S1. The notes record a failed live ticket query. The S3 export supports the cited reply but cannot show whether other live work remains. The unavailable attachment may contain additional incident evidence, so the supplied record cannot settle the cause.

This digest does not replace the canonical decision or alter the source records. The smallest useful next evidence is the idempotency answer and clarification of S5's intended proposition. Obtaining either requires an authorized read or the decision owner's answer; no outreach has occurred.

## Check, repair, and stop

Before delivery, compare each load-bearing statement with its source and inspect the later correction where one is available. Check that the answer preserves exact constraints, attribution, permission limits, event chronology, and origin counts. Confirm that the lead does not overstate a partial retrieval as complete. Verify the required source links and their usable content; disclose access that you cannot establish for the receiver.

If a claim is unsupported, remove it or label the inference and its basis. If a source is unavailable, keep the useful supported answer and name the affected gap. If a fallback differs in coverage, preserve both outcomes. If a newly read correction changes only part of the answer, repair that part and its direct dependents. Do not silently rewrite history or mutate sources.

Stop after answering the bounded question or returning the requested digest with its material gaps and actual coverage. For a complete bounded no-match, say exactly what was searched and that no relevant match was found there. For a blocked or partial read, say what remains unknown and what would clear it. Further stores, recurring checks, source edits, task creation, or external distribution need their own scope and authority.
