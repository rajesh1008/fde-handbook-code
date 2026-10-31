"""Listing 10.2: the estimator on the three customers' inventories (point, range, exposure, lint)."""
import _path  # noqa: F401
from inventories import ALL
from fieldkit.integration import SOURCES

print(f"{'customer':<18}{'day':>4}{'lines':>6}{'likely h':>10}{'tax':>6}{'P10':>6}{'P50':>6}{'P90':>6}{'exposure':>10}{'lint':>6}")
for key, make in ALL.items():
    inv = make(); e = inv.simulate()
    print(f"{inv.customer:<18}{inv.day:>4}{len(inv.lines):>6}{e.point_hours:>10,.0f}{e.point_tax:>6.2f}"
          f"{e.tax.p10:>6.2f}{e.tax.p50:>6.2f}{e.tax.p90:>6.2f}{inv.exposure():>+9,.0f}h{len(inv.lint()):>6}")
print()
print("likely hours by source")
print(f"{'source':<14}" + "".join(f"{k:>11}" for k in ALL))
rows = {k: m().by_source() for k, m in ALL.items()}
for s in SOURCES:
    print(f"{s:<14}" + "".join(f"{rows[k][s]:>11,.0f}" for k in ALL))
