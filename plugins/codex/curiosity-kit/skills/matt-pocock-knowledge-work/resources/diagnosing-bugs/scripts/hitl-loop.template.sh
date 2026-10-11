#!/usr/bin/env bash
# Human-run reproduction template; copy into an owned scratch location.
# Adapt the steps to the exact symptom before use. No installation or app
# commands execute here. Capture sanitized observations only, never secrets.
# Output is shell-escaped evidence for reading, NEVER a file to source/eval.
set -euo pipefail
trap 'printf "\nSTATUS=interrupted\n" >&2; exit 130' INT
trap 'printf "\nSTATUS=interrupted\n" >&2; exit 143' TERM
incomplete() { printf '\nSTATUS=incomplete (input ended)\n' >&2; exit 2; }
step() {
  local response
  printf '\n>>> %s\n    [Enter when done] ' "$1"
  IFS= read -r response || incomplete
}
capture() {
  # Prefix helper-local names so caller destinations cannot shadow them.
  local _hitl_dest="$1" _hitl_question="$2" _hitl_value
  case "$_hitl_dest" in
    ERRORED|ERROR_MSG) ;;
    *) printf 'Unsupported observation field\n' >&2; exit 2 ;;
  esac
  printf '\n>>> %s\n    > ' "$_hitl_question"
  IFS= read -r _hitl_value || incomplete
  printf -v "$_hitl_dest" '%s' "$_hitl_value"
}
# Edit only these scenario-specific instructions/fields as needed.
step "Open your approved local test app. Sign in yourself if needed; do not paste credentials here."
while :; do
  capture ERRORED "Click Export. Did the exact reported error occur? (y/n)"
  case "$ERRORED" in y|n) break ;; *) printf 'Please enter y or n.\n' ;; esac
done
capture ERROR_MSG "Enter only the sanitized error message, or none. Remove tokens, names, and private data first."
printf '\n--- Captured observations ---\n'
printf 'ERRORED=%q\n' "$ERRORED"
printf 'ERROR_MSG=%q\n' "$ERROR_MSG"
printf 'STATUS=complete\n'
