"""Listing 44.10: going independent. Portfolio of proof, then an 18-month runway in US dollars (illustrative, pre-tax)."""
import world as W
from practice import portfolio_score, runway
for label, p in (("v1 portfolio", W.PORTFOLIO_V1), ("v2 portfolio", W.PORTFOLIO_V2)):
    s = portfolio_score(p)
    print(f"{label}: {s['claims']} claims, {s['showable']} showable, {s['with_metric']} showable with a metric and scorer")
r = W.RUNWAY
print(f"\nrunway: savings US${r['savings']:,}, fixed US${r['fixed_monthly']:,}/month, day rate US${r['day_rate']:,}, "
      f"invoices paid net 30")
for name, s in W.SCENARIOS.items():
    c = runway(s)
    low = min(c); lm = c.index(low) + 1
    back = next((i + 1 for i, v in enumerate(c) if i + 1 > lm and v >= r["savings"]), None)
    print(f"  {name:<44} lowest US${low:>7,} (month {lm:>2}); back to savings: {('month ' + str(back)) if back else 'not by 18'}")
    print("    " + " ".join(f"{v // 1000:>3}k" for v in c))
    worked = [i for i in range(1, 19) if (s["first_month"] <= i and not (s.get("ends") and s["ends"] < i <= s["ends"] + s["gap"]))]
    idle = [i for i in range(s["first_month"], 19) if i not in worked]
    print(f"    billing months {len(worked)}; idle months after first contract {len(idle)}; clients {s['clients']}"
          + (f"; top-client share 100%" if s["clients"] == 1 else ""))
