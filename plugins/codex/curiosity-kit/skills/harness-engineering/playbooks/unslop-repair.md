# Unslop repair

Repair writing-quality drift in harness and plugin prose through audit, freeze, approval, bounded edits, reconciliation and an integrated review. Use it when the user asks for an Unslop repair of the harness or approved plugins, or when approved maintenance will change human-facing harness prose. It is not for ordinary document editing, cache cleanup, authentication, version bumps, binaries or code-only work, and it does not activate on quoted, negated, hypothetical or explanation-only mentions.

Everything this repair needs is inside this skill: the method in [Unslop method](../references/unslop-method.md), the detector and gates in `scripts/hectl.py unslop`. A separate writing skill may help with ordinary prose, but it is never required here and never approves, repairs or completes this run.

## Default scope

The active instruction chain (CLAUDE.md on Claude Code, AGENTS.md on Codex, the folder contract on Cowork), this skill's own files, and the harness project contracts the workspace names. Add another plugin only when the user names or approves it.

## Sequence

1. **Audit, read-only.** Establish each text's purpose, stakes and source-backed voice. Run:

```text
python3 scripts/hectl.py unslop audit --run-id RUN --root /abs/approved/root --output /abs/outside/audit.json
python3 scripts/hectl.py unslop voice FILE --output voice.json
```

The audit inventories text files with hashes and protected-material fingerprints and records raw detector matches. Output must sit outside the audited roots.
2. **Classify.** Separate raw matches from accepted findings. Precise technical language (for example `harness` naming the system under maintenance, plugin and skill names, commands, schema keys) is legitimate, not a defect.
3. **Freeze.** `hectl unslop freeze --audit audit.json --output freeze.json`. A file that changed since the audit stops the freeze; re-audit instead of refreshing silently.
4. **Approval.** Present accepted finding clusters with evidence, the classified raw matches, exact roots and target paths, repair groups and any worker assignments, the 8.0 floor and 10.0 target, hard gates, stop conditions and rollback. Wait for explicit approval. Repair approval does not approve installation, routing changes or publication.
5. **Repair.** Back up each target. Edit only approved paths, applying the method's rewrite rules with the minimum effective change. Protected material (code, commands, prompts, quotations, links, paths, identifiers, tables, frontmatter, structured files) does not change inside this run; a finding inside it is classified `protected`. Removing bold delimiters is allowed when the emphasized words survive. Never run global replacements across mixed prose and code.
6. **Workers, optional.** Zero to three direct subagents, only for disjoint path sets. Each gets the run id, owned paths, frozen hashes, accepted finding ids, protected categories and authority limits (may edit owned paths; may not expand scope, launch workers, integrate, install, publish or declare completion), and returns changed paths, a terminal state and evidence per finding, residuals, the commands it ran, its unresolved count and zero recursive launches. The parent rejects any return that breaks these rules.
7. **Reconcile.** Re-scan. Every accepted finding ends `repaired` or `protected` (a protected finding needs category, reason, source owner and evidence). Every raw residual is `legitimate-technical` or `protected-source` with evidence. Unresolved must reach zero; a wave that does not lower it stops the run for a new plan.
8. **Score** each category in the ledger (`assets/templates/unslop-ledger.json`): meaning fidelity 2.0, protected material 2.0, scope and authority 1.5, finding reconciliation 1.5, language quality 2.0, verification evidence 1.0. Minimum 8.0, target 10.0. Hard gates cannot be bought back with points: no fabrication, protected material intact, scope intact, all findings terminal, no credibility, routing or placeholder corruption, no authored em dashes, method self-contained.
9. **Integrated review.** One fresh read-only reviewer compares the whole candidate with the freeze: meaning, quotations, code and fences, prompt tokens, links, paths, identifiers, tables, frontmatter, routing and activation boundaries, placeholders, and the full ledgers. Any finding blocks promotion; repair inside the approved group and review again.
10. **Verify the candidate:**

```text
python3 scripts/hectl.py unslop verify --freeze freeze.json --ledger ledger.json --output qualification.json
```

It fails on out-of-scope, new or deleted files, structured-file edits, lost protected segments, remaining authored em dashes, placeholder or fence corruption, overlapping or overreaching workers, non-terminal findings, invalid residuals, score below the floor, a false hard gate, a wave without progress, or a review that does not match the current files. Its pass is functional; the qualitative verdict comes from the review and the score.
11. **Promotion.** Show the exact diff, test results, score, gates, residual classes and review. Wait for separate approval before installation, then prove it through [verification](verification.md).
