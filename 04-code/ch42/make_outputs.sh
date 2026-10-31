#!/usr/bin/env bash
# Regenerates every output Chapter 42 quotes. Deterministic stand-in: same data, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
for v in v0 v1; do "$PY" replay.py "$v" > "output/replay_$v.txt"; "$PY" deprecation.py "$v" > "output/deprecation_$v.txt"; "$PY" livestable.py "$v" > "output/livestable_$v.txt"; done
"$PY" replay.py v1 daily | grep '^DAILY' > output/replay_daily.json.txt
for v in v0 v2; do "$PY" drill.py "$v" > "output/drill_$v.txt"; done
"$PY" ownership.py > output/ownership.txt
"$PY" caldwell.py > output/caldwell.txt
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
IGN=""; for f in ../fieldkit/tests/test_*_ch4[3-9].py ../fieldkit/tests/test_*_ch5[0-9].py; do [ -e "$f" ] && IGN="$IGN --ignore=$f"; done   # later chapters
"$PY" -m pytest -q test_ch42.py ../fieldkit/tests $IGN > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
