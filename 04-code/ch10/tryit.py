"""Try It Yourself, Chapter 10.  python tryit.py a|b|c"""
import sys, _path  # noqa: F401
from inventories import pennant, greystone, PENNANT_KINDS
from fieldkit.integration import Inventory, Line, SPREAD

ex = sys.argv[1] if len(sys.argv) > 1 else "a"
if ex == "a":   # confirm the facts and watch the range narrow
    inv = pennant(); before = inv.simulate()
    for l in inv.lines:
        if l.status in ("proposed design", "decision required"):
            l.status = "direct customer fact"
    after = inv.simulate()
    for l in inv.lines:              # six more layouts timed: formats lines within 15% either side
        if l.source == "formats":
            l.low, l.high, l.status = 0.85 * l.likely, 1.15 * l.likely, "direct customer fact"
    timed = inv.simulate()
    for name, e in (("as estimated", before), ("facts confirmed", after), ("and layouts timed", timed)):
        print(f"{name:<18} tax P10 {e.tax.p10:.2f}  P50 {e.tax.p50:.2f}  P90 {e.tax.p90:.2f}  width {e.tax.p90 - e.tax.p10:.2f}")
elif ex == "b":  # the provider says no
    inv = greystone(); d = inv.deny("G-A1", "EHR provider", 41)
    print(f"Greystone day 18: tax {inv.point_tax():.2f}, exposure +{inv.exposure():,.0f} h")
    print(f"provider refuses (day 41): tax {d.point_tax():.2f}, {d.total() - inv.total():+,.0f} h")
    print(f"lint after denial: {d.lint() or 'clean'}")
elif ex == "c":  # the next logistics customer shares half of Pennant's carriers
    nxt = Inventory("next logistics customer", (420, 500, 620), day=0)
    for i, (kind, n, lo, li, hi) in enumerate(PENNANT_KINDS, 1):
        shared = n // 2
        nxt.add(Line(f"N-F{i}", "formats", kind, f"{n - shared} new layouts", (n - shared) * lo, (n - shared) * li,
                     (n - shared) * hi, "reconstructed from supplied artifact", "Pennant spike hours"))
    for l in pennant().lines:
        if not l.lid.startswith("P-F"):
            nxt.lines.append(l)
    e = nxt.simulate()
    print(f"next customer, half the carriers shared: tax {e.point_tax:.2f} (P10 {e.tax.p10:.2f}, P90 {e.tax.p90:.2f}); Pennant {pennant().point_tax():.2f}")
