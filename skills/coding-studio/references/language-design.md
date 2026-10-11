# Language and interface design

Load this when domain meaning, state ownership or caller friction affects the change. It is a design method, not a repository-wide style policy. Follow the project's actual language, compatibility promises and conventions. Use [the host contract](host-contract.md) for shared authority and verification rules.

## Start with the callers

1. Write two realistic usage examples before designing a new abstraction. Include an ordinary success path and a meaningful error, retry or cancellation path. Inspect existing callers first if the interface already exists.
2. List what a caller must know: ordering, lifecycle, error meaning, configuration, performance and ownership. An interface includes those promises as well as parameter and return types.
3. Identify the domain state and its writer. Multiple adapters may read one model; multiple competing owners of the same invariant need a reason. Prefer deriving indexes or lists from one source over hand-synchronizing copies.
4. Put transport parsing at the real trust boundary. Convert external data into the project model once, then use that model internally. Keep validation where new untrusted data can still enter. A type assertion is not runtime validation.
5. Ask what complexity the abstraction hides. A useful module gives callers a small contract while owning substantial behavior. If deleting a wrapper removes no complexity, inspect whether the wrapper earns its maintenance cost. If deleting it spreads tricky rules across callers, that is evidence to keep or deepen it.

For an expensive unresolved decision, compare genuinely different priorities. One design might own retries and ordering inside a service; another might expose a transaction for the caller to compose. Show usage, hidden behavior, dependencies and trade-offs before choosing. Do not require a panel or multiple designs for an established mechanical change.

Example: a report API returning transport pages makes every caller repeat pagination, retries and duplicate handling. A report reader may reasonably own those rules and expose a bounded result or stream. But if callers need partial progress or cancellation, hiding everything behind a single uninterruptible promise makes the interface worse. Decide using real usage and failure behavior.

## Name the domain accurately

When one word means different things to different callers, identify the concrete distinction before renaming code. Use actual business rules and examples. Record a consequential settled distinction in the project's existing glossary or decision record only within the permitted edit scope.

A good domain type prevents a meaningful mistake or carries a needed rule. It need not wrap every string. Decide whether a value is:

- an identity that must not be confused with another identity;
- a validated quantity with units and bounds;
- an entity with a lifecycle and owner;
- an external transport representation awaiting validation;
- a computed view that should not become a second mutable authority.

Use a state machine, registry, index or plain value according to the invariant and access pattern. Do not replace a simple record with a framework because the vocabulary sounds more formal.

## TypeScript examples and limits

The examples below are illustrative. Adapt names and error conventions to the project. They are not claims that a compiler or test has run.

### Distinct identities at a boundary

When confusing customer and invoice IDs is a real risk, opaque types can make the mistake visible to the compiler. Keep creation narrow and validate external values before constructing them.

```ts
declare const customerIdTag: unique symbol;
declare const invoiceIdTag: unique symbol;
type CustomerId = string & { readonly [customerIdTag]: true };
type InvoiceId = string & { readonly [invoiceIdTag]: true };

function parseCustomerId(raw: unknown): CustomerId {
  if (typeof raw !== "string" || !/^cus_[a-z0-9]+$/.test(raw)) {
    throw new Error("Invalid customer ID");
  }
  return raw as CustomerId;
}
```

The format is only an example. Use the actual domain's validity rules. A brand prevents some accidental substitutions at compile time; it proves neither that the ID exists nor that the caller may access it. Those remain runtime checks. Avoid public unchecked constructors that undo the distinction.

### Represent mutually exclusive states explicitly

Independent booleans allow impossible combinations such as both loading and failed with stale success data. A discriminated union can express the states the user or caller must handle.

```ts
type ExportState =
  | { readonly kind: "idle" }
  | { readonly kind: "running"; readonly completedRows: number }
  | { readonly kind: "ready"; readonly artifactId: string }
  | { readonly kind: "failed"; readonly reason: string; readonly retryable: boolean };

function label(state: ExportState): string {
  switch (state.kind) {
    case "idle": return "Ready to export";
    case "running": return `Exported ${state.completedRows} rows`;
    case "ready": return "Export ready";
    case "failed": return state.reason;
    default: return unreachable(state);
  }
}

function unreachable(value: never): never {
  throw new Error("Unexpected export state");
}
```

This models a snapshot, not legal transitions, concurrency or authorization. A transition function or owning service still has to reject invalid moves. Validate decoded persisted state; TypeScript types disappear at runtime. Test retry after a partial effect and stale concurrent updates where those risks exist.

### Numeric invariants require construction checks

A start plus a plain numeric duration still permits negative durations, NaN and infinity. If milliseconds must be finite and nonnegative, establish that invariant at construction.

```ts
declare const millisecondsTag: unique symbol;
type Milliseconds = number & { readonly [millisecondsTag]: true };

function milliseconds(raw: number): Milliseconds {
  if (!Number.isFinite(raw) || raw < 0) {
    throw new Error("Duration must be finite and nonnegative");
  }
  return raw as Milliseconds;
}
```

Specify integer bounds or maximum safe values if the downstream operation requires them. Arithmetic can invalidate a checked value or overflow; validate the result where needed. Check units at external boundaries. Do not claim that changing the representation alone enforced the rule.

### Readonly communicates an ownership boundary

Use readonly inputs when a function should inspect data without changing the caller's collection. Copy only when the function needs its own mutable state.

```ts
type Line = { readonly quantity: number; readonly unitPriceCents: number };
function totalCents(lines: readonly Line[]): number {
  return lines.reduce((sum, line) => sum + line.quantity * line.unitPriceCents, 0);
}
```

Readonly is compile-time and generally shallow. It does not freeze objects, prevent changes through aliases or make a computation thread-safe. This example also does not validate quantity, currency consistency, overflow or rounding. Add the checks the actual contract needs; avoid pretending the annotation supplies them. Local mutation can be clear and safe when one owner contains it.

## Keep boundaries useful

Separate internal computation, replaceable local dependencies, services the team owns and real third parties. Test the behavior at the appropriate boundary:

- Pure domain logic can use small deterministic examples and properties.
- Persistence should use a disposable real implementation where its semantics matter.
- Owned remote services need their agreed contract and relevant integration evidence.
- Third parties may need a controlled fake for local tests plus separately authorized real integration verification.

Mocking a third party is not proof that its real service works. Forcing every internal collaborator behind an adapter can make tests less representative. The needed boundary follows substitution, failure and ownership concerns, not a universal adapter count.

Expose package entry points intentionally. Check whether callers import internals, whether tests rely on private implementation, and whether cycles conceal shared ownership. A project may need import enforcement, but installing a boundary checker or adding global lint rules is a separate scoped change. If enforcement is introduced, exercise app importers as well as package importers, aliases, legitimate local tests and each forbidden path. A configuration file that names a rule is not evidence that the rule catches a violation.

## Review and verify the design

Before accepting a structural change, inspect:

- a caller that previously duplicated the rule and a caller with an unusual failure path;
- serialization formats, stored data and consumers outside the primary language;
- teardown, cancellation and repeated calls;
- whether the chosen module actually owns the invariant it claims to own;
- whether transport details or hidden mutable state leaked into more callers;
- whether independent implementation steps need the same workaround repeatedly.

Repeated workarounds may expose a wrong boundary. Revisit it rather than adding another wrapper. Preserve existing tests until replacement coverage demonstrably protects the same accepted behavior. A cleaner internal shape cannot silently change a public contract or erase a regression.

Return the selected contract, representative usage, state owner, rejected alternative and reason, compatibility implications and actual verification evidence. Do not turn a local design lesson into a global ban on classes, mutation, comments, exceptions or a particular framework.

## Explain a constraint before removing it

For a puzzling boundary, inspect the relevant source history, ADR, test and available issue or PR context. Separate current behavior from the author's stated reason. Label support as directly recorded, supported by several observations, inferred, speculative or unknown. Record contradictory evidence and meaningful empty searches rather than inventing intent.

Return what to preserve, what can change, what to avoid and what risk remains. Before deleting a seemingly dead path, check dynamic consumers, generated code, persisted formats, reflection or configuration, external clients and compatibility promises where relevant. Text-search absence alone is not proof of no caller.

When a deliberate compromise is accepted, name its owner, concrete ceiling and upgrade trigger. For example, a single-process in-memory index may be adequate for the approved read-only prototype up to its measured dataset bound. A second writer, persistence requirement or exceeded bound triggers redesign. Do not silently carry that prototype compromise into a shared production service, and do not add a distributed framework before the trigger exists.

## Add a project import-boundary check when requested

Use this for a TypeScript project with agreed public/private boundaries that currently lack enforcement. The result is a working project check, not a universal dependency or another style manifesto.

1. Read current package exports, TypeScript path aliases, build/test configuration and existing lint or dependency-analysis tools. State each intended allowed and forbidden dependency, including cycles, internal imports and any justified test-only exception. Do not infer the rules solely from today's import graph.
2. Prefer the existing installed checker if it resolves the project's actual module forms. Configure only the agreed boundaries. If no adequate tool exists, propose the smallest supported addition and observe installation authority; do not invent an available binary or claim enforcement from a source grep.
3. Put valid and deliberately invalid imports in a disposable copy or owned fixture area. Exercise every configured rule independently: valid public import, forbidden private import, cross-package alias, relative-path alternative and a cycle where cycles are forbidden. Include both application and package consumers when both exist. If the agreed boundaries cover tests, also prove that a test cannot bypass its package's public entrypoint and that another package cannot import the package's test directory; keep any deliberate local-test exception explicit. The intended violation must cause a nonzero result identifying the offending edge; a parser or missing-module error is not that proof.
4. Remove each planted violation and confirm the restored fixture passes. Run the check on the real scoped project and distinguish existing violations from new ones using actual baseline evidence. Do not suppress violations globally just to get a green result.
5. Wire the verified command into an existing requested check or CI stage only within the task's scope. Preserve current hooks and unrelated settings. Return the changed configuration, exact command, rule-by-rule observed results and limitations such as dynamic imports the tool cannot resolve.

For example, a project may allow `app` to import `payments` through its public export while forbidding `app` from importing `payments/internal/*`. A test must demonstrate both the allowed export and the rejected internal edge after alias resolution. Naming that pattern in JSON alone is not the feature. No fixed four- or five-rule count overrides the project's actual contract.
