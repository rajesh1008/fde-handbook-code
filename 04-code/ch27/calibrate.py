"""Section 27.2: calibration against the expert-scored set (cal-600, days 124 to 131)."""
from collections import defaultdict
import common as C
import world as W
from fieldkit.routing import ece

items, fit, chk = C.cal()
m = C.model()
iso, *_ = C.v0()
y = [i.right for i in chk]
print("cal-600: 600 shadow documents, days 124 to 131, every field scored by Tom Whitfield and adjuster B,")
print("disagreements settled by Anne Kessler")
print(f"  {len(items):,} fields, {C.acc(items):.1%} right; fitted on even-numbered documents ({len(fit):,} fields), "
      f"checked on odd ({len(chk):,})")
names = ["intercept"] + list(W.FEATURE_NAMES) if len(m.w) == len(W.FEATURE_NAMES) + 1 else list(W.FEATURE_NAMES)
top = sorted(zip(names, m.w), key=lambda kv: -abs(kv[1]))[:7]
print("  largest weights in the correctness model (logistic regression, ridge 1.0, Newton steps):")
for k, w in top:
    print(f"    {k:24s} {w:+.2f}")
print()
print("calibration error on the checked half (ECE, lower is better):")
print(f"  router v0 (stated confidence, synthetic calibration)  {ece([iso.predict(i.verbal) for i in chk], y):.3f}")
print(f"  correctness model before isotonic step               {ece([m.raw(i) for i in chk], y):.3f}")
print(f"  correctness model after isotonic step                {ece([m.score(i) for i in chk], y):.3f}")
print()
print("accuracy by stratum (cal-600, all fields):")
st = defaultdict(list)
for i in items:
    st[i.stratum].append(i)
for k, v in sorted(st.items(), key=lambda kv: C.acc(kv[1])):
    print(f"  {k:20s} {len(v) // 10:4d} documents  {C.acc(v):.1%}")
C.dump("calibrate", dict(v0=C.rel([iso.predict(i.verbal) for i in chk], y),
                         model=C.rel([m.score(i) for i in chk], y),
                         ece_v0=ece([iso.predict(i.verbal) for i in chk], y), ece_model=ece([m.score(i) for i in chk], y)))
