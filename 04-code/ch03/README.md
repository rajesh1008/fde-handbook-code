# Chapter 3 lab: the first week at Caldwell, done wrong

Python 3.10+, standard library only (the figures also need matplotlib). Run from this folder.

| File | What it is |
|---|---|
| `caldwell_docs.py` | the ten documents Anne Kessler brought to the day-two demo, with her corrections; Northlight's ten demo forms |
| `demo_extract.py` | **DEMO MODEL STAND-IN (deterministic; no model called).** Reproduces the demo's behavior with fixed rules, because the build machine has no model keys and a model's answers vary between runs |
| `scoring.py` | field-level scoring and a first-pass cause for each miss |
| `day2_demo_score.py` | Listing 3.1: the failure injection. 98% on the demo set, **58%** on Caldwell's ten |
| `caldwell_week.py` | days 1 to 5 recorded in a fieldkit v0 engagement repository |
| `day5_status.py` | Listing 3.2: audit the hand-written day-5 deck, lint the repo, generate the status |
| `day6_promises.py` | Listing 3.3: decision D-4, the four kickoff promises rewritten with a verifier each |
| `tryit.py` | Try It Yourself a, b, c |
| `output/` | the captured outputs printed in the chapter, and the saved engagement repository |

```
python day2_demo_score.py   # -> output/day2_demo_score.txt
python day5_status.py       # -> output/day5_status.txt, output/caldwell-repo/
python day6_promises.py     # -> output/day6_promises.txt
python tryit.py a|b|c       # -> output/tryit_*.txt
```

fieldkit v0 lives in `../fieldkit/fieldkit/engagement.py` with tests in `../fieldkit/tests/test_engagement.py`.

The chapter's figures are drawn by `../../03-figures/src/ch03/figures.py` from this lab (render command in its docstring).
