"""Listing 34.6: Caldwell's year-one margin from the Ch2 forecast to the signed addendum, with two-year
renewal-weighted gross profit beside each, as Chapter 2 requires."""
import sys, pathlib
import _paths  # noqa: F401
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "ch02"))
from margin import year_one  # noqa: E402  (Chapter 2's model)
import contracts as C2        # noqa: E402
import world as W             # noqa: E402
from extract import price, margin as m1, base_costs, REVENUE  # noqa: E402


def year_two_cost(version):
    sustain = W.SUSTAIN_FTE * W.HOURS_PER_FTE_MONTH * 12 * W.LOADED_RATE
    base = sustain + 9000 * 12 + 160_000
    _, _, _, lines = price(version, honest=True)
    recurring = 0.0
    for c, l in lines:
        if l.basis == "computed":
            recurring += l.amount / W.CREDIT_MONTHS * 12
        elif c.cid in ("CA-03.1", "CA-05.1"):          # monthly obligations: twelve months in year two
            recurring += l.amount / W.CREDIT_MONTHS * 12
        elif c.cid in ("CA-07.1", "CA-09.1"):          # annual obligations
            recurring += l.amount
    return base + recurring


def row(label, m, gp1, gp2):
    print(f"  {label:44} {m:7.1%}   ${gp1:>11,.0f}   ${gp2:>11,.0f}   ${gp1 + W.RENEWAL * gp2:>11,.0f}")


y = year_one(C2.CONTRACTS["caldwell"], C2.FIELD_ESTIMATE["caldwell"])
print("CALDWELL YEAR-ONE GROSS MARGIN (forecast) beside two-year renewal-weighted gross profit, renewal 80%")
print("  stage                                         margin   year-one GP    year-two GP    two-year weighted")
y2_ch2 = 1_600_000 - (W.SUSTAIN_FTE * W.HOURS_PER_FTE_MONTH * 12 * W.LOADED_RATE + 9000 * 12 + 160_000)
row("Ch2 field estimate (day 0)", y.margin, y.revenue - y.cost, y2_ch2)
rev = sum(REVENUE.values())
base = sum(l.amount for l in base_costs())
row("day 136, before the addendum", (rev - base) / rev, rev - base, y2_ch2)
_, _, _, hl = price("v3", honest=True)
ca01 = next(l.amount for c, l in hl if c.cid == "CA-01.1") / W.CREDIT_MONTHS * 12
for label, v, honest, naive in [("v3 priced by v0 extractor (day 137)", "v3", False, True),
                                ("v3 priced honestly (day 138)", "v3", True, False),
                                ("v5 as signed (day 149)", "v5", True, False)]:
    _, _, _, lines = price(v, honest=honest, naive=naive)
    m, r, cost = m1(lines)
    y2 = 1_600_000 - year_two_cost(v) + (ca01 if naive else 0)
    row(label, m, r - cost, y2)
print("\nWATERFALL v3 (day 138): base margin, then each commitment in order of size")
_, _, _, lines = price("v3", honest=True)
run = rev - base
print(f"  {'base, day 136':52} {run / rev:7.1%}")
for c, l in sorted(lines, key=lambda x: -x[1].amount):
    if l.amount:
        run -= l.amount
        print(f"  {c.cid:8} {l.label[:46]:46} {run / rev:7.1%}   -${l.amount:,.0f}")
print("\nWHAT LAURA FINCH TRADED (v3 -> v5, year-one cost)")
_, _, _, l5 = price("v5", honest=True)
d5 = {c.cid: l for c, l in l5}
d3 = {c.cid: l for c, l in lines}
for cid in sorted(set(d3) | set(d5)):
    a = d3[cid].amount if cid in d3 else 0.0
    b = d5[cid].amount if cid in d5 else 0.0
    print(f"  {cid:8} ${a:>9,.0f} -> ${b:>9,.0f}   {(d5[cid].label if cid in d5 else 'removed')[:60]}")
print(f"  total    ${sum(l.amount for _, l in lines):>9,.0f} -> ${sum(l.amount for _, l in l5):>9,.0f}")
