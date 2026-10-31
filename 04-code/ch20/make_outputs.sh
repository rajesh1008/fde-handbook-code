#!/usr/bin/env bash
# Regenerates every output the chapter quotes. Deterministic: same output on every run.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for s in region_drift parity iac_check cost_estate loc; do $PY $s.py > output/$s.txt; done
for x in a b c; do $PY tryit.py $x > output/tryit_$x.txt; done
$PY -m pytest -q test_ch20.py > output/tests.txt 2>&1
(cd ../fieldkit && $PY -m pytest -q) > output/fieldkit_tests.txt 2>&1
tail -1 output/tests.txt; tail -1 output/fieldkit_tests.txt
