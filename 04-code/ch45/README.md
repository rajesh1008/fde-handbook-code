# Chapter 45 lab: the hiring rubric and the debrief generator

Deterministic stand-in. The loops, scores, transcripts and calibration ratings are fixtures written for this lab
and shaped like Northlight's hiring records; there is no candidate data and no model call. `bank.py` reads the
book's own `02-manuscript/interview-bank.md`, so its counts are a snapshot of the bank when it is run.

    ./make_outputs.sh          # regenerates every output the chapter quotes and runs the tests

| Script | What it shows |
|---|---|
| `loop.py v0|v1` | coverage matrix and lint; v0 is the failure injection: a loop whose rounds all test build |
| `discovery.py c214|c231` | the discovery exercise scored from its event log against eleven hidden facts |
| `whiteboard.py c214|c231` | "classify this workflow" graded against the key; over-modeled and unsafe steps |
| `takehome.py v0|v1` | the take-home checked against an agent-only baseline |
| `debrief.py c214|c231|c236|c214-v0` | the debrief written from independent scores, with refusals and flags |
| `calibrate.py before|after` | interviewer drift on six recorded sessions |
| `moves.py weak|strong` | the five-move check on a spoken answer |
| `bank.py` | the interview bank by round and competency, and a ten-day study plan |
| `tryit.py a|b|c` | the three Try It Yourself exercises |

The module is `fieldkit/hiring.py` (fieldkit v5.3); its tests are `fieldkit/tests/test_v53_ch45.py`.
