#!/usr/bin/env bash
# Regenerate every output the chapter quotes. Usage: bash make_outputs.sh
set -e
cd "$(dirname "$0")"
PY=${PY:-/workspace/books/.venv/bin/python}
for f in sprint_zero backlog_order playback clinic sprint_review decision_register key_person; do
  $PY $f.py > output/$f.txt
done
for n in 1 2 3; do $PY try_it.py $n > output/try_it_$n.txt; done
$PY -m pytest -q test_ch13.py > output/pytest.txt
