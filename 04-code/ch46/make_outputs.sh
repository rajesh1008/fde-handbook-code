#!/usr/bin/env bash
# Regenerates every output Chapter 46 quotes. Deterministic stand-in: same data, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
"$PY" actuals.py closed > output/actuals.txt
"$PY" actuals.py all > output/actuals_all.txt
"$PY" reserve.py > output/reserve.txt
"$PY" forms.py > output/forms.txt
"$PY" phases.py > output/phases.txt
"$PY" waterfall.py > output/waterfall.txt
"$PY" playbook.py naive > output/playbook_naive.txt
"$PY" playbook.py checked > output/playbook_checked.txt
"$PY" playbook.py matrix > output/playbook_matrix.txt
"$PY" price_next.py naive > output/price_naive.txt
"$PY" price_next.py checked > output/price_checked.txt
"$PY" independent.py > output/independent.txt
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch46.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
