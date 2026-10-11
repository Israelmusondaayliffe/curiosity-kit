# Plan the web product or change

Use this method when the requested outcome, interaction model, data boundary, or implementation sequence needs definition. Scale the depth to the task: a label correction needs a short requirement and affected-flow check; a stateful product needs the full relevant procedure. Planning-only ends with a usable plan. Implementation authority and route selection remain in [the entry](../SKILL.md); this method does not add a compulsory approval ceremony.

Read [architecture and errors](../references/architecture-and-errors.md) when state, interfaces, storage, APIs, concurrency, or a structural decision is involved. Use [design](design.md) for unresolved visual direction, [reference-to-code](reference-to-code.md) for a supplied visual source, and [Sites](sites-artifact.md) for that artifact workflow. The canonical flow and record definitions live in [acceptance contracts](../references/acceptance-contracts.md).

## 1. Establish the actual starting point

Begin with the request, accepted decisions, supplied sources, current artifact and project constraints. Reuse answers already given. Separate what the user wants from what the current code happens to do.

For an existing project:

1. Read its governing instructions, README/run instructions, dependency manifest and lockfile, route entry points, relevant design tokens, and applicable architecture decisions. Use an existing glossary if present; its absence is not a blocker.
2. Inspect the current render and replay the relevant journey when the environment and task permit it. Name the route, actor, data and view you actually observed. A directory named `dashboard` is not evidence that the dashboard works.
3. Find the entry point for the changed behavior. Follow its actual calls through state, validation, service/storage and response to presentation. Read the relevant implementations and their public callers, not just filenames or symbol matches. Record unknown links rather than filling them in.
4. Inspect existing tests and one or two good neighboring implementations. Establish which command and fixture exercise this path. Notice framework/client/server boundaries, generated files, deployment assumptions and shared components.
5. Use relevant history, comments or design records to understand surprising constraints. Explicit explanations support intent; code alone establishes behavior. Distinguish direct rationale, supported inference and unknown history. Preserve a documented tradeoff unless the request or new evidence justifies reconsidering it.
6. Identify affected callers, tests, fixtures, exports, configuration and content. Use the narrow [protected working-state baseline](build.md#protect-the-existing-working-state) before edits. Do not turn a scoped change into an entire-repository audit.

For greenfield work, establish the intended execution environment, output format, expected audience, content sources, data lifetime and integration needs. Check existing host/platform capabilities before creating custom infrastructure. Use the requested stack; otherwise choose the smallest complete approach compatible with the actual environment. A static document, browser-only utility, server-rendered page and multi-user app do not need the same architecture.

If source and delivered behavior disagree, use the conditional artifact-attribution procedure in [redesign](redesign.md#delivered-artifact-and-trace-diagnosis). Do not silently plan against the wrong version.

## 2. Define the job and the useful smallest outcome

Write a short statement of who uses the product, in what situation, what they do, and what observable result makes the work useful. Include the maintainer or downstream caller when their experience constrains the implementation.

Clarify only consequential missing information:

- Audience and actor roles; first-time versus returning use; permission or tenancy boundaries
- Primary journey, frequency and environment, including the important narrow-screen or keyboard path
- Required content, facts, sources and editable versus fixed material
- Persistence, collaboration, authentication, offline, export or integration needs
- Required output, existing accepted design, delivery destination and explicit exclusions
- User-supplied timing, capacity, cost, compatibility and quality bounds, with their units

Do not make the user specify routine engineering details already determined by the repository. Do not treat a plausible assumption about money, privacy, permissions, retention, destructive actions or product policy as an accepted decision. State reversible low-risk assumptions; surface a material unresolved choice before dependent work. Separate facts you can look up from choices only the user can make. Order questions by dependency: ask what can be answered now; keep a downstream choice pending until the needed fact or earlier answer exists.

### Discovery changes with the purpose

For an existing brief or approved plan, synthesize it rather than repeat an interview. For an exploratory commercial product, distinguish observed demand from hypotheses: what specific workflow is used today, what does it cost, who has tried the alternative unassisted, what happened, and what is the narrowest useful change? Compliments and a market-growth statistic do not establish actual use. Ask only the questions that could change this decision; never invent customers, interviews, usage or willingness to pay.

For a personal tool, learning project or creative experiment, start with usefulness, delight or the thing the user wants to try. A small sound recorder may be valuable because it makes a kitchen-sound instrument possible; it does not need a revenue interview. Name a tangible first interaction and its completion condition.

When proposing new architecture or an unfamiliar product approach, first check available native capabilities, existing products, conventional solutions and useful adjacent-domain approaches. Use bounded current research when it could change the choice, verify important claims against primary sources, and distinguish actually inspected evidence from prior knowledge; public queries use general category terms without private product details. If research is unavailable, name the gap rather than invent a comparison.

When the requested solution seems misaligned with the problem, compare it with reuse, a targeted repair, or doing nothing. Recommend a smaller scope without silently reducing an accepted requirement. Likewise, an attractive larger vision is a proposal, not extra build scope.

### Compare decision-sized alternatives

Compare alternatives only for a real unresolved choice. Use two or more meaningfully different shapes when the choice warrants it, such as filtering a local dataset versus a server query, or a modal editor versus inline editing. Keep the content and constraints constant. Explain:

- What the user or caller can do in each option
- What existing work it reuses
- Complexity and operational burden at the expected scale
- Important failure, privacy and reversibility tradeoffs
- Which option best serves the stated outcome and why

If pixels or an interaction model would resolve the uncertainty, send that question to [design](design.md)'s bounded prototype method. If the uncertainty is about legal state transitions, build a driveable synthetic state-model experiment. Record what the prototype proved and what remains unproven. A selected prototype is a decision source, not production qualification.

### A logic prototype answers a state question

Use this only when a small experiment will settle a specific unresolved model. State the question visibly. Put the reducer, state machine, pure functions or stateful module behind a portable interface separate from DOM handlers. A small self-contained HTML demo is often enough; use the existing project shell when it materially affects the question, under the prototype isolation rule in [design](design.md).

Show the current state in readable domain language, not only a raw JSON dump. Provide free-play actions and guided scenarios for the normal path, an awkward boundary and an illegal transition. Starting each guided scenario resets to its known synthetic state. For example, a draft editor can expose edit, save, cancel and delayed-response controls so a reviewer can inspect what cancellation means while a save is pending. Keep the important state visible and the run/open path trivial.

Use in-memory or a specifically isolated scratch store; do not make production connectivity a prerequisite. Save the question, chosen model, observed outcome and remaining unknowns. Lift only the validated decision-rich model into the implementation plan, then build its real error handling, integration and checks through [build](build.md). A compelling demo does not establish persistence, permissions or production readiness.

## 3. Turn requirements into observable journeys

Define one acceptance flow per material user outcome, using the canonical structure in [acceptance contracts](../references/acceptance-contracts.md). Keep the requirement stable while implementation details evolve.

For each flow, establish:

1. The actor and real starting conditions: route, permission, fixture, stored state and relevant environment.
2. Small actions a user can actually perform, in order. “Use the catalog” is too broad; typing a query, selecting a category, opening an identified result and returning are observable steps.
3. The result after each action: visible content, enabled action, route/history state or a source-owned durable state. Distinguish feedback from completion.
4. The wrong result the check must reject. “At least one result” cannot prove an exact requested result set or count. A toast cannot prove a saved record is retrievable.
5. A meaningful negative or recovery path for critical work: empty search, validation refusal, lost connection, denied write, expired state, conflict, cancellation or retry as applicable.
6. The observation needed for proof. Plan screenshot/DOM/response/readback evidence now; leave actual observations and verdicts unfilled until execution.

Keep implementation internals out of a user flow unless they are themselves required. Use a public application read to establish durable retrieval; use storage inspection as a diagnostic supplement or an explicit storage-invariant check. Neither substitutes for the required interface behavior.

### Example: a small shared catalog

This is a synthetic planning example, not an executed result.

The user wants authenticated editors to maintain a catalog and readers to find and inspect items. Freeze fixtures with named IDs and known category membership.

- Reader searches for a term, selects a category, sees the exact matching IDs and count, then resets to the full expected set. A query with no matches gives a clear empty state and a working reset action.
- Reader opens an item, reads its detail, closes it by the supported keyboard action and returns to the initiating control without losing the search.
- Editor changes a title, sees pending then confirmed status, reloads, and a second authorized consumer retrieves the same saved value.
- Reader attempts the same write through the ordinary application boundary. The request is denied; a fresh authorized read proves the record did not change.
- A delayed older search response arrives after a newer query. The visible results still correspond to the newer query.

The primary flow covers the visible job. The second consumer proves the required shared lifetime; localStorage would not satisfy that requirement. A successful editor write is the legitimate control for the denied-write check. Detailed state and API construction belong in [architecture and errors](../references/architecture-and-errors.md).

## 4. Design the implementation-ready shape

Describe the real components needed, with a one-sentence responsibility, public inputs/results, dependencies, state ownership and failure behavior. A diagram or annotated flow helps when relationships are nontrivial; do not require a diagram for a one-field edit.

Trace each changed path from input to validated domain operation to storage/integration to output. Explicitly consider missing, empty, malformed, unauthorized, stale, partial, conflicting and failed data where relevant. Do not add a catch around every function; define boundaries and recovery using [architecture and errors](../references/architecture-and-errors.md).

### State and interactions

Choose where each value lives: component-local state, shared parent, URL, shared application state or server-owned state. Identify the authoritative owner and derive display-only values rather than keeping synchronized copies. Name transitions and invariants before accumulating booleans. Include pending, success, empty, validation/error and recovery states as part of the interaction, not later decoration.

For overlapping operations, write the exact invariant and its time boundary. Compare both relevant completion orders across awaits. For example, if an edit is cancelled while a save is pending, does cancellation discard only the UI draft, cancel a not-yet-started request, or require a compensating server operation? An abort signal does not by itself prove that the server rolled back. Resolve the product meaning, then choose a mechanism and a controlled pause/release check. Avoid an unsupported exactly-once guarantee.

### Data and integrations

Where storage or APIs are needed, settle:

- Entity fields, IDs, ownership, relationships, uniqueness and allowed values
- Read and write paths, required atomicity and consistency, and data lifetime
- Schema/migration strategy; compatibility with existing data and readers
- Index candidates justified by actual filtering, joins and ordering
- Endpoint or server-action inputs, success and error outputs, authentication and object-level authorization
- Validation, list limits/pagination, stale-write handling and idempotency where repeat submissions matter
- External interface contracts, secret location, unavailable-provider behavior and test substitute boundaries
- Cache ownership, key scope, invalidation and stale-data policy if caching earns its cost

Use target scale, not an invented future platform. Record expected users/data/rate from evidence or mark them as assumptions. Say what fails first as scale grows, and which observed threshold would justify the next step. A single-process in-memory list is not shared durable persistence; a database choice alone does not prove multi-user safety.

### Folder and interface decisions

In an implementation plan, give real affected paths or proposed new paths with purposes. In a durable product specification, keep requirements at stable behavior/module level and link the changing implementation map. This preserves build usefulness without filling the long-lived spec with quickly stale paths.

When a boundary is non-obvious, write the caller's usage first, then derive the interface. Compare structurally different designs if caller coordination, state ownership or dependency placement is genuinely contested. Prefer the interface that hides policy and sequencing callers should not need to repeat. Avoid adding a new wrapper, store, router or service merely to match a pattern name.

## 5. Plan proof and risk together

Select the fewest public seams that together cover the required behavior. State what each catches and what it misses. Reuse project test infrastructure. The normal combination for a stateful web feature is focused domain/API checks plus the real browser journey, with visual acceptance evaluated separately by [verify](verify.md).

Choose inputs that discriminate correct behavior: known literal outcomes, two roles for access boundaries, two consumers for required shared persistence, both completion orders for a race, and realistic long/empty content for layout. A check that only proves a mock was called cannot establish a real integration. Freeze relevant metrics and conditions before performance work; no invented p99 or unmeasured improvement target masquerades as a baseline.

For each significant risk, state the trigger, impact, prevention or recovery, and proof. Examples include losing an edit during navigation, exposing another tenant's records, returning stale search results, unbounded list rendering, or a migration that old code cannot read. Keep accepted risks distinct from unresolved ones. If the current task ends at a private preview, document deployment considerations only when necessary; do not create a release project.

## 6. Sequence complete, dependency-ready slices

A normal slice delivers a narrow usable path through the layers it needs, including its state and checks. Inside that slice, build prerequisites in dependency order. Avoid completing every schema, then every endpoint, then every screen while no path works.

For each slice, name its delivered behavior, real blockers, owned modules, affected shared modules and acceptance proof. Start unblocked slices; run independent work in parallel only when write targets and integration boundaries are clear. Shared routing, schema or canonical record changes have one writer or a sequenced integration point. Keep the dependency graph in the existing task record, not a second orchestration system.

A possible catalog sequence is: browse an isolated real data source; search/filter/reset through the same public boundary; inspect accessible details; authorized edits with durable readback and denied-role proof. Sequence a common schema or route contract first when later work truly depends on it. Per-slice passing results still need integrated review after the pieces meet.

Wide mechanical refactors can use expand–migrate–contract when one-step replacement is unsafe. Name when both forms coexist, which callers migrate in each batch, and the final removal condition. If individual batches cannot be independently green, explicitly keep them on one integration unit and promise green only at the named integration check. Do not report unfinished migration as separately complete functionality.

## 7. Leave one buildable plan

Use one existing task artifact. It should contain, at the depth the work needs:

- Outcome and why this approach serves it
- Actors, journeys, accepted content/design references and observable requirements
- Chosen technology/environment and actual relevant project conventions
- Components, state/data flow, interfaces, affected folder responsibilities and conditional schema/API decisions
- Edge/failure/recovery behavior and relevant trust boundaries
- Ordered slices with dependencies and requirement-to-proof links
- Assumptions, alternatives rejected, unresolved decisions, limits, risks and exclusions
- Current decision status and exact source of consequential acceptance

Keep proposed, accepted, observed and verified facts distinct. Preserve the rationale for changed decisions and the prior version they supersede. A saved draft is not approved; an approved plan is not executed behavior.

Before proceeding, ask: could another implementer complete the accepted outcome without inventing product policy, losing a requirement, or guessing how success is observed? Fill material gaps, or name the prerequisite that blocks them. Continue already-authorized work that does not depend on a pending choice. When implementation is in scope and ready, continue with [build](build.md) or the relevant [redesign](redesign.md) branch.
