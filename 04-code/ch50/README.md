# Chapter 50 lab: Harbourline Bank credit memo (deterministic stand-in)

Every customer value in this folder is synthetic: the Northgate statement, the 600 shadow scores, the
classification, the packs and the traces are constructed so the numbers are the same every run. No model is
called. Run `./make_outputs.sh`; outputs land in `output/` and the tests (lab plus fieldkit) in `output/tests.txt`.

| File | What it shows |
|---|---|
| world.py | formats, standards, the statement, ratio definitions, covenants, components, calendar |
| memo.py, spread_run.py | deterministic spread, ratios, covenants and lineage; a balance sheet that does not foot is quarantined |
| draft_run.py | the drafter with four injected failures and the three checks that catch them |
| pyramid_run.py | the evaluation suite by layer, and where each injection is caught |
| classify.py | two readings of the model-risk classification test |
| committee.py | submission one (returned) and two (approved), pack lint, computability, validator questions, gates |
| execpack.py | the accountable executive's eight artifacts at day 118 and day 171 |
| gateway.py | every model call through the bank gateway, pinned, unstreamed |
| boundary.py | release one in force; release two proposed, not in force |
| shadowrun.py | 600 drafts against officers' memos, per standard, and the sample-size comparison |
| tryit.py | Try It Yourself a, b, c |

Uses fieldkit 0.1.0 unchanged (gates, modelrisk, lineage, actions, pyramid).
