# Issue tracker: Local Markdown

Read the [host contract](../../references/host-contract.md) before access or writing. This is the canonical local artifact/state shape for the Matt library. Use an authorized, owned durable root; `.scratch/` below is a project convention, not permission to overwrite an existing path.

## Locations and identity

- One feature per directory: `.scratch/<feature-slug>/`.
- Spec: `.scratch/<feature-slug>/spec.md` (a spec may historically be called a PRD).
- Implementation tickets: one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order; never one combined tickets file.
- Wayfinder map: `.scratch/<effort>/map.md`; decision children: `.scratch/<effort>/issues/<NN>-<slug>.md` in map order.
- Incoming requests may use the same per-item convention with their own stable ID.
- An ID resolves within its feature/effort directory. Cross-effort edges use explicit paths. Names accompany links in human-facing prose.
- Comments/history append under `## Comments`; decision resolutions append under `## Answer`. Re-read before writes, preserve user edits and existing history.

## Canonical header

Use plain, unbolded `Field: value` lines after the title. This example is an implementation ticket:

```markdown
# 01: Show the first verified result

Artifact: implementation-ticket
Status: open
Owner: none
Parent: ../spec.md
Blocked by: none
Triage role: ready-for-agent

## What to build

One observable end-to-end result.

## Acceptance criteria

- [ ] A specific independently verifiable criterion
```

- `Artifact` is exactly `spec`, `implementation-ticket`, `incoming-request`, `wayfinder-map`, or `decision-ticket`.
- `Status` is exactly `open`, `claimed`, or `resolved`. New artifacts start `open`. A missing/unrecognized status is not implicitly ready or complete.
- `Owner` is a verified human or session/worker identifier, or `none`. Never invent an external identity for `@me`.
- `Parent` is the verified parent path/reference where applicable.
- `Blocked by` lists stable ticket IDs/paths or `none`. Missing, cyclic or unresolved dependencies block readiness.
- `Triage role` is a separate role from [triage-labels.md](triage-labels.md), used for incoming requests and approved specs/implementation tickets as applicable. `Category: bug|enhancement` is used for triaged incoming requests, not decision types.
- Decision tickets use `Decision type: research|prototype|grilling|task` and **no triage role**. A wayfinder map uses `Artifact: wayfinder-map`; it has no triage role either.
- Preserve a `Resolution` explanation when work is resolved as out of scope or rejected. `Status: resolved` alone never proves implemented code or a successful decision outcome; inspect the answer/evidence.

Existing bold headers and legacy `Status: ready-for-agent` may be read compatibly during discovery; translate that old line to `Triage role: ready-for-agent` with `Status: open` only in an authorized update. Do not silently interpret a spec as executable or a triage role as a completion state.

## Operations

**Publish:** create the correct artifact at a new, verified collision-free path. **Fetch:** read the full referenced file and comments, resolving ambiguous numbers before work.

**Frontier:** open, unclaimed tickets whose blockers are all actually resolved for the intended workflow, sorted by number/map order. For implementation orchestration, use verified landed integration evidence as specified in [implement-spec](../../playbooks/implement-spec.md), not stale tracker closure. For wayfinding, read each blocker’s resolved answer and ensure it actually releases this decision.

**Claim:** one coordinator writes `Status: claimed` plus `Owner` before work and re-reads it. Plain Markdown is not a distributed atomic lock. Use a single writer; if concurrent writers are possible, compare the observed version/hash before writing and stop on conflict rather than overwrite. A failed worker stays claimed with its blocker noted until the coordinator explicitly releases or reassigns it.

**Resolve implementation:** record fresh acceptance evidence and integration commit where relevant; change status only under task authority. Ordinary [implement](../../playbooks/implement.md) does not automatically close items.

**Resolve decision:** append the actual answer and linked assets under `## Answer`, set `Status: resolved`, then append a title-linked gist to the map’s Decisions so far. Out-of-scope closures go in the map’s Out of scope section instead. Read back both child and map; if one write fails, report the partial update and repair it without duplicating the answer.
