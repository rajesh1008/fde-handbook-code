#!/usr/bin/env bash
# Re-run every Chapter 24 listing and store its output beside the code.
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
mkdir -p output
for s in split options fanout identity rollback; do
  $PY $s.py > output/$s.txt
done
for x in a b c; do $PY tryit.py $x > output/tryit_$x.txt; done
$PY -m pytest -q test_ch24.py > output/tests.txt 2>&1 || (cat output/tests.txt; exit 1)
# fieldkit tests through v3.1; later chapters' tests are theirs to keep green
(cd ../fieldkit && $PY -m pytest -q $(ls tests/test_*.py | grep -v -E 'test_v3[2-9]|test_v[4-9]') >> ../ch24/output/tests.txt 2>&1) || (cat output/tests.txt; exit 1)
tail -n 3 output/tests.txt
