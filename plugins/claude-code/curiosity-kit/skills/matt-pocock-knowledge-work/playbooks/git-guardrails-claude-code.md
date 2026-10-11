# Matt: git-guardrails-claude-code

Source status: frozen miscellaneous. Use only inside the explicitly selected Matt library. Before first action, apply [the host contract](../references/host-contract.md).

Configure a supplemental command-text warning/block hook for an authorized Claude Code installation. The source name is retained; hosts without this hook interface must report it unsupported rather than claiming an equivalent security boundary. Platform permissions remain authoritative.

## Scope and limits

The supplied Bash adapter checks JSON tool input for literal command patterns: Git push, hard reset, force clean, forced branch deletion and checkout/restore of `.`. It handles common whitespace, `-C`, `--git-dir`, `--work-tree` and `--no-optional-locks` prefixes, but it is **not a shell parser**. Aliases, constructed commands, unrecognized global options, tool-specific alternatives and other tools are outside its reliable coverage. Benign quoted/echoed text can match and be blocked. Do not claim complete enforcement, sandboxing or demonstrated exploit resistance.

## Setup

1. Ask or reuse the user’s explicit scope choice: this project (`.claude/settings.json`) or all projects (`~/.claude/settings.json`). Global setup changes wider behavior and must not be inferred from a project request. Check current host/version hook support and actual configuration paths.
2. Inspect the existing settings and hooks. Check required Bash, `jq` and `grep` availability without installing implicitly. Read [block-dangerous-git.sh](../resources/git-guardrails-claude-code/scripts/block-dangerous-git.sh). The adapter returns exit 2 when required parsing tools are missing, input is invalid or a configured pattern matches; it never executes command text.
3. Under actual setup authority, copy the script to `.claude/hooks/block-dangerous-git.sh` for project scope or the equivalent user-home hooks path for global scope. Preserve an existing differing script unless its replacement is specifically in scope. Set the required executable mode. A migration candidate’s included resource is not a live hook installation.
4. Merge one hook entry into existing `hooks.PreToolUse`, preserving other hook entries and unrelated settings. Detect an equivalent entry to avoid duplicates on rerun. For an existing unsupported or malformed configuration, report the exact issue before replacing anything. Use the selected scope’s command template below.
5. Ask whether the user wants changes to the matched patterns, unless already supplied. Explain coverage limitations before adopting a claim such as “block all destructive Git”. Removing a pattern changes behavior and must follow the actual approved scope.
6. Test the script in an isolated setup with inert JSON strings, never by running a destructive Git command. Observe a safe `git status` pass, a literal `git push origin main` block with exit 2, force-clean spelling variants, whitespace and common global-prefix cases. Check malformed JSON, missing string command and missing jq fail closed. Exercise a harmless echoed pattern to expose conservative false positives. Review unsupported textual counterexamples as limitations, not proof of executed bypasses.
7. Verify that the real host loads the merged hook only when an authorized native test is available. A shell-script fixture pass is not proof of native interception. Report files, selected scope, observed checks and unrun host integration separately.

## Settings templates

Project entry to merge into `hooks.PreToolUse`:

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
    }
  ]
}
```

Global entry uses the same structure, with a safely quoted absolute path established from the user’s actual home directory, or this supported shell-home form where the host executes it through a shell:

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "\"$HOME/.claude/hooks/block-dangerous-git.sh\""
    }
  ]
}
```

Avoid a quoted literal `~` path, which may not expand. Verify quoting against the actual host and paths with spaces. Preserve the JSON object containing these entries; the examples are array elements, not replacement settings files.
