#!/bin/sh
# Regenerate every listing output in Chapter 10 from the lab (deterministic stand-ins, seeded).
cd "$(dirname "$0")"; PY=/workspace/books/.venv/bin/python
for f in estimate_all failure_denied_api ranges customer_page phasing; do $PY $f.py > output/$f.txt; done
for t in a b c; do $PY tryit.py $t > output/tryit_$t.txt; done
