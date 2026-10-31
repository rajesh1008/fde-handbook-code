#!/usr/bin/env bash
# Regenerates every output Chapter 38 quotes. Deterministic stand-in: same data, same numbers.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for s in evidence_set passes hardest5 residual signoff changes; do "$PY" "$s.py" > "output/$s.txt"; done
"$PY" changes.py --inject > output/changes_inject.txt
"$PY" residual.py --inject > output/residual_inject.txt
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch38.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
