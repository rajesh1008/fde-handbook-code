#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
mkdir -p output
for s in five_questions run_coverage failure_interview_vs_shadow tracer exceptions volumes permissions; do
  $PY $s.py >| output/$s.txt
done
for i in a b c; do $PY tryit.py $i >| output/try_$i.txt; done
$PY -m pytest -q test_ch06.py >| output/tests.txt
echo done
