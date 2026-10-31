# Chapter 33 lab: model risk and the customer's governance

Deterministic stand-in. **No model is called**: the provider model in `evidence.py` is a seeded stand-in that
reproduces Chapter 26's field accuracy; every other number is computed from the data in `world.py`.

| Script | Listing | What it shows |
|---|---|---|
| `classify.py` | 33.1 | failure first (the system as one model, both ways), then the component test on days 82, 132, 153 and a second customer's reading |
| `pack.py v1|v2` | 33.5 | the model-risk pack generated from evaluation-suite evidence; writes `output/pack_v*.md` |
| `monitor.py` | 33.6, 33.7 | failure injection: two of six metrics need Northlight; the fix; M1 recomputed by Caldwell |
| `evidence.py` | 33.3, 33.4 | repeat-run stability, sensitivity by condition, limits register |
| `validator.py` | 33.8 | the validator's 14 questions: evidence, translation, boundary |
| `review.py` | 33.9 | timeline, citation audit, decision and conditions |
| `pyramid_run.py` | 33.2 | the lab through the Chapter 29 pyramid runner: the injection is caught at layer 3 |
| `tryit.py a|b|c` | Try It Yourself | three variations |

`modelrisk.py` is the chapter draft of `fieldkit.modelrisk` (v4.1); `mr.py` imports fieldkit's copy once promoted.
Run `./make_outputs.sh` to regenerate `output/` and run the tests.
