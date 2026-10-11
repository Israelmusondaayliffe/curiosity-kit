# Matt: scaffold-exercises

Source status: frozen miscellaneous. Use only inside the explicitly selected Matt library. Before first action, apply [the host contract](../references/host-contract.md).

# Scaffold Exercises

Create course directory structures using the actual repository conventions and requested content. Inspect the installed course linter before invoking it; `pnpm ai-hero-cli internal lint` is the source-specific command, not a universally available tool. Static conformance does not prove a linter pass. Commit only when separately authorized.

## Directory naming

- **Sections**: `XX-section-name/` inside `exercises/` (e.g., `01-retrieval-skill-building`)
- **Exercises**: `XX.YY-exercise-name/` inside a section (e.g., `01.03-retrieval-with-bm25`)
- Section number = `XX`, exercise number = `XX.YY`
- Names are dash-case (lowercase, hyphens)

## Exercise variants

Each exercise needs at least one of these subfolders:

- `problem/` - student workspace with TODOs
- `solution/` - reference implementation
- `explainer/` - conceptual material, no TODOs

When stubbing, default to `explainer/` unless the plan specifies otherwise. The source’s broad variant list permits solution-only in prose, but its stricter lint summary requires a primary `problem/`, `explainer/` or supported `explainer.1/`. Default to that stricter shape; inspect the actual linter/version before accepting a solution-only plan.

## Required files

Each subfolder (`problem/`, `solution/`, `explainer/`) needs a `readme.md` that:

- Is **not empty** (must have real content, even a single title line works)
- Has no broken links

When stubbing, create a minimal readme with a title and a description:

```md
# Exercise Title

Description here
```

If the subfolder has code, it also needs a `main.ts` (>1 line). A code-bearing `main.ts` must be meaningful and more than one line, not padding to satisfy lint. For stubs, a readme-only exercise is fine.

## Workflow

1. **Parse the plan** - extract section names, exercise names, variant types and requested exercise content. Inspect existing paths, numbering, links and user edits. Resolve collisions without overwriting content. A request for substantive exercises needs actual learner tasks and meaningful solutions; title-only files are honestly labeled scaffolds.
2. **Create directories** - `mkdir -p` for each path
3. **Create stub readmes** - one `readme.md` per variant folder with a title and useful description, or full requested content when authoring rather than stubbing
4. **Run lint** - use the verified installed equivalent of `pnpm ai-hero-cli internal lint` when execution is authorized; if absent, report native validation blocked without fetching/installing implicitly
5. **Fix any errors** - iterate on owned output until the actual linter passes, then check links and required files. If blocked, retain the precise errors and report partial scaffolding rather than claiming a pass.

## Lint rules summary

The linter (`pnpm ai-hero-cli internal lint`) checks:

- Each exercise has subfolders (`problem/`, `solution/`, `explainer/`)
- At least one of `problem/`, `explainer/`, or `explainer.1/` exists
- `readme.md` exists and is non-empty in the primary subfolder
- No `.gitkeep` files
- No `speaker-notes.md` files
- No broken links in readmes
- No `pnpm run exercise` commands in readmes
- `main.ts` required per subfolder unless it's readme-only

## Moving/renaming exercises

When renumbering or moving exercises:

1. Apply the host safe Git protocol. For authorized tracked renames, use `git mv` on the exact owned directory; verify destination absence and preserve unrelated index entries. Git tracks content similarity, so the command expresses the rename rather than guaranteeing history.
2. Update the numeric prefix to maintain order
3. Update affected links/references, then re-run lint after moves

Example:

```bash
git mv exercises/01-retrieval/01.03-embeddings exercises/01-retrieval/01.04-embeddings
```

## Example: stubbing from a plan

Given a plan like:

```
Section 05: Memory Skill Building
- 05.01 Introduction to Memory
- 05.02 Short-term Memory (explainer + problem + solution)
- 05.03 Long-term Memory
```

Create:

```bash
mkdir -p exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer
mkdir -p exercises/05-memory-skill-building/05.02-short-term-memory/{explainer,problem,solution}
mkdir -p exercises/05-memory-skill-building/05.03-long-term-memory/explainer
```

Then create readme stubs:

```
exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer/readme.md -> "# Introduction to Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/explainer/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/problem/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/solution/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.03-long-term-memory/explainer/readme.md -> "# Long-term Memory"
```
