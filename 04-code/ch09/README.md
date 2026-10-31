# Chapter 9 lab: deterministic first

**Stand-in notice.** No model provider is called anywhere in this lab. Prices, latencies, model error rates and
the "model" in `ltv_failure.py` are deterministic, seeded stand-ins whose parameters are printed in the source.
The tree, the parsers, the routing rules, the loan-to-value service and all arithmetic are real code.

| File | Listing | What it shows |
|---|---|---|
| `classify_all.py` | 9.1 | Signature 3 applied to Caldwell (12 steps), Greystone (25, from ch14) and Pennant (15, proposed) |
| `compounding.py` | 9.3 | route success when every step is model-decided |
| `intake_paths.py` | 9.2 | the tree across Caldwell's eleven intake paths; the finance-cage refusal |
| `cost_run.py` | 9.6 | cost and latency per document, volume weighted, against the demo agent |
| `accuracy_run.py` | 9.7 | loud versus silent failure by class on 400 synthetic documents |
| `ltv_failure.py` | 9.4, 9.5 | failure injection: a model computes LTV across three documents; the service that replaces it |
| `frontier_steps.py` | | cost against frontier steps remaining |
| `tryit.py 1/2/3` | | the three Try It Yourself exercises |

The tree itself is `fieldkit.autonomy` (AUTONOMY_VERSION 1.3), Listing 9.8. Run `pytest -q` here and in `../fieldkit`.
Outputs captured from real runs are in `output/`.
