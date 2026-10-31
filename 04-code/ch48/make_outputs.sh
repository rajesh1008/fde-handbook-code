#!/usr/bin/env bash
# Regenerates every output Chapter 48 quotes. Run from 04-code/ch48 with the book venv active.
set -e
cd "$(dirname "$0")"; mkdir -p output
python calendar48.py > output/calendar.txt
python renewals.py   > output/renewals.txt
python upgrades.py   > output/upgrades.txt
python clocks.py     > output/clocks.txt
python incidents.py  > output/incidents.txt
python freeze.py     > output/freeze_v0.txt
python freeze.py v1  > output/freeze_v1.txt
python turnover.py   > output/turnover.txt
python board.py      > output/board.txt
for x in a b c; do python tryit.py $x > output/tryit_$x.txt; done
python -m pytest -q test_ch48.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
