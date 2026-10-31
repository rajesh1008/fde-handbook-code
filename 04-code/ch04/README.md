# Chapter 4 lab: Demos Versus Deployments

Run from this folder with the book's virtual environment (`/workspace/books/.venv/bin/python`). Every script
prints the output quoted in the chapter; `make_outputs.sh` writes all of it to `output/`.

| Script | Listing | What it shows |
|---|---|---|
| `deployment.py` | 4.2 | shim importing the readiness model from `fieldkit.deployment` (promoted from this lab) |
| `checklists.py` | | fixtures: the demo as sold, Caldwell day 10 and 12, projected shadow exit, Greystone, Pennant |
| `gap_register.py` | 4.1 | the 11 demo claims against the 25 proofs on day 10 |
| `run_readiness.py` | 4.3 | the demo as sold and Caldwell on day 10 through the same checklist |
| `failure_no_owner.py` | 4.4 | failure injection: a system that scores "ready" with no owner |
| `promise_rewrite.py` | 4.5 | lint Graham's four promises; rewrite them as deployment claims |
| `oversight.py` | 4.6 | oversight profile on a seeded stand-in: fix reliability, report review share |
| `rebaseline.py` | 4.7 | deal sheet, field estimate and the day-12 re-baselined plan |
| `tryit.py` | Try It | exercises a, b, c |
| `test_ch04.py` | | tests |

The oversight data is a **seeded stand-in, not Caldwell data**. Synthetic data proves the plumbing, not
the accuracy. Day-2 demo scores are carried forward from Chapter 3.
