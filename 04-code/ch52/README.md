# Chapter 52 lab: rerun Caldwell's evaluation suite on a model two generations newer

Deterministic stand-in. No model calls. Model behavior is a seeded function of (version, document, field) in
`world.py`; `gm-2026-05-14` is Caldwell's pin (Chapter 24), `gm-n1` and `gm-n2` are lab labels for one and two
generations later. Failure injection: gm-n2 states more confidence near its error boundary (the suite's layer 3
catches it) and writes shorter intake summaries that drop dispute statements (no layer scores the summary).

| Script | Listing | What it shows |
|---|---|---|
| rerun.py | 52.1, 52.2 | before/after on gold-set-300 test, pyramid verdicts for gm-n1 and gm-n2 |
| recalibrate.py | 52.3 | router calibrator refit, reliability bins, merge after refit |
| escape.py | 52.4, 52.5 | the summary change escapes; the added layer 2 slice blocks it |
| absorb.py | 52.6 | 30 Caldwell work items by owner, 2026 and 2029 forecast |
| tryit.py a/b/c | Try It Yourself | sign-off on gm-n1; no layer 3; half the calibration data |

Run `./make_outputs.sh`. Outputs land in `output/`; tests in `output/tests.txt`. fieldkit is used unchanged (0.1.0).

Listing map (text order): 52.1-52.2 rerun.py, 52.3 recalibrate.py, 52.4 suite.py l3, 52.5 absorb.py, 52.6-52.7 escape.py; Try It: tryit.py a/b/c.
