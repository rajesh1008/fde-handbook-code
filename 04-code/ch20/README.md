# Chapter 20 lab: one evaluation suite, three estates

**Deterministic stand-in.** Nothing here calls AWS, Azure or Google Cloud. `sim_clouds.py` simulates the three customers' estates: a regional model catalog with release lags, each cloud's native call shape (Caldwell's gateway, Azure named deployments with `api-version`, a Google Cloud regional endpoint), a network that answers only the private path, log sinks, and credentials that rotate. Documents, gold sets, accuracies, prices and volumes are synthetic and seeded, so every run prints the same numbers. The 85% pass line, Greystone's 2,400 and Pennant's 19,500 documents a month, and every rate in `cost_estate.py` are stand-ins. Real figures come from each customer's own records.

**Failure injection.** Pennant's EU project runs in `europe-west4`, which does not yet offer the pinned `extract-2026-04`. A deployment that asks for `extract@latest` gets `extract-2026-01` and the suite still passes. `fieldkit.estates.resolve_pin` refuses the substitution and lists the three options. Greystone's first deploy comes from Northlight's sandbox template (static key, public access, missing tags, an old `api-version`). An automated IaC repair loop then drops a diagnostics block while it fixes public access.

Run everything with `bash make_outputs.sh` (venv: `/workspace/books/.venv`). Outputs land in `output/`.

| Script | What it shows | Output |
|---|---|---|
| `region_drift.py` | where the pin is offered; the naive `latest` deployment that passes; the item-level comparison; `resolve_pin` refusing; Greystone's failover region | `output/region_drift.txt` |
| `parity.py` | the fourteen parity checks on each estate, by engagement day, to 14/14 everywhere | `output/parity.txt` |
| `iac_check.py` | each estate rendered in the customer's own IaC tool and scanned by the customer's rules; the repair loop with a partial rescan versus a full rescan | `output/iac_check.txt` |
| `cost_estate.py` | cost per scored document per estate: model calls from the call records plus fixed estate cost spread over volume | `output/cost_estate.txt` |
| `loc.py` | code lines shared by every estate against code lines specific to one | `output/loc.txt` |
| `tryit.py a|b|c` | the three Try It Yourself exercises (widen the pin's regions; add a fourth, on-premises estate; cost by volume) | `output/tryit_*.txt` |
| `test_ch20.py` | five tests of the lab's claims | `output/tests.txt` |

Supporting modules: `adapters.py` (the only cloud-specific code: one adapter per estate behind five ports), `suite.py` (the evaluation suite, unchanged across estates), `estate_configs.py` (what the customer reads and signs), `deploy.py` (deploys one configuration and collects evidence). The library code is `fieldkit/estates.py` (fieldkit v2.5, book layer; the package version stays 0.1.0).
