"""the integration-tax reserve, sized from how far each engagement's integration hours missed P50."""
import math, statistics
import _paths  # noqa: F401
from world import ACTUAL, ESTIMATE, TAX_RANGE


def misses(extra=None):
    m = {n: ACTUAL[n]["integration"] / ESTIMATE[n]["integration"] for n in ACTUAL}
    if extra:
        m.update(extra)
    return m


def reserve(m, step=0.05):
    """Worst miss among the engagements, rounded up to the next five points."""
    worst = max(m.values()) - 1.0
    return math.ceil(round(worst / step, 6)) * step


def covered(m, r):
    return sum(1 for v in m.values() if v <= 1 + r + 1e-9)


def main(extra=None):
    m = misses(extra)
    print("integration hours: actual / Chapter 10 P50 (closed at all three)")
    for n, v in m.items():
        if n in TAX_RANGE:
            lo, hi, mh = TAX_RANGE[n]
            p90h = hi * mh
            inside = "inside" if ACTUAL[n]["integration"] <= p90h else "ABOVE"
            print(f"  {n:<10} {ACTUAL[n]['integration']:>5,} / {ESTIMATE[n]['integration']:>4,.0f} = {v:.2f}"
                  f"  P90 {p90h:>5,.0f} h {inside:<6}  tax {ACTUAL[n]['integration'] / ACTUAL[n]['model']:.2f}"
                  f" (range {lo:.2f} to {hi:.2f})")
        else:
            print(f"  {n:<10} miss {v:.2f}")
    r = reserve(m)
    rules = {"median miss": statistics.median(m.values()) - 1, "mean miss": statistics.mean(m.values()) - 1,
             "worst miss": max(m.values()) - 1, "reserve (worst, rounded up to 5 points)": r}
    print()
    for k, v in rules.items():
        print(f"  {k:<40} {v:6.1%}   covers {covered(m, v)} of {len(m)}")
    print(f"\nreserve on the integration line = {r:.0%} of its P50 hours, shown as its own line in the price")
    return r


if __name__ == "__main__":
    import sys
    extra = {"fourth (exercise)": float(sys.argv[1])} if len(sys.argv) > 1 else None
    main(extra)
