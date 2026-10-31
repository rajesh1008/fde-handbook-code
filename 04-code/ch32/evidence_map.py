"""Answers mapped to evidence: reuse, owners and the expiry calendar."""
import _paths  # noqa: F401
from fieldkit.security import reuse, expiring
from world import ANSWERS, EVIDENCE, REVIEW_DAY

use = reuse(ANSWERS)
print("evidence carrying the most answers")
for e, n in use.most_common(6):
    ev = EVIDENCE[e]
    print(f"  {e}  {n} answers  {ev.title[:52]:<52} owner {ev.owner}")
print(f"evidence items: {len(EVIDENCE)}; answers per item: mean {sum(use.values()) / len(use):.1f}, max {max(use.values())}")
owners = {}
for ev in EVIDENCE.values():
    owners.setdefault(ev.owner, 0); owners[ev.owner] += 1
print("owners: " + ", ".join(f"{o} {n}" for o, n in sorted(owners.items(), key=lambda x: -x[1])))
print()
print(f"expiry calendar from day {REVIEW_DAY}, next 90 days")
for day, e, title, qs in expiring(EVIDENCE, ANSWERS, REVIEW_DAY, 90):
    print(f"  day {day}  {e}  {title[:44]:<44} takes down {', '.join(qs)}")
