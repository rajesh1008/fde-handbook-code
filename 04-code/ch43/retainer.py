"""Pricing a retainer from an hours band at Northlight's loaded rate. Usage: python retainer.py
Margin at half, full, one-and-a-half and double use; then the same band with unused hours rolling over."""
import world as W  # noqa: F401  (paths)
from fieldkit.service import price_retainer

print("RETAINER PRICING  $150/h loaded, target margin 60%, floor 40%, overage at 1.25x  (deterministic stand-in)")
print("band h  monthly fee  effective $/h  overage $/h  margin@50%  @100%  @150%  @200%")
for band in (8, 12, 16, 24, 40):
    r = price_retainer(band)
    m = [r.margin(band * k) for k in (0.5, 1.0, 1.5, 2.0)]
    print(f"{band:>6}  ${r.fee:>10,.0f}  ${r.hourly:>12,.2f}  ${r.overage:>10,.2f}  " + "  ".join(f"{x*100:>5.1f}%" for x in m))
r = W.RET12
print("\nCaldwell's 12-hour band with unlimited rollover: three quiet months bank 21 hours, then a model upgrade")
bank, rows = 0.0, []
for month, used in ((1, 5), (2, 4), (3, 6), (4, 33)):
    carried = bank
    mg = r.margin(used, carried=carried)
    bank = max(0.0, bank + r.band - used)
    print(f"  month {month}: used {used:>2} h, carried in {carried:>4.0f} h, margin {mg*100:>6.1f}%")
print("  without rollover month 4 margin: " + f"{r.margin(33)*100:.1f}%")
