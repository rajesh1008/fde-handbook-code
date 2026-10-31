"""The clock register: the incidents that appear after month six were mostly set before go-live.
Each clock has a start day and a period (or a fixed day). v0 is the register Northlight kept at go-live (contract
dates and drills); v1 adds every certificate, credential, reference revision, freeze and seasonal peak the customer's
own teams knew about. Deterministic stand-in."""
import _paths  # noqa: F401
from world import CUSTOMERS, span, month_of

CLOCKS = [  # (customer, clock, set on day, fires on day, owner, on the v0 register)
    ("Caldwell", "subscription renewal", 0, 365, "Daniel Reyes", True),
    ("Caldwell", "rollback drill R-46 (quarterly)", 339, 429, "Catherine Doyle", True),
    ("Caldwell", "severe-storm season surge", 0, 428, "Anne Kessler", False),
    ("Caldwell", "model-risk annual review", 158, 523, "Catherine Doyle", False),
    ("Caldwell", "Owen Pryce notice period ends", 458, 488, "Daniel Reyes", False),
    ("Pennant", "subscription renewal", 0, 365, "Grant Holloway", True),
    ("Pennant", "EU lane client certificate (365 days)", 102, 467, "Nadia Brooks", False),
    ("Pennant", "exit drill (twice a year)", 283, 465, "Rosa Delgado", True),
    ("Pennant", "Dana Whitaker leave starts", 300, 344, "Rosa Delgado", False),
    ("Greystone", "largest payer's criteria revision", 120, 384, "Michael Hart", False),
    ("Greystone", "provider account team rotation", 290, 346, "Erin Walsh", False),
    ("Greystone", "EHR upgrade change freeze", 395, 440, "Erin Walsh", False),
    ("Greystone", "annual penetration test", 118, 481, "Sam Oakley", False),
    ("Greystone", "subscription renewal", 196, 561, "Denise Alvarez", True),
]
INCIDENT_CLOCKS = {"severe-storm season surge", "EU lane client certificate (365 days)",
                   "largest payer's criteria revision", "EHR upgrade change freeze"}


def window(c, m0=6, m1=12):
    a, _ = span(c, m0); _, b = span(c, m1)
    return [k for k in CLOCKS if k[0] == c and a <= k[3] <= b]


def main():
    print("CLOCK REGISTER  clocks that fire in production months 6 to 12  (deterministic stand-in)")
    total = before = unreg = 0
    for c, d in CUSTOMERS.items():
        print(f"\n{c} (go-live day {d['go_live']})")
        for _, name, set_day, fire, owner, v0 in sorted(window(c), key=lambda k: k[3]):
            inc = name in INCIDENT_CLOCKS
            pre = set_day <= d["go_live"]
            print(f"  m{month_of(c, fire):>2} day {fire}  {name:<40} set day {set_day:<4} "
                  f"{'before' if pre else 'after '} go-live  owner {owner:<15} v0 register {'yes' if v0 else 'NO '}"
                  f"{'  -> incident' if inc else ''}")
            if inc:
                total += 1; before += pre; unreg += (not v0)
    print(f"\nincidents after month six with a clock: {total}; clock set before go-live: {before}; "
          f"on the v0 register: {total - unreg}")
    n0 = sum(1 for k in CLOCKS if k[5]); print(f"v0 register {n0} clocks; v1 register {len(CLOCKS)} clocks")


if __name__ == "__main__":
    main()
