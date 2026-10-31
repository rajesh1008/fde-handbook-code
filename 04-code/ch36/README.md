# Chapter 36 lab: red-teaming with the customer's security team

Deterministic stand-in. No model is called. Whether the stand-in drafting agent follows an instruction is recorded on
each attack in `world.py` (`follows`, `style`); the guardrail rules (O-22, A-06, A-10), the tool allow-list and
the panel control are real code that runs on what the stand-in produces. Suite v2 is the day-124 rule set and v3 the
day-128 set from Chapter 28. All numbers are stand-ins, not Greystone measurements.

Run everything: `./make_outputs.sh` (writes `output/*.txt`, runs the tests). Uses fieldkit book layer v4.4
(`fieldkit/redteam.py`).

| Script | What it shows | Output |
|---|---|---|
| `campaign.py --coverage` | attacks per taxonomy class, the two untried classes | `coverage.txt` |
| `campaign.py --suite v2` | the day-126 run, both oracles | `campaign-v2.txt` |
| `campaign.py --suite v3 --oracle action` | the day-128 rerun scored the Chapter 28 way: 0 of 20 | `campaign-v3-action.txt` |
| `campaign.py --suite v3` | the same rerun scored on every channel: RT-07 reached | `campaign-v3.txt` |
| `inject.py` | failure injection: one instruction in a benign referral's OCR text reaches the draft | `inject.txt` |
| `exfil.py` | output channels that can leak, v2 against v3 | `exfil.txt` |
| `agency.py` | tool scope, refused calls in the audit record, token lifetime | `agency.txt` |
| `triage.py [--naive]` | twenty report items to eleven findings | `triage*.txt` |
| `retest.py` | closure rule, burndown, validity of the result | `retest.txt` |
| `tryit.py a|b|c` | the chapter's three Try It Yourself exercises | `tryit-*.txt` |
