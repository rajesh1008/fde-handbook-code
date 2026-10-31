#!/usr/bin/env bash
# Regenerate every listing output in output/. Deterministic: no randomness, no network.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
for c in kickoff day12 day40 champions three oakley status series architects; do $PY lab.py $c > output/$c.txt; done
for t in 1 2 3; do $PY tryit.py $t > output/tryit_$t.txt; done
$PY -m pytest -q test_ch11.py > output/pytest.txt 2>&1 || true
echo "outputs written"
