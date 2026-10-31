"""Try It Yourself. Usage: tryit.py a|b|c"""
import sys
import _paths  # noqa: F401
from fieldkit.gates import wilson, judge, Measurement, Criterion
import world

p = sys.argv[1] if len(sys.argv) > 1 else "a"
if p == "a":   # move the per-class bar
    for bar in (0.75, 0.78, 0.80, 0.82, 0.85):
        c = Criterion("S-1", "", bar, per="class")
        v = {k: judge(c, Measurement("S-1", n, d * 10, scope=k)).verdict for k, (d, n) in world.STRATA.items()}
        bad = [k for k, x in v.items() if x != "met"]
        print(f"bar {bar:.0%}: aggregate {'met' if 1689 / 2010 >= bar else 'below'}; classes not met: "
              + (", ".join(f"{k} ({v[k]})" for k in bad) or "none"))
elif p == "b":  # how many fields resolve a class this close to the bar
    for n in (490, 1000, 2000, 5000, 10000, 20000):
        k = round(0.794 * n)
        lo, hi = wilson(k, n)
        print(f"{n:>6} fields at 79.4%: interval {lo:.1%} to {hi:.1%} -> {judge(world.S1, Measurement('S-1', k, n, scope='mail')).verdict}")
elif p == "c":  # same per-class rates, different production mix
    rate = {k: n / (d * 10) for k, (d, n) in world.STRATA.items()}
    z = {k: 0 for k in rate}
    mixes = {"gold-heldout mix": {k: d for k, (d, _) in world.STRATA.items()},
             "first notices only (20/40/40)": {**z, "first notice, email": 20, "first notice, fax": 40,
                                               "first notice, mail": 40},
             "fax and mail only (60/40)": {**z, "first notice, fax": 60, "first notice, mail": 40}}
    for name, w in mixes.items():
        tot = sum(w.values())
        agg = sum(rate[k] * w[k] for k in rate) / tot
        print(f"{name:30} aggregate {agg:.1%}  {'met' if agg >= 0.80 else 'below'} at 80%")
