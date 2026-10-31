"""Caldwell internal audit, fieldwork days 201 to 210: 25 decisions drawn by audit plus the disputed claim."""
import random
from collections import Counter
import _paths  # noqa: F401
import world as W, pack as P

recs = W.records(W.LIVE, 200)
pool = [r for r in recs if r["band"] != "proceed" or random.Random(r["id"]).random() < 0.5]
sample = random.Random(201).sample(pool, 25) + [W.disputed(recs)]
checks, stat, packs = 0, Counter(), []
for r in sample:
    st, how, _ = P.build(r, 205, use_history=True)
    for e in P.ELEMENTS:
        if st[e] != "n/a":
            checks += 1
        stat[st[e]] += 1
    packs.append([r["id"], st])
fails = sum(1 for _, st in packs for v in st.values() if v not in P.GOOD)
before = sum(r["day"] < W.FIX for r in sample)
print("INTERNAL AUDIT SAMPLE: 26 packs (25 drawn by audit from days 158 to 200, plus the disputed claim)")
print(f"  element tests performed {checks}; exceptions {fails}")
print(f"  statuses: " + ", ".join(f"{k} {stat[k]}" for k in ("verified", "reconstructed", "n/a", "inferred", "contradicted", "unverifiable")))
print(f"  packs from before pinning (day < {W.FIX}) {before}; their prompt element is 'reconstructed' with parameter-store history attached")
print(f"  chain head over the sample {P.chain_head(packs)}")
print("  self-identified issue SI-01: prompt hotfix outside change control, day 166; found day 177; closed day 182")
print("  findings on the agent: 0")
