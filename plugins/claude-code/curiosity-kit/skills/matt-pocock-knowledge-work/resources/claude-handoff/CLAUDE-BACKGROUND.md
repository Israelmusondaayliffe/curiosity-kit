# Claude CLI background adapter

Conditional host reference for [claude-handoff](../../playbooks/claude-handoff.md). Use only for an authorized installed Claude Code CLI whose inspected help supports this interface; otherwise use a supported authorized native/cloud task or report launch blocked.

Source command shape:

```bash
claude --bg --name "Fix login bug" -- "$(cat -- "$summary_file")"
```

Resolve `summary_file` to the actual saved handoff and quote its path. `--name` (or `-n`) is required, so the job list, session picker and terminal title identify the task. The CLI starts in the current working directory and returns immediately. The source management command is `claude agents`; inspect available lifecycle commands before promising a particular control.

Double-quoted command substitution passes the file text as one argument. Backticks and `$()` appearing **inside the file contents** are not recursively evaluated as shell syntax. Do not interpolate the summary into an executable shell program, use `eval`, or substitute an unquoted filename. A process-argument prompt may be visible to local process inspection; remove secrets and unnecessary sensitive data first. Check argument-size limits for large summaries and use an actually supported file-input alternative if needed rather than truncating critical scope.

Before launch, verify the working directory, destination authorization and accessible pointers. After launch, record the real task ID/name and observed state. If the CLI errors or returns an ambiguous result, inspect the job list before retrying. Sending the prompt successfully is not proof that the task completed; only an observed terminal result supports completion.
