"""Listing 2.4: failure injection. The forecast treats Pennant's fixed-price deployment as T&M, so every
overrun hour is booked as revenue. Run once without the guard, then with it."""
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import year_one, with_, BillingBasisMismatch


def main():
    c = CONTRACTS["pennant"]
    p = with_(FIELD_ESTIMATE["pennant"], integration_tax=3.0)
    wrong = year_one(c, p, assume_billing="tm", strict=False)
    right = year_one(c, p)
    print("FAILURE INJECTION  Pennant Logistics  integration tax 3.0")
    for y in (wrong, right):
        print(f"  billing assumed {y.billing_assumed:<6} services {y.services/1e3:>6,.0f}k  revenue {y.revenue/1e3:>6,.0f}k"
              f"  cost {y.cost/1e3:>5,.0f}k  margin {y.margin:6.1%}")
    print(f"  the wrong forecast overstates margin by {100*(wrong.margin-right.margin):.1f} points "
          f"and revenue by {(wrong.revenue-right.revenue)/1e3:,.0f}k dollars")
    try:
        year_one(c, p, assume_billing="tm")
    except BillingBasisMismatch as e:
        print(f"  guard: BillingBasisMismatch: {e}")


if __name__ == "__main__":
    main()
