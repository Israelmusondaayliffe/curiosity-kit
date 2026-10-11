# Brief and clarify

Use this method to turn accepted direction into an execution-ready brief, or to resolve the local questions that prevent one. A brief-only request ends with the complete brief. Do not reopen settled choices just to fill an interview script.

## Inspect before asking

Read the supplied conversation, current source documents, accepted decisions and relevant artifacts. Find the closest authority for each consequential fact. A public page does not override an authorized internal decision about the user's own project; an old approval does not establish the current artifact's approval.

State the intended result from its user's point of view. Distinguish the artifact to produce from the eventual benefit: a revised intake procedure can be delivered today, while reduced turnaround time needs later observation. Identify who uses it, its destination, exact requested format and scope of allowed action. Record known dates and versions; mark missing facts as unknown rather than inventing them.

Classify unresolved items:

- A discoverable fact: inspect the permitted source and retain its actual scope.
- An answerable decision: name the choice, owner and tradeoff.
- A question waiting on another answer: settle the prerequisite first.
- Unclear uncertainty: find one observation that would make it an answerable question.
- A deliberately deferred item: record owner, trigger and which work it blocks.
- Out-of-scope work: exclude it explicitly, without relabeling a required outcome as optional.

A consequential unresolved choice can block dependent execution without blocking independent drafting. If the user requests a draft with unknowns, provide it and label its readiness accurately. Do not let a polished draft hide an unapproved choice.

## Bounded clarification

Use local clarification only to make the requested outcome executable. Inspect facts first. Ask the highest-impact unresolved choice whose prerequisites are settled, offer a supported recommendation and its main tradeoff, then carry the answer into downstream decisions. One dependent question at a time is useful; independent factual questions can be grouped when that saves the user effort.

Define important domain terms before relying on them. Preserve precise terms already used by the project. Push back on an answer that conflicts with the user's goal, sources, constraints or earlier decision, explaining the consequence rather than arguing for a favorite method.

Keep a compact decision record, not an interview transcript. After several consequential answers or a noticeable change of direction, summarize what changed and what remains. Check the likely failure path, the person bearing its cost and any edge case that alters the proposed scope. Honor stop, summarize and skip. A skipped material question remains unresolved or explicitly deferred; it does not silently become approved. If the user delegates a choice, make a reversible in-scope choice, label assumptions and preserve remaining external-action boundaries.

Stop clarifying when material branches are resolved, verifiably discoverable before they are needed, excluded, or explicitly deferred with an owner and trigger. For an open general strategic decision, explain what still needs deciding. An available specialist may help if appropriate, but no sibling skill is required for this local process.

## Write the whole brief

Synthesize the known context into a useful document another person or agent can execute. Use the user's template when supplied. Otherwise the canonical brief in [work records](../assets/work-records.md) supplies these fields:

- Outcome: what changes for whom, at what scope, and what artifact or action is actually requested.
- Audience or user: the reader, operator, approver or recipient and their relevant context.
- Success evidence: observable checks through the real use path, with independent expected results and what they cannot establish.
- Constraints: sources, dates, format, budget, time, rights, available tools, allowed locations and actions.
- Decisions: accepted values, who accepted them and their source/version; proposed alternatives remain labeled separately.
- Requirements: each required behavior or piece of content, including exact quantities and format constraints.
- Risks and unknowns: assumptions, evidence gaps, failure consequences and how they will be tested or managed.
- Blockers: what prevents which work, owner and the evidence/decision that clears it; write None only if none remain.
- Out of scope: exclusions and actions the current assignment does not authorize.
- Next action: the smallest useful step, owner and relevant dependency.

Use requirement IDs when several slices or assets need reliable coverage. A brief for one memo does not need a large registry. Keep durable requirements separate from incidental implementation paths; include a precise snippet or interface only when it captures a settled decision better than prose. Do not generate fictional user stories or stretch a small brief into a generic specification.

Cite consequential source-dependent claims with actual accessible locations and limits. Separate observation, a source's explanation, inference and recommendation. If a correction changes one clause, preserve the unaffected terms. An assumption is a working choice, not a substitute for required evidence.

## Several coordinated assets

Name the complete set and its shared message, facts, quantities and deadline. Record each asset's ID, audience, format, owner, version and intended destination. Add governing decision IDs, risks and recovery owners, review gates and evidence, dependency-bearing slices and honest delivery state. The [plan example](../assets/plan-example.json) shows a single machine-checkable representation when cross-references matter.

Do not maintain a second contradictory asset-dependency table. Map asset work into the slice graph. A reviewer needs a verified draft, not an externally published asset. Distinguish content approval, legal/brand approval when required, and permission to send or publish. Record exactly which asset/version and action each approval covers. Keep old approvals as history, and reopen affected approval after a material edit.

The skill coordinates production and can complete general knowledge artifacts itself. Specialist media generation, application work or a required native format needs the actual appropriate tool and expertise. Do not claim a prompt, plan or placeholder is the requested final media. Optional help must not conceal a missing essential capability.

## Check readiness and hand off

Read the finished brief against the actual request, source passages and accepted decisions. Check every requirement, exact format, quantities, denominators, scope and named blocker. Confirm that proposed values never appear as settled in the next action. Check consistency across the entire asset set.

For a canonical local Markdown brief, run the bundled `check_outcome.py brief FILE` using the [checker contract](../references/checker.md). A structural pass establishes neither valid sources nor approval. For another required format, use its appropriate checks and disclose what was not machine-checked; do not copy a shadow Markdown artifact just to pass the helper.

Return the complete brief, its status and any dependency that prevents execution. A user-approved end-to-end scope can proceed into [slicing](slice-and-coordinate.md) without an unnecessary new interview. A request to write a brief alone ends here.
