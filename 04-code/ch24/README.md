# Chapter 24 lab: surface where they work, brain where it is governed

Deterministic stand-in. Nothing here is Caldwell data: the time-in-tool sample, the option scores, the six source
latency profiles, the 14 adjusters and their 3,000 results, the 42 pilot surfaces and every rate are generated or
assumed so that each number in the chapter re-runs exactly. Run `./make_outputs.sh` (uses `/workspace/books/.venv`).

| Listing | File | Output | Section |
|---|---|---|---|
| 24.1 | `split.py` | `output/split.txt` | 24.2 The hybrid: one call per turn |
| 24.2 | `options.py` (with `fieldkit.surface`) | `output/options.txt` | 24.3 Scoring the options and sensitivity |
| 24.3 | `fanout.py` | `output/fanout.txt` | 24.4 Parallel fan-out (failure injection 1: sequential) |
| 24.4 | `identity.py` | `output/identity.txt` | 24.5 Token brokerage (failure injection 2: forwarded token, service role) |
| 24.5 | `rollback.py` | `output/rollback.txt` | 24.6 Reversibility (failure injection 3: client-side flag) |
| 24.6 | `../fieldkit/fieldkit/surface.py` | `output/tests.txt` | 24.8 fieldkit v3.1 |
| Try It | `tryit.py a|b|c` | `output/tryit_a.txt`, `tryit_b.txt`, `tryit_c.txt` | Try It Yourself |

`caldwell.py` holds the fixtures (weights, scores, sources, records). `make_outputs.sh` runs the fieldkit tests only
through v3.1 (`test_v3[2-9]` and later are excluded), so later chapters' work in progress cannot change this output.
