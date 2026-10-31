"""Ordering rule and displacement guard. Failure injection: Pennant's sprint 2 as it was actually planned,
with a P3 speed item pinned by the sponsor, then the Architecture Review entry check on day 46."""
from cadence_data import pennant_sprint2
from fieldkit.cadence import plan_sprint, gate_check

def show(title, plan):
    print(title)
    for i in plan.selected:
        print(f"  in   {i.key} {i.priority} {i.points:>2} pts  {i.title}")
    for i in plan.deferred:
        print(f"  out  {i.key} {i.priority} {i.points:>2} pts  {i.title}")
    print(f"  points {plan.points} of {plan.capacity}; displacements: {len(plan.violations)}")
    for v in plan.violations:
        print(f"  DISPLACED  {v}")

def main():
    items = pennant_sprint2()
    show("PLAN A  ordering rule (P0 > P1 > P2 > P3), capacity 20", plan_sprint(items, 20))
    items = pennant_sprint2()
    b = plan_sprint(items, 20, pinned=("P-05", "P-03"))
    show("PLAN B  as run: sponsor pins P-05 and P-03, no decision record", b)
    # sprint 2 runs plan B; everything in it is accepted at review on day 42
    for i in b.selected:
        i.status = "accepted" if i.done else "not accepted"
    ok, missing = gate_check("Architecture Review", items, 46)
    print(f"ARCHITECTURE REVIEW ENTRY CHECK  day 46  {'PASS' if ok else 'FAIL'}")
    for m in missing:
        print(f"  missing  {m}")
    acc = [i.key for i in items if i.accepted]
    print(f"sprint 2 review: accepted {len(acc)} of {len(b.selected)} planned items ({', '.join(acc)})")

if __name__ == "__main__":
    main()
