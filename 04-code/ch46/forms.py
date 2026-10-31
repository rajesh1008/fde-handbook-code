"""one engagement, four ways to price the services, and who carries the integration tax.

The next insurer at its calibrated hours. Each form is priced at signature; then integration lands at a range
of misses against P50. Year-one margin per form (FDE cost in cost of revenue)."""
import _paths  # noqa: F401
from world import BILL
from price_next import priced_hours, year_one, fee_for, actual_hours

MISSES = (0.8, 1.0, 1.2, 1.35, 1.5, 1.8)
DEADLINE = 8.0     # outcome form: the fee is earned only if production starts by month 8


def forms():
    reserved, r = priced_hours("checked")
    bare, _ = priced_hours("checked", res=0.0)
    fee_bare = fee_for(bare); fee_res = fee_for(reserved, overrun=reserved["integration"] - reserved["integration"] / (1 + r))
    cap_h = sum(reserved.values()) - reserved["blocked"]
    out = {}
    for miss in MISSES:
        h, over = actual_hours(reserved, r, miss)
        billable = sum(h.values()) - h["blocked"]
        row = {}
        row["fixed, no reserve"] = year_one(h, fee_bare, over)[0]
        row["fixed with 35% reserve"] = year_one(h, fee_res, over)[0]
        row["T&M, capped at priced hours"] = year_one(h, BILL * min(billable, cap_h), over)[0]
        m, months, _ = year_one(h, 0, over)
        row["outcome fee at go-live"] = year_one(h, 1.6 * fee_res, over)[0] if months <= DEADLINE else m
        out[miss] = (row, months)
    return out, fee_bare, fee_res, cap_h


def main():
    out, fb, fr, cap = forms()
    print(f"fees at signature: fixed, no reserve ${fb:,}; fixed with reserve ${fr:,}")
    print(f"  T&M ${BILL:.0f}/h capped at {cap:,.0f} billable h; outcome ${1.6 * fr:,.0f} if live by month {DEADLINE:.0f}")
    names = list(next(iter(out.values()))[0])
    print(f"{'integration miss':<30}" + "".join(f"{m:>7.2f}" for m in MISSES))
    for n in names:
        print(f"{n:<30}" + "".join(f"{out[m][0][n]:>7.1%}" for m in MISSES))
    print(f"{'month of production':<30}" + "".join(f"{out[m][1]:>7.1f}" for m in MISSES))


if __name__ == "__main__":
    main()
