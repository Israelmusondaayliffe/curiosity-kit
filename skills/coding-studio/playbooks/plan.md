# Plan a change

Use this method to turn a request, accepted brief, or partly developed plan into work an implementer can complete without inventing product decisions. An explicit planning request ends with a usable plan. Planning does not itself authorize implementation, tracker publication, or delivery.

Read [the host contract](../references/host-contract.md) for environment, authority, and evidence boundaries. Use this method directly for a small change. Load additional methods only for decisions the task actually needs.

## Bring the right inputs

Start with the requested outcome, existing decisions, target project, and requested deliverable. Read a supplied plan in full before revising it. Preserve its identifiers, owner-written sections, and unaffected decisions. A new heading convention is not a reason to rewrite it.

Check the project's applicable instructions and relevant source. Find the user or system entry point, the path through the affected components, current tests, and any design record governing the change. Keep source identity with navigation hints when code may move. A path helps someone find current code; it is not a permanent requirement.

Choose the smallest useful output:

- A clear one-pass change can use a few sentences with the change, affected area, and check.
- A feature with several decisions needs a short brief and ordered units.
- A change to shared data, permissions, a public interface, or an independently deployed service needs the relevant compatibility, failure, and recovery details. Its line count does not determine its risk.

For broader product exploration or a prototype to resolve one expensive uncertainty, use [explore.md](explore.md). For an internal app's ownership, risk, or release obligations, use [operate.md](operate.md). These are selected methods, not mandatory stages.

Use an existing project document or the requested destination. If no file is needed, keep the plan in the conversation. Do not create a tracker, glossary, issue, or planning directory as a compulsory prerequisite.

## 1. Establish the outcome and preserve decisions

State who uses the result, what they will do, and what will be observably different. Separate the outcome from a prescribed means. For example, "an operator can resume an interrupted import without duplicate records" is an outcome; "use the existing job queue" may be a settled implementation constraint.

Distinguish:

- An explicit user decision or an accepted design, with its source.
- A fact established by current code or another inspected source.
- A working assumption that still needs a check.
- An unresolved choice that changes the plan.

Do not reopen a settled choice because another approach seems neater. Report new evidence that makes it unsafe, infeasible, or inconsistent with another requirement. Ask only about the resulting conflict. A settled decision does not make a real defect disappear.

Read stated product intent separately from recent activity. A commit history shows what changed; it cannot establish the intended audience or silently expand the product. For an existing internal app, identify changes in users, dependent consumers, roles, data, consequential writes, and ownership. Turn a changed obligation into an affected behavior and its proof rather than leaving it in a risk label.

## 2. Resolve only questions that change the work

Research facts the project can answer. Ask the user for decisions that belong to them. An unfamiliar term, a missing success condition, or a choice affecting cost, data exposure, or compatibility can merit a question. A helper's eventual name usually does not.

When direction is genuinely open, ask about the problem, affected users, their current workaround, the smallest useful outcome, and important exclusions. Use only the questions needed here. Offer concrete alternatives with the consequence that separates them. If the user cannot evaluate an unfamiliar choice, explain it briefly and recommend a default. Record an unconfirmed default as an assumption, never as the user's choice.

Generate alternatives before selecting one when an expensive unresolved decision warrants comparison. Change the mechanism or product shape meaningfully, such as synchronous processing versus a durable job, rather than comparing three spellings of the same design. Include the existing approach or doing less when it could meet the outcome. Once the decision is settled, stop producing alternatives.

Separate knowable planning questions from execution questions. Source compatibility may be researchable now. The exact query plan or a timing-sensitive failure may need an authorized experiment later. Name the experiment, its expected discriminating result, and what remains conditional. Do not invent execution evidence to finish a plan.

## 3. Make requirements observable

Write requirements in terms of actor, action, precondition, outcome, and important constraint. Add concrete examples for ambiguous words such as "correct," "fast," "safe," and "compatible."

For each material behavior, establish how someone can tell that it works. Use known expected values, accepted examples, existing contracts, or a trusted independent reference. An expected result computed by the proposed implementation is not an independent check.

Cover failure cases that follow from the accepted behavior and actual risks. For a shared write, ask who may perform it, what can race, what persists, and what happens after an interrupted response. Do not invent unrelated features merely to fill a checklist. Equally, do not drop a required denied-action or persistence case because a happy-path test is cheaper.

Keep one authoritative statement of each rule. Link units and checks to existing requirement identifiers where available. For a new complex plan, stable local identifiers can reduce ambiguity. A two-line change does not need an identifier system.

## 4. Design from real callers

Before proposing types or folders, sketch realistic use. One normal caller and one meaningfully different caller often expose the difficult part. Include the result they need, the errors they must handle, the state they retain, and any ordering or cancellation they rely on. For a UI, use the actual interaction sequence. For a background job, start with its trigger and required durable effect.

Then trace ownership:

1. Where does untrusted transport or stored data enter?
2. Where does it become validated domain data?
3. Which component owns the business invariant and each state transition?
4. Which callers read or write that state?
5. What does the caller need to know, and what complexity can the implementation hide?

Use the project's terms. If "account" means a person in one place and a billing organization in another, resolve the consequential ambiguity before choosing a schema. Test definitions with a concrete counterexample. Keep a glossary about business meanings; put implementation choices in the plan or an existing design record. Create or edit those records only within the task's writing scope.

Select a representation that makes valid behavior easier to express. A state model can prevent impossible combinations of booleans. A table can replace duplicated dispatch rules. Runtime parsing is still needed at real trust boundaries even when internal types are strict. Preserve numeric units, nullability, identity, and ownership semantics across conversions.

Question pass-through wrappers, duplicated domain checks, transport types leaking into callers, several writers for one invariant, and hand-maintained lists that could be derived. Apply a practical deletion test: would removing this abstraction remove complexity, or merely force every caller to reproduce it? Reuse an adequate project implementation before adding a framework, adapter layer, or dependency.

Give acquired resources an owner and an end condition. A connection, subscription, file handle, background task, or temporary process needs defined behavior on success, failure, cancellation, and teardown. Check who can still use it during cleanup. Do not hide a lifetime assumption inside a wrapper.

If successive units need the same exception, conversion, or cross-owner write, revisit the boundary before adding another workaround. Several supported ways to perform the same operation, callers reaching into internals, and parallel lists that drift are signals to reconsider the design. Use [language-design.md](../references/language-design.md) for language-specific representations and checks when relevant.

For concurrent work, first separate state that need not be shared. Keep a real shared invariant at one enforceable boundary. Two processes reserving the last item need a transaction, uniqueness rule, compare-and-swap, or another suitable existing mechanism. Separate result files do not solve that race.

## 5. Break work into verifiable units

Prefer a narrow complete behavior through the required layers. "Create and reopen a reservation" is a useful unit. "Finish the database layer" is usually only a prerequisite, not a delivered feature.

Each unit needs enough information to execute:

- The behavior or structural result, with relevant requirement and decision references.
- Its true prerequisites. Distinguish a parent grouping from a blocking dependency.
- The likely files and ownership area, including tests and generated outputs.
- The approach and existing patterns worth following.
- Specific input/action/expected-result scenarios.
- The evidence needed to call it complete, including any original user route or durable effect.
- A decision or permission that blocks it, if one remains.

Preserve stable unit identifiers when reordering or splitting an existing plan. New units receive new identifiers. Do not renumber old references for cosmetic neatness.

Check the graph before proposing parallel work. Reject cycles and missing prerequisites. Inspect overlap beyond filenames: shared interfaces, migrations, lockfiles, generated clients, databases, browser sessions, and build outputs may serialize otherwise separate edits. Decompose only when the saved time or clearer responsibility outweighs integration cost. No worker fleet is required.

For a broad rename or data migration, use [refactor.md](refactor.md). Expansion, bounded consumer migration, and final contraction may be safer than ordinary vertical slices. If intermediate batches cannot remain usable, name the isolated integration boundary and the final verification owner. Do not promise independently passing units that cannot actually pass.

## 6. Plan proof and recovery alongside the behavior

Choose the interface before the driver. A URL may identify an API rather than a web page. State whether the contract runs through a browser, API, CLI, job, webhook, or a necessary combination. Identify owned fixtures and downstream destinations. A localhost endpoint can still call a real service, so establish isolation before promising a harmless test.

For a new CLI, package, or app, identify how the intended user will obtain and run it. Plan the relevant newcomer journey: installation or access, first success, real use, diagnosis of a likely error, and upgrade. Use an isolated newcomer setup during later verification when the task warrants it. Imagined confusion is a hypothesis until observed. Source code existing in a repository does not establish delivery to its intended user, and planning the distribution route does not authorize publication.

Map changed public behavior to the documentation someone uses: reference, task instructions, first-use tutorial, or explanation. Update only the types that serve the task; a matrix need not produce a document for every cell. Include affected diagrams and operational commands when names or dependencies change.

Inspect existing test homes and project commands before proposing new tooling. Name checks at the level that can detect the failure. A shared HTTP validation change may need both web and import callers. A toolbar test does not establish the keyboard path.

Use interface-level assertions for stable behavior. Add an independent effect observation where persistence, denial, concurrency, or downstream completion is part of the claim. Reopening a record in a fresh process may be enough. A database or service readback may be needed when the public reader could repeat the writer's defect. A response accepting a job does not prove completion of its work.

Use [verify.md](verify.md) for the later acceptance procedure. Separate focused implementation tests from acceptance of the integrated result. A worker can test its own unit. The integration owner must inspect the actual changes and affected combined behavior. If independent review is requested, say what evidence and candidate it will receive. Self-checking is still useful, but must not be relabeled independent acceptance.

For a consequential change, name the recovery boundary. Reverting code, restoring application data, recovering decision records, and reconciling an already accepted external action are different operations. State the backout condition, the state it restores, and what remains irreversible or unknown. Plan those operations without granting authority to perform them.

## Example plan excerpt

The following is an illustrative plan, not evidence of execution.

Goal: Allow two existing operators to reserve one shared item through the current reservation page. Keep the existing role policy and database.

Accepted constraints: One item can have one active reservation. A denied request creates neither a reservation nor a queued notification. An uncertain response must not cause a duplicate reservation on retry.

U1, reserve and reopen: Carry the existing page action through the service and storage boundary. Use the current transaction mechanism. Test a permitted request, an unavailable item, and a fresh-session read of the resulting reservation. Own the reservation service, its endpoint, and their existing tests. No dependency.

U2, concurrent and interrupted requests: Depends on U1. Exercise two separate clients against one available item. Expect one reservation and one defined conflict. Simulate a lost response after the write, repeat the same operation identity, and verify that the result refers to the same reservation. Check denial leaves no downstream effect.

U3, integrated page acceptance: Depends on U1 and U2. Exercise the original page in the actual development instance using disposable records. Verify the displayed result and fresh-session persistence. If browser access is missing, the service evidence can complete while page acceptance remains blocked.

Open decision: Whether the existing notification system can carry a stable reservation identity is unverified. Inspect it before U2 chooses retry handling. Sending real notifications is outside the isolated test scope.

## Finish and recover

Read the plan once as an implementer who has not attended the conversation. Can that reader locate the project, preserve agreed behavior, start the first ready unit, and tell whether each unit succeeded? Remove duplicated rules, speculative machinery, and empty sections. Check for contradictory examples, missing consumers, and invented decisions.

Return the plan and the exact unresolved conditions. If implementation is already authorized, continue with [implement.md](implement.md). Otherwise stop at the requested plan. No ceremonial approval is needed for a choice the user already made, and no plan artifact can substitute for approval they have not given.

On resume, compare the plan with current source and new user decisions. Preserve still-valid units and evidence. Mark only affected decisions stale. An interruption is not a reason to restart discovery or erase the previous plan.
