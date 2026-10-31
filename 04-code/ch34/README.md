# Chapter 34 lab: procurement, legal and the contract

Deterministic stand-in. **No model is called** and no contract is real; every number is computed from `world.py`
and the Chapter 2 margin model (`04-code/ch02`). Stand-in rates are labeled in the outputs.

| Script | Listing | What it shows |
|---|---|---|
| `extract.py v0` | 34.1 | failure first: the v0 extractor prices Caldwell's v3 at 17.9% |
| `dataterms.py` | 34.2 | data maps for Caldwell, Greystone and Pennant, uncovered hops |
| `liability.py` | 34.3 | action tiers and the liability each can carry; reconstructability retrofit cost |
| `readings.py` | 34.4 | four honest readings of "98% accurate" |
| `sl.py` | 34.5, 34.6 | point rules versus designed rules; four customers; zero tolerance; reporting and remedies |
| `pricing.py` | 34.7 | integration tax drawn 10,000 times; fixed, T&M, capped, phased |
| `extract.py check` | 34.8 | honest check of v3: 8 findings, -8.0% |
| `margin.py` | 34.9 | margin by stage, waterfall, what was traded |
| `extract.py v5` | 34.10 | v5 as signed: 0 findings, 48.7% (forecast) |
| `marcus.py` | 34.11 | Greystone redline day 108 to signature day 127 |
| `tryit.py a|b|c` | Try It Yourself | point rule rescue, Harbourline Schedule A, Pennant caps |

Uses `fieldkit.contract` (v4.2). Run `./make_outputs.sh` to regenerate `output/` and run the fieldkit and lab tests (213).
