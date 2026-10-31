#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
mkdir -p output
for s in rooms classify_pipeline five_day_run day_five scope_doc_run tryit; do
  $PY $s.py >| output/$s.txt
done
$PY five_day_run.py --no-fax >| output/five_day_run_nofax.txt
$PY -m pytest -q test_ch14.py >| output/tests.txt
echo done
