"""Listing 47.1: what repeats across twenty engagements, by name and by shape."""
import _paths  # noqa: F401
from fieldkit.playbooks import recurrence
from world import INSTANCES
rows = recurrence(INSTANCES)
print(f"{'component':38} {'eng':>3} {'shapes':>6} {'hours':>6}  {'by name':9} {'by shape'}")
for r in rows:
    flag = "  <- differs" if r["by_name"] != r["by_shape"] else ""
    print(f"{r['component']:38} {r['n']:>3} {r['variants']:>6} {r['hours']:>6}  {r['by_name']:9} {r['by_shape']}{flag}")
tot = {k: sum(r["hours"] for r in rows if r["by_shape"] == k) for k in ("platform", "playbook", "bespoke")}
print("\nbespoke hours by class (shape rule):", ", ".join(f"{k} {v:,}" for k, v in tot.items()))
print("rule: platform if built at >= 8 engagements with shapes/engagements <= 0.25; playbook if >= 3 and <= 0.50")
