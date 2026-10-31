"""Hand-over readiness for one customer state. Usage: python readiness.py caldwell-before|caldwell-after|pennant"""
import sys
import world as W
from fieldkit.handover import score, without, single_points

STATES = {"caldwell-before": (W.CALDWELL_BEFORE, "Caldwell, day 176 (drill 1)"),
          "caldwell-after": (W.CALDWELL_AFTER, "Caldwell, day 183 (drill 2)"),
          "pennant": (W.PENNANT, "Pennant, readiness review")}
state, label = STATES[sys.argv[1]]
it = W.items(state)
print(f"hand-over readiness: {label}")
print(f"{'item':<5}{'dimension':<12}{'status':<10}{'gate':<6}demonstrated by")
for i in it:
    print(f"{i.id:<5}{i.dim:<12}{i.status:<10}{'gate' if i.gate else '':<6}{', '.join(i.by) or '-'}")
s = score(it)
print(f"naive (artifact exists)      {s.naive:.2f}")
print(f"evidence credit (raw)        {s.raw:.3f}")
print(f"gated score                  {s.gated:.2f}" + (f"  capped: gates failing {', '.join(s.failing_gates)}" if s.failing_gates else ""))
dims = {}
for i in it:
    dims.setdefault(i.dim, []).append(i)
print("by dimension: " + "  ".join(f"{d} {score(v).raw:.2f}" for d, v in dims.items()))
sp = single_points(it)
print("largest single-person drops: " + ("; ".join(f"{p} -{d:.2f} (to {s.gated - d:.2f})" for p, d in sp[:3]) or "none"))
