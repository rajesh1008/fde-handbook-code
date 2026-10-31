#!/usr/bin/env bash
# Re-run every Chapter 22 listing and store its output beside the code.
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
mkdir -p output
$PY shadow_week.py v1 > output/week_v1.txt
$PY shadow_week.py v2 > output/week_v2.txt
for s in thumb steps routing scorecard breakdown; do $PY $s.py > output/$s.txt; done
for x in a b c; do $PY tryit.py $x > output/tryit_$x.txt; done
$PY -m pytest -q -p no:cacheprovider test_ch22.py > output/tests.txt 2>&1 || (cat output/tests.txt; exit 1)
(cd ../fieldkit && $PY -m pytest -q -p no:cacheprovider tests >> ../ch22/output/tests.txt 2>&1) || (cat output/tests.txt; exit 1)
tail -n 3 output/tests.txt
