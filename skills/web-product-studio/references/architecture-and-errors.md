# Web architecture, state boundaries and error diagnosis

Load the relevant section when planning or changing web state, data, APIs, component interfaces or a concrete failure. This is domain-local implementation guidance, not a requirement to add every layer. Use [plan](../playbooks/plan.md) for decisions, [build](../playbooks/build.md) for construction, [redesign](../playbooks/redesign.md) for causal diagnosis/refactoring and [verify](../playbooks/verify.md) for review and proof.

## Choose the smallest shape that owns the real behavior

Existing project conventions are the starting point. These examples are alternatives and omit unrelated infrastructure; they are not a scaffolding checklist.

### Browser-only, no server requirement

A single HTML file can own a small local utility with embedded CSS and JavaScript. Separate files when they improve reuse or maintainability, not to satisfy a layer count.

```text
index.html          semantic page, local styles and browser behavior
```

This suits an isolated calculator or demonstrator. Browser storage can preserve a preference on one browser; it is not an authentication system, secret store, shared database or promise of permanent storage. If the user needs multi-user writes or cross-device retrieval, choose a real server/storage boundary.

### Component-based frontend

```text
src/
  pages/            route-level composition and route data
  components/       reusable controls and presentation
  hooks/            shared lifecycle/state logic when warranted
  lib/              coherent domain operations and formatting
  styles/           project tokens and global rules
  App.tsx           application composition
```

Use the framework's existing structure and extensions. A component's purpose is a coherent visual/interaction responsibility. Do not split every paragraph into a component or put all business policy into a root page. Shared code belongs where its callers can find its single owner.

### Feature-based frontend

```text
src/
  features/
    catalog/
      components/   catalog-specific views
      model.ts      state and catalog rules
      api.ts        catalog transport boundary
      index.ts      intentional public surface
    account/
      components/
      model.ts
      api.ts
      index.ts
  shared/
    ui/             genuinely shared primitives
    lib/            cross-feature mechanisms
```

Use when features have enough distinct behavior to be maintained independently. Do not let other features import arbitrary internals. Apply the repository's exports/module rules where supported. Avoid broad barrel exports that accidentally make internal state public or create cycles.

### Small backend: route handlers

```text
server/
  routes/           URL/method to handler
  middleware/       authentication and request-level mechanics
  catalog.ts        operation, validation and policy owner
  db.ts             connection/lifecycle boundary
  server.ts         composition and startup
```

Good for a few operations. A handler parses/authenticates, calls a coherent operation, and maps the result. Keep framework plumbing thin; do not force a controller/service/repository chain whose layers merely forward identical arguments.

### Data-driven backend: MVC

```text
server/
  models/           data relationships and storage behavior
  controllers/      use-case coordination and responses
  routes/           routing
  middleware/       request-wide policy/mechanics
  config/           nonsecret configuration definitions
```

Use the project's meaning of each layer. Domain rules must have one owner even when both UI and API use them. A browser may validate for feedback while the server validates the untrusted request; that is two trust boundaries, not wasteful duplication.

### Complex domain with multiple interfaces

```text
server/
  domain/           business model and operations
  infrastructure/   storage and external-service adapters
  interfaces/       HTTP, jobs or other delivery adapters
  composition/      construct and wire concrete dependencies
```

Domain behavior should not need a web framework to express its rules. Depend on the contract a domain operation needs; construct concrete implementations at the composition boundary. Use this when meaningful policy and different interfaces justify it, not because “clean architecture” sounds more production-ready.

### Full-stack relationship

A single deployable app may hold `client/`, `server/` and a narrow `shared/` contract. A framework may co-locate these using its own conventions. Separate API and client projects when multiple consumers, deployment ownership or independent lifecycles justify it. Do not expose server-only modules or secrets through the shared package. Types shared with the browser describe a contract; they do not replace runtime parsing or authorization.

Honor established naming, test locations, build scripts and static-asset paths. `src`, `tests`, `public` and `scripts` are useful conventions, not universal mandates. Do not move an existing project merely to match these diagrams.

### Pick the data-flow pattern by the job

A local UI commonly follows action → authoritative state update → render. A request/response path follows request → parse/authenticate/authorize → operation → storage or integration → response. Its failure branch must return the agreed error rather than leave the caller waiting indefinitely.

Use event-driven work when the operation genuinely needs asynchronous processing: producer → durable queue or event channel → handler → effect. Name who owns the job, when acceptance differs from completion, the retry/idempotency rule, ordering needs, cancellation and the observable failed/dead-letter outcome. Do not report a queued notification as delivered, or add a queue where an ordinary request is sufficient.

Pub-sub is one-to-many delivery: publisher → topic/channel → subscribers. It can suit live updates, chat or collaboration. Define subscription lifetime and cleanup, authorized audience, reconnect/resume or resync behavior, event ordering and what a disconnected subscriber may miss. A transient event stream is not automatically durable storage. Shared state still needs one authoritative owner; subscribers should not each invent competing write policy.

## Design a useful public interface

An interface includes everything a caller must know: input/result types, allowed sequence, invariants, failure modes, configuration, lifetime and relevant performance. Its quality is how much work it hides from callers, not its ratio of implementation lines to exported lines.

Write two realistic caller examples first. For an editor, a useful operation might be “save this permitted catalog edit and return the new version.” A shallow design makes every caller load the record, check tenant/role, validate, compare versions, write and format errors itself. Put coherent policy behind an operation that owns it; keep transport-specific requests/responses at the adapter.

Use this design review:

- Does deleting the module cause important complexity to reappear across callers? If not, it may be a needless pass-through.
- Can one caller complete the job without knowing internal phases or calling methods in a fragile order?
- Is a representation/policy hand-synchronized in several files? Derive it from one owner when possible.
- Can unrelated modules mutate the same state? Prefer one owner; otherwise define real concurrency control.
- Are modules divided by “load/validate/transform/save” while each knows the same domain invariants? Group by the knowledge they protect.
- Is an internal framework/storage/wire type leaking into a public contract?
- Is the abstraction hiding work, or just adding an indirection? Preserve a forwarding boundary when it performs genuine adaptation or policy.

If the shape is genuinely contested, compare alternatives that optimize different needs: fewer entry points, easiest common caller, or an actual second transport. Each must show caller usage, hidden behavior, dependency strategy and tradeoffs. A routine button does not need an architecture tournament. Repeated casts, duplicated special cases, exposed ordering or surprise shared writes are reasons to revisit a sketch during implementation.

### Dependencies and test seams

Test through the operation's real public interface. Keep internal collaborators real unless a specific dependency requires substitution:

- **Pure/in-process:** call it directly with representative inputs; control time/randomness where those affect meaning.
- **Local storage with a supported test substitute:** use an isolated real database/filesystem or appropriate compatible stand-in. State compatibility limits; an in-memory collection cannot prove SQL constraint or transaction behavior.
- **Remote service owned by this application:** inject the needed operation contract, with production transport and an isolated adapter for domain tests. Add integration proof of the actual transport when required.
- **Third-party service:** inject its operation-specific boundary and test success, refusal, malformed response and timeout fixtures. A mock proves local handling, not provider availability or the live contract.

Do not expose every internal seam as public configuration. A second adapter is useful when there is a real substitution need; do not add hypothetical flexibility. An operation-specific interface such as `fetchCatalogPage` or `saveCatalogEdit` is usually easier to reason about than a generic fetcher whose mock contains a second router.

## State ownership and domain shape

Choose the smallest appropriate owner:

- **Local:** disclosure/open state, an unsaved field or transient hover belongs to one component or closure.
- **Lifted:** siblings share one value through their nearest useful owner.
- **URL:** shareable filter, selected page or route state when reload/back/forward should preserve it.
- **Application store/context:** widely shared client state with a clear lifetime and update owner.
- **Server state:** authoritative records, permissions and shared durable writes. A client cache is a view of it, with explicit freshness and invalidation.

Do not copy derived values into independently mutable state. Derive a result count from the current accepted result set; derive “has selection” from the selected ID. Avoid both `isLoading` and `isLoaded` flags that can become simultaneously true.

An illustrative TypeScript model makes useful distinctions explicit:

```typescript
type CatalogItem = {
  id: string;
  title: string;
  category: string;
  version: number;
};

type CatalogView =
  | { kind: "loading"; requestId: number; previous: CatalogItem[] | null }
  | { kind: "ready"; items: CatalogItem[] }
  | { kind: "failed"; message: string; previous: CatalogItem[] | null };

type EditorState =
  | { kind: "closed" }
  | { kind: "editing"; original: CatalogItem; draftTitle: string }
  | { kind: "saving"; original: CatalogItem; draftTitle: string; requestId: string }
  | { kind: "conflict"; draftTitle: string; latest: CatalogItem };
```

These types are a design example, not a complete app or proof. An empty successful collection is still `ready`; its UI can derive the empty presentation. A pending request can preserve previous data without falsely describing it as current. Adding a new variant should lead to an explicit handling decision, using exhaustive matching where the language supports it.

Model semantic IDs or values distinctly when confusing them creates real risk; do not introduce branded types solely for decoration. Derive types from an authoritative schema when the project supports it. External JSON remains unknown until parsed. Do not use a cast to convert malformed data into a trusted model.

### Parse a real boundary

This complete small example illustrates a parser for a title/version edit. It accepts only the two public fields and retains zero as a valid initial version. It does not implement authentication or storage.

```typescript
type EditInput = { title: string; expectedVersion: number };
type ParseEdit =
  | { ok: true; value: EditInput }
  | { ok: false; message: string };

function parseEdit(value: unknown): ParseEdit {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    return { ok: false, message: "Send one edit object." };
  }
  const input = value as Record<string, unknown>;
  if (Object.keys(input).some(key => key !== "title" && key !== "expectedVersion")) {
    return { ok: false, message: "The edit contains an unsupported field." };
  }
  if (typeof input.title !== "string") {
    return { ok: false, message: "Enter a title." };
  }
  const title = input.title.trim();
  if (title.length === 0 || title.length > 160) {
    return { ok: false, message: "Use a title between 1 and 160 characters." };
  }
  const version = input.expectedVersion;
  if (typeof version !== "number" || !Number.isSafeInteger(version) || version < 0) {
    return { ok: false, message: "Reload the item before saving this edit." };
  }
  return { ok: true, value: { title, expectedVersion: version } };
}
```

The length is illustrative product policy, not a universal title limit. JavaScript string length counts UTF-16 code units; choose and test code-point/grapheme limits instead when the accepted requirement is about user-perceived characters. A typed internal operation need not re-parse this same object on every function call. Cross-process, persisted legacy or plugin data may create another boundary that needs validation.

## Data, API and failure contracts

### Data design starts with access patterns

For each entity define keys, ownership, relationships, allowed values, uniqueness, timestamps/versioning where required and deletion/retention behavior. Derive indexes from real filters, joins and ordering. Plan compatibility for existing rows and code; a new migration is not tested merely because the new application boots on an empty database.

A small shared catalog might need an item table keyed by tenant and item, a membership/role source and a version counter. A selected database could express the item fragment as:

```sql
CREATE TABLE catalog_items (
  tenant_id TEXT NOT NULL,
  id TEXT NOT NULL,
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 0 CHECK (version >= 0),
  PRIMARY KEY (tenant_id, id)
);
CREATE INDEX catalog_items_category
  ON catalog_items (tenant_id, category, title, id);
```

This is an illustrative SQLite-compatible fragment, not a complete migration or authorization system. The title limit, collation, foreign keys, timestamps, role source and supported query shape still follow the product/project contract. Validate whether the proposed index helps the actual query plan; extra indexes cost writes and space.

A versioned update can use a conditional write:

```sql
UPDATE catalog_items
SET title = ?, version = version + 1
WHERE tenant_id = ? AND id = ? AND version = ?;
```

Use bound parameters from parsed data and trusted request context. Check affected rows and distinguish stale version, missing object and denied access using the project's privacy policy. Authorization must apply to the operation, with a transaction/consistency strategy appropriate to concurrent role changes. The SQL predicate alone does not prove permission.

### Define each public operation

For an HTTP API or equivalent server action, document:

- Method/path or operation name and its actual consumer
- Parsed path/query/body input, defaults, bounds and rejected fields
- Current authenticated identity, tenant scope and required permission
- Result shape, durable effect and relevant version/consistency guarantee
- Error categories, status/result mapping and safe user message
- Pagination/filter/sort semantics for lists
- Repetition, conflict, cancellation and timeout behavior

An illustrative catalog surface:

- `GET /api/catalog`: bounded list with query/category/sort and cursor; returns items plus the next cursor and the count meaning actually promised.
- `GET /api/catalog/:id`: one authorized detail, with no reliance on whether it appeared in a previous list.
- `PATCH /api/catalog/:id`: validated title and expected version; server-owned identity determines permission; returns the updated record/version on confirmed success.

Do not return a guessed exact total for a paginated result when the API supplies only a page count. Use a stable tie-breaker in pagination ordering. A cursor must preserve the filter/order meaning and be checked as untrusted input. Choose API versioning when an actual compatibility need exists; do not add `/v1` ceremony to an internal endpoint automatically.

### Error and rescue map

For each meaningful boundary, name the trigger, category, recovery and user-visible outcome. A useful response envelope may contain a stable error code, plain message, field details and a nonsecret request ID. Never return stack traces, SQL, credentials or unauthorized object details as user-facing errors.

Distinguish these cases where they exist:

- Invalid input: reject before mutation, retain correctable user work and attach field feedback.
- Unauthenticated: follow the established sign-in/session flow without treating anonymous data as authorized.
- Forbidden/missing: use the product's disclosure policy consistently on list, detail and download paths.
- Conflict: retain the user's draft, retrieve current state and offer the agreed resolution rather than silently overwrite.
- Timeout/disconnect: completion may be unknown; reconcile before retrying a non-idempotent write.
- Rate limit/temporary outage: use allowed bounded recovery and make delayed/unavailable work visible.
- Malformed/empty external response: distinguish schema failure from a valid empty result.
- Partial result: preserve useful accepted data while explaining the unavailable portion.
- AI/provider refusal or invalid structured output: treat each as a distinct result if the product uses it; never turn refusal or invented fields into validated data.

Catch errors where a boundary can add context, translate them or perform useful recovery. Internal programming errors should remain diagnosable; swallowing every exception into an empty success result hides defects. Use structured diagnostics with operation and safe request context, not entire raw payloads. Alerting/runbooks belong to the actual operational scope; a tiny private prototype need not invent an observability platform.

## Concurrency, retry and cache decisions

### Protect invariants across asynchronous work

Single-threaded JavaScript does not make operations atomic across `await`. State the invariant at the consumer/time boundary. For search, “the result belongs to the latest submitted query” may be protected by request identity and cancellation. For shared writes, the server may need transactions, uniqueness constraints, conditional versions or another actual concurrency mechanism.

Prefer separate state for independent actors/experiments before adding locks. When one canonical mutable record is genuinely shared, enforce the ordering structurally. A per-process lock does not coordinate multiple server instances. A UI disabled button does not stop a repeated request or another consumer.

For conflicting operations, test relevant completion orders using controlled pause/release points. After the competing operation completes, resume the paused one and check through a fresh consumer. Exclude an order only when a real mechanism prevents it. An invariant written in a comment is the requirement, not evidence it is met.

### Retry only what the operation permits

Set a bounded deadline that matches the task and surface. Treat timeout, cancellation and confirmed failure separately. Use bounded backoff/jitter for eligible transient failures, respect server retry guidance when provided, and stop for permanent validation/permission failures.

Reads are often safe to repeat; writes require the operation's actual idempotency semantics or a readback that resolves uncertainty. For idempotency keys, define scope (actor/tenant/operation), payload identity, uniqueness/storage lifetime, in-progress handling and repeated-response behavior. Reusing a key with a different payload must not silently replay the first operation. Do not claim exactly-once execution merely because the client sends a key.

Browser abort cancels the client's wait; it may not undo a server mutation. If a request or tool fails after a possible side effect, observe authoritative state before replaying. Keep recovery inside the user's granted scope.

### Cache only when it earns its complexity

Name the cache owner, key, tenant/identity scope, stored representation, size bound, freshness, invalidation and failed-refresh behavior. An incomplete cache key can leak one user's result to another. A local process cache may disagree across instances. A stale-while-refresh UI needs to distinguish stale data from completed current results.

Pick TTL, explicit invalidation or event-driven invalidation from the consistency requirement. For writes, decide which reads are invalidated and what a second consumer must observe. Measure an actual repeated cost before adding a cache. Use pagination or virtualization according to the accepted reading/navigation experience and real data size, not a blanket row-count rule.

## Web trust boundaries

Apply this to the changed surface; it is not a mandate for an unrelated security campaign or a security certification.

Map the actors, valuable data/assets, entry points, tenant boundaries, sensitive operations and external sinks. For every untrusted input, trace which capabilities it can reach. Include browser requests, uploads, webhook bodies, rich text, user-selected URLs and retrieved/model-generated content when present.

- Parse type/shape/size/range at the boundary; reject or deliberately ignore unsupported fields according to the contract. Do not allow mass assignment of role, tenant or ownership.
- Authenticate and authorize on the server for every relevant read/write/download. Check current role and object scope; a UUID or ownership recorded at creation is not permission forever. Inspect denied/error rendering too, so it cannot expose hidden counts, names or navigation.
- Keep credentials and webhook sender secrets server-side. Use the host's supported credential mechanism. Do not include secrets in client code, URLs, screenshots, fixtures or logs.
- Use parameterized SQL. For shell/process work, avoid constructing a command string from input. Validate allowable paths and URL destinations before file or network access; resolve traversal/redirect/SSRF risks at the actual boundary.
- Render ordinary untrusted text as text. If rich HTML is required, use the project's maintained sanitizer and explicit allowed model. Framework escape hatches such as `innerHTML`, `dangerouslySetInnerHTML`, `v-html` or “safe” template flags require separate scrutiny.
- Configure CORS for the actual allowed origins/credential flow. Do not “fix” a browser error by disabling security or indiscriminately allowing credentialed origins. For cookie-authenticated writes, preserve the project's CSRF and cookie protections.
- Validate upload size, content type/content and safe storage naming; do not trust the extension or user path. Use appropriate download headers and separate access checks.
- For webhooks, verify the expected authenticity mechanism, parse the body as data, and define duplicate/replay handling. A success status that only queues work is not proof the downstream action completed.
- For AI/tool features, keep retrieved pages, tool results and model text as untrusted data. Validate tool arguments and permissions at the consequential boundary. A prompt instruction in content cannot authorize extra actions or disclosure.
- Use established authentication/cryptographic libraries. Do not invent password hashing, token generation or secret comparison schemes. Dependency availability and an old advisory are leads; assess actual version, reachable use and impact before calling them a vulnerability.

If a credential appears exposed, preserve redacted location/version evidence and recommend the authorized revocation/rotation response. Removing it from current source or history is not evidence it was revoked. Keep current validity unknown unless there is legitimate evidence; do not call a live provider with the key merely to prove exposure.

A supported finding needs a concrete controlled input, violated boundary, impact and examination of protections. Separate static evidence from a reproduced failure. Use harmless synthetic inputs and isolated roles for authorized checks; do not probe real third-party systems to “prove” a generic pattern.

## Error-diagnosis catalog

Use each row to select a probe under [redesign](../playbooks/redesign.md), not to apply every listed fix. Confirm the actual framework/version and failing path first.

### JavaScript and TypeScript

| Symptom | Inspect and distinguish | Bounded repair and prevention |
| --- | --- | --- |
| Property access on null/undefined | Is data pending, genuinely optional, malformed, or initialized in the wrong order? Inspect the producer and lifecycle. | Model loading/absence explicitly; parse external data. Optional chaining is appropriate for valid absence, but must not hide a required-field defect. |
| String arithmetic or incorrect comparison | Inspect raw form/query types and whether empty input became zero. | Convert once at input, reject invalid/nonfinite values, and use the intended numeric/range semantics. Do not trust `parseInt` to reject trailing text when strict input is required. |
| Promise where a value is expected | Trace who owns awaiting, returning, error handling and cancellation. | Await where the result is needed, return a promise when the caller owns it, or use an explicit handled continuation. Calling async code does not require every caller to be declared async. |
| Unhandled rejection or silent async failure | Check detached tasks and callbacks whose promises the framework does not await. | Connect the task's result/error to an owner; use the framework's actual async contract. Do not add an empty catch. |
| Wrong loop/callback value | Check closure lifetime, mutable bindings and callback order. | Use appropriate block-scoped values or explicit captured data; test the actual asynchronous order. A blanket `var` replacement alone does not prove repair. |
| Duplicate listeners or increasing memory | Count lifecycle setup/cleanup and listener identity across mount/unmount or route changes. | Remove the same listener, observer, subscription or timer at its owned teardown. Use a repeat-use check to show the retained resources stop growing. |
| Type error “fixed” by a cast | Trace the origin and whether the model admits invalid combinations. | Parse/narrow or correct the domain shape. A cast can express a justified local fact but cannot validate external data. |

### React and similar reactive UIs

| Symptom | Inspect and distinguish | Bounded repair and prevention |
| --- | --- | --- |
| Too many renders or effect loop | Look for state updates during render, unstable dependencies and effects that update the state they watch. | Derive values during render when possible; move effects to the correct lifecycle, stabilize the meaningful dependency, and preserve actual dependencies rather than suppressing warnings. |
| Stale state in callback | Determine whether the callback should use the event-time value or latest value. | Use a functional update when deriving from previous state, appropriate dependencies, or a deliberate ref for latest external access. Do not indiscriminately move all state to refs. |
| Wrong item retains input after reordering | Inspect list keys and identity versus array position. | Use a stable unique domain key; verify reorder/filter/insertion preserves the intended item state. |
| Old request overwrites new results | Compare request/query identity and completion order. | Cancel when supported and/or guard result acceptance by current identity. Debounce alone does not prevent this race. |
| Hydration mismatch | Compare server/client inputs, time/randomness, locale, browser-only values and invalid markup. | Make the initial render consistent, then use the correct client boundary. Do not hide every warning without fixing the differing source. |
| Data disappears across pages or duplicate notifications | Inspect provider lifetime, duplicate mounts, effect replay and local versus shared state. | Place the actual owner at the required lifetime and make subscriptions/events idempotent where needed. Development double-invoke is useful evidence of a lifecycle bug, not a reason to disable safeguards. |
| Deep prop threading | Determine whether state is genuinely cross-cutting or composition is awkward. | Lift/combine components or use existing context/store for a real shared owner. A new global store is not the automatic cure. |

### Python-backed web services

| Symptom | Inspect and distinguish | Bounded repair and prevention |
| --- | --- | --- |
| Indentation/syntax error | Read the exact parser location and surrounding block; check tabs/spaces. | Correct syntax and run the project's parser/linter. Text delimiter counts are not a Python parse. |
| List/dict content persists unexpectedly between calls | Check mutable default arguments or module state. | Use `None` and create a new value only when the argument is `None`; avoid `items or []` when an intentionally supplied empty container must retain identity. |
| Module not found | Check interpreter, virtual environment, module path, declared dependency and filename shadowing. | Use the intended environment or correct the import. A missing package does not automatically authorize installation. |
| Off-by-one result | Inspect inclusive/exclusive boundary and indexing convention using first/last/empty cases. | Correct the range or prefer direct iteration/enumeration where appropriate. Keep the regression on the meaningful boundary. |
| Missing file or leaked handle | Check resolved path, working directory, permissions and ownership/lifetime. | Use safe path construction and context managers; preserve the distinction between absent, denied and invalid paths. Do not mask every error as “file not found.” |
| Event loop blocked | Check synchronous I/O/CPU work inside async handlers with an actual timing/profile. | Use the framework's supported offload/async path or redesign the heavy operation. Declaring a function async does not make blocking work concurrent. |

### Network, browser and API boundaries

| Symptom | Inspect and distinguish | Bounded repair and prevention |
| --- | --- | --- |
| Browser CORS failure | Inspect origin, preflight, server headers, credentials and whether the response itself is an auth/error page. | Correct the owned server/proxy configuration for intended origins. Do not use `no-cors` to pretend an unreadable response is a working API. |
| Connection refused/timeout | Check server readiness, address/port, network route, actual deadline and request size. | Repair the correct environment or slow path; use eligible bounded recovery. Neither a stopped dev server nor unavailable credentials is automatically a product defect. |
| HTTP error appears as success | Check whether the client evaluates HTTP status before parsing and whether response shape matches its expectation. | Map status/domain error deliberately. `fetch` resolving does not mean an HTTP request succeeded. |
| 404 versus routing problem | Compare requested path, base path, API route, SPA fallback and direct reload behavior. | Correct path/deployment routing; do not route every missing API request to HTML. |
| 401/403 or redirect loop | Inspect session/cookie scope, expiry, callback/state validation, proxy scheme and current permission. | Fix the owned configuration or code while preserving access controls. Do not copy a user's live cookies into another runtime. |
| Save uncertain after lost connection | Look for request acceptance, transaction/result identity and a fresh public read. | Reconcile completion first; retry only with the operation's safe repetition contract. Do not blindly replay a mutation. |

### Database and shared state

| Symptom | Inspect and distinguish | Bounded repair and prevention |
| --- | --- | --- |
| Many similar queries per page | Inspect real query count and relationships under the target dataset. | Batch/join/preload the relevant relation without changing authorization or result semantics. Check the query shape and returned data after repair. |
| Slow filter/sort | Read the query plan, cardinality, selectivity and existing indexes. | Add/change an index or query when evidence supports it. Indexing every WHERE column blindly can waste space and hurt writes. |
| Unsafe SQL concatenation | Trace which input reaches which SQL position. | Use parameters for values and a strict allowlist for identifiers/order clauses where binding cannot apply. |
| Too many connections | Inspect leaks, transaction lifetime, pool settings, number of processes and database limits. | Use the database/runtime-appropriate lifecycle or pool. Embedded/serverless/managed drivers differ; “always pool” is not a universal remedy. |
| Lost update or duplicate write | Reproduce overlapping requests and inspect transaction/uniqueness/version boundaries. | Enforce the needed invariant with actual storage semantics. A local lock or disabled button does not protect all writers. |
| Old data survives successful save | Inspect cache keys, transaction commit, replica lag and which source the reader used. | Apply the agreed consistency/invalidation policy; do not claim the write failed solely from a stale cache. |
| Migration works only on empty database | Inspect old rows, defaults/backfill, locks and mixed-version readers. | Test the migration on representative isolated prior data and define compatibility/rollback limits before real application. |

## Conditional component and library guidance

Start with task fit and installed dependencies. An adequate project primitive beats churn. Check current official documentation, compatibility, license and actual version before implementing a new library/API; these are source-derived examples of categories, not a mandatory current recommendation list.

- Accessible unstyled primitives: Base UI or the project's existing equivalent; verify the actual dialog/menu/focus behavior in context.
- Command palette: cmdk; toast feedback: Sonner; one-time-code input: input-otp.
- Interactive parameter panels: Leva or dialkit when a real editor/demo needs them.
- Springs/layout/exit/gestures: Motion when CSS/WAAPI cannot cheaply meet the required behavior. A fade does not need a new animation dependency.
- Animated values/text: NumberFlow or torph when motion serves the content; do not animate essential data simply to decorate it.
- Specialized visual output: Cobe for a globe, Satori for generated social images, Shiki for syntax highlighting, only for the requested capability.
- Streaming charts versus general charts: Liveline and Recharts illustrate different workloads. Choose based on data, interaction and accessibility needs.
- Drag/drop and large-list rendering: dnd kit and Virtuoso are examples; preserve keyboard/click alternatives and the accepted pagination/navigation behavior.
- Shared client state: Zustand is one option when local/lifted state no longer suffices.
- Conditional classes, variant APIs and theme: clsx, cva and next-themes respectively illustrate distinct jobs. Do not add all three for a simple component.

### When the project uses Sonner

Inspect its actual version before copying API names or defaults. Keep a single root toaster unless intentional multiple targets are part of the design. Invoke toast feedback from the client result/event path; a server action should return its result to that client owner. Duplicate mounts or development effect replay can explain double notifications.

Choose a plain/typed message for a completed outcome, a loading message updated by stable ID for manually managed work, a promise-bound toast for a promise that actually settles, and an action/custom surface only for the real interaction. Update an existing operation's toast rather than stack duplicates. Distinguish user dismissal from auto-close callbacks. Multiple toaster instances need explicit targeting according to the installed API.

Use defaults first, then the supported styling/parts API, then a headless design-system component when customization genuinely warrants it. Inspect the actual cascade before adding blanket `!important`. Diagnose missing theme wiring, lost injected styles, Shadow DOM placement, ancestor stacking contexts, portal position and mobile offsets. Do not create an app-wide toast wrapper for a page that needs no toast. Critical validation or failure information must remain accessible beyond transient notification lifetime.

## Explain and verify the right thing

Translate the mechanism plainly: what the user observed, what evidence supports the cause, what changed, and what actual check now succeeds. “The older response replaced the newer search” is more useful than a raw stack trace. Preserve diagnostic details in the appropriate artifact when needed, redacting secrets rather than hiding material uncertainty.

Use project-native parser, lint, type, build and test tools for their actual purpose. Pattern searches can locate suspicious SQL, `innerHTML`, long functions or debug statements; they cannot prove exploitability, undefined-variable correctness, type safety, architecture compliance or absence of defects. Unsupported languages/tools and unrun checks remain explicit. [Verify](../playbooks/verify.md) determines the separate technical, functional and visual verdicts from current evidence.
