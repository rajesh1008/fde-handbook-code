#!/usr/bin/env bash
# Regenerates every output Chapter 49 quotes. Deterministic stand-in: same data, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for m in scoreboards daily greystone pennant shared london; do "$PY" retro.py "$m" > "output/$m.txt"; done
"$PY" fourth.py naive > output/fourth_naive.txt
"$PY" fourth.py checked > output/fourth_checked.txt
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch49.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
