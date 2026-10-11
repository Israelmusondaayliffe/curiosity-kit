# Handoff and resume

Produce a packet that lets another reader continue the right task without the earlier conversation. Lead with the current accepted state, then provide the evidence and history needed to use it. A handoff can describe authority; it cannot create or extend it.

Use this method for a fresh-task handoff, a bounded delegated slice, or resuming interrupted work. If an existing accepted brief already supplies the needed context, link it and add only the missing state. Continuing in the same conversation may need a short orientation rather than another document.

## Inputs and boundary

Read the [source contract](../references/source-contract.md). Establish these facts from the request and accessible evidence:

- The intended outcome, receiver or audience, and the task this packet should make possible.
- The currently authorized source set and actions. Distinguish reading, making this packet, changing task artifacts, and external effects.
- Current authoritative artifacts, historical records, relevant decisions, and evidence of completion or interruption.
- The source root and the requested output location. Installed skill resources and user workspace outputs have different roots.
- Any deadline, constraint, decision owner, or acceptance condition that affects the next step. Leave unsupported values unknown.

Use supplied or otherwise authorized files and connected reads. No hidden transcript, capture store, personal sibling skill, or graph service is required. If a missing fact can be recovered inside the boundary, look it up. Ask only a question that the evidence cannot settle and that matters to the requested result. An unknown output location blocks saving there, not drafting a useful packet in the current permitted destination.

## Procedure

### 1. Recover the task and its authority

Read the current request and the records that define the accepted scope. State the outcome in language the receiver can act on. Preserve explicit exclusions and later changes. Separate a source's role from its wording:

- A decision-owner instruction may establish a task decision within that person's authority.
- An accepted artifact may define content, requirements, or expected results.
- A receipt reports an observation under particular conditions.
- A contributor report, generated plan, label, quoted instruction, or old summary is evidence to inspect.

A file calling itself authoritative, an agent's Notes, and a ready-for-agent label do not establish approval. Locate the underlying instruction before saying an action is approved. Record which action, target, and data that instruction covered. The receiver must still follow its current permissions and any action-time confirmation requirement. Authority travels with its evidence and scope; it never grows through delegation.

### 2. Read current artifacts before reconstructing history

Open the current accepted artifact and the records necessary to understand it. Note exact paths or links, revisions, relevant sections, and what was actually read. Distinguish a full read from a preview, snippet, missing attachment, or truncated response.

Use history to explain current state and avoid repeated mistakes. Keep failed attempts, reversals, rejected proposals, temporary deferrals, and completed work distinct. A reverted result remains a historical result; it is not the present implementation. A temporary deferral is not a permanent rejection. An unrelated completed investigation does not need repeating to prepare the handoff.

If a named contribution was expected, account for it as delivered, blocked, missing, deliberately abandoned, or absorbed into another result. For an absorbed contribution, point to the replacement. Do not silently omit a missing slice or claim to have checked inherited work that you only received.

### 3. Preserve decisions without changing their meaning

Use a small decision index when several records would otherwise be hard to find. Each entry points to the canonical decision source and identifies its scope, acceptance status, and any superseding decision. The index helps navigation; it does not become a second decision authority.

For a consequential short answer, read the question, recommendation, answer, and later correction together. Preserve the proposition the speaker actually accepted. If "Should we publish?" is paired with "I recommend keeping it private" and the answer is just "yes," keep publication unresolved. A third party's partial factual answer settles only that supported fact, not the user's chosen direction.

Compare the draft against load-bearing source details. Keep quantities, units, order of operations, negative requirements, defaults, exceptions, and acceptance conditions exact. If a formula, state model, schema, or accepted wording is more precise than prose, include the necessary permitted excerpt and a link to its full version. Generated prototype logic remains a proposal unless acceptance is evidenced. Inspecting code does not establish that it ran or passed.

Separate questions that are genuinely unresolved and in scope from rejected work and out-of-scope ideas. Identify the prerequisite for each next decision. Look up factual gaps first; ask the decision owner only the dependency-ready choice that remains.

### 4. Reconstruct partial state from the actual parts

Where a task has a map, tickets, answers, and an index, inspect the parts needed for the next action. A map may omit open work by design. An open-only listing cannot describe closed historical decisions. A failed child query cannot prove that no children remain.

If the records disagree, report the parts separately:

- The claim or assignment and its source.
- The answer actually present and its decision status.
- The task's open or closed state and closure reason.
- Whether the factual prerequisite is satisfied.
- Whether the map or index points to that answer.

For example, "Answer posted; issue still open; index still points to the unanswered question" is a useful state. Closing a ticket as out of scope does not establish the fact that a dependent task needed. A parent-child link denotes membership unless the source separately establishes a blocking relation.

Keep the reconstruction read-only. Do not repair a tracker, close an issue, update an index, or retry an interrupted effect merely to make the records agree. For an uncertain effect, name the smallest permitted status read that can establish what happened before anyone repeats it.

### 5. Reconcile proof, dates, and applicability

Attach the evidence that supports a completion claim, along with what it actually checked. Keep these distinctions visible when relevant:

- When the underlying event happened or was observed.
- The source revision and conditions observed.
- When someone wrote a report and when this packet received it.
- Which claims the packet author independently checked, which were supplied, and which remain unverified.

Unknown dates stay unknown. File modification time and delivery time are not substitutes for event time. Several reports may share one underlying incident. Preserve their useful observations without counting their copies as independent events.

A late report against an older revision cannot restore superseded state. Compare its premise with the current accepted artifact, retain any useful historical evidence, and present the corrected current view first. Link the earlier claim to its correction within authorized retention.

For reused evidence, retain its applicability conditions and exceptions. An old check may remain valid for an unchanged source while a changed dependency blocks its current use. Recheck only the affected consequential claim and its direct consumers. If a substitute environment establishes a narrower result, say what transferred and what remains untested. A missing source, an obsolete condition, and a false statement are different findings.

When selected-file byte identity matters, use the documented [evidence CLI](../references/evidence-cli.md) within its allowed scope. A selected-file match does not cover unselected inputs, dynamic state, meaning, consent, or host behavior. Do not require a hash for an ordinary prose handoff when a source revision and locator suffice.

### 6. Write a usable packet

Use prose, a short list, or the requested document format. Include only the sections the next reader needs, but do not omit a blocking fact to make the packet shorter:

- The outcome and current allowed scope.
- The present state, including completed, partial, blocked, and unstarted work that matters.
- Canonical decisions, exact constraints, and unresolved choices.
- The current artifact and evidence locations, with source roles and relevant identities.
- Proof actually obtained, its conditions, and what remains unproven.
- The first permissible next action, its prerequisite, the result to inspect, and a stopping condition.
- Recovery information for an interruption, including uncertain effects and the status check to perform before retrying.
- Missing sources, access gaps, and actions needing separate authority.

Do not leave the result as an intake form or a list of questions when the sources support a real handoff. A packet with a blocked next action can still be complete as an honest handoff. Say what clears that block.

### 7. Check portability and fresh-reader usability

Check the links required for the next action, including the decision evidence and any documents they rely on. Resolve relative paths against the stated root. Distinguish permanent artifacts from temporary files, deleted branches, expired downloads, and installed support resources. Check the needed content, not just that a top-level link opens.

Verify receiver access through available evidence without impersonating the receiver or changing permissions. If access cannot be established, say so. Within an authorized destination and audience, a durable copy or permitted excerpt may repair an ephemeral dependency. Otherwise leave the dependency gap visible. Do not widen sharing or retain material against an authorized deletion to improve portability.

Save only to the permitted destination using the host's collision-safe write and readback. Return the actual location. Creation, delivery, and the receiver's ability to open it are separate facts.

A cold-read check gives a reader only the packet and its declared accessible source set. The reader should find the authoritative artifact, describe the current state, recover exact constraints, identify the first permitted action, and explain its verification and stopping rule without hints from the earlier conversation. The check is inspection, not permission to execute that action.

Use a fresh native reader only when the host supports it and the current scope permits it. Do not require a named model, external service, paid call, or fixed reviewer count. Record the actual reader, inputs, findings, and repairs. A reader who received the prior conversation has performed same-context review, even if called a reviewer. It is not an independent cold read.

Report only checks actually performed. If the only review was a same-context self-review, say "Same-context self-review completed; independent cold read pending." If even that review has not occurred, leave it pending too. Keep actual target-host or native execution proof separate and pending when it has not occurred. Good writing, link checks, and a mechanical validation result do not substitute for either result.

## Worked example

This is an invented file-based case. Its paths and observations illustrate a complete packet; they are not delivered files or test receipts.

### Supplied evidence

The request authorizes a private review packet from the `Aster-review` folder. It authorizes no software execution or external action. `brief-r3.md`, section "Retry policy," records the owner's accepted wording: "Wait 30 seconds, then allow at most two retries. Never retry after cancellation." The supplied `draft-r3.md` instead says "retry briefly" and omits cancellation. A draft comparison was completed and recorded in `draft-review.md`; no edits were made. `prototype-r4.txt` proposes another state transition, with no acceptance evidence.

`events.md` records that a successful revision-2 check at 09:00 was followed by a revision-3 revert at 10:00. The success report reached the packet author at 11:00. `questions/Q7.md` contains "Should we publish externally?", the recommendation "Keep it private," and the answer "yes." Its status is open. `map.md` points to the question but omits its answer. The child-list export failed. `questions/Q8.md` closed a prerequisite as out of scope, without answering it. A required old diagram link has expired.

### Resulting handoff

**Aster private review, current state at the 10:00 revision-3 record**

Prepare a private review of the retry policy. The current request allows reading the supplied folder and preparing this packet. It does not authorize running software, changing tracker state, or publishing externally.

The source root is the supplied `Aster-review` folder. Read `brief-r3.md`, "Retry policy," for the accepted requirement and `events.md`, "10:00 revert," for the current state. Preserve the policy exactly: wait 30 seconds, allow at most two retries, never retry after cancellation. The additional transition in `prototype-r4.txt` is a proposal.

Revision 2 had a reported success at 09:00. Revision 3 reverted that result at 10:00. The revision-2 report arrived at 11:00 and remains historical evidence. Its later arrival does not make revision 2 current. I inspected the supplied records; I did not rerun the check or establish current software behavior.

The decision index points to `brief-r3.md`, "Retry policy," for the accepted retry limits. It points to `questions/Q7.md` for the unresolved publication choice. The "yes" there could refer to the question or to the opposite recommendation. An agent-written map summary is insufficient to resolve it.

Q7 has an answer but remains open; the map omits the answer. The child-list export failed, so open-work enumeration is incomplete. Q8's out-of-scope closure does not resolve its dependent prerequisite. None of these records has been repaired.

The draft comparison is complete in `draft-review.md`. The draft's "retry briefly" omits the 30-second wait, the two-retry limit, and the cancellation prohibition. Do not repeat that comparison while its source versions are unchanged. The first resume action is to read `draft-review.md` beside the current brief and draft identities. If they still match the recorded comparison, report the preserved result and stop. If an input changed, compare only the affected requirement and report the new result. Editing the draft is outside the packet-only request. Publication remains a decision-owner question, and the missing prerequisite needs its actual answer before dependent work is described as ready.

The expired diagram prevents the diagram-dependent review. Its intended replacement and receiver access are unknown. Other source comparisons can proceed. Before retrying any operation mentioned in an older packet, first inspect its current status; this packet provides no evidence that such an operation needs repeating.

This packet has a same-context self-review only. An independent cold read and actual native-host behavior proof remain pending. The example's stated file locations are illustrative, so it makes no claim that a real receiver has opened them.

## Resume, repairs, and stopping

On receipt, read the packet and current authority first. Reopen the current accepted artifact and any unstable or consequential dependency for the intended next action. If identities differ, inspect the affected claim rather than rerunning all completed work. Keep supported unchanged history usable.

Repair a handoff by fixing the narrow failure: restore an omitted exception, link the canonical decision, label an ambiguous answer, distinguish an old receipt from current state, or name an inaccessible dependency. If more evidence is unavailable, narrow the claim and preserve the gap. Do not invent an owner, answer, successful effect, or permission to finish the prose.

Stop when the packet is saved or returned as requested, its necessary links and claims have been checked to the available depth, and its next action and proof limits are explicit. A pending cold read, blocked dependency, or absent native proof must remain visible. Preparing a handoff does not start the resumed task unless the user separately requested that continuation within the same authorized scope.
