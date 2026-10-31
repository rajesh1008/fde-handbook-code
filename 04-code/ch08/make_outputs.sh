#!/usr/bin/env bash
# Regenerate every listing output in Chapter 8 (deterministic stand-in; no model calls, no customer data).
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
export PYTHONPATH=../fieldkit:${PYTHONPATH:-}
mkdir -p output
for s in generate_scope calibration failure_lint laundering volumes register_export suite_export; do
  $PY $s.py > output/$s.txt
done
for t in a b c; do $PY tryit.py $t > output/tryit_$t.txt; done
$PY -m pytest -q test_ch08.py > output/pytest.txt 2>&1 || { cat output/pytest.txt; exit 1; }
echo "outputs written to output/"
