"""Try It Yourself 52.a to 52.c."""
import sys, _paths  # noqa: F401
from fieldkit.pyramid import MergeGate, caught_at
import world as W, suite as S

which = sys.argv[1] if len(sys.argv) > 1 else "a"
if which == "a":   # Anne signs off the lost critical items on gm-n1
    res = S.pyramid().run({"version": W.N1}, stop_on_fail=False)
    lost = S.lost_critical(W.N1)
    print("gm-n1 lost critical items:", ", ".join(f"{d}/{f}" for d, f in lost))
    print("without sign-off:", MergeGate("Anne Kessler").decide(res)["decision"])
    res2 = S.pyramid().run({"version": W.N1, "signed_off": lost}, stop_on_fail=False)
    print("with Anne Kessler's item-by-item sign-off:", MergeGate("Anne Kessler").decide(res2)["decision"],
          "| L2:", [r.verdict for r in res2 if r.layer == 2][0])
elif which == "b":  # Caldwell with the accuracy gate only: no layer 3
    S.LAYERS[:] = [l for l in S.LAYERS if l.n != 3]
    from fieldkit.pyramid import Pyramid
    pyr = Pyramid(S.LAYERS).add(1, "output contract", S.l1).add(2, "gold set", S.l2).add(4, "budgets", S.l4)
    res = pyr.run({"version": W.N2, "signed_off": S.lost_critical(W.N2)}, stop_on_fail=False)
    print("gm-n2 without the calibration layer:", MergeGate("Anne Kessler").decide(res)["decision"])
    pin, n2 = S.proceed_error(W.PIN, S.PIN_CAL), S.proceed_error(W.N2, S.PIN_CAL)
    per_month = 14800 * len(W.MODEL_FIELDS)
    for name, p in (("pin", pin), ("gm-n2", n2)):
        print(f"  {name:<6} wrong fields auto-proceeded a month at 14,800 documents: {per_month * p['share'] * p['rate']:.0f}")
else:               # half the calibration data
    docs = W.CAL_DOCS[1::2][:150]
    for v in (W.PIN, W.N2):
        res = S.pyramid().run({"version": v, "check_docs": docs}, stop_on_fail=False)
        r = [x for x in res if x.layer == 3][0]
        print(f"{v:<15} 150 check documents: L3 {r.verdict}: {r.detail}")
