"""The sixty questions: rehearsal status by group and what the panel actually asked."""
import _path  # noqa: F401
from harbourline import panel, GROUPS, OFF_LIST

rows = panel()
print(f"sixty-question bank: {len(rows)} questions")
print("group                            proof  rehearsed  none  asked")
for name, *_ in GROUPS:
    g = [r for r in rows if r["group"] == name]
    c = lambda s: sum(r["status"] == s for r in g)
    print(f"  {name:<30} {c('proof'):>5}  {c('rehearsed'):>9}  {c('not rehearsed'):>4}  {sum(r['asked'] for r in g):>5}")
asked = [r for r in rows if r["asked"]]
for s in ("proof", "rehearsed", "not rehearsed"):
    print(f"asked from the bank, {s}: {sum(r['status'] == s for r in asked)}")
print(f"asked from the bank: {len(asked)} of 60; off the list: {len(OFF_LIST)}; total {len(asked) + len(OFF_LIST)} "
      f"in 90 minutes")
for q in OFF_LIST:
    print(f"  off list: {q}")
