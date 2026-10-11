# Build the complete web outcome

Use for authorized implementation of a website, component or web product, including its local data/API work. This is a complete local engineering method; no Coding Studio, donor toolkit or sibling skill is required. Diagnosis and structural changes use the corresponding branches in [redesign](redesign.md). Final review and acceptance are owned by [verify](verify.md).

Start from the current task contract established in [the entry](../SKILL.md) and, when needed, [plan](plan.md). Load [architecture and errors](../references/architecture-and-errors.md) only for the applicable state, interface, persistence, integration or error work. Follow [design](design.md) or [reference-to-code](reference-to-code.md) for the governing visual decision; do not reselect a style while implementing it.

## 1. Reconcile scope with the real project

Read the current plan, required outcomes, exact selected design/source version and relevant repository conventions. Recheck the affected source before editing if the plan or collaborator's work was produced against an earlier version. Protect existing work using the baseline below.

Inventory every requested deliverable and its dependencies: pages, components, data/API behavior, states, assets, configuration, tests and run/use instructions. Reused components count as fulfilled only when they actually provide the required behavior in this context. Include the integration work needed to connect the pieces. Mark items implemented only after the code exists, and verified only after the relevant check runs.

Inspect the manifest, lockfile and actual build configuration. Use the existing framework, styling system, router, component primitives, package manager and test conventions. Resolve real import names and supported APIs; do not infer them from a remembered library version. A Tailwind v3 project and v4 project can require different configuration. A server/client framework boundary can make a working isolated component fail inside the app.

Create only the files the selected shape needs. Do not create empty directory trees or parallel configuration for ceremony. An implementation map may change when a smaller coherent structure emerges; update it and explain consequential deviations. If the plan turns out infeasible, surface the exact constraint and a useful alternative rather than silently omit the feature.

### Protect the existing working state

Before edits, inspect the actual repository/workspace, current revision and status. Use explicit `git --no-optional-locks` for read-only Git inspections when preserving dirty working state, adding command-local `-c diff.autoRefreshIndex=false` to diff reads to prevent implicit index refresh; do not assume the host shell inherits `GIT_OPTIONAL_LOCKS`. For Git, distinguish staged changes, unstaged tracked changes and untracked files; include relevant submodule state if the task touches one. Inspect both index and working-tree differences. A clean diff against HEAD does not describe a staged/unstaged mix correctly.

Identify which existing changes belong to the user or another worker, especially in overlapping files. Record a narrow baseline outside the changed application paths: protected paths and their bytes/digests, staged entries/blob identities, and relevant staged/unstaged diffs. Preserve needed recovery copies privately without printing secrets. For non-Git work, record the affected files and protected neighbors directly. Do not collect unrelated large trees merely to create a baseline.

Make surgical edits on top of the actual working copy. Do not reset, clean, stash, overwrite from HEAD, stage someone else's changes, or restore a whole file to undo one failed experiment. If an overlapping change makes ownership unclear, stop that edit and resolve it. A worktree or branch is not isolation from a shared database, generated output or service.

After a fix, refactor, retry or integration, compare protected file bytes and the protected index state with the baseline. Inspect the final diff for unexpected files and removed content. Undo only this task's known change when a hypothesis fails. If another writer changed a protected path, reconcile the new evidence rather than overwrite it with the old snapshot. Repeat this check at the final candidate boundary.

### Choose the smallest complete construction

Take the first option that fully satisfies the accepted behavior:

1. Reuse an existing project component, helper or service in its established way.
2. Use the platform or standard library when the project has no appropriate house solution.
3. Use an already-installed dependency that fits the actual task.
4. Add straightforward local code; introduce an abstraction when it removes repeated policy, caller coordination or invalid state.
5. Consider a new dependency only when its benefit and lifecycle cost justify it, under the task's permission boundary.

A readable one-liner is useful; a compressed expression that hides policy is not. Preserve validation, recovery, access control and accessibility when moving code. A shortcut must name its actual ceiling and upgrade trigger, for example “isolated demo dataset is loaded in memory; replace before shared writes or data beyond the agreed size.” It cannot waive requested durability or security. No automatic dependency installation, framework migration or paid-service use follows from this ladder.

## 2. Implement one observable slice at a time

Choose a ready slice from the plan. Inside it, establish the domain/data prerequisites, operation, route or adapter, UI and integration needed for that path. Treat error handling as part of those boundaries, not a final blanket wrapping pass.

Use this loop for a new behavior or a defect with a suitable seam:

1. **Name the behavior.** Write the observable result and a concrete wrong result the check rejects. Reuse the planned public seam, fixture and expected values.
2. **Create the smallest meaningful check.** Prefer an existing domain/API/component/browser seam that reaches the real behavior. Keep internal helpers real; replace true external services, time or randomness at an appropriate boundary when needed.
3. **Run it before the implementation.** Confirm it fails for the intended missing or broken behavior. A missing package, wrong URL, syntax error in the test or broken fixture is setup failure, not valid red evidence. Preserve a real initial failure.
4. **Implement the complete narrow path.** Add the minimum code that meets the requirement, including required denied/error/recovery behavior. Do not batch a speculative test suite for features whose interfaces have not been understood.
5. **Run it again.** If it fails, inspect the result and fix the cause. Do not weaken the expected value to fit the implementation.
6. **Refactor only from green.** If the project permits in-loop refactoring, make a bounded simplification and rerun the same proof. Otherwise defer structure to the review stage. In both cases, behavior remains pinned.
7. **Integrate and continue.** Run the closest neighboring checks and update the slice's actual state. Start dependent work only after the prerequisite is ready.

For existing working behavior, write/run a characterization check before structural change. Where a durable automated test is impractical, retain the closest useful executable regression: a focused browser action sequence, HTTP probe, fixture-driven script or controlled comparison. Name why no durable test exists and what the substitute misses. Code inspection alone cannot certify execution, but lack of a suitable runtime does not prevent clearly labeled implementation or static diagnosis.

### Make tests sensitive to the requirement

Call the application the way its consumers do. Prefer independent expected literals or examples derived from the accepted specification. For a synthetic catalog query, derive the expected IDs independently from the frozen fixture definition and assert that exact result set, relevant count and order when order is required. Do not compute “expected” by applying the same filtering function under test.

For a save, create through the real public operation and retrieve through a fresh public read. For a refusal, include a legitimate allowed control and prove the denied operation left the relevant state unchanged. Negative and empty outcomes can be valid assertions; pair them with controls that show the fixture and interface are active. A test that passes when the exercised behavior is replaced by a no-op has not locked down that behavior.

Avoid testing private method calls, incidental component nesting, arbitrary function length, source-token presence or a mock's invocation count when the user cares about an outcome. Use a local test database for a persistence requirement when available. A mocked provider response demonstrates only the owned boundary; record live integration as unrun until it is actually exercised under authority.

## 3. Construct the domain, storage and API boundaries

Implement the chosen state model and operations before scattering policy across handlers. Apply the concrete patterns and error contracts in [architecture and errors](../references/architecture-and-errors.md), including its trust-boundary section when inputs, identities, uploads, rich text, URLs or external events are involved.

The construction sequence for a persistent slice is:

1. Define the authoritative entity and required constraints using the project's schema/types.
2. Implement the operation and its permitted transitions. Keep pure calculations separate from transport and rendering where that makes them easier to reason about.
3. Add storage with the required lifetime and atomicity. Write the migration only when needed and retain compatibility/rollback limits in the plan.
4. Parse transport inputs at the boundary, authenticate and authorize using server-owned identity, invoke the domain operation, then map its result to the agreed response.
5. Connect the UI to that real boundary. Keep fixture mode visibly identified and isolated from real accounts/data.
6. Exercise the operation through its public consumer path, including denied and recovery cases that are part of the contract.

Do not let hiding a button become the only authorization check. Do not accept role or ownership from a request body as trusted identity. Do not store server secrets in frontend bundles, URLs or browser storage. Avoid a generic catch that turns malformed data or denied access into a success-shaped empty list.

For a read-only static artifact, omit unused storage, authentication and API layers. For a real shared app, do not substitute browser storage or hardcoded arrays for the requested backend. If credentials or an external service are unavailable, isolate an honest fixture-backed path and label the unconnected requirement; do not claim it is working live.

## 4. Build the visible state model, not just the happy screenshot

Use semantic HTML and existing accessible primitives. Buttons perform actions; links navigate. Forms have associated labels, meaningful types and validation connected to the relevant field. Visible labels and accessible names should describe the same action. Use native behavior unless a real product need calls for a custom interaction.

Implement states alongside each feature:

- **Initial/loading:** meaningful initial content or pending feedback; preserve layout when practical; avoid presenting fake data as a completed load.
- **Empty:** distinguish no records yet from no matching results; provide a valid next action such as create or reset when authorized by the product.
- **Partial/stale:** keep usable data visible when appropriate, indicate what is missing or old, and define retry/refetch behavior.
- **Validation/error/denied:** explain the specific recoverable problem, keep entered work where safe, associate field errors, and offer the appropriate retry, correction or navigation.
- **Success:** show the actual completed result and relevant next action. Do not announce persisted success while only an optimistic local change exists.
- **Busy/repeated/cancelled:** prevent unintended duplicate submissions, define cancellation, and keep rapid or reversed input consistent with the model.

Prefer a loading indicator that matches the latency and information available. A skeleton is not universally better than a short label or spinner. Do not add fabricated progress percentages. Keep important failure information where it can be found after a transient toast disappears.

For dialogs and popovers, implement the primitive's correct focus, dismissal, background interaction and return behavior; [verify](verify.md) owns the actual keyboard acceptance. Preserve state that should survive close/reopen or route navigation, and reset what the contract says is transient. A detail dialog must remain attached to the selected record, including after a filter removes that record from the underlying list.

For search and filters, derive the displayed result from a single current query/filter state. Preserve shareable URL behavior where requested. Debouncing can reduce work but does not resolve stale response order. Use cancellation or request identity as appropriate and ensure only the current request can replace the visible result. Make reset, back/forward and direct-entry routes agree.

## 5. Carry visual authority into working code

Implement the selected content, hierarchy, composition and tokens, including responsive interpretation and documented unknowns from the visual method. Work from large structure to detail: page/frame and major proportions, type and content width, image framing, controls/states, then optical adjustments. Do not compensate for a wrong layout with extra gradients, cards or decorative assets.

Use the project styling system consistently. Reuse known tokens and meaningful component variants. Use grid/flex/layout flow for responsive structure rather than screenshot-wide absolute coordinates. Keep semantic content accessible when a decorative visual treatment duplicates it. Image asset identity, source and authorization remain with the design/reference method.

Treat text as real layout input. Use supplied facts and approved copy; label draft/sample content. Preserve meaningful amounts, dates, names and exact copyable text. Do not invent testimonials, contact destinations or metrics to make a page look complete. Implement long and missing content cases as part of the real component.

Prefer browser-native text flow. If the selected composition genuinely requires measured text, verify the installed measurement API and use it only for that need. Wait for fonts before measuring; cache by text/font/locale as appropriate; invalidate on changes; relayout on relevant container resize; guard zero-width states and clean up observers. Keep a semantic selectable text equivalent when rendering into canvas or manually positioned lines. Measurement is not a reason to make all text editable or to add a library to an ordinary page.

Use [visual craft](../references/visual-craft.md) for typography, optical alignment and assets; load [motion and mobile](../references/motion-and-mobile.md) only when that behavior is involved. Motion is conditional on purpose and frequency. A static result can be correct. Implement reduced-motion and input alternatives with the chosen effect; preserve cancellation and rapid reversal rather than locking a user out while animation finishes.

## 6. Integrate the real application

Integration is a required slice, not implied by separately working components.

- Check route navigation, deep links, refresh and history behavior in the actual router/hosting shape.
- Confirm server/client imports, module exports and dependency versions resolve through the project's normal build.
- Check stylesheet and asset paths from the real served origin, including base paths and case sensitivity. An image that works through a local absolute path may fail in the artifact.
- Connect shared authentication, theme, context and data providers at the intended lifetime. Avoid duplicate providers or isolated state copies that reset or diverge between pages.
- Exercise multiple consumers and roles where the requirement depends on them. Separate browser contexts alone do not isolate shared server data; use owned fixture data too.
- Implement bounded external waits, retry semantics and duplicate protection according to the operation, using [architecture and errors](../references/architecture-and-errors.md#concurrency-retry-and-cache-decisions). Read authoritative state before retrying an uncertain mutation.
- Keep console/log diagnostics useful without leaking private inputs or credentials. Remove task-owned temporary instrumentation before final review.

Use actual project-native parser, lint, type, test and build tools for their respective checks. A text heuristic cannot establish syntax, undefined variables, types or security. If a tool is missing or unsupported, name that uncovered check rather than claim an equivalent pass from reading. Preserve existing failing tests separately from new failures; establish whether the candidate caused them.

Do not run the widest or most expensive suite after every keystroke. Run focused proof during slices and the applicable integrated checks once the candidate is assembled, then rerun affected checks after repairs according to [verify](verify.md)'s evidence-freshness rules.

## 7. Prepare a complete candidate for review

Before handing to verification:

1. Compare actual artifacts with every requested deliverable and planned behavior. No skipped component, dead control, omitted section or disconnected endpoint may hide behind “the rest follows the same pattern.”
2. Ensure changed files are usable in the requested environment. Include necessary imports, configuration and actual content; remove task-created stub implementations from the accepted path.
3. Record intentional limitations, remaining unconnected services and blocked checks explicitly. A prototype or partial implementation remains labeled as such.
4. Provide the actual run/open procedure, required nonsecret configuration, fixture/setup steps and common recovery guidance. Match the user's technical level and the requested delivery format.
5. Freeze the candidate identity and pass the requirements, source/design identities, changed scope, observed check outputs and remaining gaps to [verify](verify.md).

If a response or work session is interrupted, preserve complete files and a clear next boundary in the task record. Do not shorten unfinished code into placeholder comments or claim full completion. Delivering a patch, repository change or full file is determined by the user's requested format; a full-code request gets full usable files. [Deliver](deliver.md) owns the final destination and result report after the applicable acceptance work.
