# Chapter 48 lab: twelve months across three customers

A deterministic stand-in. Every customer, day and count is the book's illustrative Northlight world (Caldwell,
Pennant, Greystone); no live model is called. The arithmetic, the gates and the checks are real code built on
`fieldkit` (version 0.1.0, unchanged by this chapter).

| Script | What it shows |
|---|---|
| `world.py`, `calendar48.py` | one engagement-day calendar; production months; month nine at all three |
| `renewals.py` | the v0 renewal pack against each customer's own list (the Caldwell runbook sidebar) |
| `upgrades.py` | three customers x three model versions through `liveops.upgrade_gate`; the pooled v0 gate |
| `clocks.py`, `incidents.py` | the clock register; the four incidents after month six with ttd/tta/ttm |
| `freeze.py` | **failure injection**: a change freeze that blocks a critical security fix (v0 and v1) |
| `turnover.py` | ownership coverage on both sides before and after departures |
| `board.py` | the quarterly board scoreboard, per customer; writes `output/data.json` for the figures |
| `tryit.py a|b|c` | the three Try It Yourself exercises |

Run `./make_outputs.sh` with `/workspace/books/.venv` active. It rewrites `output/*.txt` and runs this lab's tests
plus the full fieldkit suite into `output/tests.txt`.
