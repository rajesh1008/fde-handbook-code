#!/usr/bin/env bash
# Regenerates every output shown in Chapter 30 (deterministic stand-in data; nothing here is Caldwell's).
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=4
mkdir -p output
for s in failure_injection compare labels cost instructions guard governance; do $PY $s.py > output/$s.txt; done
for v in a b c; do echo "== tryit $v"; $PY tryit.py $v; done > output/tryit.txt
$PY -m pytest -q -p no:cacheprovider test_ch30.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
