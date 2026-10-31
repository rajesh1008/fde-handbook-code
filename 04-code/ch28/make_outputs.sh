#!/usr/bin/env bash
# Regenerates every output the chapter quotes. Deterministic: same seeds, same numbers.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for s in elicit rules_as_tests replay redteam tradeoff loop; do
  "$PY" "$s.py" > "output/$s.txt"
done
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch28.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
