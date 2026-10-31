"""Listing 3.3: rewrite the four kickoff promises so each has a verifier at Caldwell (decision D-4, day 6).

Run:  python day6_promises.py
"""
from caldwell_week import build_week

REWRITES = [  # (old promise starts with, new statement, verifier at Caldwell, or None if withdrawn)
    ("Accuracy above 95%",
     "Field accuracy is scored by Anne Kessler on a sample she selects; the target is set after the first score.",
     "Anne Kessler"),
    ("Live in production",
     "Production means passing five gates, each with a named approver at Caldwell and a date in the plan.",
     "Priya Natarajan"),
    ("No integration work",
     None, None),
    ("Works on any document",
     "In scope: first notice of loss by email, fax and mail, as listed by Anne Kessler; everything else is out.",
     "Anne Kessler"),
]
CALDWELL_WORK = ("Caldwell's work list: sandbox account, gateway key, claims-core read-only account, "
                 "each with an owner in the access list.")


def main():
    repo = build_week()
    before = [p for p in repo.lint(today=5) if p.startswith("PROMISE")]
    print(f"day 5  promises with no verifier: {len(before)}")
    promises = [n for n in repo.notes if n.kind == "promise"]
    for old, new, verifier in REWRITES:
        note = next(n for n in promises if n.text.startswith(old))
        note.closed_day = 6
        if new is None:
            print(f"  withdrawn  {note.text}")
            repo.note(6, "Laura Finch", "promise", CALDWELL_WORK, source="D-4", verifier="Daniel Reyes")
            print(f"  replaced   {CALDWELL_WORK}  [verifier: Daniel Reyes]")
        else:
            repo.note(6, "Laura Finch", "promise", new, source="D-4", verifier=verifier)
            print(f"  rewritten  {new}  [verifier: {verifier}]")
    repo.decide(
        "D-4", 6, "Three promises rewritten, one withdrawn and replaced by a work list; sent to Daniel Reyes in writing.")
    after = [p for p in repo.lint(today=6) if p.startswith("PROMISE")]
    print(f"day 6  promises with no verifier: {len(after)}")
    print("remaining lint:")
    for p in repo.lint(today=6):
        print(f"  {p}")


if __name__ == "__main__":
    main()
