"""Renewal evidence: what each customer's renewal is actually decided on, checked against the event log.
v0 is the renewal pack Northlight planned on day 300 (usage and uptime); v1 is the customer's own list, which at
Caldwell included one runbook executed alone. Deterministic stand-in."""
import _paths  # noqa: F401
from world import CUSTOMERS, MONTHLY

V0 = ["uptime over 99.5%", "volume growth", "monthly service review held"]
REQUIRED = {
    "Caldwell": [("Exhibit E inside the line every month", "Anne Kessler", "monthly"),
                 ("rollback run alone by Caldwell staff (R-46)", "Catherine Doyle", "drill"),
                 ("model-risk annual review opened", "Catherine Doyle", "review"),
                 ("cost per document under the budget line", "Daniel Reyes", "finance")],
    "Pennant": [("matched-definition sample read every week", "Rosa Delgado", "monthly"),
                ("exit drill passed in the last six months", "Grant Holloway", "drill"),
                ("every model change recorded and approved", "Joanne Pruitt", "review"),
                ("cost per document under the budget line", "Joanne Pruitt", "finance")],
    "Greystone": [("material errors inside the line every month", "Michael Hart", "monthly"),
                  ("critical patches inside 14 days", "Sam Oakley", "security"),
                  ("clinic coordinators' acceptance", "Denise Alvarez", "review"),
                  ("cost per referral under the budget line", "Denise Alvarez", "finance")],
}
# evidence log: (customer, item index, day, result, note)
LOG = [
    ("Caldwell", 1, 331, False, "RB-D2 step 4: rollback target extract-2026-01 returned 404 model_not_found"),
    ("Caldwell", 1, 339, True, "RB-D2 passed in 41 minutes; Priya Natarajan ran it, Owen Pritchard refereed"),
    ("Caldwell", 2, 342, True, "Catherine Doyle opened the annual review"),
    ("Caldwell", 3, 345, True, "USD 0.0556 a document against 0.0600"),
    ("Pennant", 0, 351, False, "weeks starting day 344 and day 351 unread: Dana Whitaker on leave, no deputy"),
    ("Pennant", 0, 354, True, "Rosa Delgado read both weeks: 9 and 11 mismatches of 100; Tasha Greene named deputy"),
    ("Pennant", 1, 283, True, "MS-RB-01 passed at 03:00, day 283"),
    ("Pennant", 2, 350, True, "one model change in the year, MC-EU-02, recorded and approved by Joanne Pruitt"),
    ("Pennant", 3, 352, True, "USD 0.0358 a document against 0.0400"),
    ("Greystone", 1, 446, True, "attachment-parser fix live 3 days after the advisory, by emergency change"),
    ("Greystone", 2, 520, True, "coordinator survey, nine clinics"),
    ("Greystone", 3, 525, True, "USD 0.2673 a referral against 0.3000"),
]


def status(c, upto_day):
    req = REQUIRED[c]
    rows = []
    for i, (item, owner, kind) in enumerate(req):
        ev = [e for e in LOG if e[0] == c and e[1] == i and 0 < e[2] <= upto_day]
        if i == 0 and not ev:
            d = CUSTOMERS[c]; m = MONTHLY[c]
            n = sum(1 for k in range(12) if d["go_live"] + 30 * (k + 1) - 1 <= upto_day)
            bad = [k + 1 for k in range(n) if m["errors"][k] >= d["line"]]
            rows.append((item, owner, not bad, f"{n} closed months; at or over the line in month(s) {bad or 'none'}"))
            continue
        ev = [e for e in LOG if e[0] == c and e[1] == i and 0 < e[2] <= upto_day]
        if not ev:
            rows.append((item, owner, None, "no evidence yet")); continue
        last = ev[-1]
        rows.append((item, owner, last[3], f"day {last[2]}: {last[4]}"))
    return rows


def show(c, day, title):
    print(f"\n{c} renewal evidence on day {day} ({title}); renewal due day {CUSTOMERS[c]['renewal_day']}")
    for item, owner, ok, note in status(c, day):
        mark = {True: "PASS", False: "FAIL", None: "OPEN"}[ok]
        print(f"  {mark:<4} {item:<48} owner {owner:<16} {note}")
    rows = status(c, day)
    return sum(1 for r in rows if r[2] is True), len(rows)


def main():
    print("RENEWAL EVIDENCE  (deterministic stand-in)")
    print("v0, the pack Northlight planned on day 300: " + "; ".join(V0) + ". Every line green at all three.")
    print("v1, the customer's list, checked against the evidence log:")
    for c, day, t in [("Caldwell", 333, "after the first drill"), ("Caldwell", 346, "before signature"),
                      ("Pennant", 352, "before signature"), ("Greystone", 466, "after month 9")]:
        k, n = show(c, day, t)
        print(f"  -> {k} of {n} pass")


if __name__ == "__main__":
    main()
