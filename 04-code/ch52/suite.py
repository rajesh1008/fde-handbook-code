"""Caldwell's evaluation suite as a fieldkit pyramid (layers 1 to 4). Owner of the gold set: Anne Kessler."""
import _paths  # noqa: F401
from fieldkit.evals import CustomerGate, wilson
from fieldkit.pyramid import Layer, Pyramid, paired_slices, slice_verdict, PASS, FAIL, INCONCLUSIVE
from fieldkit.routing import Isotonic
import world as W

LAYERS = [Layer(1, "unit", "output contract on every field", "every change", 1.0, 0.0),
          Layer(2, "component", "gold-set-300 test split, aggregate and every field", "every change", 60.0, 2.5),
          Layer(3, "integration", "router calibration on cal-600 odd documents", "model or threshold", 120.0, 7.0),
          Layer(4, "system", "cost, latency and fingerprint budgets", "release", 300.0, 12.0)]
BOUND = 0.015          # proceed-band error ceiling the router v1.1 threshold record promises (upper 95% bound)
PROCEED = 0.95

GATE = CustomerGate(customer="Caldwell Mutual", owner="Anne Kessler", scorer="Anne Kessler's gold set",
                    document_set="gold-set-300 test (201)", critical_fields=W.CRITICAL,
                    max_drop_points=0.5, max_lost_critical=0)


def lost_critical(version):
    b, a = W.scored(W.PIN), W.scored(version)
    return sorted(k for k in b if k[1] in W.CRITICAL and b[k] and not a[k])


def calibrator(version, docs):
    xs = [W.stated(version, d, f) for d in docs for f in W.MODEL_FIELDS]
    ys = [W.correct(version, d, f) for d in docs for f in W.MODEL_FIELDS]
    return Isotonic().fit(xs, ys)


PIN_CAL = calibrator(W.PIN, W.CAL_DOCS[0::2])     # router v1.1 was fitted on the pinned model


def proceed_error(version, cal, docs=None):
    docs = docs or W.CAL_DOCS[1::2]
    rows = [(cal.predict(W.stated(version, d, f)), W.correct(version, d, f)) for d in docs for f in W.MODEL_FIELDS]
    band = [ok for p, ok in rows if p >= PROCEED]
    wrong = sum(not ok for ok in band)
    lo, hi = wilson(wrong, len(band))
    return dict(n=len(band), wrong=wrong, rate=wrong / max(1, len(band)), lo=lo, hi=hi, share=len(band) / len(rows))


def l1(sys):
    bad = [f for f in W.FIELDS if f not in sys.get("emits", W.FIELDS)]
    return (FAIL if bad else PASS), ("missing " + ", ".join(bad)) if bad else "10 of 10 fields, types valid", 0.4, 0.0, {}


def l2(sys):
    before, after = W.scored(W.PIN), W.scored(sys["version"])
    status, reasons, cells, wb, wa = GATE.check(before, after, weight_of=lambda k: W.WEIGHT[k[1]],
                                                signed_off=sys.get("signed_off", ()))
    slices = paired_slices(before, after, lambda k: k[1])
    worse = [f"{f} {v}" for f, s in slices.items()
             for v in [slice_verdict(s["n"], s["gains"], s["losses"])[0]] if v != PASS]
    extra = [c for c in sys.get("extra_checks", ())]
    extra_fail = [c(sys) for c in extra]
    extra_fail = [x for x in extra_fail if x]
    v = FAIL if status == "block" or any("fail" in w for w in worse) or extra_fail else (
        INCONCLUSIVE if status == "owner review" or worse else PASS)
    detail = f"weighted {wb:.1%} -> {wa:.1%}; gate {status}" + (f"; {'; '.join(reasons)}" if reasons else "") + \
             (f"; slices {', '.join(worse)}" if worse else "") + (f"; {'; '.join(extra_fail)}" if extra_fail else "")
    return v, detail, 41.0, 2.1, dict(wb=wb, wa=wa, cells=cells)


def l3(sys):
    pe = proceed_error(sys["version"], sys.get("calibrator", PIN_CAL), sys.get("check_docs"))
    v = PASS if pe["hi"] <= BOUND else (FAIL if pe["lo"] > BOUND else INCONCLUSIVE)
    return v, (f"proceed-band error {pe['wrong']}/{pe['n']} = {pe['rate']:.1%} "
               f"(95% {pe['lo']:.1%}-{pe['hi']:.1%}, ceiling {BOUND:.1%}); proceed share {pe['share']:.1%}"), 88.0, 5.6, pe


def l4(sys):
    v = sys["version"]
    ok = W.COST[v] <= 0.020 and W.P95[v] <= 6.0
    return (PASS if ok else FAIL), f"${W.COST[v]:.4f}/doc (budget $0.0200), p95 {W.P95[v]} s (floor 6.0), fingerprint recorded", \
        210.0, 9.4, {}


def pyramid():
    return Pyramid(LAYERS).add(1, "output contract", l1).add(2, "gold set", l2).add(3, "calibration", l3) \
        .add(4, "budgets", l4)
