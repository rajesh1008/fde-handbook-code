"""Listing 44.1: the function's headcount, month by month (deterministic stand-in)."""
import world as W
from practice import headcount
rows = headcount()
print("month  headcount  in/out this month")
for m, n, _on in rows:
    ev = [f"{'+' if k == 'in' else '-'}{p}" for (em, p, k, _x) in W.EVENTS if em == m]
    print(f"{m:>5}  {n:>9}  {', '.join(ev)}")
avg = sum(n for _m, n, _o in rows) / 12
left = [p for (_m, p, k, _x) in W.EVENTS if k == "out"]
print(f"peak headcount: {max(n for _m, n, _o in rows)} (months {', '.join(str(m) for m, n, _o in rows if n == 6)})")
print(f"left the function: {len(left)} ({', '.join(left)}); average headcount {avg:.2f}; "
      f"annualized attrition {len(left) / avg:.0%}")
print(f"hires through the old loop: 3; of those still on the function at month 12: 1")
