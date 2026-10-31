"""Listing 34.9: liability follows the action. Each action the system can take, its release level, who decides,
and what the signed clause says. Also the reconstructability retrofit cost ([CHECK ch34] from Chapter 4)."""
import _paths  # noqa: F401
from fieldkit.contract import extract, lint
import world as W

ACTIONS = [  # customer, action, level, who decides, clause treatment
    ("Caldwell", "extract fields from a claim file", "read and draft", "adjuster reviews or the router proceeds",
     "CA-09 v5 cap: 12 months of fees"),
    ("Caldwell", "route a document to review", "draft", "router threshold signed by Anne Kessler",
     "CA-09 v5 cap; the threshold record is evidence"),
    ("Caldwell", "write an accepted draft to the claim", "write (compensated)", "release boundary (Ch25)",
     "CA-09 v5 cap; compensation path is evidence"),
    ("Caldwell", "set reserve, status or assignment", "refused", "Anne Kessler refused (Ch25)", "outside the system"),
    ("Greystone", "draft a prior-authorization request", "draft", "coordinator, then clinician",
     "GA-03 v127: capped; decisions on drafts are Greystone's"),
    ("Greystone", "submit to a payer", "refused", "Michael Hart's rule (Ch25)", "GA-03 v108 indemnified it anyway"),
    ("Greystone", "contact a patient", "refused", "Michael Hart's rule (Ch25)", "GA-03 v108 indemnified it anyway"),
]


def main():
    print("ACTIONS, RELEASE LEVEL AND LIABILITY")
    for c, a, lvl, who, tr in ACTIONS:
        print(f"  {c:10} {a:37} {lvl:20} {who:40} {tr}")
    cs, _, _ = extract(W.GREYSTONE_108)
    lint(cs, dependencies=W.GREYSTONE_DEPS, decisions=W.GREYSTONE_DECISIONS)
    print("\nLINT ON GREYSTONE GA-03 (day 108)")
    for c in cs:
        if c.kind == "liability":
            for k, why in c.findings:
                print(f"  {c.cid:8} {k:12} {why}")
    print("\nRECONSTRUCTABILITY: WHAT THE AUDIT AND LIABILITY CLAUSES ASSUME (Caldwell)")
    have = [("document, page, field per output", True), ("prompt, model and code versions per run", True),
            ("gateway logs readable by Caldwell", True), ("reviewer corrections with who and when", True),
            ("evidence-pack format agreed with model risk", True)]
    for k, v in have:
        print(f"  {'recorded' if v else 'MISSING '}  {k}")
    built, retro = 60, 240
    print(f"  recorded from the first shadow run (day 106): build cost about {built} h (${built * W.LOADED_RATE:,}), "
          f"already spent in Ch17")
    print(f"  retrofit if it had been missing at signature: about {retro} h (${retro * W.LOADED_RATE:,}) forward only;"
          f" every earlier output stays unreconstructable and has to be carved out of the audit clause")


if __name__ == "__main__":
    main()
