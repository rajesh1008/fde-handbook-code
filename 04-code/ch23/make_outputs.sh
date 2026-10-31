#!/usr/bin/env bash
# Regenerates every output shown in Chapter 23 (deterministic stand-in data; nothing here is Caldwell's).
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/books/.venv/bin/python
mkdir -p output
for s in store_options acl_inherit acl_drift supersession evaluate cost; do $PY $s.py > output/$s.txt; done
for v in a b c; do echo "== tryit $v"; $PY tryit.py $v; done > output/tryit.txt
$PY -m pytest -q test_ch23.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
