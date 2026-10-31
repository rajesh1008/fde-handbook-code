"""Breakdowns the figures read: documents by day and channel, door holds by channel and cause."""
import _paths  # noqa: F401
from collections import Counter
from shadow_week import week

docs, bk, res, g, store, refs, fx = week(lineage=False)
print("day  edi scan photo")
for dd in range(124, 131):
    c = Counter(d["channel"] for d in docs if d["day"] == dd)
    print(f"{dd}  {c['edi']:>3} {c['scan']:>4} {c['photo']:>5}")
print("door by channel: accept request reject")
for ch in ("edi", "scan", "photo"):
    rs = [r for d, r in zip(docs, res) if d["channel"] == ch]
    rej = sum(1 for r in rs if r["outcome"] == "held" and "reject" in r["why"])
    req = sum(1 for r in rs if r["outcome"] == "held") - rej
    print(f"{ch:<6} {len(rs) - req - rej:>5} {req:>5} {rej:>5}")
