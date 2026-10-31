# Chapter 10 lab: the integration-tax estimator

**Deterministic stand-in.** Every number here comes from synthetic inventories of the book's three composite customers (Caldwell Mutual, Greystone Health, Pennant Logistics) and a seeded triangular simulation (seed 10, 20,000 draws). No customer system, API or model is called. Hours, layouts and owners are illustrative; the code and the method are real.

## Run

```bash
source /workspace/books/.venv/bin/activate
cd 04-code/ch10
bash make_outputs.sh          # writes output/*.txt
pytest -q test_ch10.py ../fieldkit/tests/test_integration.py
```

## Files

| File | What it does |
|---|---|
| `inventories.py` | the three inventories as `fieldkit.integration.Line` objects; `pennant(day, denied)` rebuilds Pennant before and after the API denial |
| `estimate_all.py` | point tax, P10/P50/P90, exposure, lint and hours by source for all three (Table 10.1, Figs 10.1, 10.2) |
| `failure_denied_api.py` | **failure injection**: the TMS status API (P-A2, vendor position) is denied on day 23; an unpriced denial raises `ValueError`; the priced alternative moves Pennant from 1,050 h (tax 2.10) to 1,500 h (tax 3.00) (Fig 10.5) |
| `ranges.py` | simulated ranges and the share of width resting on unconfirmed facts (Figs 10.6, 10.7) |
| `customer_page.py` | the one-page customer estimate (Listing 10.5) |
| `phasing.py` | phase A/B/C for Pennant (Fig 10.8) |
| `tryit.py` | Try It Yourself a, b, c |
| `test_ch10.py` | lab tests |

The estimator itself is `fieldkit/integration.py` (module version 1.4; package version stays 0.1.0).
