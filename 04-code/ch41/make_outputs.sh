#!/usr/bin/env bash
# Regenerates every output Chapter 41 quotes. Deterministic stand-in: same data, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for s in caldwell-before caldwell-after pennant; do "$PY" readiness.py "$s" > "output/readiness_$s.txt"; done
for v in v1 v2 pennant; do "$PY" routes.py "$v" > "output/routes_$v.txt"; done
for v in v1 v2; do "$PY" runbooks.py "$v" > "output/runbooks_$v.txt"; "$PY" raci.py "$v" > "output/raci_$v.txt"; "$PY" reference.py "$v" > "output/reference_$v.txt"; done
"$PY" training.py > output/training.txt
for d in 1 2 pennant pennant-rerouted; do "$PY" drill.py "$d" > "output/drill_$d.txt"; done
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch41.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
