"""Try It Yourself. Run: python tryit.py 1|2|3"""
import sys
import _path  # noqa: F401
from fieldkit.bid import Clarification, extract, lint, triage, five_moves, Question
import harbourline as H

ex = sys.argv[1] if len(sys.argv) > 1 else "1"
if ex == "1":   # a new clarification arrives in round 2: does it contradict anything we already wrote?
    new = Clarification("CL-36", "Does the bank's directory provision vendor tenants on the day of a change?",
                        "No. Joiner and leaver changes reach vendor tenants overnight, on the next business day.",
                        ("directory",), ("on the day",), False, 2)
    claims = extract(H.RESPONSE_V10)
    for k, lvl, code, msg in lint(claims, H.clarifications() + [new]):
        if code == "CONTRADICTED":
            print(k, code, msg)
elif ex == "2":  # your own RFP: tag five questions and route them as your bid manager did
    qs = [Question("Q1", "X", "Describe the integration with our CRM.", ("integration",), "engineering"),
          Question("Q2", "X", "State the price per user.", ("price",), "sales"),
          Question("Q3", "X", "State uptime and service credits.", ("operations", "terms"), "sales"),
          Question("Q4", "X", "Describe your support model and its cost.", ("operations", "price"), "joint"),
          Question("Q5", "X", "Describe how you will exit.", ("exit",), "sales")]
    print(triage(qs)[0]); print(triage(qs)[2])
else:            # write your five moves for: "What happens when our gateway refuses a call?"
    mine = dict(position="", evidence="", example="", boundary="", proof="")
    print(five_moves(mine))
