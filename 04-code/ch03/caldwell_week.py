"""The first week at Caldwell, as an engagement repository (fieldkit v0).

Every record below is something that happened on days 1 to 5 of the engagement in Chapter 3: day 1 is
the kickoff, day 5 the day the first weekly status went out.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.engagement import EngagementRepo  # noqa: E402

FDE = "Northlight FDE"


def build_week() -> EngagementRepo:
    r = EngagementRepo("Caldwell Mutual")
    # day 1: kickoff in Hartford
    for text in ("Accuracy above 95% on Caldwell's documents.",
                 "Live in production in under five months.",
                 "No integration work on Caldwell's side.",
                 "Works on any document Caldwell receives."):
        r.note(1, "Graham Lowell", "promise", text, source="sales cycle, repeated at kickoff")
    r.note(1, "Daniel Reyes", "fact", "Two earlier pilots stopped at the security review.", source="kickoff")
    r.note(1, "Anne Kessler", "fact", "First notice arrives by mail, fax and email; mail is scanned and "
           "stamped received in the mailroom.", source="kickoff")
    r.request("synthetic-claims-set", "synthetic claims set (Northlight-built, no customer data)",
              "Laura Finch", 1)
    # day 2: the demo
    r.request("aws-sandbox-account", "AWS sandbox account in Caldwell's organization", "Daniel Reyes", 2,
              "in review", blocks="every build inside Caldwell's estate")
    r.measure("E-1", "Field accuracy of the demo on Caldwell documents", "58% (58/100 fields)",
              "Anne Kessler", "10 documents from one week's intake (4 email, 3 fax, 3 mail)", 2,
              location="deleted day 4, attestation filed",
              caveat="ten documents from one week; not a sample")
    r.measure("E-2", "Field accuracy of the demo on Northlight's demo set", "98% (98/100 fields)",
              FDE + " (self-scored)", "10 typed demo forms", 2, location="Northlight demo repository",
              caveat="the forms the demo was built on")
    r.decision("D-1", "Who owns the gold set and the scoring rule?", "Anne Kessler", 2, due_day=8)
    # day 3: the vague ask
    r.request("claims-data-export", "a representative export of claims data", "", 3)
    r.note(3, FDE, "ask", "Email asking for 'a representative export of claims data'; forwarded six times.",
           source="email")
    r.decision("D-2", "Who at Caldwell is the named owner for claims data requests?", "", 3)
    # day 4: architecture review
    r.request("gateway-key", "model gateway key for the Northlight workload", "Priya Natarajan", 4,
              blocks="every model call from Caldwell's estate")
    r.note(4, "Priya Natarajan", "question", "Where does it run? Whose identity does it use? Who sees the logs?",
           source="architecture review")
    r.note(4, "Priya Natarajan", "finding", "Ten Caldwell documents were processed on a Northlight laptop "
           "through Northlight's own model-provider account, outside Caldwell's gateway.",
           source="architecture review")
    r.decision("D-3", "Where does the build run until the sandbox account exists?", "Priya Natarajan", 4,
               due_day=9)
    # day 5: the first weekly status
    r.request("claims-core-readonly", "read-only service account on the claims system", "Daniel Reyes", 5)
    r.decision("D-4", "Which of the four kickoff promises stand, in writing?", "Laura Finch", 5, due_day=6)
    for text in ("Answer Priya Natarajan's three questions in writing.",
                 "Agree the scoring rule and the gold-set owner with Anne Kessler.",
                 "Replace the day-3 email with named, tracked requests."):
        r.note(5, FDE, "plan", text)
    return r


DAY5_DECK = [  # the status deck as it was actually sent on day 5, line by line, with what it cited
    ("Kickoff complete; strong alignment with Caldwell leadership.", None),
    ("Demo validated on Caldwell documents.", None),
    ("Extraction accuracy 98% on claim forms.", "E-2"),
    ("Data access in progress; expect claims data next week.", None),
    ("On track for production in under five months.", None),
    ("Overall status: green.", None),
]
