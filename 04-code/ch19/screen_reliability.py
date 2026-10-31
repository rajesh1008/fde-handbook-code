"""Listing 19.4: two facts about screens. (1) Per-step reliability compounds: a seeded simulation of a
screen task of n steps, 20 runs at a time, ten times. (2) When a vendor patch adds a field, a script that types
by position writes garbage that the test system accepts; a fingerprinted connector stops at the first screen.
The agent numbers are a model of compounding, not a measurement of any product."""
import random
import _paths  # noqa: F401
from fieldkit.connectors import ScreenChanged
from adapter import ClaimsCoreTarget
from sim import ClaimsCore, caldwell_sample

print("end-to-end success for a task of n steps at per-step success p (p**n)")
print("  n   p=0.99  p=0.97  p=0.95")
for n in (6, 14, 30):
    print(f" {n:2}   {0.99**n:6.2f}  {0.97**n:6.2f}  {0.95**n:6.2f}")
rng = random.Random(7)
batches = [sum(all(rng.random() < 0.97 for _ in range(14)) for _ in range(20)) for _ in range(10)]
print(f"14 steps at 0.97, ten batches of 20 runs: passes {batches} (min {min(batches)}, max {max(batches)})")

recs = [d for d in caldwell_sample() if d["kind"] == "fnol"][:40]
app = ClaimsCore("uat", patched=True)
wrong = 0
for d in recs:                                   # the positional script: values in the order they used to sit
    vals = dict(zip(app.labels("FNOL-1"), [d["policy_no"], d["claimant"], d["loss_date"], d["loss_type"], d["doc"]]))
    ok, cid, _ = app.submit("FNOL-1", vals, d["doc"])
    wrong += app.claims[cid].get("Loss Date") != d["loss_date"]
print(f"\npatched FNOL-1, positional script: {len(app.claims)} of {len(recs)} accepted by UAT, "
      f"{wrong} with the wrong value in Loss Date")
t = ClaimsCoreTarget(ClaimsCore("uat", patched=True))
try:
    t.write(recs[0], recs[0]["doc"])
except ScreenChanged as e:
    print(f"patched FNOL-1, fingerprinted connector: 0 written, stopped: {e}")
