"""Listing 52.3: refit the router's calibrator on gm-n2 (even cal-600 documents), check on the odd ones."""
import _paths  # noqa: F401
from fieldkit.pyramid import MergeGate, caught_at
import world as W, suite as S

print(f"{'calibrator':<34}{'model':<10}{'proceed n':>10}{'wrong':>7}{'rate':>7}{'95% upper':>11}{'share':>8}")
n2_cal = S.calibrator(W.N2, W.CAL_DOCS[0::2])
for name, v, cal in (("v1.1 (fitted on the pin)", W.PIN, S.PIN_CAL), ("v1.1 (fitted on the pin)", W.N2, S.PIN_CAL),
                     ("v1.2 (refitted on gm-n2)", W.N2, n2_cal)):
    p = S.proceed_error(v, cal)
    print(f"{name:<34}{v:<10}{p['n']:>10}{p['wrong']:>7}{p['rate']:>7.1%}{p['hi']:>11.1%}{p['share']:>8.1%}")
print()
print("reliability on cal-600 odd documents (stated confidence bin -> observed accuracy)")
for v in (W.PIN, W.N2):
    row = []
    for lo in (0.5, 0.6, 0.7, 0.8, 0.9):
        b = [W.correct(v, d, f) for d in W.CAL_DOCS[1::2] for f in W.MODEL_FIELDS if lo <= W.stated(v, d, f) < lo + 0.1]
        row.append(f"{lo:.1f}-{lo + 0.1:.1f}: {sum(b) / max(1, len(b)):.0%} (n={len(b)})")
    print(f"  {v:<14}" + "  ".join(row))
print()
res = S.pyramid().run({"version": W.N2, "signed_off": S.lost_critical(W.N2), "calibrator": n2_cal}, stop_on_fail=False)
d = MergeGate(owner="Anne Kessler").decide(res)
print(f"gm-n2 with router v1.2: decision {d['decision']}; layers failing: {caught_at(res)}")
print("threshold record v1.2: proceed 0.95 unchanged, calibrator refitted; signature required: Anne Kessler")
