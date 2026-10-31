# Chapter 41 lab: the hand-over test

The customer team runs a failure drill alone; Northlight observes with hands off. Failure injection: alert rule A-07
(gateway 401 rate) routed to a Northlight address, `nl-caldwell-alerts@northlight.example`.

All data are a **deterministic stand-in** (`world.py`); no model calls. Regenerate everything the chapter quotes:

    ./make_outputs.sh

| Script | What it prints |
|---|---|
| `readiness.py caldwell-before|caldwell-after|pennant` | 20 hand-over items, naive and gated scores, single-person drops |
| `routes.py v1|v2|pennant` | alert routing check (customer-owned destinations) |
| `runbooks.py v1|v2` | runbook lint RB1 to RB6 |
| `raci.py v1|v2` | one customer accountable per activity |
| `reference.py v1|v2` | engagement reference reading paths and gaps |
| `training.py` | competence checks by session |
| `drill.py 1|2|pennant|pennant-rerouted` | the drill timeline and verdict |
| `tryit.py a|b|c` | Try It Yourself exercises |

Library code: `../fieldkit/fieldkit/handover.py` (fieldkit v5, book layer; package version 0.1.0).
