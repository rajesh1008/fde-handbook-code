"""Try It Yourself, three variations. Run: python try_it.py 1|2|3"""
import sys
from dataclasses import replace
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import year_one, with_, renewal_probability


def show(tag, c, p):
    y = year_one(c, p)
    print(f"  {tag:<34} months {p.months_to_production:4.1f}  hours {y.hours:6,.0f}  margin {y.margin:6.1%}"
          f"  renewal {renewal_probability(p.months_to_production):.0%}")


def v1():
    """What is the clause worth? Greystone's subscription starting at signature instead of production."""
    c, p = CONTRACTS["greystone"], FIELD_ESTIMATE["greystone"]
    print("VARIATION 1  Greystone Health: subscription start clause")
    show("starts at production (signed)", c, p)
    show("starts at signature", replace(c, subscription_starts="signature"), p)


def v2():
    """Does a third engineer help Pennant? More hours per month, same work, shorter elapsed time."""
    c, p = CONTRACTS["pennant"], FIELD_ESTIMATE["pennant"]
    print("VARIATION 2  Pennant Logistics: staffing")
    for fte in (1.5, 2.0, 3.0):
        show(f"{fte} FDEs", c, with_(p, fde_fte=fte))


def v3():
    """The value of the access ladder: Caldwell with its customer waits removed."""
    c, p = CONTRACTS["caldwell"], FIELD_ESTIMATE["caldwell"]
    print("VARIATION 3  Caldwell Mutual: customer waits")
    for w in (1.5, 0.75, 0.0):
        show(f"{w} months blocked", c, with_(p, wait_months=w))


if __name__ == "__main__":
    {"1": v1, "2": v2, "3": v3}[sys.argv[1] if len(sys.argv) > 1 else "1"]()
