# Chapter 27 lab: confidence, calibration and routing at Caldwell Mutual

Deterministic stand-in. Nothing here is Caldwell data and nothing calls a model: documents, fields, the model's
stated confidence, the evidence signals, the expert labels and the reviewers' behavior are generated from hashes in
`world.py` so that every number in the chapter re-runs exactly. Run `./make_outputs.sh` (uses `/workspace/books/.venv`).

| Listing | File | Output | Section |
|---|---|---|---|
| 27.1 | `failure_injection.py` | `output/failure_injection.txt` | 27.1 Router v0 on the first real sample (failure injection) |
| 27.2 | `resolution.py` | `output/resolution.txt` | 27.1 What a confidence score is and is not |
| 27.3 | `calibrate.py` | `output/calibrate.txt` | 27.2 Calibration against the expert-scored set |
| 27.4 | `thresholds.py` | `output/thresholds.txt` | 27.3 Bands, thresholds and who set them |
| 27.5 | `floor.py` | `output/floor.txt` | 27.4 No recommendation below the floor |
| 27.6 | `failclosed.py` | `output/failclosed.txt` | 27.5 Fail closed |
| 27.7 | `notindocs.py` | `output/notindocs.txt` | 27.6 Evidence is not probability (Chapter 23's index) |
| 27.8 | `audit.py` | `output/audit.txt` | 27.7 Post-review error |
| 27.9 | `drift.py` | `output/drift.txt` | 27.8 Re-calibration after drift |
| 27.10 | `../fieldkit/fieldkit/routing.py` | `output/tests.txt` | 27.10 fieldkit v3.4 |
| Try It | `tryit.py a|b|c` | `output/tryit.txt` | Try It Yourself |

Sets: `synthetic-2000` (Northlight's synthetic set, router v0, day 120), `gold-heldout` (201 held-out documents of
gold-set-300, day 122), `cal-600` (600 shadow documents scored by Tom Whitfield and adjuster B, days 124 to 131;
even-numbered documents fit, odd-numbered check), `audit-400` (routed review days 136 to 139, audited day 140),
`week-N` (drift rehearsal). Reviewer rates in `world.SCRATCH` and `world.MISS` are assumptions, not measurements.
`notindocs.py` reuses Chapter 23's library and Anne Kessler's 150 questions.
