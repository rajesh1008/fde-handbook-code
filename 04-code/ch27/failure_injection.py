"""Section 27.1 failure injection: router v0, calibrated on synthetic data, meets the first real sample (day 122)."""
from collections import defaultdict
import common as C
import world as W
from fieldkit.routing import ece

iso, t, lb, n = C.v0()
syn, g = C.synthetic(), C.gold()
cs = lambda items: [iso.predict(i.verbal) for i in items]
sb = [i for i in syn if iso.predict(i.verbal) >= t]
gb = [i for i in g if iso.predict(i.verbal) >= t]
print("router v0, day 120: the model's stated confidence, isotonic calibration on Northlight's synthetic set")
print(f"  synthetic-2000: {len(syn):,} fields, {C.acc(syn):.1%} right, calibration error (ECE) "
      f"{ece(cs(syn), [i.right for i in syn]):.3f}")
print(f"  proceed threshold {t:.2f}: Wilson lower bound {lb:.1%} on {n:,} fields; "
      f"{len(sb) / len(syn):.1%} of fields proceed, {C.acc(sb):.1%} of them right")
print()
print("first real sample, day 122: gold-heldout, 201 documents of gold-set-300, Anne Kessler's labels")
wrong = sum(not i.right for i in gb)
print(f"  {len(g):,} fields, {C.acc(g):.1%} right, calibration error (ECE) {ece(cs(g), [i.right for i in g]):.3f}")
print(f"  proceed band: {len(gb) / len(g):.1%} of fields, {C.acc(gb):.1%} right: {wrong} wrong of {len(gb)}, "
      f"error {wrong / len(gb):.1%} against a promise of at most 2%")
print()
print(f"{'stated confidence':>17s} {'synthetic n':>11s} {'right':>6s} {'gold n':>7s} {'right':>6s}")
by = lambda items: {v: [i for i in items if i.verbal == v] for v in W.VERBAL}
bs, bg = by(syn), by(g)
for v in W.VERBAL:
    print(f"{v:17.2f} {len(bs[v]):11,d} {C.acc(bs[v]):6.1%} {len(bg[v]):7,d} "
          + (f"{C.acc(bg[v]):6.1%}" if bg[v] else "     -"))
print()
print("gold-heldout by document condition: the model is surest where the page is worst")
tiers = defaultdict(list)
for i in g:
    tiers[W.tier(i.q)].append(i)
for k in ("clean", "medium", "hard"):
    its = tiers[k]
    print(f"  {k:7s} {len(its) // 10:3d} documents  mean stated confidence {sum(i.verbal for i in its) / len(its):.3f}"
          f"  right {C.acc(its):.1%}")
C.dump("failure_injection", dict(
    threshold=t, synthetic=C.rel(cs(syn), [i.right for i in syn]), gold=C.rel(cs(g), [i.right for i in g]),
    band_error=wrong / len(gb), band_n=len(gb), band_wrong=wrong))
