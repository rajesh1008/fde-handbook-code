#!/usr/bin/env bash
# Re-run every Chapter 16 listing and store its output beside the code.
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
mkdir -p output
for s in synth_v1 failure_no_exceptions represent gap_line shadow_tap deid_attack sample_plan; do
  $PY $s.py > output/$s.txt
done
for x in a b c; do $PY tryit.py $x > output/tryit_$x.txt; done
$PY -m pytest -q test_ch16.py > output/tests.txt 2>&1 || (cat output/tests.txt; exit 1)
(cd ../fieldkit && $PY -m pytest -q tests >> ../ch16/output/tests.txt 2>&1) || (cat output/tests.txt; exit 1)
tail -n 3 output/tests.txt
