# Context subtraction

Find model compensation in persistent context, prove it, and propose removals with reasons. This playbook reads and reports; applying the ledger goes through [instruction files](instruction-files.md), [skill authoring](skill-authoring.md) or [plugin authoring](plugin-authoring.md), then [build](build.md).

## Scope

Name every file to be judged: one file, a skill directory, a plugin bundle or an instruction chain. The doctrine is the same on every platform; the chain differs (CLAUDE.md layers on Claude Code, app instructions plus folder contract on Cowork, AGENTS.md layers on Codex).

## Steps

1. Read [context doctrine](../references/context-doctrine.md).
2. Run the scanner:

```text
python3 scripts/hectl.py context-scan PATH... [--verification-policy review-all|keep-one] [--long-run] --output SCAN.json
```

Findings are signals to judge and test with the model that will run the context, not proof a line is unneeded. `--verification-policy keep-one` keeps the first test-your-work line and flags the rest; the default `review-all` flags every verification line for review. `--long-run` relaxes verification findings for a long unattended run, where a fresh-context verifier is still allowed. A file that documents banned patterns can carry `context-scan: catalogue` in its first 20 lines; a single line can carry `context-scan: ignore`. Lines that name a pattern only to forbid it are reported as INFO for you to confirm.
3. Judge what the scanner cannot see: judgement calls, examples that could be interface design, upfront detail that could load on demand, content that restates the file system.
4. Keep suspected model compensation separate from user policy, taste, gotchas, authority boundaries and data routing. Compensation is a hypothesis for a tested change, not automatically removable. Preserve meaningful verification and every essential control.
5. Rank by the actual task impact, evidence and risk. A scanner category, model generation or token weight alone is not a removal priority. Replace demands for hidden reasoning with concise rationale or observable evidence; do not infer that all verification reminders are harmful.

## Output

A ledger with one row per finding: file, line, category, severity, text, reason, proposed action (remove, rewrite, move, keep). A file with no findings gets a row saying so. Include the keep set with its justification. For a measured reduction claim, follow [subtraction protocol](../references/subtraction-protocol.md); a shorter file is not evidence by itself.
