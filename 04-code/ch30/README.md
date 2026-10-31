# Chapter 30 lab: small models, fine-tuning and the cost curve on site

Deterministic stand-in data; nothing here is Caldwell's. `world.py` generates documents as bags of words from fixed
seeds; `models.py` holds the two arms: `SmallModel`, a real classifier trained with numpy (standing in for a
fine-tuned small open-weight model), and `frontier()`, a deterministic stand-in for the prompted frontier model whose
error profile is a written assumption. `./make_outputs.sh` regenerates everything in `output/` (about two minutes).

| Listing | File | Output | What it shows |
|---|---|---|---|
| 30.1 | failure_injection.py | output/failure_injection.txt | c06-ft1 wins on the test split and Anne's set, fails on attorney letters |
| 30.2 | compare.py | output/compare.txt | paired comparison, exact McNemar, per-kind accuracy |
| 30.3 | cost.py | output/cost.txt | cost per document, latency, monthly cost, serving options, crossovers |
| 30.4 | fieldkit finetune.py + guard.py | output/guard.txt, output/familiarity.json | familiarity distributions and the absent-class guard |
| 30.5 | instructions.py | output/instructions.txt | the day-146 supplement ruling: one prompt line vs relabel and retrain |
| 30.6 | labels.py | output/labels.txt | learning curve and the crossover with the prompted arm |
| 30.7 | governance.py | output/governance.txt | training-data record, model-risk classification, switch gate |
| Try It | tryit.py a, b, c | output/tryit.txt | missing subclass, your volume, a different absent class |

fieldkit v3.7 adds `fieldkit/finetune.py` (tests in `fieldkit/tests/test_v37_ch30.py`); package version stays 0.1.0.
