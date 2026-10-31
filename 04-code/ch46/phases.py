"""delivery margin by phase, frozen at each gate (revenue minus FDE, run and support cost)."""
import _paths  # noqa: F401
from world import CONTRACT, PHASES, RUN, RATE, BILL, SUPPORT


def run_cost(name, a, b):
    pilot, prod, p0, l0 = RUN[name]
    c = 0.0
    for d in range(a, b + 1):
        if l0 and d >= l0:
            c += prod * 12 / 365
        elif p0 and d >= p0:
            c += pilot * 12 / 365
    return c


def phase_rows(name):
    k = CONTRACT[name]; rows = []; used_h = 0.0; billed = 0.0
    for ph, a, b, h, blk in PHASES[name]:
        days = b - a + 1
        sub = k["acv"] * days / 365 if k["sub_from"] else 0.0
        if k["form"] == "fixed fee":                       # fee recognized cost-to-cost against the hours it priced
            svc = k["fee"] * (min(used_h + h, k["priced_h"]) - min(used_h, k["priced_h"])) / k["priced_h"]
        elif k["form"] == "T&M with cap":                  # blocked hours are not billable; the cap stops billing
            svc = min((h - blk) * k["rate"], k["fee"] - billed); billed += svc
        else:                                              # phased: discovery T&M, then fixed at P90, cost-to-cost
            svc = (min(h, k["disc_h"]) * BILL) if ph == "discovery" else (k["fee"] - k["disc_h"] * BILL) * h / (k["priced_h"] - k["disc_h"])
        used_h += h
        rev = sub + svc
        cost = h * RATE + run_cost(name, a, b) + SUPPORT * sub
        rows.append(dict(phase=ph, a=a, b=b, h=h, rev=rev, cost=cost))
    return rows


def main():
    for name in PHASES:
        k = CONTRACT[name]
        print(f"{name}: {k['form']}, ACV ${k['acv']:,}")
        R = C = 0.0
        for r in phase_rows(name):
            R += r["rev"]; C += r["cost"]
            m = (r["rev"] - r["cost"]) / r["rev"] if r["rev"] else float("nan")
            ms = "   n/a" if r["rev"] == 0 else f"{m:6.1%}"
            print(f"  {r['phase']:<9} {r['a']:>3}-{r['b']:<3} {r['h']:>6,} h  rev ${r['rev'] / 1000:>6,.1f}k"
                  f"  cost ${r['cost'] / 1000:>6,.1f}k  phase {ms}  to date {(R - C) / R:6.1%}")
        print()


if __name__ == "__main__":
    main()
