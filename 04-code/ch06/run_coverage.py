"""Listing 6.6: the coverage report on day 26, and how it grew from day 9 (deterministic stand-in)."""
from caldwell_discovery import build_log

log = build_log()
print(log.coverage(26).render())
print()
print("day  known  covered  known vol/mo  covered vol/mo")
for d in (9, 12, 14, 16, 19, 22, 26):
    r = log.coverage(d)
    print(f"{d:>3}  {len(r.rows):>5}  {sum(x.covered for x in r.rows):>7}  {r.total_volume:>12,.0f}  {r.covered_volume:>14,.0f}")
