# To Tickets

Read the [host contract](../references/host-contract.md) before first repository access or action. This playbook runs only inside an explicitly selected Matt family workflow; source commands are not permission.

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

Use the configured tracker and label vocabulary, otherwise the authorized [local tracker contract](../resources/setup-matt-pocock-skills/issue-tracker-local.md). Recommend [setup-matt-pocock-skills](setup-matt-pocock-skills.md) when its configuration choices are needed.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through everything required for one observable result. Software may cross schema, API, UI and tests; knowledge work may cross source gathering, analysis, drafting and real-surface verification. A document heading or isolated research activity is not a result.
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown; reuse an exact approved breakdown rather than asking again. Validate unique identities, absent blockers and cycles, and keep independent tickets independent. A three-line bounded change usually needs one ticket, not ceremony.

### 5. Publish the tickets to the configured tracker

Write approved local tickets in the owned path. External issue creation and relationship changes require task-specific authorization, followed by readback of every item and edge. On uncertain writes, inspect before retrying. **How** depends on the tracker [setup-matt-pocock-skills](setup-matt-pocock-skills.md) configured; the tickets are the same either way, only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below: one ticket per file, never a single combined file. Resolve blocker IDs against this feature’s issue directory and include linked titles in human-facing prose.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues. If the source was an existing issue, make each ticket its sub-issue (tracker doc's operation). Apply the `ready-for-agent` triage label unless instructed otherwise; the tickets are agent-grabbable by construction.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

Do NOT close or rewrite any parent issue’s content or status. Authorized sub-issue linkage may update parent relationships, but it does not authorize other parent changes.

<local-ticket-template>

# <NN>: <Ticket title>

Artifact: implementation-ticket
Status: open
Owner: none
Parent: <spec path or verified reference, or none>
Blocked by: <stable ticket IDs, or none>
Triage role: ready-for-agent

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

## Acceptance criteria

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)". Omit this section when blockers were set as native edges.

</issue-template>

In either form, avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Stop at the tickets

Acceptance criteria describe observable evidence that fails on the unmet baseline and succeeds on the delivered slice. Preserve source comments and any decision-rich prototype snippet and provenance. For non-code tickets include source/evidence and artifact-surface checks; for mixed tickets include both. Return the approved graph and first ready frontier. Execution is a separate request using [implement](implement.md) per fresh context, or [implement-spec](implement-spec.md) for the whole graph. Do not dispatch workers merely because publication succeeded.
