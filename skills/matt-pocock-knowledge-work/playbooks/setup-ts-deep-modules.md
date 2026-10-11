# Matt: setup-ts-deep-modules

Source status: beta / experimental. Use only inside the explicitly selected Matt library. Before first action, apply [the host contract](../references/host-contract.md).

Make package boundaries visible and mechanically checkable in an explicitly selected TypeScript repository. First read [codebase-design](codebase-design.md) for deep module, interface, seam and depth. A deep module offers substantial behavior through a small interface.

## Shape and rules

```text
src/packages/
  example/
    index.ts           public entry point
    client.ts          another public entry point
    lib/impl.ts        private implementation
    tests/example.test.ts
    tests/fixtures.ts
```

Packages are flat immediate children of the chosen packages root. Every root file is public; every subfolder is private, with arbitrary nesting allowed inside it. `lib/` and `tests/` are conventions, not the only protected folders. Prefer several small entry points over a giant barrel re-exporting an entire subtree. Interface boundaries govern **how** packages import; optional layering governs **which** packages may depend on which and remains separate.

The supplied config contains **five actual forbidden rules**, all errors:

1. `entrypoint-boundary-from-app`: app/root code outside packages can reach only package-root files.
2. `entrypoint-boundary-across-packages`: non-test package code can use its own internals, but only another package’s root files.
3. `tests-through-entrypoints`: package tests exercise all packages, including their own, through root files; own test fixtures are allowed, other packages’ private subfolders are not.
4. `tests-folder-is-private`: non-test code, even in the same package, cannot import package test files or fixtures.
5. `no-circular`: no cycles across the scanned graph.

Thus intra-package freedom is qualified by the test-isolation rules. Dependency-cruiser capture-group backreferences preserve same-package exceptions; verify their support in the installed version instead of flattening the rules per package.

## Seven phases

### 1. Inspect the repository

Apply the host’s safe Git-read protocol before repository inspection. Identify the workspace root, package manager/version (packageManager field plus lockfiles; include modern `bun.lock` and legacy `bun.lockb`), current scripts and configs. Multiple inconsistent lockfiles need a resolved manager choice. Prefer an established packages root; absent a convention, propose `src/packages` when `src/` exists, otherwise `packages`. Confirm unconventional existing layout before imposing a new one. Inspect all app/source importer roots and actual TS configs/resolution mode.

Find existing `.dependency-cruiser.*`, package-folder README, agent instruction files and example directories. Plan a merge, not replacement. Done when manager, paths, scan coverage and preserved configuration are known.

### 2. Resolve dependency readiness

Use installed dependency-cruiser if suitable. If missing, propose installation as a **devDependency** with the detected manager under the host contract. Inspect the actual supported API/version before execution. Without installation authority or dependency access, prepare the configuration and exact blocked next operation, leaving native validation unrun. No unqualified enforcement claim is possible.

### 3. Merge the configuration

Read [dependency-cruiser.config.cjs](../resources/setup-ts-deep-modules/dependency-cruiser.config.cjs). Set its package root; the template escapes regex metacharacters in the configured root. Preserve five rule identities, `$1` same-package exceptions, optional layering stub and existing unrelated rules/options. Use `.cjs` for CommonJS even when package type is module. Reconcile the template’s `tsconfig.json` with the repository’s real config; remove or select that option deliberately when necessary. The boundaries are path-depth based, but actual extension and resolver support are version-dependent: merge required `.ts`, `.tsx`, `.js`, `.jsx`, `.json`, and applicable modern module extensions only when supported.

Done when the actual config has correct paths and all five rules, with no unrelated config loss.

### 4. Wire full-graph checks

Add `lint:boundaries` using the installed local `depcruise` and actual config path. Scan packages **and app importers**: `depcruise src` works only when all relevant sources live under `src`; otherwise supply each verified source root. Scanning packages alone cannot prove app boundary coverage. Exclude generated/vendor trees deliberately.

Merge the boundary check into the existing umbrella command that runs typecheck, preserving its order/behavior. If no umbrella exists, add a standalone script and report CI integration still pending; do not falsely require or claim an umbrella that the allowed branch lacks. Do not change tsconfig or add path aliases as a side effect.

### 5. Scaffold a non-destructive example

Use a new noncolliding example path or merge a specifically approved existing one. Root `index.ts` exports behavior implemented in `lib/impl.ts`; `tests/example.test.ts` uses only `../index`. Match the existing test runner and conventions. Include meaningful behavior/assertions, not a pointless forwarding wrapper. Tell the user this is a copy-or-remove starter. Creating it does not authorize staging or committing it.

### 6. Prove pass → fail → pass

Run authorized checks in isolated fixtures or carefully scoped owned files. Observe a clean pass, introduce a known internal import from the example test, observe `tests-through-entrypoints` fail, restore only that owned change and observe another pass. Static inspection cannot substitute for this observed red proof.

Also exercise the distinct rules: clean root and multiple-entry imports; legal own internals; app deep import; cross-package deep import; own-test deep import; another package’s test fixture; non-test import of own tests; legal own test fixture; arbitrary private folder; cycle. Each negative must fail for its expected rule, not a missing-file or unrelated resolver error. Include an app importer in the actual scan. Use a package root containing regex punctuation in an isolated check. Preserve test evidence and remove only injected violations. Dependency unavailable means native positives remain unrun, with readiness/blocker reported.

### 7. Document and deliver

Merge a package-local README beside the packages: layout snippet, root-entry rule, qualified internal freedom, test isolation, no cycles, how to run checks and explicit discouragement of giant barrels. Explain all five actual rules even if grouped into four conceptual paragraphs. Add one concise context pointer in the actual host's active instruction file, using [setup's host-selection rule](setup-matt-pocock-skills.md#4-write); do not substitute a file the host does not read or create a competing authority. Preserve unrelated instructions and existing custom pointers.

Report paths, installed/configured versus verified state, actual pass/fail/pass evidence, CI wiring or pending standalone integration and any unresolved version/resolution limits. Commit only if separately authorized with exact scoped paths; preserve unrelated index and working-tree content.
