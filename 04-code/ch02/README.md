# Chapter 2 lab: the engagement margin model

Plain Python 3.10+, no third-party packages (pytest for the tests). No model calls: this lab is arithmetic,
so the deterministic stand-in convention is not needed. All money is US dollars and every figure is
illustrative, belonging to the fictional Northlight AI and its three customers.

| File | What it does | Output |
|---|---|---|
| `margin.py` | Contract, Plan, year-one P&L, billing-basis guard, pilot-month cost, renewal bands, gate days | |
| `contracts.py` | Three contracts; a deal-sheet plan and a field-estimate plan each (imports `fieldkit` names) | |
| `run_margin.py` | Listing 2.3 (with the `margin.py` excerpt): margins, the gap, and the stuck-pilot comparison | `output/run_margin.txt` |
| `hours_ledger.py` | Listing 2.1: Caldwell days 1-47 rebuilt into seven buckets, blocked hours traced via `fieldkit` | `output/hours_ledger.txt` |
| `integration_tax.py` | Listing 2.2: Pennant margin as integration hours per model hour rises | `output/integration_tax.txt` |
| `failure_tm_on_fixed.py` | Listing 2.4: failure injection, T&M assumed on a fixed-price deal, then the guard | `output/failure_tm_on_fixed.txt` |
| `pilot_cost.py` | Listing 2.5: cost of one more pilot month and the nine-month rule | `output/pilot_cost.txt` |
| `gate_timeline.py` | Listing 2.6: planned day per gate; feeds Signature figure 1 | `output/gate_timeline.txt` |
| `try_it.py 1/2/3` | Try It Yourself variations | `output/try_N.txt` |

Run everything:

    for s in run_margin hours_ledger integration_tax failure_tm_on_fixed pilot_cost gate_timeline; do python3 $s.py; done
    for v in 1 2 3; do python3 try_it.py $v; done
    python3 -m pytest -q test_ch02.py

The loaded rate of $150 per FDE hour is an assumption: a base salary near the advertised median for the
role in a hiring snapshot of September 2026 (about $188,000), times 1.3 for benefits, tax and equipment,
spread over about 1,650 hours a year that land on customer accounts. Change `LOADED_RATE` to your own.
