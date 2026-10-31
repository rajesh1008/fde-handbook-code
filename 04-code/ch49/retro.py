"""Listings 49.1 to 49.6: the three year-one scoreboards, the Greystone clock, the Pennant reconciliation,
what the three share, and the London stall. Deterministic stand-in (see world.py). No model calls.

Usage: python retro.py scoreboards | daily | greystone | pennant | shared | london
"""
import sys
import _paths  # noqa: F401
from world import CUST, AFTER, MILESTONES, LOADED, SUPPORT, YEAR, year_one, daily, hours

ORDER = ("caldwell", "greystone", "pennant")


def money(x):
    return f"-${-x:,.0f}" if x < 0 else f"${x:,.0f}"


def scoreboards():
    print("Year one, signature (day 1) to day 365, US dollars (deterministic stand-in)")
    ys = {c: year_one(c) for c in ORDER}
    print(f"{'':34s}" + "".join(f"{CUST[c]['name']:>20s}" for c in ORDER))
    keys = []
    for c in ORDER:
        for k in list(ys[c]["rev"]) + list(ys[c]["cost"]):
            if k not in keys:
                keys.append(k)
    for c in ORDER:
        pass
    print("revenue")
    for k in [k for k in keys if any(k in ys[c]["rev"] for c in ORDER)]:
        print(f"  {k:32s}" + "".join(f"{money(ys[c]['rev'].get(k, 0)):>20s}" for c in ORDER))
    print(f"  {'total revenue':32s}" + "".join(f"{money(ys[c]['revenue']):>20s}" for c in ORDER))
    print("cost of revenue")
    for k in [k for k in keys if any(k in ys[c]["cost"] for c in ORDER)]:
        print(f"  {k:32s}" + "".join(f"{money(ys[c]['cost'].get(k, 0)):>20s}" for c in ORDER))
    print(f"  {'total cost':32s}" + "".join(f"{money(ys[c]['costs']):>20s}" for c in ORDER))
    print(f"{'gross profit':34s}" + "".join(f"{money(ys[c]['gp']):>20s}" for c in ORDER))
    print(f"{'year-one gross margin':34s}" + "".join(f"{ys[c]['margin']:>20.1%}" for c in ORDER))
    print(f"{'FDE hours, year one':34s}" + "".join(f"{ys[c]['hours']:>20,}" for c in ORDER))
    print(f"{'revenue per FDE hour':34s}" + "".join(f"{money(ys[c]['revenue'] / ys[c]['hours']):>20s}" for c in ORDER))
    print("target 60%, floor 40% (Chapter 2). Caldwell matches Chapter 46's waterfall (47.6%).")
    print("hours after day 190 (stand-in):")
    for c in ORDER:
        print(f"  {c:10s} " + "; ".join(f"{k} {v}" for k, v in AFTER[c].items()))
    print("MARGINS " + str({c: round(ys[c]["margin"] * 100, 1) for c in ORDER}))
    print("GP " + str({c: ys[c]["gp"] for c in ORDER}))
    print("HOURS " + str({c: ys[c]["hours"] for c in ORDER}))
    print("REV " + str({c: ys[c]["revenue"] for c in ORDER}))
    print("COSTS " + str({c: {k: v for k, v in ys[c]["cost"].items()} for c in ORDER}))


def daily_out():
    print("Cumulative gross profit at each month end, US dollars (deterministic stand-in)")
    print(f"{'day':>5s}" + "".join(f"{c:>14s}" for c in ORDER))
    series = {c: daily(c) for c in ORDER}
    for day in list(range(30, 361, 30)) + [365]:
        print(f"{day:>5d}" + "".join(f"{money(series[c][day - 1]):>14s}" for c in ORDER))
    for c in ORDER:
        s = series[c]
        low = min(range(YEAR), key=lambda i: s[i])
        cross = next((i + 1 for i in range(low, YEAR) if s[i] >= 0), None)
        print(f"{c:10s} lowest {money(s[low])} on day {low + 1}; back above zero "
              + (f"on day {cross}" if cross else "not within year one"))
    print("SERIES " + str({c: [round(series[c][d - 1]) for d in range(5, 366, 5)] for c in ORDER}))


def greystone():
    d = CUST["greystone"]
    y = year_one("greystone")
    billed = d["fee"] / d["rate"]
    print("Greystone Health: the open engagement (deterministic stand-in)")
    print(f"  T&M at ${d['rate']}/h, cap {money(d['fee'])}: cap reached after {billed:,.0f} billed hours")
    print(f"  year-one hours {y['hours']:,}; hours worked above the cap {y['hours'] - billed:,.0f}")
    print(f"  year-one gross profit {money(y['gp'])}, margin {y['margin']:.1%}")
    shadow = round(1.8 * 140 * LOADED + d["run_rates"][0])
    live_m = round(d["acv"] / 12 * (1 - SUPPORT) - d["run_rates"][1] - 0.5 * 140 * LOADED)
    print(f"  one month in shadow costs {money(shadow)} (1.8 FTE plus pilot hosting)")
    print(f"  one live month earns {money(live_m)} (subscription less support, production hosting, 0.5 FTE)")
    print(f"  a month of slip therefore moves two-year profit by {money(shadow + live_m)}")
    print(f"  (Chapter 34's $235,500 counts the subscription gross; net of support and hosting it is the line above)")
    print("live in month   year-two GP     two-year GP   [forecast]")
    rows = []
    for L in range(13, 25):
        m0 = L - 13
        g2 = live_m * (12 - m0) - shadow * m0
        rows.append((L, g2, y["gp"] + g2))
        print(f"  {L:>13d}  {money(g2):>12s}  {money(y['gp'] + g2):>14s}")
    g2 = -shadow * 0
    print(f"  {'stopped at 12':>13s}  {money(0):>12s}  {money(y['gp']):>14s}   loss locked, exit costs aside")
    be = next(L for L, _, t in reversed(rows) if t >= 0)
    print(f"break-even: live by month {be} recovers year one inside two years; later than that, it does not")
    print("TWOYEAR " + str({L: t for L, _, t in rows}))


def pennant():
    y = year_one("pennant")
    d = CUST["pennant"]
    print("Pennant Logistics: the margin claim, reconciled (deterministic stand-in)")
    print(f"  year-one revenue {money(y['revenue'])}; cost {money(y['costs'])}; gross profit {money(y['gp'])}; "
          f"margin {y['margin']:.1%}")
    print("  what the margin would have been under each services form, same hours:")
    forms = [("fixed $120,000 (Chapter 19 draft)", 120_000), ("phased, signed (Chapters 34 and 37)", d["fee"])]
    out = {}
    for label, fee in forms:
        R = y["revenue"] - d["fee"] + fee
        out[label] = (R - y["costs"]) / R
        print(f"    {label:40s} revenue {money(R):>12s}  margin {(R - y['costs']) / R:6.1%}")
    svc_cost = y["hours"] * LOADED
    print("  the services line alone (fee less FDE hours, before subscription):")
    for label, fee in forms:
        print(f"    {label:40s} {money(fee - svc_cost):>12s}")
    ops = y["rev"]["managed service"]
    print(f"  managed service days 290 to 365: revenue {money(ops)}, margin {d['managed_margin']:.1%} "
          f"(Chapter 43; floor 40%)")
    booked = y["hours"] - AFTER["pennant"]["night duty never booked"]
    print(f"  FDE ledger hours {booked:,}; retrospective hours {y['hours']:,} (night duty found {AFTER['pennant']['night duty never booked']})")
    print("  verdict: under the signed form Pennant earned money in year one; the services line would have lost")
    print("  money under the fixed draft, and the operations line runs below the floor")
    print("FORMS " + str({k: round(v * 100, 1) for k, v in out.items()}))


def shared():
    print("What the three share: the same five measures, three customers (deterministic stand-in)")
    rows = [
        ("days, signature to live", "158", "not live by day 365", "168"),
        ("days, live to Live Stable", "90", "n/a", "90"),
        ("integration tax (Chapter 46)", "0.97", "2.00", "1.96"),
        ("share of hours blocked to day 190", f"{340 / 3450:.0%}", f"{380 / 3300:.0%}", f"{120 / 2460:.0%}"),
        ("person who could stop go-live", "model-risk committee", "clinical authority", "data protection"),
        ("year-one margin", *(f"{year_one(c)['margin']:.1%}" for c in ORDER)),
    ]
    print(f"{'measure':36s}{'caldwell':>22s}{'greystone':>22s}{'pennant':>22s}")
    for r in rows:
        print(f"{r[0]:36s}{r[1]:>22s}{r[2]:>22s}{r[3]:>22s}")
    print("capability transfer (T transferred, R rebuilt, N not needed):")
    cap = [("deterministic-first routing", "T", "R", "T"), ("evaluation suite on real documents", "T", "T", "T"),
           ("five gates with named signers", "T", "R", "R"), ("shadow with silent-wrong count", "T", "T", "T"),
           ("ownership map and deputies", "T", "N", "R"), ("integration adapters", "R", "R", "R"),
           ("security answers library", "T", "R", "R"), ("runbooks and exit drill", "T", "N", "R")]
    for r in cap:
        print(f"  {r[0]:36s}{r[1]:>8s}{r[2]:>8s}{r[3]:>8s}")
    print("CAP " + str(cap))


def london():
    print("The London asset manager that stalled (fictional cameo; pounds sterling; deterministic stand-in)")
    stages = [("first workshop to signed NDA", 21), ("use case agreed", 34), ("vendor risk questionnaire", 96),
              ("model and data-residency review", 71), ("waiting for an information-security steering slot", 76), ("paused by the client", 0)]
    t = 0
    for s, n in stages:
        t += n
        print(f"  {s:50s} {n:>4d} days  (cumulative {t})")
    sec = sum(n for s, n in stages[2:5])
    print(f"  inside information security: {sec} days ({sec / 30.4:.1f} months)")
    hours_spent, rate_gbp = 420, 118
    print(f"  Northlight hours spent {hours_spent}; cost at a loaded GBP{rate_gbp}/h: GBP{hours_spent * rate_gbp:,}")
    print("  proposed: pilot fee GBP85,000, subscription GBP540,000 a year; revenue booked: GBP0")
    print("  first real document seen: never")
    print("STAGES " + str(stages))


if __name__ == "__main__":
    {"scoreboards": scoreboards, "daily": daily_out, "greystone": greystone, "pennant": pennant,
     "shared": shared, "london": london}[sys.argv[1]]()
