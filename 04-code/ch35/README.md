# Chapter 35 lab: data protection across three jurisdictions

Runs on the deterministic, labeled stand-in in `world.py` (every person and record is invented). No model calls.

- `datamap.py v1|v2`: generate Greystone's data map from deployed configuration, compare with the drawn map, lint for HIPAA, digest for approval.
- `pii_scan.py before|after`: the failure injection. The provider's stored-request log kept referral fragments; patterns alone find about half; the known-value scan finds the rest; the day 124 rescan is clean.
- `regimes.py`: which regime applies to each customer, the lint over each map, retention by customer.
- `erasure.py v1|v2`: trace one Pennant consignee through every store and show how each store lets them go.
- `minimum.py`: fields the drafting service read against the fields the task needs.
- `tryit.py a|b|c`: Try It Yourself.
- `make_outputs.sh`: regenerates `output/` and runs the tests (lab plus the fieldkit suite).

fieldkit module: `fieldkit/privacy.py` (v4.3). Which law applies, and whether a finding is acceptable, is the customer's decision.
