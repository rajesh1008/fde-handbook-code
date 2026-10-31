# Chapter 43 lab: managed service or hand-over, the year after

Deterministic stand-in. No model calls, no network. Same data, same numbers on every run.

* `world.py` loads the start states from the Chapter 41 and Chapter 42 labs (Pennant 0.80 at production day 70,
  Caldwell 0.90 at day 183) and defines the operating paths, the managed-service runbooks v0 and v1, and the
  asset-owner register. Fees, hours, practice schedules, events and renewal probabilities are stand-in values.
* `model.py pennant|caldwell`: the two-year cost and dependency model for every path, both sides.
* `exitcheck.py v0|v1`: Chapter 41's runbook lint against the exit lint (failure injection: runbooks only
  Northlight staff can execute).
* `drill.py v0|v1`: Nadia Brooks runs MS-RB-01 at night as if Northlight were gone.
* `retainer.py`: retainer pricing from an hours band, and what unlimited rollover does to margin.
* `yearafter.py`: Pennant and Caldwell at month 12.
* `tryit.py a|b|c`: the chapter's Try It Yourself exercises.
* `make_outputs.sh` regenerates `output/` and runs `test_ch43.py` plus the full fieldkit suite.

fieldkit v5.2 adds `fieldkit/service.py`; the package version stays 0.1.0.
