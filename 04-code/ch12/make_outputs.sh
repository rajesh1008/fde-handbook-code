#!/bin/sh
# Regenerate every captured output of the Chapter 12 lab.
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
for s in triage_run crosswalk_run extract_run failure_contradiction panel_run five_moves_run safety_net_run after_award; do
  $PY $s.py > output/$s.txt
done
for n in 1 2 3; do $PY tryit.py $n > output/tryit_$n.txt; done
