"""The twelve-month calendar: production months per customer on the shared engagement-day calendar, the events
that land in each, and how the months map onto Chapter 43's retainer and service months. Deterministic stand-in."""
import _paths  # noqa: F401
from world import CUSTOMERS, span, month_of

EVENTS = [  # (customer, day, kind, text)
    ("Caldwell", 158, "go-live", "production day 0, ~520 documents a day, router v1.1"),
    ("Caldwell", 183, "people", "hand-over drill 2, readiness 0.60 to 0.90"),
    ("Caldwell", 248, "contract", "Live Stable; retainer signed, 12-hour band"),
    ("Caldwell", 331, "renewal", "rollback drill alone fails at step 4"),
    ("Caldwell", 339, "renewal", "rollback drill alone passes"),
    ("Caldwell", 358, "renewal", "subscription renewal signed (due day 365)"),
    ("Caldwell", 370, "model", "upgrade dry run alone; observer duty ends"),
    ("Caldwell", 402, "model", "extract-2027-01 promoted by Caldwell staff"),
    ("Caldwell", 430, "incident", "storm surge, review queue past 48 hours"),
    ("Caldwell", 488, "people", "Owen Pryce leaves; sole holder of T3"),
    ("Pennant", 168, "go-live", "production day 0, ~2,100 documents a weekday"),
    ("Pennant", 223, "model", "EU lane migrated to extract-2026-04"),
    ("Pennant", 258, "contract", "Live Stable"),
    ("Pennant", 290, "contract", "managed service starts"),
    ("Pennant", 358, "renewal", "subscription renewal signed (due day 365)"),
    ("Pennant", 344, "people", "Dana Whitaker on twelve weeks' leave"),
    ("Pennant", 422, "model", "extract-2027-01 promoted under MC-EU-03"),
    ("Pennant", 465, "contract", "second exit drill due"),
    ("Pennant", 467, "incident", "EU lane client certificate expires 02:10"),
    ("Greystone", 181, "contract", "Shadow Exit signed"),
    ("Greystone", 196, "go-live", "draft-only at two clinics"),
    ("Greystone", 256, "contract", "four clinics live (wave 2)"),
    ("Greystone", 316, "contract", "nine clinics live (wave 4)"),
    ("Greystone", 346, "people", "managed-service provider rotates its account team"),
    ("Greystone", 384, "incident", "payer criteria revision; drafts cite old criteria"),
    ("Greystone", 410, "model", "extract-2027-01 replay: ROLLBACK, stays on extract-2026-04"),
    ("Greystone", 440, "freeze", "EHR upgrade change freeze, days 440 to 461"),
    ("Greystone", 443, "incident", "critical advisory in the attachment parser"),
    ("Greystone", 561, "renewal", "subscription renewal due (from production)"),
]
NORTHLIGHT = [(301, "Maya Brooks leaves Northlight (function month 11)"),
              (331, "lead FDE moves to lead Harbourline; Sofia Brennan leads Caldwell, Callum Reid Greystone, "
                    "Leo Martens Pennant (function month 12)")]


def main():
    print("THE TWELVE-MONTH CALENDAR  one engagement-day calendar, 30-day production months  (deterministic stand-in)")
    for c, d in CUSTOMERS.items():
        s1, _ = span(c, 1); _, e12 = span(c, 12)
        print(f"\n{c}: go-live day {d['go_live']}, month 12 ends day {e12}, renewal day {d['renewal_day']} "
              f"(production month {month_of(c, d['renewal_day'])}), subscription {d['subscription']}")
        for m in range(1, 13):
            a, b = span(c, m)
            ev = [f"{day} {kind}: {t}" for cc, day, kind, t in sorted(EVENTS, key=lambda x: x[1])
                  if cc == c and a <= day <= b]
            tag = "  <- month nine" if m == 9 else ""
            print(f"  m{m:>2} days {a}-{b}{tag}")
            for e in ev:
                print(f"        {e}")
    print("\nMONTH MAPPING")
    print("  Caldwell retainer month k  = production month k + 3 (retainer month 1 starts day 248)")
    print("  Pennant service month k    = production month k + 4 (service month 1 starts day 290)")
    print("  Northlight function month n = engagement days 30(n-1)+1 to 30n")
    for day, t in NORTHLIGHT:
        print(f"  day {day}: {t}; Caldwell m{month_of('Caldwell', day)}, Pennant m{month_of('Pennant', day)}, "
              f"Greystone m{month_of('Greystone', day)}")
    print("\nMONTH NINE AT ALL THREE")
    for c in CUSTOMERS:
        a, b = span(c, 9)
        print(f"  {c:<9} days {a}-{b}: " + "; ".join(t for cc, day, k, t in EVENTS if cc == c and a <= day <= b))


if __name__ == "__main__":
    main()
