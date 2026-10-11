#!/usr/bin/env bash
# Baseline-left/target-right rows with distinct frame indices and time sidecars.
set -euo pipefail
if [[ $# -lt 2 || $# -gt 4 ]]; then
  echo "usage: $0 baseline.mp4 translated.mp4 [output-dir] [samples]" >&2; exit 2
fi
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$HERE/compare_media.py" strip "$1" "$2" "${3:-./strip-out}" --samples "${4:-8}"
