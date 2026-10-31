# Chapter 39 lab: the shadow evaluation suite and the Shadow Exit rule

**Deterministic stand-in.** Seeded generators reproduce Caldwell's Chapter 31 shadow window document by
document (2,410 documents, 2,121 agreements, 289 adjudicated disagreements, routing 1,494 / 714 / 189 / 13)
and a 20 clinic-day Greystone shadow of prior-authorization drafts. No model calls, no customer data.

| File | What it does |
|---|---|
| `world.py` | the shadow window, the holiday-mix failure injection, Greystone's window |
| `suite.py` | Signature 14 funnel, adjudication, the six streams before output, the Shadow Exit rule (G-1 to G-8) |
| `run.py` | prints each listing: `funnel`, `adjudication`, `streams`, `gate`, `holiday`, `greystone` |
| `duration.py` | four stopping rules on 2,000 simulated windows (fixed 5, fixed 10, until stable, the exit rule) |
| `live.py` | conditions C-1 and C-2, the blind 5% sample, the first Exhibit E month |
| `tryit.py` | the three Try It Yourself exercises |
| `test_ch39.py` | invariants; `make_outputs.sh` runs these plus the full fieldkit suite |

Run `./make_outputs.sh`. fieldkit is used as it stands (shadow.keyed_id, evals.wilson, sampling.allocate);
this chapter adds no fieldkit module.
