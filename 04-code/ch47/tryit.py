"""Try It Yourself 47.a to 47.c."""
import sys, _paths  # noqa: F401
from fieldkit.playbooks import recurrence, classify, Registry, FieldReport, rank_reports, evidence_score
from world import INSTANCES, PB1, PB2, PB3, PB4, ESTATE, REPORTS
p = sys.argv[1]
if p == "a":   # lower the platform bar: 5 engagements, shapes ratio 0.35
    for r in recurrence(INSTANCES):
        new = classify(r["n"], r["variants"], platform_min=5, platform_ratio=0.35)
        if new != r["by_shape"]:
            print(f"{r['component']}: {r['by_shape']} to {new} ({r['n']} engagements, {r['variants']} shapes)")
    print("each move is a component the platform team must own, version and support at every customer")
elif p == "b":  # a new bank with no vault and no gateway
    r = Registry()
    for b in [PB1("1.4", True), PB2("1.2", True), PB3("0.9.1", True), PB4()]:
        r.add(b)
    est = dict(cloud="onprem", gateway="none", vault="none", egress_proxy="yes", object_store="none", edi="none",
               fhir="none")
    for key, status, unmet in r.match(est, "claims-intake"):
        print(key, status, [(s, f, h) for s, f, _, h in unmet])
else:           # give FR-003 a working artifact and see where it lands
    reps = [FieldReport(rid, t, o, list(e), [h] * len(e), v, a, art, fm) for rid, t, o, e, h, v, a, art, fm in REPORTS]
    for x in reps:
        if x.rid == "FR-003":
            x.artifact = "theming.py + test"
    for i, x in enumerate(rank_reports(reps), 1):
        if x.rid == "FR-003":
            print(f"FR-003 with an artifact: rank {i} of {len(reps)}, score {evidence_score(x):.0f}")
