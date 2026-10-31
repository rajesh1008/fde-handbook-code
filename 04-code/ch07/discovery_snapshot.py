"""Snapshot of Chapter 6's discovery output at Caldwell Mutual as of day 22 (frozen here so this lab runs on its
own; source: 04-code/ch06, caldwell_discovery.py and permissions.py) [CHECK ch06].
Thirty-one discovery items: eleven intake paths, seven exception types, four permission gaps, nine open notes."""
PATHS = {  # id: (name, documented in the 2014 procedure, documents a month)
    "P01": ("paper mail, Hartford mailroom", True, 4100), "P02": ("main claims fax line", True, 2300),
    "P03": ("claims shared mailbox", True, 2900), "P04": ("agent portal upload", False, 2450),
    "P05": ("closed Springfield fax number, forwarded", False, 610), "P06": ("email to an adjuster, forwarded", False, 540),
    "P07": ("phone report, papers follow by mail", False, 980), "P08": ("administrator's nightly file transfer", False, 420),
    "P09": ("mail routed through the finance cage", False, 160), "P10": ("attorney letters through legal", False, 230),
    "P11": ("repair-estimate platform email", False, 110),
}
EXCEPTIONS = {"X1": "existing claim, not new", "X2": "policy number missing or unreadable",
              "X3": "duplicate via a second door", "X4": "wrong line of business", "X5": "loss date missing",
              "X6": "several claims in one envelope", "X7": "not a claim"}
GAPS = {"G1": "find the policy when the number is missing (policy search by name and address)",
        "G2": "attach papers to an existing claim", "G3": "read attorney letters", "G4": "read mail held by finance"}
NOTES = {"N1": "date received meant different things to Northlight and to Anne Kessler (Ch3)",
         "N2": "claims-core read-only account in review since day 5",
         "N3": "adjusters correct first-notice fields after contact",
         "N4": "phone reports open a claim before any paper arrives",
         "N5": "special investigations and litigated claims handled apart",
         "N6": "claims-sample-200 request: 200 closed first-notice files",
         "N7": "Priya Natarajan's day-4 question: who reads the logs",
         "N8": "Northlight copies deleted on day 4; derived data not discussed",
         "N9": "administrator's nightly file arrives with its own timestamps"}
ITEMS = list(PATHS) + list(EXCEPTIONS) + list(GAPS) + list(NOTES)
TOTAL_DOCS = sum(v[2] for v in PATHS.values())
