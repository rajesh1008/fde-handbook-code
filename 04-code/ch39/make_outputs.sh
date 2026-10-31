#!/usr/bin/env bash
# Regenerates every output Chapter 39 quotes. Deterministic: same seeds, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for w in funnel adjudication streams gate holiday greystone; do "$PY" run.py "$w" > "output/$w.txt"; done
"$PY" duration.py > output/duration.txt
"$PY" live.py > output/live.txt
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch39.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
