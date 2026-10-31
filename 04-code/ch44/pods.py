"""Listing 44.6: month-12 staffing as solo owners, as two pods, and as pods with a shared evaluation lead."""
import world as W
from practice import PLANS, evaluate_plan
print("engagement needs at level 3:")
for e, v in W.ENGAGEMENTS.items():
    print(f"  {e:<12} {v['fte']:.1f} FTE  {v['phase']:<32} {', '.join(v['needs'])}")
for name, plan in PLANS.items():
    r = evaluate_plan(name, plan)
    print(f"\n{name}: needs met {r['met']} of {r['needed']}; met by a single person {r['single']}; "
          f"coordination {r['coord']:.0f} h/week")
    for e, x in r["engagements"].items():
        extra = f"; Pennant overnight rota depth {x['oncall']}" if x["oncall"] else ""
        print(f"  {e:<12} gaps: {', '.join(x['gaps']) or 'none':<26} single: {', '.join(x['single']) or 'none'}{extra}")
    print("  load (need FTE, staff FTE, ratio): " + "; ".join(f"{k} {v}" for k, v in r["load"].items()))
