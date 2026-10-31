# Chapter 38 lab: Greystone's security review, three passes

Deterministic stand-in. Every number is generated from `world.py`; none is a Greystone measurement.
Pass 1 (day 103) is loaded unchanged from `04-code/ch32/world.py`. Uses fieldkit as it stands (no new layer).

| script | what it shows |
|---|---|
| `evidence_set.py` | the complete evidence set at pass 3: link check, evidence check (39 of 41 at 08:00, 41 of 41 after the egress rerun), claims per pass, reuse, expiry |
| `passes.py` | the three passes: 29/12, 37/4, 41/0 with 2 residual risks accepted; burn-down to day 129 |
| `changes.py` | **failure injection**: answers that changed since the last review; naive carry-forward against fingerprints and falsifiers. `--inject` adds an unannounced edit to SQ-28 |
| `hardest5.py` | the hardest five questions with their defeaters and how each was closed |
| `residual.py` | residual risk register and its lint; `--inject` runs a vendor-written acceptance |
| `signoff.py` | the Greystone gate stack on days 103, 121, 129, 130; conditions; projection against actual |
| `tryit.py a|b|c` | the three Try It Yourself exercises |

Run `./make_outputs.sh` (writes `output/*.txt`, runs `test_ch38.py` and the fieldkit suite).
