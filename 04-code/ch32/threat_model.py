"""Threat model of the document agent: STRIDE plus an agent category, scored before and after controls."""
import _paths  # noqa: F401
from fieldkit.security import CATEGORIES, AGENT, band
from world import THREATS

tm = THREATS
print(f"{tm.system}: {len(tm.threats)} threats across {len({t.component for t in tm.threats})} components")
bc = tm.by_category()
print("by category: " + ", ".join(f"{c} {bc[c]}" for c in CATEGORIES))
print(f"found by STRIDE alone: {tm.stride_only()} of {len(tm.threats)}; the agent category adds {bc[AGENT]}")
b = tm.bands(residual=False)
print("inherent risk:  " + ", ".join(f"{k} {b[k]}" for k in ("high", "medium", "low")))
b = tm.bands(residual=True)
print("with controls:  " + ", ".join(f"{k} {b[k]}" for k in ("high", "medium", "low")))
print("no control in place on day 103:")
for t in tm.uncontrolled():
    print(f"  {t.id} {t.component:<15} {t.category:<23} L{t.likelihood} x I{t.impact} = {t.inherent:>2} {band(t.inherent):<6} -> {t.finding}")
