# Chapter 29 lab: the pyramid runner over the Caldwell agent

Everything here runs on a laptop in under a second of compute. **Deterministic stand-in:** Caldwell's documents,
labels, rule cases, questions and scenarios are generated from fixed seeds in `world.py`; model calls are simulated
and their minutes and dollars are modeled from the stand-in rate card ($3 per million input tokens, $15 per million
output tokens, 5,200 in and 450 out per document, two passes). At Caldwell the same scripts run on Caldwell's CI
runners in AWS account 111122223333 (us-east-1) under the job identity `nl-eval`; every model call goes through
Priya Natarajan's model gateway; logs land in `/caldwell/nl-eval/pyramid`, readable by `nl-shadow-readers`, Anne
Kessler and Owen Pryce; evidence records go to the write-once store `claims-eval/evidence/` (object lock).

Run all: `./make_outputs.sh` (writes `output/*.txt` and `output/*.json`, then runs the tests).

| Listing | Script | What it shows |
|---|---|---|
| opening | `failure_injection.py` | the PR #212 gate output Callum Reid saw on day 146 (unnumbered, start of chapter) |
| 29.1 | `why_not_enough.py` | 41 defects of days 106 to 140 by category; Caldwell's 312 API and 58 UI tests caught 3 |
| 29.2 | `../fieldkit/fieldkit/pyramid.py`, `layers.py` | `select_layers` excerpt; the five layers, coverage target, frequency, minutes and dollars per run |
| 29.3 | `rules.py` | PR #231 (date library 3.9 to 4.0) blocked at layer one |
| 29.4 | `faithfulness.py` | 150 questions, claim support by type, the checker against Joan Mercer, stratified subset |
| 29.5 | `scenarios.py` | golden-set schema check, 1,200 scenarios, day 145 triage, metamorphic pairs |
| 29.6 | `failure_injection.py` | PR #212 continued: aggregate up, mailed first notices down, blocked at layer two |
| 29.7 | `../fieldkit/fieldkit/pyramid.py` | `slice_verdict` and `MergeGate` excerpt |
| 29.8 | `control.py` | twelve seeded mutants on day 145 and day 152 |
| 29.9 | `streams.py` | six verification streams before and after the second pass moved to another pin |
| 29.10 | `evidence.py` | hash-chained evidence records and the trace matrix |
| 29.11 | `month.py` | days 141 to 170: runs, minutes, dollars, blocks |
| 29.12 | `common.py` | the runner configuration (the listing is simplified) |
| Try It | `tryit.py a|b|c` | margins and set size; drop one stream; the two pyramid gaps |

Library: `fieldkit.pyramid` (v3.6, book layer; package version 0.1.0). Tests: `test_ch29.py` plus
`../fieldkit/tests/test_v36_ch29.py`.
