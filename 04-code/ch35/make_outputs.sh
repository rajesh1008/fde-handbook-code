#!/usr/bin/env bash
# Regenerates every output Chapter 35 quotes. Deterministic: same seeds, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for v in v1 v2; do "$PY" datamap.py "$v" > "output/datamap_$v.txt"; "$PY" erasure.py "$v" > "output/erasure_$v.txt"; done
for m in before after; do "$PY" pii_scan.py "$m" > "output/scan_$m.txt"; done
for s in regimes minimum; do "$PY" "$s.py" > "output/$s.txt"; done
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch35.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
