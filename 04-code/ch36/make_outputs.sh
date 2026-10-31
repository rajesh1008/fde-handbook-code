#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
mkdir -p output
$PY campaign.py --coverage > output/coverage.txt
$PY campaign.py --suite v2 > output/campaign-v2.txt
$PY campaign.py --suite v3 --oracle action > output/campaign-v3-action.txt
$PY campaign.py --suite v3 > output/campaign-v3.txt
$PY inject.py > output/inject.txt
$PY exfil.py > output/exfil.txt
$PY agency.py > output/agency.txt
$PY triage.py --naive > output/triage-naive.txt
$PY triage.py > output/triage.txt
$PY retest.py > output/retest.txt
for t in a b c; do $PY tryit.py $t > output/tryit-$t.txt; done
$PY -m pytest -q test_ch36.py ../fieldkit/tests 2>&1 | tail -1 > output/tests.txt
echo done
