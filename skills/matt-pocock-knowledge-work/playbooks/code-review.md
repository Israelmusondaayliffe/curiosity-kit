Before acting, read [the host contract](../references/host-contract.md). It governs actual tools, authority, owned output roots, safe first Git reads, worker identity, and evidence.

# Code Review

Review the actual requested candidate on two separate axes: **Standards** (documented conventions and labelled smell heuristics) and **Spec** (required behavior and acceptance evidence). A review request authorizes inspection, not repair, commits, or publication.

## Process

### 1. Pin the actual review surface before repair

Read the host contract before the first repository command; its command-local safe Git settings apply to every read below. Resolve the user-supplied commit, branch, tag, or merge-base to a commit ID. Infer a base only when unambiguous; otherwise ask. Resolve HEAD too. State whether the user requested merge-base comparison or direct comparison; three-dot semantics are not interchangeable with direct comparison.

Identify whether the candidate includes committed, staged, unstaged, and/or explicitly in-scope untracked source. “Review my current changes” normally includes all four; “review this commit” does not silently include the working tree. Ask only when scope materially remains ambiguous. Capture:

- Base and HEAD IDs, comparison semantics, and commit list (`log <base>..HEAD --oneline`).
- Committed diff (`diff <merge-base> HEAD` or direct base as requested).
- Staged diff (`diff --cached HEAD`) and unstaged diff (`diff`) when in scope.
- NUL-delimited untracked path inventory (`ls-files --others --exclude-standard -z`), then read each in-scope source file explicitly. Exclude secrets, generated and unrelated files; report exclusions. Never omit new source merely because ordinary diff does not show it.
- Candidate bytes or hashes, rename/deletion information, and sufficient surrounding files to understand behavior. Staged-only review uses index versions, not newer working-tree content.

Freeze those read-only inputs in an owned temporary review snapshot when supported. Otherwise perform scoped reads and verify hashes/HEAD/index after review. Record the index bytes/hash before and after through the host contract; no stash, checkout, staging, refresh, or index rewriting to prepare a review. If the candidate changes during inspection, invalidate affected findings and reread affected inputs, rather than silently reviewing a mixed snapshot. Do not copy ignored/private material wholesale.

Both axes must receive the same snapshot identity and content. Reject an invalid base early. An empty committed diff is not an empty dirty-tree review: check every requested layer first. A genuinely empty surface is reported with scope, not sent to workers.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.), fetched through an available authorized tracker adapter, or supplied local evidence.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Search the repo for every file that documents how code should be written. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Spawn both sub-agents in parallel

Use two real independent leaf workers when available; each inspects its assigned axis directly and must not invoke this delegating playbook or spawn further reviewers. Give each the task, source snapshot, read-only scope, required result, and evidence requirements from the host contract. If unavailable, perform two separately recorded passes yourself and disclose reduced independence. Never label a role-play as an independent review.

**Standards sub-agent prompt** should include:

- The exact candidate snapshot, included layers, exclusions, commit list, and context paths.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full (the sub-agent has no other access to it).
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Keep the report under 400 words; link a complete finding appendix if material findings need more space."

**Spec sub-agent prompt** should include:

- The same candidate snapshot identity, included layers, exclusions, and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Keep the report under 400 words; link a complete finding appendix if material findings need more space."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present one integrated final review with separate `## Standards` and `## Spec` sections, verbatim or lightly cleaned. Do **not** merge or rerank findings, because the two axes are deliberately separate (see _Why two axes_).

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes: that's the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.

## Verdict, coverage, and authorized repair

For each axis give pass, pass with fixes, fail, or blocked; attach severity, file/hunk, source rule or requirement, observed evidence, confidence, and smallest corrective action to every finding. A missing spec is “not assessed,” never a pass. Distinguish missing implementation from missing acceptance coverage. A passing test does not establish an untested requirement.

Keep findings within each axis; never trade a Spec failure against clean Standards. Report snapshot identity, excluded layers/files, checks actually observed, and remaining uncertainty. Example: “Standards: possible Middle Man in parse.ts, heuristic; Spec: requirement 4 missing retry behavior, no coverage.”

Only after presenting findings, and only within existing implementation authorization, repair concrete findings. Review owns behavior-preserving refactoring: start from green evidence, change names/structure without changing required behavior, rerun focused tests and relevant checks. Added behavior returns to a specified slice and [TDD](tdd.md), rather than hiding inside a refactor. Preserve user edits. Verify affected Standards and Spec findings on the repaired snapshot; reopen full review only for material scope change, not recursive review loops. Record actual final evidence and unresolved findings. No commit, push, or external review comment follows merely from review completion.
