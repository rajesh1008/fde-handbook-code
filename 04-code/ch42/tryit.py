"""Try It Yourself exercises for Chapter 42. Usage: python tryit.py a|b|c
a  Move the leading alarm: the fingerprint PSI alarm at 0.10, 0.25 and 0.50. First alarm day, and silently wrong
   documents between the layout change (day 19) and the day after the alarm (containment), in this replay.
b  Move the provider notice: the same 21-day deprecation notice landing on days 20, 30, 41 and 50 against the
   day 45-75 freeze. Which ones need a freeze exception, and how much slack is left.
c  The two-of-five rule and its blind spot: one person holds three proofs and the provider account."""
import sys
import _paths  # noqa: F401
from world import CAL, day_docs, outcome, bins
from fieldkit.liveops import deprecation_plan, OwnershipMap
from fieldkit.synthetic import psi

ex = sys.argv[1] if len(sys.argv) > 1 else "a"
if ex == "a":
    FP = lambda docs: bins([x[5] for x in docs])
    base = FP([x for d in range(-7, 0) for x in day_docs(d)])
    series = {d: psi(base, FP([x for k in range(max(1, d - 6), d + 1) for x in day_docs(k)])) for d in range(1, 46)}
    silent = {d: sum(outcome(x, 0.80) == "silent" for x in day_docs(d)) for d in range(1, 46)}
    print("alarm  first day  silently wrong days 19 to containment")
    for a in (0.10, 0.25, 0.50):
        first = next(d for d, p in series.items() if p >= a)
        print(f"{a:5.2f}  {first:>9}  {sum(silent[d] for d in range(19, first + 2)):>5}")
    print("max PSI before day 19 (false-alarm margin): "
          f"{max(p for d, p in series.items() if d < 19):.3f}")
elif ex == "b":
    print("notice  retire  in freeze  exception  action")
    for n in (20, 30, 41, 50):
        p = deprecation_plan(n, n + 21, [CAL["freeze"]], evidence_days=7)
        print(f"{n:>6}  {n + 21:>6}  {str(p['retire_in_freeze']):>9}  {str(p['freeze_exception']):>9}  "
              f"{p['action']} (slack {p['slack_days']})")
else:
    m = OwnershipMap()
    m.add("own-exec", "Jenna Ruiz")
    m.add("own-operations", "Jenna Ruiz", deputy="Rosa Delgado")
    m.add("own-override", "Jenna Ruiz", deputy="Rosa Delgado")
    m.add("own-gold-set", "Dana Whitaker", exercised=True)
    m.add("own-model-risk", "Joanne Pruitt", exercised=True)
    m.add("provider account", "Jenna Ruiz")
    print(f"two-of-five rule: {m.two_of_five() or 'passes (3 proofs, 2 with a deputy)'}")
    print("no deputy: " + "; ".join(m.single_points()))
    m.leave("Jenna Ruiz")
    print("orphaned when Jenna Ruiz leaves: " + ", ".join(m.orphans()))
