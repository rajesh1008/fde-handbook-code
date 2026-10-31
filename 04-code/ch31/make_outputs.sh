#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
export PYTHONDONTWRITEBYTECODE=1
mkdir -p output
for s in walkthrough tree failure_injection shadow_run scorecard memory; do $PY $s.py > output/$s.txt; done
$PY tryit.py abc > output/tryit.txt
$PY -m pytest -q -p no:cacheprovider test_ch31.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
