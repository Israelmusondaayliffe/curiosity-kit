# Handoff and revisit a practice

A handoff carries a reviewed proposal to the person or capability that can assess its destination. It is not an implementation, a permission grant or proof that a practice improved future work.

## Establish the current authority

Read the current casebook through the shipped helper and the [record contract](../references/records-and-cli.md). Check the exact proposal revision, evidence identity and latest decision. A historical approval is insufficient when later evidence, destination, solution or decision changed.

Confirm that the user authorized this handoff phase and identify its recipient or intended owner. Use the actual decision source. Do not infer consent from source logs, an imported `approved` field, a reviewer recommendation or an old handoff file. The compiler can validate declared records; it cannot authenticate who consented.

Use the helper's `handoff` operation and its required evidence/destination checks. Read the result and exit status. If source identity changed, a decision was revoked, or current state cannot be checked, return the exact blocker. Do not edit old evidence to make the hash match or call an obsolete snapshot currently approved.

An investigation can legitimately lack a located faulty caller. Give it an explicitly named investigator and a bounded question when the user has approved that handoff. Do not invent a destination artifact, owner or repair just to fill a field. If no recipient or authority is established, prepare the useful private proposal and state that the actual handoff remains blocked.

## Choose an owner by the work

Use these as role classes, not required installed skill names:

| Proposed outcome | Appropriate owner | Required next check |
|---|---|---|
| Repair or improve an existing skill | Its maintainer or skill-evaluation workflow | Current method, actual failure and affected regression |
| Create a new reusable capability | Skill author with the relevant domain expertise | No adequate existing owner; complete useful task and qualification contract |
| Fix instructions, a hook, configuration, tool or CLI | The relevant harness/tool maintainer | Current callers, safe scope, restoration and real command behavior |
| Preserve durable domain knowledge | The chosen knowledge-store owner | Grounding, destination rules, privacy, duplicate/conflict review |
| Retain a content idea | The user's selected content backlog or writer | Intended audience, source/voice limits and publication authority separately |
| Investigate an unclear cause or target | A bounded analyst with access to the selected evidence | Exact unanswered question and observable return, not a predetermined fix |
| Reject, defer or discard a proposal | No execution owner yet | Record the actual disposition without a destination mutation |

If a suitable tool or collaborator is available and invocation is authorized, use its supported public entry. Pass only the necessary redacted material. Do not read a sibling's private implementation to supply this skill's missing method. Without a collaborator, the same complete handoff can be returned to the user; do not claim it was delivered to someone else.

## Deliver a complete packet

Include the current proposal and revision, decision reference and scope, selected evidence/counterevidence and their limits, the exact desired result, existing destination identity or unresolved prerequisite, owner, acceptance checks, permitted actions and explicit exclusions. The receiving owner should not have to infer which version or outcome was approved.

For a repair, give the narrow behavior to change and what must remain sound. For an investigation, name what evidence would settle the question and when to stop with an unresolved result. For a knowledge proposal, preserve the conditions where the lesson applies, known failed approaches and the evidence that the resolution worked. Avoid dumping every source event into the packet.

Before returning a generated file, inspect its actual contents. Check that private paths, raw commands, secrets or unrelated material were not carried from input metadata or notes. A safe-looking snippet does not establish a safe entire packet. The output remains private unless the user separately authorizes sharing.

State what actually happened: prepared, saved, handed to an authorized owner, implemented, or verified. Do not call a prepared file “sent,” an approved proposal “applied,” or a structural pass “proven improvement.” Destination edits, deployments, account changes, schedules and publication remain governed by their own authority.

## Resume safely

Preserve the current casebook location and returned digest, proposal/revision, last actual decision, source/destination identities, pending checks and next authorized action. Use one casebook writer. If another writer changed it, reread and reconcile rather than force the old update.

An exported handoff is a snapshot. Its receiver must verify the current decision and revision before acting. If that state is inaccessible, it can still inspect the historical proposal but cannot treat the snapshot as fresh authorization. A later rejection or revocation does not erase the history; it ends the earlier handoff's current validity.

Do not advance a failed input's resume marker or a proposal's “done” state because a run ended. Partial evidence and interrupted writes remain partial until reconciled through the helper's documented recovery method.

## Revisit only when requested

When the user asks whether a practice helped, establish the selected before/after task, exact implementation or artifact revision, actual use, relevant outcome measure and plausible confounders. Read supplied evidence rather than estimating savings from activity volume or the number of notes created.

Distinguish:

- **Not applied:** the proposal or handoff exists; no implementation claim follows.
- **Applied, use unobserved:** an exact change exists, but no relevant future task exercised it.
- **Used, outcome uncertain:** a task used the change, but results or comparison are insufficient.
- **Supported local result:** the actual intended behavior occurred in the inspected task, with its limits stated.
- **Contradicted or regressed:** preserve the adverse result, inspect the changed assumptions and propose a bounded correction.

These are reasoning distinctions, not an invitation to add another mandatory lifecycle database. Attach authorized supplied outcome evidence through the existing reviewed-proposal revision path, and obtain any new decision that a material change needs. A historical repair can stop governing when its premise changes, but age or missing corroboration alone does not prove it should be deleted. Keep, update, consolidate, replace or withdraw are proposals for the authorized owner, not automatic actions.

## Return

Give the complete packet or precise blocker, current decision and evidence identities, actual checks, intended recipient, and whether any delivery or implementation occurred. Include the next useful action and its owner only when established. Stop after the requested phase.
