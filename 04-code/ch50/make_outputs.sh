#!/usr/bin/env bash
# Regenerates every output Chapter 50 quotes. Deterministic stand-in: same data, same numbers. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
"$PY" spread_run.py > output/spread.txt
for m in clean model_ratio model_calc unlabeled; do "$PY" draft_run.py "$m" > "output/draft_$m.txt"; done
"$PY" pyramid_run.py > output/pyramid.txt
"$PY" classify.py > output/classify.txt
for s in 1 2; do "$PY" committee.py "$s" > "output/committee_s$s.txt"; done
for d in 118 171; do "$PY" execpack.py "$d" > "output/pack_d$d.txt"; done
"$PY" gateway.py > output/gateway.txt
"$PY" boundary.py > output/boundary.txt
"$PY" shadowrun.py > output/shadow.txt
"$PY" shadowrun.py json > output/funnel.json
for p in a b c; do "$PY" tryit.py "$p" > "output/tryit_$p.txt"; done
"$PY" -m pytest -q test_ch50.py ../fieldkit/tests > output/tests.txt 2>&1 || { cat output/tests.txt; exit 1; }
tail -1 output/tests.txt
