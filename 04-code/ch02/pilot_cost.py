"""Listing 2.5 driver: what one more month before production costs, and the stop rule at month 9."""
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import pilot_month_cost, renewal_probability

STOP_MONTH = 9


def main():
    print("COST OF ONE MORE PILOT MONTH  (field estimate staffing)")
    print(f"{'customer':<18}{'FDE h':>7}{'FDE $':>9}{'run $':>8}{'deferred $':>12}{'total $':>10}{'months':>8}{'verdict':>22}")
    for k, c in CONTRACTS.items():
        p = FIELD_ESTIMATE[k]
        d = pilot_month_cost(c, p)
        m = p.months_to_production
        verdict = "inside 9-month rule" if m <= STOP_MONTH else "decide: live or stop"
        print(f"{c.customer:<18}{d['fde_hours']:>7.0f}{d['fde_cost']:>9,.0f}{d['run']:>8,.0f}"
              f"{d['deferred_subscription']:>12,.0f}{d['total']:>10,.0f}{m:>8.1f}{verdict:>22}")
    print("renewal probability by months to production (Northlight history, illustrative):")
    for m in (4, 6, 8, 9, 11, None):
        print(f"  {('never live' if m is None else f'{m} months'):<12}{renewal_probability(m):.0%}")


if __name__ == "__main__":
    main()
