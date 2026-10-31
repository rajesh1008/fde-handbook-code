"""Listing 7.4: what three data answers change, measured on synthetic records (deterministic stand-in)."""
from caldwell_records import duplicates, loss_date_corrections
from discovery_snapshot import TOTAL_DOCS

d = duplicates(); same = sum(x == 0 for x in d)
print("FRESHNESS  duplicate check against the nightly mart (Q14)")
print(f"  {len(d)} second-door duplicates: caught by mart {len(d)-same}, missed {same} ({100*same/len(d):.0f}%); "
      f"claims-core read catches all {len(d)}")
dup_month = round(TOTAL_DOCS * 0.031)
print(f"  at about {dup_month} duplicates a month (3.1% of {TOTAL_DOCS:,} documents), the mart misses about {round(dup_month*same/len(d))}")
c = loss_date_corrections()
print("\nLATE-ARRIVING FACTS  gold loss dates taken at age N days (Q15)")
for age in (0, 3, 7, 14, 30):
    wrong = sum(1 for x in c if x is not None and x > age)
    print(f"  age {age:2d} days: {wrong:3d} of {len(c)} gold values later corrected ({100*wrong/len(c):.1f}%)")
print("\nGRAIN  rows per claim in the mart (R03): 1.4 on average; counting rows overstates claims by 40%")
