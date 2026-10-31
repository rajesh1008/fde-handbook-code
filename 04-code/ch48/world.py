"""Chapter 48 world: three customers, twelve production months each, on the book's one engagement-day calendar.

DETERMINISTIC STAND-IN. Every monthly number in this file is the lab's, chosen to be consistent with the canon of
Chapters 39 to 43; none is a measurement. Production month m at a customer runs from go_live + 30 (m - 1) for 30 days.
Canon carried in: Caldwell go-live day 158, Exhibit E errors 2, 4, 3 in months 1 to 3 on 310 a month, breach at 7;
retainer from day 248 (retainer month k = production month k + 3), readiness by retainer month from Chapter 43.
Pennant go-live day 168, managed service from day 290 (service month k = production month k + 4), readiness by
service month from Chapter 43. Greystone go-live day 196 is this chapter's (ledgered), draft-only at two clinics.
"""
MONTH = 30
CUSTOMERS = {
    "Caldwell": dict(go_live=158, renewal_day=365, subscription="from signature", acv=1_600_000,
                     measure="Exhibit E errors in 310", line=7, sample=310,
                     scorer="Lena Ortiz and Tom Whitfield", decider="Anne Kessler", executive="Daniel Reyes"),
    "Pennant": dict(go_live=168, renewal_day=365, subscription="from signature", acv=740_000,
                    measure="matched-definition mismatches in 400", line=24, sample=400,
                    scorer="Dana Whitaker", decider="Rosa Delgado", executive="Grant Holloway"),
    "Greystone": dict(go_live=196, renewal_day=561, subscription="from production", acv=2_400_000,
                      measure="drafts with a material error in 120", line=6, sample=120,
                      scorer="Tess Moreno", decider="Michael Hart", executive="Denise Alvarez"),
}

MONTHLY = {
    "Caldwell": dict(
        volume=[520, 525, 531, 540, 538, 546, 552, 549, 561, 690, 570, 566],          # documents a day
        errors=[2, 4, 3, 3, 2, 4, 3, 2, 3, 6, 3, 2],                                  # of 310, Exhibit E
        proceed=[62.3, 62.0, 62.6, 63.1, 63.4, 63.0, 62.8, 63.5, 66.1, 59.4, 65.8, 66.0],  # % routed proceed
        readiness=[0.90, 0.90, 0.90, 0.925, 0.925, 0.95, 0.95, 0.975, 0.975, 0.975, 0.975, 0.925],
        hours=[310, 190, 120, 5, 4, 6, 9, 8, 21, 9, 7, 12],                          # Northlight hours
        model=["extract-2026-04"] * 8 + ["extract-2027-01"] * 4,
    ),
    "Pennant": dict(
        volume=[2100, 2380, 2450, 2150, 2120, 2140, 2180, 2160, 2200, 2230, 2190, 2260],  # weekday documents
        errors=[15, 21, 13, 12, 11, 10, 12, 11, 14, 17, 11, 10],                           # of 400 a month
        proceed=None,
        readiness=[0.80, 0.80, 0.80, 0.80, 0.75, 0.75, 0.75, 0.775, 0.775, 0.80, 0.80, 0.80],
        hours=[290, 330, 240, 150, 112, 110, 108, 111, 109, 126, 108, 107],
        model=["extract-2026-01"] * 2 + ["extract-2026-04"] * 6 + ["extract-2027-01"] * 4,
    ),
    "Greystone": dict(
        volume=[90, 95, 170, 265, 400, 405, 410, 415, 420, 410, 425, 430],     # referrals a day
        clinics=[2, 2, 4, 6, 9, 9, 9, 9, 9, 9, 9, 9],
        errors=[5, 4, 4, 3, 3, 4, 9, 3, 2, 3, 2, 2],                           # of 120 drafts, material error
        proceed=None,
        readiness=[0.40, 0.45, 0.50, 0.55, 0.60, 0.55, 0.60, 0.65, 0.65, 0.70, 0.75, 0.80],
        hours=[420, 380, 400, 360, 330, 250, 210, 190, 230, 170, 160, 150],
        model=["extract-2026-04"] * 12,
    ),
}


def span(c, m):
    s = CUSTOMERS[c]["go_live"] + MONTH * (m - 1)
    return s, s + MONTH - 1


def month_of(c, day):
    return (day - CUSTOMERS[c]["go_live"]) // MONTH + 1
