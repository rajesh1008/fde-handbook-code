"""Figure 29.2: Signature 12, the test pyramid (first appearance; Caldwell's plan on day 140, Listing 29.2)."""
from _common import S, js  # noqa: F401  (sets paths)
import signature12
L = js("layers")
c = lambda n: (f"{L[str(n)][0]:.0f} s" if L[str(n)][0] < 120 else f"{L[str(n)][0] / 60:.0f} min") + f" · ${L[str(n)][1]:.2f}"
signature12.STATES.setdefault("ch29-plan", dict(
    version="Caldwell plan, day 140",
    rows=[("unit", "every commit", c(1)), ("component", "every behavior change", c(2)),
          ("integration", "every merge, nightly", c(3)), ("system", "weekly, every release", c(4)),
          ("operational", "live, daily", f"daily · ${L['5'][1]:.2f}")],
    foot="merge gate: L1 to L3 can block", changed=()))
signature12.render("ch29-plan", "fig29-02", __file__)
