#!/usr/bin/env bash
# Regenerates every output Chapter 34 quotes. Deterministic: same seeds, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for st in v0 check v5; do "$PY" extract.py "$st" > "output/extract_$st.txt"; done
for s in readings sl margin pricing dataterms liability marcus; do "$PY" "$s.py" > "output/$s.txt"; done
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch34.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
