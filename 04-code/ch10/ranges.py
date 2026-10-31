"""Listing 10.4: ranges, not points. Pennant's day-24 estimate as a seeded simulation, and the share of the range
width that sits on unconfirmed facts, for each customer."""
import _path  # noqa: F401
from inventories import ALL, pennant
from fieldkit.integration import UNCONFIRMED

inv = pennant(); e = inv.simulate()
print(f"PENNANT day 24  20,000 draws, seed 10")
print(f"  integration hours  P10 {e.hours.p10:,.0f}   P50 {e.hours.p50:,.0f}   P90 {e.hours.p90:,.0f}   most likely {e.point_hours:,.0f}")
print(f"  integration tax    P10 {e.tax.p10:.2f}    P50 {e.tax.p50:.2f}    P90 {e.tax.p90:.2f}    most likely {e.point_tax:.2f}")
print(f"  P50 above most likely by {e.tax.p50 - e.point_tax:+.2f}: the high ends are longer than the low ends")
print()
print(f"{'customer':<18}{'width h':>9}{'on unconfirmed':>16}{'share':>7}")
for k, m in ALL.items():
    i = m(); w = sum(l.stretched_high - l.low for l in i.lines)
    u = sum(l.stretched_high - l.low for l in i.lines if l.status in UNCONFIRMED)
    print(f"{i.customer:<18}{w:>9,.0f}{u:>16,.0f}{u / w:>7.0%}")
