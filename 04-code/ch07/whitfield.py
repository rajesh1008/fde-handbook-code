"""Listing 7.7: Tom Whitfield's permissions as a design constraint. The agent acts for an adjuster, so it may
not do anything the adjuster may not. Each gap becomes an identity question with a named owner."""
from questionbank import acting_for_gaps

NEEDS = ("read intake queues", "policy lookup by number", "policy search by name and address",
         "read claim by claim number", "search claims across units", "attach to existing claim")
GRANTS = {"Tom Whitfield (senior adjuster)": ("read intake queues", "policy lookup by number",
          "read claim by claim number", "attach to existing claim")}
OWNER = {"policy search by name and address": "underwriting service desk, under a purpose rule (Q34)",
         "search claims across units": "information security lead and privacy office (Q35)"}
NEED_A_MONTH = {"policy search by name and address": 1099, "search claims across units": 459}
for who, g in GRANTS.items():
    gaps = acting_for_gaps(NEEDS, g)
    print(f"agent acting for {who}: {len(NEEDS)} actions needed, {len(gaps)} not permitted")
    for n in gaps:
        print(f"  GAP {n}: owner {OWNER[n]}; about {NEED_A_MONTH[n]:,} documents a month")
print("\ndesign after day 24:")
print("  name search -> agent drafts a request to the service desk queue; it does not search")
print("  cross-unit duplicate check -> purpose-bound service identity returns claim number and unit only,")
print("                                every read stamped with the adjuster it serves")
