#!/usr/bin/env bash
# Regenerates every output Chapter 45 quotes. Deterministic stand-in: same data, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for v in v0 v1; do "$PY" loop.py "$v" > "output/loop_$v.txt"; "$PY" takehome.py "$v" > "output/takehome_$v.txt"; done
for c in c214 c231 c236 c214-v0; do "$PY" debrief.py "$c" > "output/debrief_$c.txt"; done
for c in c214 c231; do "$PY" discovery.py "$c" > "output/discovery_$c.txt"; "$PY" whiteboard.py "$c" > "output/whiteboard_$c.txt"; done
for w in before after; do "$PY" calibrate.py "$w" > "output/calibrate_$w.txt"; done
for a in weak strong; do "$PY" moves.py "$a" > "output/moves_$a.txt"; done
"$PY" bank.py > output/bank.txt
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch45.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
