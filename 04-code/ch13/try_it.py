"""Try It Yourself, three variations. Run: python try_it.py 1|2|3"""
import sys
from cadence_data import pennant_sprint2, caldwell_sprint2, caldwell_register
from fieldkit.cadence import plan_sprint, review

def one():
    """Shrink Pennant's capacity to 13 points. Which P0 item survives, and does the guard fire?"""
    for cap in (20, 13, 10):
        p = plan_sprint(pennant_sprint2(), cap)
        print(f"capacity {cap:>2}: in {[i.key for i in p.selected]}  out {[i.key for i in p.deferred]}  "
              f"displacements {len(p.violations)}")
        for w in p.warnings:
            print(f"    WARN {w}")

def two():
    """Give C-03 a follow-up with no date. The review must turn it into 'not accepted'."""
    items = [i for i in caldwell_sprint2() if i.key != "C-06"]
    for i in items:
        if i.key == "C-03":
            i.follow_up_day = None
    rv = review("sprint 2", items, 56)
    print({k: [i.key for i in v] for k, v in rv.outcomes.items()}, f"goal {rv.goal_share:.0%}")

def three():
    """Walk the register forward. On which day does each open record cross the stop rule's day-75 deadline?"""
    for day in (56, 63, 70, 77):
        reg = caldwell_register()
        al = reg.alerts(day)
        d01 = reg.records["D-01"]
        print(f"day {day}: alerts {len(al)}; D-01 open {d01.age(day)} days; "
              f"{'PAST the day-75 stop condition in D-07' if day > 75 else f'{75 - day} days to the D-07 deadline'}")

if __name__ == "__main__":
    {"1": one, "2": two, "3": three}[(sys.argv + ["1"])[1]]()
