"""Listings 47.9 and 47.10: time to production by adoption order, hours by layer, and month-18 capacity."""
import sys, _paths  # noqa: F401
from world import TTP, HOURS, N17_LOST, ENGAGEMENTS, PHASE_HOURS, FIELD_HOURS_PER_FDE, FDES, name
if sys.argv[1] == "ttp":
    for pb, rows in TTP.items():
        print(pb + ": " + ", ".join(f"{name(e)} {d}" for e, d in rows))
    print(f"N17 includes {N17_LOST} days lost to the undeclared gateway step; without them {TTP['PB-1 claims intake'][-1][1] - N17_LOST}")
    print("\nFDE hours per engagement by layer (signature to Live Stable):")
    for c, h in HOURS.items():
        t = sum(h.values())
        print(f"  {c:30} bespoke {h['bespoke']:>5,}  playbook {h['playbook']:>4}  platform {h['platform']:>4}  total {t:>5,}")
else:
    pl = nb = bs = 0
    for e, v in ENGAGEMENTS.items():
        p, q, r = PHASE_HOURS[v[5]]
        bespoke_only = v[1] in ("kyc-review", "permit-review", "correspondence")
        pl += q if bespoke_only else p
        nb += q if bespoke_only else 0
        bs += r
    cap = FIELD_HOURS_PER_FDE * len(FDES)
    print(f"month 18: 20 engagements, {len(FDES)} FDEs, field capacity {cap} h a month ({FIELD_HOURS_PER_FDE} h each)")
    print(f"  demand, playbook-led where a playbook exists: {pl} h ({pl / cap:.2f} of capacity)")
    print(f"    of which the five engagements with no playbook: {nb} h ({nb / pl:.0%})")
    print(f"  demand if every engagement were bespoke with no platform: {bs} h ({bs / cap:.2f} of capacity, "
          f"{bs / FIELD_HOURS_PER_FDE:.1f} FDEs)")
