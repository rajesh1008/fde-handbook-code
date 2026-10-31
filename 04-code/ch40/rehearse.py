"""Reconstruction rehearsal: draw decisions, build packs, count element statuses.
usage: rehearse.py v0 | history | months | v1"""
import random, sys
from collections import Counter
import _paths  # noqa: F401
import world as W, pack as P

mode = sys.argv[1] if len(sys.argv) > 1 else "v0"
recs = W.records(W.LIVE, W.END)
if mode == "v1":
    pool, asof, hist, label = [r for r in recs if W.FIX <= r["day"] <= 200], 201, False, "v1 records, days 180 to 200, as of day 201"
elif mode == "months":
    pool, asof, hist, label = [r for r in recs if r["day"] < W.DISPUTE], 340, False, "v0 records, days 158 to 175, as of day 340 (traces gone)"
else:
    pool, asof, hist = [r for r in recs if r["day"] < W.DISPUTE], W.REHEARSAL, mode == "history"
    label = "v0 records, days 158 to 175, as of day 177" + (", parameter-store history" if hist else "")
sample = random.Random(40).sample(pool, 40)
counts = {e: Counter() for e in P.ELEMENTS}
for r in sample:
    st, _, _ = P.build(r, asof, hist)
    for e in P.ELEMENTS:
        counts[e][st[e]] += 1
print(f"REHEARSAL {mode}: 40 decisions, {label}")
print(f"  {'element':<21} {'verified':>8} {'reconst':>8} {'inferred':>8} {'contra':>7} {'unverif':>8} {'n/a':>5}")
for e in P.ELEMENTS:
    c = counts[e]
    print(f"  {e:<21} {c['verified']:>8} {c['reconstructed']:>8} {c['inferred']:>8} {c['contradicted']:>7} {c['unverifiable']:>8} {c['n/a']:>5}")
ok = sum(P.complete(P.build(r, asof, hist)[0]) for r in sample)
post = sum((r['day'], r['minute']) >= (W.HOTFIX_DAY, W.HOTFIX_MIN) for r in sample)
print(f"  packs reconstructable {ok} of 40; decisions after the day-{W.HOTFIX_DAY} hotfix in sample {post}")
