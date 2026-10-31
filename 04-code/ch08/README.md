# Chapter 8 lab: the scoping document as code

Deterministic stand-in. No model is called and no customer data is held; Caldwell Mutual's documents, scorers'
marks and volumes are synthetic, built to be consistent with the running project (Chapter 6 readout, day 26).

| File | What it does |
|---|---|
| `scoping.py` | the module (candidate for `fieldkit.scoping`, book layer v1.2): Claim, Criterion, DocType, Exclusion, OpenDecision, ScopeDoc with lint, strips, coverage, register and evaluation suite export |
| `caldwell_scope.py` | Caldwell's signed scope v1.0 (day 28), draft v0.3 (day 24) and the earlier documents |
| `generate_scope.py` | prints the signed scope with claim-status strips (Listing 8.1) |
| `calibration.py` | three scorers on 60 synthetic documents, 14 fields, two rounds; per-field kappa |
| `failure_lint.py` | failure injection: criteria with no measurement, a status upgraded by repetition |
| `laundering.py` | traces the proposal that became a fact, then repairs it |
| `volumes.py` | volumes, latency and cost, each with its basis |
| `register_export.py` | the open decisions as engagement decision-register records (fieldkit.cadence) |
| `suite_export.py` | the criteria as evaluation-suite configuration |
| `tryit.py` | Try It Yourself a, b, c |
| `test_ch08.py` | pins |

Run everything: `./make_outputs.sh` (writes `output/*.txt`). Python 3.11+, standard library only (pytest for tests).
