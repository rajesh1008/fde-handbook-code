"""Listing 10.3: failure injection. Pennant's day-21 estimate assumes the TMS has a status API; on day 23 the
architects say it does not. Shown twice: the estimate as Northlight first wrote it (point, no lint), and the
estimator's guard on the same inventory with the alternative left unpriced."""
import _path  # noqa: F401
from inventories import pennant
from fieldkit.integration import Inventory

FDES, HOURS_PER_WEEK, RATE = 2, 32, 150   # integration hours per FDE per week; loaded rate, USD (Chapter 2)

day21 = pennant(denied=False)
print(f"DAY 21  estimate as sent to Laura Finch: {day21.total():,.0f} integration h / {day21.model_hours[1]} model h"
      f" = tax {day21.point_tax():.2f}  (Chapter 2 field estimate 2.0)")
print("  TMS line: P-A2 pull shipment status from the TMS REST API (v2), 40 h, rests on: vendor documentation")
print()
print("DAY 23  Kofi Mensah, integration architect: 'There is no status API. The module is not licensed here.")
print("        Status leaves the TMS once a night, as a CSV, at 02:00 Central.'")
naive = Inventory(day21.customer, day21.model_hours, 23)
naive.lines = [l for l in day21.lines]
for l in naive.lines:
    if l.lid == "P-A2": l_alt = l.alt; l.alt = []        # as first written: no alternative was priced
try:
    naive.deny("P-A2", "Kofi Mensah", 23)
except ValueError as err:
    print(f"  ValueError: {err}")
for l in naive.lines:
    if l.lid == "P-A2": l.alt = l_alt
day24 = pennant()
added = day24.total() - day21.total()
weeks = added / (FDES * HOURS_PER_WEEK)
print()
print(f"DAY 24  re-estimated with the CSV path priced: {day24.total():,.0f} h, tax {day24.point_tax():.2f}"
      f"  (+{added:,.0f} h, +{day24.point_tax() - day21.point_tax():.2f})")
for l in day24.lines:
    if l.lid.startswith("P-T"):
        print(f"    {l.lid:<6}{l.source:<13}{l.likely:>5.0f} h  {l.what}")
print(f"  cost of the surprise: {added:,.0f} h x ${RATE} = ${added * RATE:,.0f}; {weeks:.1f} weeks at {FDES} FDEs")
print()
print("GUARD  the same day-21 inventory through lint, alternative unpriced:")
for l in naive.lines:
    if l.lid == "P-A2": l.alt = []
for x in naive.lint():
    print(f"  REFUSED  {x}")
print(f"  P-A2 is {40 / naive.total():.1%} of the estimate; its denial was worth {added:,.0f} h. Estimate not sent.")
