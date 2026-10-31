#!/usr/bin/env bash
# Regenerates every output pasted into Chapter 7. Deterministic: synthetic records are seeded.
set -euo pipefail; cd "$(dirname "$0")"; mkdir -p output
for f in failure_vendor_assumption prep_sheet day24_session data_questions whitfield rapid_fire roles generate_bank; do
  /workspace/books/.venv/bin/python $f.py > output/$f.txt; done
for x in a b c; do /workspace/books/.venv/bin/python tryit.py $x > output/tryit_$x.txt; done
/workspace/books/.venv/bin/python -m pytest -q test_ch07.py > output/pytest.txt 2>&1 || { cat output/pytest.txt; exit 1; }
echo ok
