"""Caldwell sprint 2 review on day 56: three outcomes, the exception list, flow measures, and the status lint."""
from cadence_data import caldwell_sprint2, caldwell_register
from fieldkit.cadence import review, lint_status, gate_check, GATES

def main():
    items = [i for i in caldwell_sprint2() if i.key != "C-06"]       # C-06 (P3) was not planned
    rv = review("sprint 2", items, 56)
    print(f"SPRINT REVIEW  Caldwell Mutual  {rv.sprint}  day 56")
    for outcome, its in rv.outcomes.items():
        print(f"  {outcome:<24}{', '.join(i.key for i in its) or '-'}")
    print(f"  goal: {rv.accepted_points} of {rv.committed} points accepted ({rv.goal_share:.0%}); "
          f"carried over: {', '.join(i.key for i in rv.carried) or '-'}; blocked days: {rv.blocked_days}")
    reg = caldwell_register()
    oldest = max((r for r in reg.records.values() if r.status == "open"), key=lambda r: r.age(56))
    print(f"  oldest open dependency: {oldest.key} ({oldest.age(56)} days, {oldest.owner})")
    print("EXCEPTION LIST")
    for k, owner, what, gate in rv.exceptions:
        print(f"  {k:<6}{owner:<18}{what}  [gate: {gate}]")
    ok, missing = gate_check("Architecture Review", items, 56)
    print(f"Architecture Review entry evidence from this sprint: {'complete' if ok else 'incomplete'}")
    gates = {g: False for g in GATES}
    draft = ("Sprint 2 accepted. Extraction is production-ready for the 200-document set; "
             "next sprint we start on the adjuster queue.")
    print("STATUS LINT (draft from the account team)")
    for p in lint_status(draft, gates) or ["clean"]:
        print(f"  {p}")
    fixed = ("Sprint 2: 18 of 23 points accepted; C-03 accepted with a follow-up due day 63. "
             "Gates passed 0 of 5; Architecture Review booked inside the day 40-60 window.")
    print(f"  rewritten: {'clean' if not lint_status(fixed, gates) else 'still flagged'}")

if __name__ == "__main__":
    main()
