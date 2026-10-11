#!/usr/bin/env bash
# Paired-video preflight, ordered per-frame SSIM and localized diagnostics.
set -euo pipefail
if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: $0 baseline.mp4 translated.mp4 [output-dir]" >&2; exit 2
fi
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$HERE/compare_media.py" diff "$1" "$2" "${3:-./diff-out}"
