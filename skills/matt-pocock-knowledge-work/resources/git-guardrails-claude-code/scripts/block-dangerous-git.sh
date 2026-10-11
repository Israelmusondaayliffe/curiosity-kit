#!/usr/bin/env bash
# Conservative text guard for the Claude Code Bash PreToolUse adapter.
# This is not a shell parser or a security boundary. Platform permissions govern.
set -u

block_input() {
  printf '%s\n' "BLOCKED: Git guard could not safely inspect the tool input: $1" >&2
  exit 2
}
command -v jq >/dev/null 2>&1 || block_input 'jq is unavailable'
command -v grep >/dev/null 2>&1 || block_input 'grep is unavailable'
INPUT=$(cat) || block_input 'stdin read failed'
COMMAND=$(printf '%s' "$INPUT" | jq -er '.tool_input.command | if type == "string" then . else error("command must be a string") end' 2>/dev/null) || block_input 'invalid JSON or missing string command'

# Supports literal git, whitespace, common -C/--git-dir/--work-tree prefixes,
# and --no-optional-locks. This deliberately does not interpret shell syntax.
GLOBAL='(((-C|--git-dir|--work-tree)[[:space:]]+("[^"]*"|'"'"'[^'"'"']*'"'"'|[^[:space:]]+)|--(git-dir|work-tree)=[^[:space:]]+|--no-optional-locks)[[:space:]]+)*'
GIT="(^|[[:space:];|&()])git[[:space:]]+${GLOBAL}"
DANGEROUS_PATTERNS=(
  "${GIT}push([[:space:]]|$)"
  "${GIT}reset[[:space:]]+([^;&|]*[[:space:]])?--hard([[:space:]]|$)"
  "${GIT}clean[[:space:]]+([^;&|]*[[:space:]])?(-[[:alpha:]]*f[[:alpha:]]*|--force)([[:space:]]|$)"
  "${GIT}branch[[:space:]]+([^;&|]*[[:space:]])?(-[[:alpha:]]*D[[:alpha:]]*|--delete[[:space:]]+--force|--force[[:space:]]+--delete)([[:space:]]|$)"
  "${GIT}(checkout|restore)[[:space:]]+(--[[:space:]]+)?\\.([[:space:]]|$)"
)
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if printf '%s\n' "$COMMAND" | grep -qE "$pattern"; then
    printf '%s\n' 'BLOCKED: Command text matches a configured dangerous Git pattern. Review the intended action with the user.' >&2
    exit 2
  else
    result=$?
    [ "$result" -eq 1 ] || block_input 'pattern matching failed'
  fi
done
exit 0
