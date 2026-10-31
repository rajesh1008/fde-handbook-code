"""Listing 47.11: anchor changes as each customer saw them, before and after the anchor rule."""
import _paths  # noqa: F401
from fieldkit.playbooks import continuity
from world import CHANGES_BEFORE, CHANGES_AFTER, name
for label, ch in [("months 13 to 15, no anchor rule", CHANGES_BEFORE), ("months 16 to 18, anchor rule", CHANGES_AFTER)]:
    res = continuity(ch)
    bad = sum(len(r["bad"]) for r in res.values())
    print(f"{label}: {len(ch)} anchor changes at {len(res)} customers, {bad} below 10 overlap days or 30 notice days")
    for c, r in sorted(res.items()):
        for mth, old, new, ov, no in r["bad"]:
            print(f"  {name(c):10} month {mth}: {old} to {new}, overlap {ov} d, notice {no} d")
    worst = max(res.items(), key=lambda kv: kv[1]["changes"])
    print(f"  most changes: {name(worst[0])} with {worst[1]['changes']}")
