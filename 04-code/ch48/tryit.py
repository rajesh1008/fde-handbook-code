"""Try It Yourself: the three exercises in Chapter 48. Run: python tryit.py a|b|c"""
import sys
import _paths  # noqa: F401
import freeze
import upgrades
from fieldkit.evals import wilson
from world import CUSTOMERS, MONTHLY


def a():
    print("A. Change the freeze and the policy, and read the conflict check")
    for fz, pol in [((440, 461), 14), ((440, 461), 7), ((440, 469), 14), ((430, 445), 14)]:
        r0 = freeze.v0(fz, pol); r1 = freeze.v1(fz, pol)
        print(f"  freeze {fz} policy {pol:>2} d: v0 live day {r0['live']} ({r0['past_policy']} d past policy); "
              f"conflict={r1['conflict']}" + (f"; v1 live day {r1['live']}, {r1['manual_referrals']} manual referrals"
                                               if r1['conflict'] else ""))


def b():
    print("B. Loosen Greystone's criteria-citation floor and replay extract-2027-01")
    keep = upgrades.FLOORS["Greystone"]
    for f in (0.97, 0.95, 0.94):
        upgrades.FLOORS["Greystone"] = (keep[0], f) + tuple(keep[2:])
        v, why = upgrades.gate("Greystone", "extract-2027-01", "extract-2026-04")
        print(f"  floor {f}: {v}; " + "; ".join(why))
    upgrades.FLOORS["Greystone"] = keep


def c():
    print("C. Blend the three customers two ways, then read each on its own")
    for w in ("sample", "volume"):
        acc = []
        for m in range(12):
            k = n = 0
            for cu, d in CUSTOMERS.items():
                share = 1 if w == "sample" else MONTHLY[cu]["volume"][m] / d["sample"]
                k += MONTHLY[cu]["errors"][m] * share; n += d["sample"] * share
            acc.append(round(100 * (1 - k / n), 1))
        print(f"  blended by {w:<6}: month 7 {acc[6]}%, month 10 {acc[9]}%, range {min(acc)} to {max(acc)}")
    for cu, d in CUSTOMERS.items():
        e = MONTHLY[cu]["errors"]
        worst = max(range(12), key=lambda i: e[i] / d["line"])
        print(f"  {cu:<9} worst month {worst + 1}: {e[worst]} of {d['sample']} against line {d['line']} "
              f"(upper {wilson(e[worst], d['sample'])[1]:.3f})")


if __name__ == "__main__":
    {"a": a, "b": b, "c": c}[sys.argv[1] if len(sys.argv) > 1 else "a"]()
