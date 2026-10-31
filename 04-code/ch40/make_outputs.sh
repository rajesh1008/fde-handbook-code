#!/usr/bin/env bash
# Regenerates every output Chapter 40 quotes. Deterministic: same seeds, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for m in v0 history months v1; do "$PY" rehearse.py "$m" > "output/rehearse_$m.txt"; done
for s in dispute rerun monitor conventions review audit; do "$PY" "$s.py" > "output/$s.txt"; done
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch40.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
