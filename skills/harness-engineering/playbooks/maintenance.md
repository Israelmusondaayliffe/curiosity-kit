# Maintenance

Audit fresh state, repair authorized drift and verify the result. This method includes its own prose-repair procedure; optional writing help does not become a dependency.

## Inputs and diagnosis

Read the current goal, approved roots/actions, source revision, active instruction chain, installed state and last verified receipt. Inspect existing user edits before choosing a baseline. Run relevant deterministic checks first.

Classify differences as intentional user changes, platform/model changes, broken dependencies, stale guidance or missing enforcement. Compare observed behavior rather than timestamps alone. Consult current official documentation before changing model-specific or host-specific configuration; preserve an explicitly selected model.

Weekly output reviews, monthly instruction reviews and post-release/model reviews are possible scopes when requested. Do not create schedules as a maintenance side effect.

## Narrow repair

Choose the smallest reversible change that fixes the observed failure. Reuse existing tooling. Turn repeated mechanically detectable failures into regression checks rather than accumulating instructions. Keep judgment criteria explicit.

Freeze approved paths, hashes, protected material and acceptance tests; back up affected files. Use hash-preconditioned, previewable operations and atomic writes. Stop on concurrent edits, unexpected paths or changed authority. Do not overwrite user work to restore an old baseline.

Use the bundled operation tool with explicit roots, expected hashes, dry-run preview, bounded apply and recovery evidence: `hectl plan`, `hectl apply --mode dry-run`, then `hectl apply --mode apply` with a backup directory and manifest, and `hectl rollback MANIFEST` (see [build](build.md)). If that mechanism is unavailable, stop the mutation rather than inventing an unguarded shell replacement.

## Local prose repair

Use this procedure for authorized human-facing instruction/prose changes, not authentication, binary work, cache cleanup or version-only edits.

1. Audit without rewriting. Establish purpose, stakes and source-supplied voice. Separate scanner matches from accepted defects; precise technical terms are not automatically defects.
2. Freeze the text and protected fingerprints. Preserve commands, code, quotations, prompt blocks, identifiers, paths, links, structured data and frontmatter. Structural changes require their own scoped operation.
3. Edit accepted findings: remove filler, unsupported significance, vague attribution, repetition and confusing phrasing. Prefer ordinary precise words. Preserve useful uncertainty, source rhythm and strong sentences. Never invent facts, opinions, experience or personality. Avoid global replacement across mixed prose and code.
4. Rescan and compare meaning line by line. Restore voice or detail lost through overediting. Reconcile every accepted finding as repaired or protected with a reason and evidence.
5. Apply the repair rubric: factual fidelity 2, protected material 2, scope 1.5, reconciliation 1.5, language 2, evidence 1. Minimum 8/10; target 10. Fabrication, protected drift, unapproved scope, unresolved findings, credibility/routing/placeholder corruption or authored em dashes block acceptance regardless of score.
6. Review the integrated result. Use the skill's local repair taxonomy, workflow and validators for full repair-engine claims: [Unslop method](../references/unslop-method.md), [Unslop repair](unslop-repair.md) and `hectl unslop audit|freeze|scan|voice|verify`. Missing required components block that claim. An optional helper receives scope, protected constraints and the requested diff; it does not gain authority to promote its own result.

## Model/context changes and cleanup

Freeze model, effort, tools, routes, scorer, prompts and baseline outputs ([subtraction protocol](../references/subtraction-protocol.md)); `hectl context-scan` supplies the deterministic over-constraint findings. Repeat model-change comparisons under fixed conditions. Subtract one coherent instruction group at a time; restore any critical, category or overall regression. Recheck loaded behavior after context mutations. A failing baseline needs diagnosis and repair before a reduction claim.

Generic cleanup requests, including "clean it up safely", authorize inventory and dry-run only. Use `hectl cleanup --host claude-code|codex` without `--apply`. Present the exact candidate paths, the deletion scope and the preservation exclusions from its receipt. Run `--apply --approved-receipt <that dry-run receipt>` only after the user approves those candidates; reuse a prior explicit approval when it covers that exact set and scope. The tool revalidates before deletion; new candidates stay excluded without new approval, and changed safety conditions stop execution. Preserve retention floors, ceilings, locking, symlink/open-file/process checks and protection of active, installed, memory-referenced and backup data. Never interchange host roots or deletion contracts. A permission, ownership or preservation stop requires reporting the blocker, not weakening guards or removing preservation references; do not recommend those bypasses. Report no candidates only after the required checks succeed; unavailable checks or incomplete receipts mean blocked or unknown, never empty success.

## Close

Test affected behavior, then use [verification](verification.md) read-only on the integrated revision. Roll back authorized failed changes in reverse order without overwriting intervening edits. Preserve evidence and report restored, verified, partially applied or blocked accurately.

Stop a repair approach when unresolved work does not fall; diagnose or change the approach within authority. Finish with the actual changed outcome, remaining requirements and recovery state.
