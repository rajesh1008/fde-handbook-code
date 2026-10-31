# Chapter 44 lab: staffing, hiring and the FDE career

Deterministic stand-in data for Northlight's FDE function over twelve months (world.py). No network, no model calls.
Uses fieldkit as it stands (cadence.bus_factor and the Ch29 pyramid runner); no fieldkit change in this chapter.

| Script | What it does | Output |
|---|---|---|
| headcount.py | joins, leavers, average headcount, annualized attrition | output/headcount.txt |
| profile.py | eight-competency profile scored 0 to 3, holders, single holders, bottleneck flags | output/profile.txt |
| rubric.py | four exercises E1 to E4, floors on discovery, build, communication, judgment; old loop vs new loop replay | output/rubric.txt |
| calibrate.py | three raters, eight sessions, pairwise Cohen's kappa before and after anchors | output/calibrate.txt |
| pyramid_run.py | the hiring loop tested as a system with seeded defects at four layers | output/pyramid_run.txt |
| pods.py | solo, two pods, two pods with shared evaluation lead: needs met, single holders, coordination hours, rota depth | output/pods.txt |
| rotation.py | load index (travel/10 + pages/4 + 0.25 per month beyond six) and red months; policy replay | output/rotation.txt |
| ladder.py | criteria-based ladder check on packets, gap named | output/ladder.txt |
| learn.py | skill half-life times use ranking | output/learn.txt |
| portfolio.py | independent practitioner portfolio and runway model, including a single-client failure | output/portfolio.txt |
| tryit.py | Try It Yourself a, b, c | output/tryit_a.txt, tryit_b.txt, tryit_c.txt |

Run: `bash make_outputs.sh` (regenerates every output and runs `pytest`; result in output/tests.txt).
