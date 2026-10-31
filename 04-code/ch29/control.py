"""Listing 29.7: the weekly control run. Twelve seeded mutants; each must be caught at the layer designed to catch
it. Day 145 (first run) and day 152 (after the two fixes)."""
import json
import common as C
from fieldkit.pyramid import Mutant, control_run

M = [Mutant("M01", "router floor lowered to 0.30", 1, lambda s: dict(s, router_floor=0.30)),
     Mutant("M02", "fail-closed gates disabled", 1, lambda s: dict(s, failclosed=False)),
     Mutant("M03", "permission filter bypassed", 1, lambda s: dict(s, acl_filter=False)),
     Mutant("M04", "dates read day first", 1, lambda s: dict(s, datelib=4.0)),
     Mutant("M05", "V-118 cause codes off by one", 1, lambda s: dict(s, v118_map_ok=False)),
     Mutant("M06", "mail date received dropped", 2, lambda s: dict(s, drop_mail_date=True)),
     Mutant("M07", "superseded wording retrieved", 2, lambda s: dict(s, lifecycle_filter=False)),
     Mutant("M08", "retry outside the intent key", 3, lambda s: dict(s, retry_inside_intent=False)),
     Mutant("M09", "key rotation not handled", 3, lambda s: dict(s, rotation_handled=False)),
     Mutant("M10", "step budget raised to 120", 4, lambda s: dict(s, breaker_steps=120)),
     Mutant("M11", "judge passes more failures", 5, lambda s: dict(s, judge_fp_rate=0.35)),
     Mutant("M12", "drift window 30 days", 5, lambda s: dict(s, drift_window_days=30))]
p = C.build()
out = {}
for day, base in ((145, dict(C.BASE, faith_subset="first40", judge_rule="20 docs, >3 false passes")), (152, C.BASE)):
    rows = control_run(p, base, M)
    out[day] = rows
    ok = sum(r["status"] == "caught" for r in rows)
    print(f"day {day}: {ok} of {len(rows)} caught at their designed layer")
    for r in rows:
        at = f"L{r['caught_at']}" if r["caught_at"] else "--"
        print(f"  {r['id']} {r['what']:32} designed L{r['designed']}  caught {at:3} {r['status']:8} {', '.join(r['by'])}")
json.dump({str(k): [[r["id"], r["designed"], r["caught_at"], r["status"]] for r in v] for k, v in out.items()},
          open("output/control.json", "w"), indent=1)
