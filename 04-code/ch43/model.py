"""Two-year cost and dependency model for each operating path. Usage: python model.py pennant|caldwell
Both sides of every path: what the customer pays, what Northlight earns and spends, how much FDE capacity the path
consumes, and what the customer could still do alone (readiness with use-decay, takeover hours). Stand-in values."""
import json
import sys
import world as W
from fieldkit.service import two_year, summary


def run(which):
    paths, start, items0 = ((W.PENNANT_PATHS, W.PN_START, W.PENNANT0) if which == "pennant"
                            else (W.CALDWELL_PATHS, W.CW_START, W.CALDWELL0))
    print(f"TWO-YEAR MODEL  {which.capitalize()}  month 1 starts engagement day {start + 1}  (deterministic stand-in)")
    print(f"rates: Northlight ${150:.0f}/h loaded (Chapter 2); customer ${W.CUSTOMER_RATE:.0f}/h loaded (stand-in); "
          "subscription excluded, same on every path")
    print(f"start readiness {W.score(W.items(items0)).gated:.2f}")
    res = {}
    for key, p in paths.items():
        rows = two_year(p, W.items(items0))
        sm = summary(p, rows)
        res[key] = (rows, sm)
        print(f"\n{p.name}")
        print("  year  customer pays  NL revenue  NL cost   NL gross profit  NL margin  FDE share  readiness  takeover h")
        for y in (1, 2):
            s = sm[y]
            mg = "-" if s["margin"] is None else f"{s['margin']*100:.1f}%"
            print(f"  {y:>4}  ${s['customer']:>11,}  ${s['revenue']:>9,}  ${s['cost']:>7,}  ${s['gp']:>14,}  "
                  f"{mg:>9}  {s['fde']:>9.2f}  {s['readiness']:>9.3f}  {s['takeover']:>10}")
        print(f"  two-year NL gross profit, renewal-weighted (assumed p={p.renewal:.2f}): ${sm['weighted_gp']:,}")
        print("  readiness by month: " + " ".join(f"{r.readiness:.2f}" + ("*" if r.capped else "") for r in rows))
        lost = [(r.month, r.decayed) for r in rows if r.decayed]
        firsts = {}
        for m, ids in lost:
            for i in ids:
                firsts.setdefault(i, m)
        if firsts:
            print("  first month each item counts below its start state: " +
                  ", ".join(f"{i} m{m}" for i, m in sorted(firsts.items(), key=lambda x: (x[1], x[0]))))
    print("\n* capped at 0.60 while a gate item is not done alone")
    print("MONTHS " + json.dumps({k: dict(customer=[r.customer_cost for r in rows], readiness=[r.readiness for r in rows],
                                          takeover=[r.takeover_hours for r in rows], margin=[r.vendor_margin for r in rows])
                                  for k, (rows, _s) in res.items()}, separators=(",", ":")))
    return res


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "pennant")
