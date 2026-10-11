# Designing a useful skill

Use this reference while authoring or restructuring. It preserves the useful design depth of Skill Creator Pro and applies the current builder's independence and evidence requirements. Architecture is chosen from the work, not a tier label.

## Decide what deserves a skill

Name a repeated workflow, a costly recurring error, or a body of domain knowledge that materially improves output. Walk a representative task from input to result. Inspect the existing owner: extending one good local method may be better than adding a second route. A one-off request can remain a task without becoming permanent context.

Write a capability contract in ordinary language:
- Owned job and useful result.
- Inputs, governing sources and quality standard.
- Distinct branches and near misses.
- Required tools and permissions, with unavailable-tool behavior.
- What the user or downstream system can inspect to judge completion.

A title such as research assistant is too broad. A method that reconciles conflicting source claims into a dated decision brief has identifiable inputs, output and failure conditions.

## Select resources by function

Use instructions alone when the task needs judgment and a small method. Add references for domain facts and branch-specific depth, assets for reusable output structure, and scripts for exact transformations or repeated operations. Multi-phase work may use local playbooks in one context; it does not automatically need agents or another router.

Keep required expertise local. A tool prerequisite can be external, such as a workbook reader, but the skill must still know its own method. Do not depend on another personal skill's internal file to supply the actual workflow. Optional composition uses public invocation and honors explicit-only boundaries.

A helper earns its cost when it protects a real invariant, removes repeated work or enables an operation the method actually needs. Prefer an adequate native capability, existing project code, stdlib or installed dependency in that order. Do not add wrappers, registries or services to satisfy a directory template.

## Six workflow patterns

### Sequential delivery

Use when a later output depends on an earlier result. Name each prerequisite and its completion condition. Carry source identity and accepted decisions forward. If an input changes, invalidate dependent outputs rather than reusing stale approval.

Example: read supplied notes, reconcile factual disagreements, draft a workshop guide, inspect it against sources, then prepare delivery. A good draft does not authorize sending it.

### Multiple tools or services

Map each input/output to its owner and real tool. Verify availability and permission before the dependent step. Keep an explicit handoff artifact and recovery point at external side effects. A connector name in prose is not proof the connector is connected.

Example: read an authorized sheet and draft a report locally. If publication requires a missing connector or approval, return the finished report and the exact blocked publication step. Do not silently switch accounts or post elsewhere.

### Bounded refinement

Start from a concrete defect or quality goal, freeze the criterion, change one coherent cause, inspect the new artifact and retain or revert. Define finite effort and a stop for repeated failure or no useful progress. Do not force a minimum number of iterations after the outcome is already adequate.

### Context-aware tool choice

Choose the simplest available tool that meets the actual requirement. Declare what a fallback can and cannot do. A text-only fallback can analyze a table's values but cannot prove visual layout or a workbook's formulas. When an essential capability is absent, return a partial result instead of quietly lowering the task.

### Domain checks before action

Validate consequential preconditions before mutation: source identity, allowed roots, current approval, schema, account destination or irreversible effects. Keep the user's decision separate from a validator's consistency check. Checks should fail closed on malformed or missing required evidence.

### Create versus edit

Creation begins in a new approved destination. Editing starts from a frozen existing identity and preserves unrelated material. A missing target may mean create; it does not mean overwrite its parent directory. An edit keeps the original skill's name unless the user approved a rename. Show the intended diff and bind application to the inspected bytes.

Patterns combine only when the task needs their distinct behavior. Do not stack all six around a small formatting request.

## Five reliability patterns

### Deterministic operations

Use code for exact calculations, identity, parsing, repeatable conversion and state transitions. Define units, allowed inputs, boundary values and errors. Test a known wrong case. Code that validates structure does not prove factual truth or human permission.

### Validation at boundaries

Validate before accepting external input and after producing consequential output. Check type, shape, source and completeness at the boundary that needs them. Distinguish absent, malformed, denied and valid-empty states. Avoid repeated checks of unchanged data just to lengthen a workflow.

### Templates and examples

Use strict templates for machine contracts and flexible examples for judgment-heavy prose. State which fields are required and which are illustrative. Include a good output, a plausible failure and why they differ. Never let fictional examples become claimed user facts.

### Error-aware recovery

Name likely failure classes and safe recovery: denied source, missing tool, malformed data, partial write, timeout, stale approval, conflicting evidence. Retry only a recoverable failure within the actual budget and authority. Preserve dispatched work and unknown effects before deciding whether retrying risks duplication.

### Judgment plus exact machinery

Let the model choose and explain the appropriate method; let exact mechanisms enforce the properties they can actually measure; inspect the result qualitatively where needed. For example, a script can check record IDs and counts while a reviewer checks whether the explanation preserves uncertainty and gives useful advice.

## Freedom and instruction quality

Use a fixed procedure for fragile operations, parameterized steps when variation is bounded, and judgment where several valid approaches exist. Preserve user policy and domain knowledge even if a capable model might often infer them. Do not make unsupported claims that a new model makes a safeguard unnecessary.

Front-load the action or decision. Explain why only when the reason changes behavior. Use familiar terms with concrete meaning; avoid invented jargon that needs a second manual. State the desired behavior positively when clearer, but retain necessary prohibitions at authority and safety boundaries.

A phase needs a checkable completion condition. Produce a plan is weaker than account for each approved target and its verification. Sharpen the condition before adding a new context or agent boundary. Splitting files does not remove already-read future steps from the current context.

## Pointers, loading and splitting

A pointer must identify the resource and the branch that needs it. One trigger per distinct branch is better than a synonym list. Required common material belongs in the entry; conditional depth belongs behind a direct pointer. Co-locate the definition, caveat, example and rule for one concept.

Split by meaningful differences in inputs, authority, evidence, failure handling or human invocation. Keep branches together when they share one contract and splitting would create fragile dependencies. Do not hide an essential method behind an undocumented helper or a user-only skill another caller cannot reach.

Always-loaded description cost and human recall burden are different. Observe actual host discovery before claiming zero context load or portability. Validate adapter metadata, explicit calls and supporting reads separately. A metadata-hidden skill may need a corrected invocation policy, not more description keywords.

## Pruning without damage

For each proposed cut, identify what behavior it currently protects, whether another mechanism reliably owns it, and what evidence supports removal. Preserve rare critical recovery and authority even when the small example set never triggers them. Lack of a failing test is not proof a rule has no purpose.

Keep one local authoritative statement where inheritance is reliable. Independent consumers may need deliberate repetition of essential constraints. Move detail only when the intended route still reads it. Treat file length and scanner findings as diagnostics; outcome quality and preserved behavior decide.

The environment is also a source of truth. Prefer reading an actual command's help to copying every option into prose, but retain non-obvious gotchas and a working example. Dates, host assumptions and model-specific claims must be refreshed when the task depends on them.

## Generated skill quality gate

A complete candidate has a useful entry, full selected methods, resolved resource dependencies, real examples, working exact operations where needed and honest unsupported-tool behavior. Its authored outputs preserve facts, uncertainty, counts, permissions and requested format across every delivered file and final answer. Meaningful checks inspect those properties, not merely the presence of filenames or headings.

Test direct use without siblings, a resource-dependent branch, near misses, missing prerequisites and a realistic failure. Match the amount of evidence to the decision. Distinguish an exploratory self-check from frozen comparison, independent review, native qualification and installation. Package identity and a clean parser never grant a stronger claim by themselves.
