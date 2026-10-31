"""Listing 2.3 driver: year-one margin for the three contracts, deal sheet against field estimate."""
from contracts import CONTRACTS, DEAL_SHEET, FIELD_ESTIMATE
from margin import year_one, renewal_probability, two_year_gross_profit, with_, LOADED_RATE


def row(y, p):
    m = "never" if y.months_to_production is None else f"{p.months_to_production:4.1f}"
    return (f"{y.customer:<18}{p.label:<16}{m:>6}{y.hours:>7,.0f}{y.revenue/1e3:>9,.0f}k"
            f"{y.cost/1e3:>8,.0f}k{y.margin:>8.1%}{renewal_probability(p.months_to_production):>8.0%}")


def main():
    print(f"YEAR-ONE MARGIN  loaded rate ${LOADED_RATE:.0f}/FDE hour  (illustrative, Northlight-fictional)")
    print(f"{'customer':<18}{'plan':<16}{'months':>6}{'hours':>7}{'revenue':>10}{'cost':>9}{'margin':>8}{'renew':>8}")
    for k, c in CONTRACTS.items():
        for plans in (DEAL_SHEET, FIELD_ESTIMATE):
            print(row(year_one(c, plans[k]), plans[k]))
    print("gap the deal sheet does not show:")
    for k, c in CONTRACTS.items():
        a, b = year_one(c, DEAL_SHEET[k]), year_one(c, FIELD_ESTIMATE[k])
        print(f"  {c.customer:<18} {100*(a.margin-b.margin):5.1f} margin points, "
              f"{b.hours-a.hours:6,.0f} extra FDE hours, {FIELD_ESTIMATE[k].months_to_production-DEAL_SHEET[k].months_to_production:4.1f} extra months")
    print("year one flatters a stuck pilot (field estimate vs never live, two-year renewal-weighted gross profit):")
    for k, c in CONTRACTS.items():
        p = FIELD_ESTIMATE[k]
        live, stuck = two_year_gross_profit(c, p), two_year_gross_profit(c, with_(p, never_live=True))
        print(f"  {c.customer:<18} margin y1 {year_one(c, p).margin:6.1%} live vs {year_one(c, with_(p, never_live=True)).margin:6.1%} stuck;"
              f"  2-yr GP {live['total']/1e3:6,.0f}k live vs {stuck['total']/1e3:6,.0f}k stuck")


if __name__ == "__main__":
    main()
