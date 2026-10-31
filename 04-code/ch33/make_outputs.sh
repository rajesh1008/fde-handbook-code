#!/usr/bin/env bash
# Regenerates every output Chapter 33 quotes. Deterministic: same seeds, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for s in classify evidence monitor validator review pyramid_run; do
  "$PY" "$s.py" > "output/$s.txt"
done
"$PY" pack.py v1 > output/pack_v1.txt
"$PY" pack.py v2 > output/pack_v2.txt
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch33.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
