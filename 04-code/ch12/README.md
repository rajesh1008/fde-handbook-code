# Chapter 12 lab: the engineering half of a bid

Deterministic stand-in. No model calls; the extractor is rules, not a model. Harbourline Bank is fictional, and every RFP
question, platform standard, clarification and response sentence in `harbourline.py` was written for this lab.

| Script | What it shows | Output |
|---|---|---|
| `triage_run.py` | 200 RFP questions routed to engineering, joint or sales; three misroutes | `output/triage_run.txt` |
| `crosswalk_run.py` | 47 platform standards, drafts v0.6 and v1.0 | `output/crosswalk_run.txt` |
| `extract_run.py` | commitments and estate claims in the submitted response, with statuses and lint | `output/extract_run.txt` |
| `failure_contradiction.py` | failure injection: a gateway capability stated as a customer fact, contradicted by CL-17 | `output/failure_contradiction.txt` |
| `panel_run.py` | the sixty-question bank against what the panel asked | `output/panel_run.txt` |
| `five_moves_run.py` | a strong and a weak oral answer checked for the five moves | `output/five_moves_run.txt` |
| `safety_net_run.py` | the one page taken into the oral defense | `output/safety_net_run.txt` |
| `after_award.py` | commitments moved into the open-decision register; two renegotiated | `output/after_award.txt` |
| `tryit.py 1/2/3` | Try It Yourself exercises | `output/tryit_N.txt` |

Run `./make_outputs.sh` to regenerate every capture, `pytest test_ch12.py` for the lab tests, and
`pytest ../fieldkit/tests/test_bid.py` for the module (`fieldkit.bid`, book layer v1.5; package version 0.1.0).
