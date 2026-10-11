# Matt: migrate-to-shoehorn

Source status: frozen miscellaneous. Use only inside the explicitly selected Matt library. Before first action, apply [the host contract](../references/host-contract.md).

# Migrate to Shoehorn

## Why shoehorn?

`shoehorn` lets you pass partial data in tests while keeping TypeScript happy. It offers helpers for expressing the intent of test fixtures. These are TypeScript conveniences, not runtime validation; `fromAny` deliberately permits invalid data.

**Test code only.** Never use shoehorn in production code.

Problems with `as` in tests:

- Assertions can hide which test-fixture compromise is intentional
- Must manually specify target type
- Double-as (`as unknown as Type`) for intentionally wrong data

## Install

Inspect the repository’s manager, lockfile and installed version first. The intended placement is a devDependency because this method is test-only. Install with the detected manager only under actual installation authority; reuse a compatible dependency when present. Inspect the installed/exported API before migrating, because contextual inference and helper signatures are version-dependent. An unavailable dependency leaves typecheck/runtime verification unrun.

## Migration patterns

### Large objects with few needed properties

Before:

```ts
type Request = {
  body: { id: string };
  headers: Record<string, string>;
  cookies: Record<string, string>;
  // ...20 more properties
};

it("gets user by id", () => {
  // Only care about body.id but must fake entire Request
  getUser({
    body: { id: "123" },
    headers: {},
    cookies: {},
    // ...fake all 20 properties
  });
});
```

After:

```ts
import { fromPartial } from "@total-typescript/shoehorn";

it("gets user by id", () => {
  getUser(
    fromPartial({
      body: { id: "123" },
    }),
  );
});
```

### `as Type` → `fromPartial()`

Before:

```ts
getUser({ body: { id: "123" } } as Request);
```

After:

```ts
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));
```

### `as unknown as Type` → `fromAny()`

Before:

```ts
getUser({ body: { id: 123 } } as unknown as Request); // wrong type on purpose
```

After:

```ts
import { fromAny } from "@total-typescript/shoehorn";

getUser(fromAny({ body: { id: 123 } }));
```

## When to use each

| Function        | Use case                                           |
| --------------- | -------------------------------------------------- |
| `fromPartial()` | Pass partial data that still type-checks           |
| `fromAny()`     | Pass intentionally wrong data (keeps autocomplete) |
| `fromExact()`   | Force full object (swap with fromPartial later)    |

## Workflow

1. **Gather requirements.** Reuse supplied scope; ask which tests/fixture builders are affected, whether large objects need only a few properties and which negative tests intentionally pass invalid input. Keep production code outside the migration.
2. **Inspect real test boundaries.** Use repository conventions and configuration to identify tests, including TSX, helpers, generics, lowercase aliases and multiline assertions. A grep for ` as [A-Z]` in only `.test.ts`/`.spec.ts` files is incomplete; search is a candidate finder, not a rewrite decision. Read each candidate in context.
3. **Choose by meaning.** An incomplete otherwise valid fixture usually calls for `fromPartial`; an intentionally wrong type may call for `fromAny`; a deliberately complete fixture calls for `fromExact`. Preserve `as const`, narrowing, branded types and ordinary assertions where these helpers do not express the same intent. Never classify solely by single versus double cast.
4. **Migrate one representative case first.** Add or merge the exact helper imports once; exploit contextual inference only where the installed API supports it. Retain properties the behavior actually reads. Preserve the intentionally invalid field/value in negative tests. For a complete fixture, a contextual `fromExact({ ...allRequiredFields })` must still include its required shape; do not weaken it just to silence an error.
5. **Check and expand.** Run the authorized typecheck and relevant behavioral tests against the real installed package. Confirm inference, test intent and expected failures remain correct. Then migrate other reviewed cases in scope, deduplicating imports and keeping lockfiles consistent. Missing tools produce a precise blocked verification step, not a claim of success.
6. **Inspect the final diff.** Verify production files are unchanged, ordinary casts were not swept up, incomplete and invalid fixtures remain semantically different and unrelated user edits survived. Report files/cases migrated, actual checks and deferred candidates with reasons. No blanket stage or publication.
