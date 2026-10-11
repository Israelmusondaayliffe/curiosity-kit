# Matt: setup-pre-commit

Source status: frozen miscellaneous. Use only inside the explicitly selected Matt library. Before first action, apply [the host contract](../references/host-contract.md).

Set up a staged formatting gate followed by whole-project typecheck and tests. Preserve the existing repository’s workflow and user-owned dirty state. Merely choosing this method is not permission to install packages, alter unrelated settings or commit.

## 1. Inspect and choose the manager

Apply the host’s safe Git-read protocol first. Require a real Git repository and `package.json`; otherwise report what is missing and stop setup. Inspect `packageManager`, installed tool versions, lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`, `bun.lockb`), current hooks, `prepare`, lint-staged sources and all Prettier configuration forms, including package.json. Resolve conflicting manager signals instead of choosing arbitrarily. Where no signal exists, propose npm explicitly.

Record the relevant HEAD/index/staged/unstaged/untracked state under the host preservation contract. Inspect `core.hooksPath` without replacing another hook system. Determine whether Husky and lint-staged already exist and how their installed versions work.

## 2. Prepare dependencies and initialization

The intended devDependencies are `husky`, `lint-staged` and `prettier`. Reuse compatible installed packages; otherwise request or apply existing specific installation authority using the selected manager. Do not use a runner that silently fetches an absent tool. Without the dependency or authority, deliver a precise readiness plan and leave runtime proof unrun.

For a new compatible Husky setup, its initializer can create `.husky/` and a `prepare` script. Inspect its effects before using it: do not run an initializer over existing hooks/scripts if it would replace them. Merge Husky preparation with the existing `prepare` behavior using a supported sequence, preserving failure propagation. Do not replace `prepare` with just `husky` when it already does other work.

## 3. Merge the gate

Create or update `.husky/pre-commit` in the installed version’s supported format. Preserve existing commands and their intended order; explain conflicts before changing semantics. Husky v9+ source examples omit a shebang, but actual version/platform conventions govern executable mode and invocation.

The new quality sequence is:

1. Local lint-staged (staged-only Prettier).
2. Existing `typecheck` script, if present.
3. Existing `test` script, if present.

Use the selected manager consistently for local binaries and scripts, rather than hardcoding `npx`. Ensure a failing step aborts the hook (for example, an explicit `set -e` or a correctly chained sequence supported by the actual shell). Omit absent typecheck/test commands and disclose each omission; do not invent scripts or call an unconfigured test runner.

Merge this lint-staged behavior into its existing canonical configuration, avoiding overlapping conflicting format jobs:

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

Unknown file types are skipped. Formatting mutates staged files; inspect lint-staged’s version and partially staged handling before any real invocation. Preserve existing custom lint tasks and ensure each intended file has a coherent order of operations.

## 4. Prettier defaults only if genuinely absent

Inspect all supported configuration locations before creating a config. Existing preferences win. For a new `.prettierrc`:

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

## 5. Verify without consuming user work

Check hook existence/executable requirements, merged prepare behavior, canonical lint-staged configuration and resolved Prettier config. Prefer an isolated disposable repository with representative staged, partially staged, unstaged and unknown-type files. Verify formatting touches only the intended staged surface, unrelated unstaged bytes survive, then typecheck and tests run in order. Inject a controlled failure to prove the gate aborts. Restore only owned fixture changes. A static config review is not proof that a native hook ran.

Never run lint-staged on a user’s real staged work as a casual smoke test. Such an invocation needs the actual write scope and preservation strategy. Avoid concurrent index/stash operations. Report dependency or host limitations as unrun checks.

## 6. Optional commit smoke test

An actual commit can prove the hook is wired only when a commit is authorized. In a disposable test repository it may be part of the approved isolated test. In a real repo, stage only verified setup-owned paths/hunks and preserve pre-existing staged work; never `git add .` or stage everything. Suggested message: `Add pre-commit hooks (husky + lint-staged + prettier)`. If committing is not authorized, leave the reviewed setup changes and report the unperformed native commit test.

Deliver the actual files changed, manager/version, commands/checks observed, preserved existing behavior, missing quality scripts and any remaining CI or native-hook limits.
