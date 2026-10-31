# Chapter 37 lab: the gate tracker and the accountable executive's pack

Deterministic stand-in. The Caldwell numbers come from the Chapter 31 lab output (rc-1 on gold-heldout, the shadow window
on days 142 to 153, audit-shadow-400). Items marked STAND-IN in `world.py` (the draft packet's non-customer evidence and
the model-risk component count) are illustrative. No customer data appears anywhere.

Run everything:

    ./make_outputs.sh          # writes output/*.txt and runs the fieldkit and lab tests

| Script | Output | What it shows |
|---|---|---|
| `tracker.py aggregate` | `tracker_aggregate.txt` | failure injection: the Shadow Exit packet passes on the aggregate |
| `tracker.py perclass` | `tracker_perclass.txt` | the same packet judged per class: blocked (fax below, mail not shown) |
| `tracker.py terms` | `tracker_terms.txt` | day 157 exit terms: fax excluded, mail accepted, two dated conditions |
| `tracker.py evidence` | `tracker_evidence.txt` | model confidence, component tests, fluent summaries and logs refused |
| `tracker.py order` | `tracker_order.txt` | effective gate days; a later gate is held while an earlier one is open |
| `classes.py` | `classes.txt` | per-class field accuracy at p7 and rc-1 with Wilson intervals |
| `pack.py logs`, `pack.py day157` | `pack_logs.txt`, `pack_day157.txt` | the eight artifacts on day 141 and day 157 |
| `residual.py v1`, `residual.py v2` | `residual_v1.txt`, `residual_v2.txt` | residual-risk lint: 3 problems, then 0 |
| `stack.py` | `stack.txt` | the five-gate stack and who is accountable at each customer |
| `tryit.py a`, `b`, `c` | `tryit_*.txt` | Try It Yourself: bar sweep, sample size, mix |

The library is `fieldkit.gates` (v4.5), in `04-code/fieldkit/fieldkit/gates.py`. The package version stays 0.1.0.
