#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
"$PY" rerun.py > output/rerun.txt
"$PY" recalibrate.py > output/recalibrate.txt
"$PY" escape.py > output/escape.txt
"$PY" absorb.py > output/absorb.txt
for t in a b c; do "$PY" tryit.py $t > output/tryit_$t.txt; done
"$PY" -m pytest -q -p no:cacheprovider test_ch52.py ../fieldkit/tests > output/tests.txt 2>&1
