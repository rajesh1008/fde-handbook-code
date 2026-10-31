"""Section 27.3: bands, the thresholds and who set them (signed day 132)."""
import common as C
from fieldkit.routing import wilson, ThresholdRecord

_, fit, chk = C.cal()
m, th = C.model(), C.thresholds()
s = [(m.score(i), i.right) for i in chk]
print("threshold sweep on cal-600's checked half (fields with a calibrated score at or above t):")
print(f"{'t':>5s} {'share':>6s} {'right':>6s} {'Wilson low':>10s}")
sweep = []
for k in range(80, 100):
    t = k / 100
    band = [o for x, o in s if x >= t]
    if not band:
        continue
    lo, _ = wilson(sum(band), len(band))
    sweep.append(dict(t=t, share=len(band) / len(s), right=sum(band) / len(band), lo=lo))
    if k % 2 == 1 or k == 95:
        print(f"{t:5.2f} {len(band) / len(s):6.1%} {sum(band) / len(band):6.1%} {lo:10.1%}")
print()
print(f"chosen: {th}")
print(f"  proceed at {th.proceed:.2f}: the lowest t at or above the 0.95 field minimum whose band clears 98% at the Wilson lower bound "
      f"({th.lower_bound:.1%} on {th.checked_n:,} fields)")
print(f"  floor at {th.floor:.2f}: below it fewer than half of fields are right, so no value is suggested")
bands = dict(proceed=sum(x >= th.proceed for x, _ in s), review=sum(th.floor <= x < th.proceed for x, _ in s),
             below=sum(x < th.floor for x, _ in s))
for k, v in bands.items():
    sub = [o for x, o in s if (x >= th.proceed if k == "proceed" else (th.floor <= x < th.proceed if k == "review" else x < th.floor))]
    print(f"  {k:8s} {v / len(s):6.1%} of fields, {sum(sub) / len(sub):6.1%} right")
rec = ThresholdRecord(
    proceed=th.proceed, floor=th.floor,
    target="at least 98% right on proceed fields, scored by Anne Kessler's adjusters",
    calibration_set="cal-600: 600 shadow documents, days 124-131, Tom Whitfield and adjuster B",
    checked_on="odd-numbered half, 300 documents, not used to fit",
    lower_bound=th.lower_bound,
    routing="expected 60-65% proceed by document; to be confirmed on audit-400",
    post_review_error="to be measured: audit-400, days 136-140, Anne Kessler's team",
    owner="Anne Kessler", signed_by=("Anne Kessler", "Daniel Reyes"), day=132,
    review_trigger="weekly proceed-band audit lower bound above 2%; PSI above 0.2; any model, prompt or form change")
print()
print("ThresholdRecord, day 132:")
for k, v in rec.__dict__.items():
    print(f"  {k:18s} {v:.3f}" if isinstance(v, float) else f"  {k:18s} {v}")
print(f"  missing: {rec.missing() or 'nothing'}")
draft = ThresholdRecord(th.proceed, th.floor, "98%", "", "", th.lower_bound, "", "", "", (), 120, "")
print(f"router v0's record, day 120, missing: {draft.missing()}")
C.dump("thresholds", dict(sweep=sweep, proceed=th.proceed, floor=th.floor, lo=th.lower_bound))
