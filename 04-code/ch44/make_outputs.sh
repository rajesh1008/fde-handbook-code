#!/usr/bin/env bash
# Regenerates every output the chapter quotes. Deterministic stand-in; no network, no model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for s in headcount profile rubric calibrate pyramid_run pods rotation ladder learn portfolio; do
  $PY $s.py > output/$s.txt
done
for v in a b c; do $PY tryit.py $v > output/tryit_$v.txt; done
$PY -m pytest -q test_ch44.py ../fieldkit/tests > output/tests.txt 2>&1 || true
tail -1 output/tests.txt
