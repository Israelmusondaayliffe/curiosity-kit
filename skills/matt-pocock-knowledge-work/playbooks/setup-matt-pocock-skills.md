# Setup Matt Pocock's Skills

Read the [host contract](../references/host-contract.md) before first repository access or action. This playbook runs only inside an explicitly selected Matt family workflow; source commands are not permission.

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker**: where issues live (reuse an existing configured tracker; otherwise local Markdown by default)
- **Triage labels**: the strings used for the five canonical triage roles
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- Safe remote metadata under the host contract: is this GitHub, GitLab or another host, and which repository? Avoid reading or displaying credential-bearing remote URLs or config values.
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Is there already an `## Agent skills` section in either?
- `GLOSSARY.md` and `GLOSSARY-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/`: does this skill's prior output already exist?
- `.scratch/`: a sign that a local-markdown issue tracker convention is already in use
- Is the `triage` skill installed? (the bundled [triage](triage.md) playbook, or an explicitly selected compatible installation.) This decides whether Section B runs at all.
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. These are present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed, Section C when there's no monorepo).

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `triage`, and `to-spec` read from and write to it. They need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Prefer the project’s existing tracking convention. With no configured tracker, recommend local Markdown; a GitHub/GitLab remote is evidence for an available alternative, not permission to create remote state. Offer:

- **GitHub**: issues live in the repo’s GitHub Issues (use an eligible connected tool, or verified `gh` CLI capability)
- **GitLab**: issues live in the repo’s GitLab Issues (use an eligible connected tool, or verified [`glab`](https://gitlab.com/gitlab-org/cli) CLI capability)
- **Local markdown**: issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off**. Leave it off and don't raise it: a user who wants external PRs in the triage queue can flip the flag in the file later.

**Section B: Triage label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you), since an uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is. Only if the user says no, usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`), collect the overrides so `triage` applies existing labels instead of creating duplicates.

**Section C: Domain docs.** Default to **single-context** (one `GLOSSARY.md` + `docs/adr/` at the repo root). This fits almost every repo; write it without asking.

Offer **multi-context** (a root `GLOSSARY-MAP.md` pointing to per-context `GLOSSARY.md` files) only when exploration found monorepo signals. Then confirm which layout they want.

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` (the last only when `triage` is installed)

Let them edit before writing.

### 4. Write

**Pick the actual host instruction file:** inspect the active instruction chain and use the file the current host actually reads. On a Claude host the source preference is existing `CLAUDE.md`, otherwise existing `AGENTS.md`; on a Codex host follow its active `AGENTS.md` chain and do not edit `CLAUDE.md` as a substitute. Reuse an existing appropriate file or pointer; if neither is suitable, ask what to create. Never create a competing instruction authority just because another host’s filename appears in this template.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

Include the `### Triage labels` sub-block, and write `docs/agents/triage-labels.md`, only when `triage` is installed and Section B ran. When it isn't, both are omitted.

When Section B ran on GitHub or GitLab, inspect configured labels and propose only missing ones. Create them only under specific setup authority and verify readback. Five state labels do not cover category (`bug`/`enhancement`) or wayfinder types; inspect those separately when the corresponding workflow needs them, preserve existing mappings, and obtain any missing authority.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](../resources/setup-matt-pocock-skills/issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-gitlab.md](../resources/setup-matt-pocock-skills/issue-tracker-gitlab.md): GitLab issue tracker
- [issue-tracker-local.md](../resources/setup-matt-pocock-skills/issue-tracker-local.md): local-markdown issue tracker
- [triage-labels.md](../resources/setup-matt-pocock-skills/triage-labels.md): label mapping (only if `triage` is installed)
- [domain.md](../resources/setup-matt-pocock-skills/domain.md): domain doc consumer rules + layout

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

When relocating a seed, rebase its package-resource links to the actual accessible installed library, rewrite selected-tracker self/sibling links to the generated `issue-tracker.md`, and verify every retained link from the generated destination. Do not leave package-relative paths that now resolve inside the project or assume the recipient shares your installation path.

### 5. Done

Re-read the edited files and check that the actual host can find them and unrelated content is intact. Report any pending remote setup separately. Tell the user which setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later; re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.

## Knowledge-work verification surfaces

During discovery also identify durable glossary/decision/spec/handoff/evidence locations, output conventions, software test/build/lint commands and non-code renderers, source ledgers, connector checks, review and delivery gates. Record the smallest necessary paths and checks in the existing project convention alongside the tracker pointer. Non-code and mixed slices need a real deliverable surface, source-to-claim evidence and review against the brief. Keep external actions explicitly permission-gated.

Before writing, re-read live files and merge the exact previewed change into existing sections; preserve custom paths, user edits and unrelated hooks, scripts and configuration. Setup configures the project, not this library's runtime skill files. Re-running should update one pointer block and the selected docs without duplicates. Do not create empty glossary/ADR files: [domain-modeling](domain-modeling.md) creates them lazily when meaningful content is resolved.
