#!/usr/bin/env bash
# Regenerates every output Chapter 43 quotes. Deterministic stand-in: same data, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for c in pennant caldwell; do "$PY" model.py "$c" > "output/model_$c.txt"; done
for v in v0 v1; do "$PY" exitcheck.py "$v" > "output/exitcheck_$v.txt"; "$PY" drill.py "$v" > "output/drill_$v.txt"; done
"$PY" retainer.py > output/retainer.txt
"$PY" yearafter.py > output/yearafter.txt
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch43.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
