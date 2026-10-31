#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
mkdir -p output
for s in gap_register run_readiness failure_no_owner promise_rewrite oversight rebaseline tryit; do
  $PY $s.py >| output/$s.txt
done
$PY -m pytest -q test_ch04.py >| output/tests.txt
echo done
