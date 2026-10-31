#!/usr/bin/env bash
# Re-run every Chapter 21 listing and store its output beside the code.
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
mkdir -p output
for s in register variability scorer ask_vs_guess reconstruct retrofit granularity; do
  $PY $s.py > output/$s.txt
done
$PY lineage_break.py > output/lineage_broken.txt
$PY lineage_break.py fixed > output/lineage_fixed.txt
for x in a b c; do $PY tryit.py $x > output/tryit_$x.txt; done
$PY -m pytest -q test_ch21.py > output/tests.txt 2>&1 || (cat output/tests.txt; exit 1)
(cd ../fieldkit && $PY -m pytest -q tests >> ../ch21/output/tests.txt 2>&1) || (cat output/tests.txt; exit 1)
tail -n 3 output/tests.txt
