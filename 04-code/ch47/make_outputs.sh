#!/usr/bin/env bash
# Regenerates every output Chapter 47 quotes. Deterministic stand-in: same data, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
"$PY" repeats.py > output/repeats.txt
for m in 15 18; do "$PY" lint_run.py "$m" > "output/lint_m$m.txt"; done
for m in form n17 probe match; do "$PY" registry_run.py "$m" > "output/registry_$m.txt"; done
for m in rank ship; do "$PY" loop.py "$m" > "output/loop_$m.txt"; done
for m in ttp cap; do "$PY" absorb.py "$m" > "output/absorb_$m.txt"; done
"$PY" rotation.py > output/rotation.txt
"$PY" pod_loops.py > output/pod_loops.txt
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q -p no:cacheprovider test_ch47.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
