#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
mkdir -p output
for s in homes economics playbook failure_vendor_playbook_at_integrator reuse disagreements customer_view choose; do
  $PY $s.py >| output/$s.txt
done
for i in 1 2 3; do $PY tryit.py $i >| output/try_$i.txt; done
$PY -m pytest -q test_ch05.py >| output/tests.txt
echo done
