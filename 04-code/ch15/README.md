# Chapter 15 lab: Shipping When Access Takes Three Months

Runs with the book's fieldkit (v2 modules added in this chapter: `escalation.py`, `datareadiness.py`,
`histories.py`, and the `ball` field on `AccessRequest`). No model or API key is needed: every stage is
deterministic code, and the plumbing check is labeled as a stand-in for the model step.

| Script | Listing | What it shows |
|---|---|---|
| day47_status.py | 15.1 | the day-47 tracker and the Chapter 3 readiness check |
| escalate_day47.py | 15.2 | dated level-1 escalations generated from the tracker |
| register_card.py | 15.3 | the field-level register entry and its assessment |
| failure_key_removed.py | 15.4 | failure injection: the delivery with `claim_id` removed |
| plumbing_check.py | 15.5 | seven stages on synthetic and real files |
| greystone_day112.py | 15.6 | the second customer, days 40, 61, 104 and 112, with the audit |
| ladder_dates.py | 15.7 | rung dates for four customers (Signature 6 data) |
| weekly_progress.py | 15.8 | what shipped in each week before data |
| tryit.py a/b/c | Try It Yourself | escalation on day 60, a do-not-deliver field, which delay set day 112 |

```
./make_outputs.sh            # regenerates output/*.txt
python -m pytest -q          # checks outputs are reproducible
```
