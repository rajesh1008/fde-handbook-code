#!/usr/bin/env bash
# Regenerates every output Chapter 37 quotes. Deterministic: same inputs, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for m in aggregate perclass terms evidence order; do "$PY" tracker.py "$m" > "output/tracker_$m.txt"; done
"$PY" classes.py > output/classes.txt
for w in logs day157; do "$PY" pack.py "$w" > "output/pack_$w.txt"; done
for v in v1 v2; do "$PY" residual.py "$v" > "output/residual_$v.txt"; done
"$PY" stack.py > output/stack.txt
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch37.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
