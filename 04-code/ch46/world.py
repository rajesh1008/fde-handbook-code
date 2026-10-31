"""Chapter 46 world: three engagements' hours ledgers frozen at day 190, their estimates and contracts.

Deterministic stand-in. The actual hours are this book's invented actuals, consistent with the canon
(Caldwell 2,750 hours by day 136 and about 400 more to go-live; Greystone still in shadow; Pennant on the
phased services form). Estimates are the Chapter 2 field estimates for every bucket except integration,
where Chapter 10's itemized P50 superseded them. Dollars are US dollars. Loaded FDE rate $150 an hour.
"""
RATE = 150.0                      # loaded cost of an FDE hour, US dollars
BILL = 260.0                      # Northlight's time-and-materials rate
FTE_MONTH = 140                   # hours one FDE books to one account in a month (Chapter 2)
CUTOFF = 190                      # day the ledgers were frozen for this chapter
BUCKETS = ("discovery", "access", "model", "integration", "gates", "handover", "blocked")

ACTUAL = {   # hours booked days 1 to 190
    "caldwell":  dict(discovery=260, access=430, model=720, integration=700, gates=620, handover=380, blocked=340),
    "greystone": dict(discovery=270, access=480, model=530, integration=1060, gates=560, handover=20, blocked=380),
    "pennant":   dict(discovery=160, access=190, model=520, integration=1020, gates=300, handover=150, blocked=120),
}
# Chapter 2 field estimates; blocked = wait months x FTE x 140 x 0.5; integration = Chapter 10 P50 (Pennant: phase-one option B)
ESTIMATE = {
    "caldwell":  dict(discovery=220, access=260, model=700, integration=585, gates=380, handover=200, blocked=262.5),
    "greystone": dict(discovery=260, access=420, model=900, integration=803, gates=560, handover=240, blocked=630),
    "pennant":   dict(discovery=200, access=160, model=500, integration=886, gates=200, handover=160, blocked=70),
}
# a bucket counts toward calibration only once it is closed (its work is finished, not merely started)
CLOSED = {
    "caldwell":  set(BUCKETS),                                            # live day 158, hand-over drill passed
    "greystone": {"discovery", "access", "model", "integration"},         # in shadow since day 131
    "pennant":   {"discovery", "access", "model", "integration"},         # build finished, gates still open
}
# Chapter 10 tax ranges (P10 to P90) on the model hours the inventory assumed
TAX_RANGE = {"caldwell": (0.81, 1.02, 643), "greystone": (1.34, 1.78, 521), "pennant": (1.60, 2.05, 500)}

# integration hours itemized by the six sources (Caldwell actuals, ledger tags)
CALDWELL_SOURCES = dict(access=40, identity=90, formats=210, exceptions=160, environments=90, gateways=110)

CONTRACT = {
    "caldwell":  dict(acv=1_600_000, form="fixed fee", fee=200_000, priced_h=1260, sub_from=1),
    "greystone": dict(acv=2_400_000, form="T&M with cap", fee=450_000, rate=BILL, sub_from=None),
    "pennant":   dict(acv=740_000, form="phased", fee=41_600 + 779_684, disc_h=160, priced_h=2999, sub_from=1),
}
# phases: (name, first day, last day, hours, blocked hours inside)
PHASES = {
    "caldwell":  [("discovery", 1, 26, 400, 30), ("build", 27, 141, 2430, 260), ("shadow", 142, 157, 300, 20), ("live", 158, 190, 320, 30)],
    "greystone": [("discovery", 1, 19, 330, 20), ("build", 20, 130, 2240, 200), ("shadow", 131, 190, 730, 160)],
    "pennant":   [("discovery", 1, 28, 200, 0), ("build", 29, 190, 2260, 120)],
}
RUN = {"caldwell": (3000, 9000, 142, 158), "greystone": (4000, 12000, 131, None), "pennant": (2500, 6000, None, None)}
SUPPORT = 0.10                    # product support and platform share of subscription revenue (Chapter 2)


def total(d):
    return sum(d[b] for b in BUCKETS)


def tax(name):
    a = ACTUAL[name]
    return a["integration"] / a["model"]
