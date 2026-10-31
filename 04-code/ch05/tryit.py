"""Try It Yourself, Chapter 5. Usage: python tryit.py 1|2|3"""
import sys

import economics as E
from choose import best
from homes import HOMES
from playbook import P, VENDOR_PLAYBOOK, fit, run, tally


def try1():
    """Break-even bill rate: below what rate does one more month stop paying the integrator?"""
    print("TRY 1: integrator net on one more month as the bill rate falls")
    for rate in (240, 200, 180, 150, 140):
        E.BILL_RATE = rate
        r = [s for s in E.extra_month_split() if s.home.startswith("integrator")][0]
        print(f"  bill ${rate}/h  integrator net {r.employer_net:>8,.0f}  customer pays {r.customer_pays:>8,.0f}")
    E.BILL_RATE = 240.0
    print("  the duration incentive turns only when the bill rate falls to the loaded cost")


def try2():
    """Add a play and see where it survives."""
    play = P("bundle-fde", "bundle FDE time into the subscription price", ["subscription"],
             assumes=[("month", -1)])
    print("TRY 2: one new play, three homes")
    for k, h in HOMES.items():
        f = fit(play, h)
        print(f"  {k:<11}{f.verdict:<8}{f.reason}")
    pb = VENDOR_PLAYBOOK + [play]
    print("  vendor playbook v1 + bundle-fde at the lab: "
          + "  ".join(f"{k} {v}" for k, v in tally(run(pb, HOMES['lab'])).items()))


def try3():
    """Your own weights (edit these six numbers; they must sum to 1.0)."""
    mine = [0.20, 0.10, 0.10, 0.30, 0.10, 0.20]
    top, s = best(mine)
    print("TRY 3: a candidate who weights staying to production and changing the core")
    print("  " + "  ".join(f"{h} {v:.2f}" for h, v in s.items()) + f"   -> {top}")


if __name__ == "__main__":
    {"1": try1, "2": try2, "3": try3}[sys.argv[1] if len(sys.argv) > 1 else "1"]()
