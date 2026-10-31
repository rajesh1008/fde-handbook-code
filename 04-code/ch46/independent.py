"""the independent practitioner. One engineer prices Pennant's phase-one integration work package
(the 886-hour P50 inventory from Chapter 10) as a fixed price, carries professional-indemnity (PI) insurance,
and has no bench: hours past the plan push the next engagement back. Assumptions are labeled; US dollars."""
import sys
import _paths  # noqa: F401

P50 = 886                 # Chapter 10, Pennant phase one, option B
BILL = 230.0              # the practitioner's rate (assumption)
FLOOR = 150.0             # what an hour of the practitioner's own time must earn: pay, benefits, unbilled time (assumption)
MONTH_H = 140             # billable hours a month for one person
PI_PREMIUM = 9_000.0      # a year, for a $2,000,000 PI limit (assumption)
PI_LIMIT = 2_000_000
TOOLS = 2_400.0           # test accounts, gateway sandbox, backups for the work package
SALES_H = 40              # unbilled hours to win and scope the work


def run(reserve, miss, liability_cap, next_rate=BILL):
    price = round(P50 * (1 + reserve) * BILL, -2)
    hours = P50 * miss
    months = hours / MONTH_H
    planned_months = P50 * (1 + reserve) / MONTH_H
    pi = PI_PREMIUM * months / 12
    own = (hours + SALES_H) * FLOOR
    slip = max(0.0, months - planned_months)
    displaced = slip * MONTH_H * (next_rate - FLOOR)       # the margin the next engagement would have earned in the slip
    margin = (price - own - pi - TOOLS) / price
    margin_after_slip = (price - own - pi - TOOLS - displaced) / price
    eff_rate = (price - pi - TOOLS) / (hours + SALES_H)
    uninsured = max(0.0, liability_cap - PI_LIMIT) if liability_cap is not None else float("inf")
    return dict(price=price, hours=hours, months=months, margin=margin, after=margin_after_slip,
                eff=eff_rate, slip=slip, uninsured=uninsured)


def show(label, reserve, miss):
    r = run(reserve, miss, 0)
    print(f"  {label:<30} {r['hours']:>6,.0f} h  {r['months']:4.1f} mo  margin {r['margin']:6.1%}"
          f"  after slip {r['after']:6.1%}  ${r['eff']:>4.0f}/h")
    return r


def liability():
    price = run(0.35, 1.15, 0)["price"]
    print(f"liability cap against the PI limit (price ${price:,.0f})")
    for label, cap in (("cap = fees paid", price), ("cap = 10x fees (customer paper)", 10 * price),
                       ("uncapped data-breach indemnity", None)):
        u = run(0.35, 1.15, cap)["uninsured"]
        print(f"  {label:<34} uninsured exposure {'UNLIMITED' if u == float('inf') else f'${u:,.0f}'}")


def main(reserve=None, terms=True):
    print(f"sole practitioner, Pennant phase-one package: P50 {P50} h, ${BILL:.0f}/h, floor ${FLOOR:.0f}/h")
    print(f"professional indemnity: ${PI_LIMIT:,} limit for ${PI_PREMIUM:,.0f} a year")
    rs = (0.0, 0.35) if reserve is None else (reserve,)
    for res in rs:
        print(f"reserve {res:.0%}: fixed price ${run(res, 1.0, 0)['price']:,.0f}")
        show("integration on P50", res, 1.00)
        show("Pennant's actual miss (1.15)", res, 1.15)
        show("Greystone's miss (1.32)", res, 1.32)
    if terms:
        liability()


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else None)
