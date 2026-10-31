#!/usr/bin/env bash
# Regenerate every printed output in Chapter 51. Deterministic stand-in: no network, no clock, no randomness.
set -euo pipefail
cd "$(dirname "$0")"; PY=${PY:-/workspace/books/.venv/bin/python}; mkdir -p output
$PY lint_run.py > output/lint_run.txt
$PY audit.py > output/audit.txt
$PY audit.py --brief > output/audit_brief.txt
for t in a b c; do $PY tryit.py $t > output/tryit_$t.txt; done
for f in r02 r03 r07; do $PY -c "import inspect, linter; print(inspect.getsource(linter.$f), end=\"\")" > output/src_$f.txt; done
$PY -m pytest -q test_ch51.py ../fieldkit/tests 2>&1 | tail -3 > output/tests.txt
cat output/tests.txt
