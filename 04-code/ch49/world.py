"""Chapter 49 world: the three engagements' year-one ledgers, signature (day 1) to day 365.

Deterministic stand-in. Hours to day 190 are the frozen ledgers of Chapter 46 (Listing 46.1); hours after day 190
are this chapter's stand-in, itemized so a reader can argue with each line. Cost basis is Chapter 2's: hours at a
$150 loaded rate, model and hosting, a 10% product-support share of subscription recognized, and contract
commitments. Every amount is US dollars. No model calls.
"""
LOADED = 150
SUPPORT = 0.10
YEAR = 365

CUST = {
    "caldwell": dict(name="Caldwell Mutual", acv=1_600_000, sub_from=1, fee=200_000, fee_kind="fixed",
                     live=158, stable=248, h190=3_450, run_total=63_123, commitments=142_000, commit_from=149,
                     run_rates=(3_000, 9_000)),
    "greystone": dict(name="Greystone Health", acv=2_400_000, sub_from=None, fee=450_000, fee_kind="T&M cap",
                      rate=260, live=None, stable=None, h190=3_300, run_total=None, commitments=0, commit_from=None,
                      run_rates=(4_000, 12_000)),
    "pennant": dict(name="Pennant Logistics", acv=740_000, sub_from=1, fee=41_600 + 779_684, fee_kind="phased",
                    live=168, stable=258, h190=2_460, run_total=None, commitments=0, commit_from=None,
                    run_rates=(2_500, 6_000), managed_from=290, managed_fee=22_000, managed_margin=0.345),
}

# Hours after day 190 (stand-in). Caldwell's line is Chapter 46's 0.5 FTE sustain forecast.
AFTER = {
    "caldwell": {"sustain and retainer (0.5 FTE)": 403},
    "greystone": {"shadow support and letter fixes": 520, "evaluation suite reruns": 260,
                  "payer-rule changes": 230, "steering and sponsor": 120, "blocked": 158},
    "pennant": {"production operations to Live Stable": 300, "hand-over rebuild after the sponsor left": 180,
                "Live Stable evidence": 120, "incident INC-P-038": 90, "runbooks and exit drills": 140,
                "managed-service scoping": 40, "night duty never booked": 61},
}

MILESTONES = {
    "caldwell": [(47, "first real documents"), (141, "Build Complete"), (157, "Shadow Exit"), (158, "live"),
                 (183, "hand-over review 0.90"), (248, "Live Stable"), (249, "retainer")],
    "greystone": [(103, "security review 29/12"), (130, "security sign-off"), (131, "pilot, draft-only"),
                  (152, "go-live asked, declined"), (270, "month nine, not live"), (365, "still in shadow")],
    "pennant": [(23, "API denied"), (124, "shadow"), (142, "DPA v3"), (168, "live"), (182, "sponsor leaves"),
                (258, "Live Stable"), (283, "exit drill passed"), (290, "managed service")],
}


def hours(c):
    return CUST[c]["h190"] + sum(AFTER[c].values())


def run_total(c):
    d = CUST[c]
    if d["run_total"]:
        return d["run_total"]
    pilot, prod = d["run_rates"]
    live = d["live"] or YEAR + 1
    return round(pilot * (min(live, YEAR + 1) - 1) / 30.4 / 10) * 10 + round(prod * max(0, YEAR + 1 - live) / 30.4 / 10) * 10


def _month_round(x):
    return round(x / 250) * 250


def year_one(c):
    """Revenue and cost lines for days 1 to 365."""
    d = CUST[c]
    rev, cost = {}, {}
    sub = d["acv"] if d["sub_from"] else 0
    rev["subscription"] = sub
    rev["services (" + d["fee_kind"] + ")"] = d["fee"]
    if d.get("managed_from"):
        months = (YEAR + 1 - d["managed_from"]) / 30.4
        rev["managed service"] = _month_round(d["managed_fee"] * months)
    h = hours(c)
    cost["FDE hours"] = h * LOADED
    if d.get("managed_from"):
        cost["managed service delivery"] = round(rev["managed service"] * (1 - d["managed_margin"]))
    cost["model and hosting"] = run_total(c)
    cost["product support and platform"] = round(SUPPORT * sub)
    if d["commitments"]:
        cost["contract commitments"] = d["commitments"]
    R, C = sum(rev.values()), sum(cost.values())
    return dict(rev=rev, cost=cost, revenue=R, costs=C, gp=R - C, margin=(R - C) / R, hours=h)


def daily(c):
    """Cumulative gross profit at each day, 1..365 (revenue and cost spread by the rules in the docstring)."""
    d = CUST[c]
    y = year_one(c)
    h_a = sum(AFTER[c].values())
    pilot, prod = d["run_rates"]
    live = d["live"] or YEAR + 1
    w = [pilot if day < live else prod for day in range(1, YEAR + 1)]
    run = [y["cost"]["model and hosting"] * x / sum(w) for x in w]
    out, cum, billed = [], 0.0, 0.0
    for day in range(1, YEAR + 1):
        hr = d["h190"] / 190 if day <= 190 else h_a / (YEAR - 190)
        r = (d["acv"] / YEAR) if d["sub_from"] else 0.0
        if d["fee_kind"] == "T&M cap":
            add = min(hr * d["rate"], d["fee"] - billed)
            billed += add
            r += add
        else:
            r += d["fee"] / (live - 1) if day < live else 0.0
        k = hr * LOADED + run[day - 1] + SUPPORT * ((d["acv"] / YEAR) if d["sub_from"] else 0.0)
        if d["commitments"] and day >= d["commit_from"]:
            k += d["commitments"] / (YEAR + 1 - d["commit_from"])
        if d.get("managed_from") and day >= d["managed_from"]:
            m = y["rev"]["managed service"] / (YEAR + 1 - d["managed_from"])
            r += m
            k += m * (1 - d["managed_margin"])
        cum += r - k
        out.append(cum)
    return out
