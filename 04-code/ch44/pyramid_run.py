"""Listing 44.5: the hiring loop as a system under test, run through the fieldkit pyramid (layers 1 to 4)."""
import _paths  # noqa: F401
from fieldkit.pyramid import Layer, Pyramid, caught_at, PASS, FAIL, LAYER_NAMES
import world as W
from practice import decide, observed, calibration

LAYERS = [Layer(1, "unit", "every competency observed", "every change", 0.1, 0.0),
          Layer(2, "component", "known cases decided correctly", "every change", 0.5, 0.0),
          Layer(3, "integration", "raters agree (kappa >= 0.60)", "monthly", 1.0, 0.0),
          Layer(4, "system", "offer rate 20% to 60%, every decision has a reason", "per pool", 1.0, 0.0)]
KNOWN = {"aces build, fails discovery": (W.CANDIDATES["C-3"], "no hire"),
         "strong discovery, build 1": (W.CANDIDATES["C-5"], "no hire"),
         "balanced 3s": (W.CANDIDATES["C-1"], "hire")}


def d(loop, s):
    return decide(s, loop["exercises"], floors=loop["floors"], mode=loop["mode"])


def l1(loop):
    missing = [c for c in W.COMPETENCIES if c not in observed(loop["exercises"])]
    return (FAIL if missing else PASS), ("not observed: " + ", ".join(missing)) if missing else "all eight observed", 0.0, 0.0, {}


def l2(loop):
    wrong = [f"{k}: got {d(loop, s)[0]}, want {want}" for k, (s, want) in KNOWN.items() if d(loop, s)[0] != want]
    return (FAIL if wrong else PASS), "; ".join(wrong) or "3 of 3 known cases correct", 0.0, 0.0, {}


def l3(loop):
    k = calibration(loop["ratings"])["mean_kappa"]
    return (PASS if k >= 0.60 else FAIL), f"mean kappa {k:.2f}", 0.0, 0.0, {"kappa": round(k, 2)}


def l4(loop):
    ds = [d(loop, s) for s in W.CANDIDATES.values()]
    rate = sum(x[0] == "hire" for x in ds) / len(ds)
    ok = 0.2 <= rate <= 0.6 and all(x[2] for x in ds)
    return (PASS if ok else FAIL), f"offer rate {rate:.0%}", 0.0, 0.0, {"offer_rate": rate}


pyr = Pyramid(LAYERS).add(1, "coverage", l1).add(2, "known cases", l2).add(3, "calibration", l3).add(4, "pool", l4)
LOOPS = {
    "old loop (months 1 to 8)": dict(exercises=W.OLD_LOOP, floors={}, mode="old", ratings=W.RATINGS_BEFORE),
    "new exercises, no floors (failure injection)": dict(exercises=W.EXERCISES, floors={}, mode="new", ratings=W.RATINGS_AFTER),
    "new exercises, unanchored raters": dict(exercises=W.EXERCISES, floors=W.FLOORS, mode="new", ratings=W.RATINGS_BEFORE),
    "new loop (month 10 onward)": dict(exercises=W.EXERCISES, floors=W.FLOORS, mode="new", ratings=W.RATINGS_AFTER),
}
for name, loop in LOOPS.items():
    res = pyr.run(loop)
    at = caught_at(res)
    print(f"{name}: " + (f"caught at layer {at} ({LAYER_NAMES[at]})" if at else "passes layers 1 to 4"))
    for r in res:
        print(f"  L{r.layer} {r.check:<12} {r.verdict:<8} {r.detail}")
