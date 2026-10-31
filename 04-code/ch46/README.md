# Chapter 46 lab: price the next engagement from the last three

Deterministic stand-in. All data lives in `world.py`; nothing calls a model or a live system.

    ./make_outputs.sh      # regenerates output/*.txt and runs the tests

| Script | What it prints |
|---|---|
| actuals.py closed/all | hours ledgers and calibration factors from closed buckets |
| reserve.py | integration misses and the reserve rule |
| forms.py | fixed, reserve, capped T&M and outcome forms across misses |
| phases.py | margin by phase, to date |
| waterfall.py | Signature 17 data for Caldwell year one |
| playbook.py naive/checked/matrix | playbook credit with and without the transfer check |
| price_next.py naive/checked | the next insurer's price and scenarios |
| independent.py | a firm of one: reserve, slip and liability |
| tryit.py a/b/c | the chapter's three exercises |

Failure injection: PB-04 assumes `claims_core_doc_api`, which the next insurer lacks.
