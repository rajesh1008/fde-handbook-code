#!/usr/bin/env bash
# Regenerates every output pasted into Chapter 15. Run from anywhere.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for s in day47_status escalate_day47 register_card failure_key_removed plumbing_check greystone_day112 ladder_dates weekly_progress; do
  "$PY" "$s.py" > "output/$s.txt"
done
for x in a b c; do "$PY" tryit.py "$x" > "output/tryit_$x.txt"; done
echo "outputs written to $(pwd)/output"
