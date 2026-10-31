"""Listings 47.4 to 47.6: the playbook registry, the form-only linter, the failure at N17 and the probe."""
import sys, _paths  # noqa: F401
from fieldkit.playbooks import Registry, lint_playbook, check_preconditions
from world import PB1, PB2, PB3, PB4, ESTATE
mode = sys.argv[1]
if mode == "form":
    books = [PB1("1.3", False), PB2("1.1", False), PB3("0.9", False), PB4()]
    print("v5.4 form-only lint (P1 to P4), registry as of month 15")
    for b in books:
        f = lint_playbook(b, probe=False)
        print(f"  {b.key:11} {b.title:36} steps {len(b.steps)}  findings {len(f)}  maturity {b.maturity}")
    print("  all four admitted to the registry")
elif mode == "n17":
    pb, est = PB1("1.3", False), ESTATE["N17"]
    print("N17 estate:", ", ".join(f"{k}={v}" for k, v in est.items()))
    print(f"adopted {pb.key} on day 0 (form lint: 0 findings)")
    days = {"PB-1.S1": (1, 9), "PB-1.S2": (10, 18), "PB-1.S3": (19, 22), "PB-1.S4": (23, 23)}
    for s in pb.steps[:4]:
        a, b = days[s.sid]
        if s.sid == "PB-1.S4" and est["gateway"] == "none":
            print(f"  day {a:>2}       {s.sid} FAILED: route registration endpoint not found; estate has no model gateway")
            break
        print(f"  day {a:>2} to {b:<2} {s.sid} done: {s.text}")
    print("  days 23 to 31 lost: a change request for a customer gateway that does not exist; PB-4 direct mode set up instead")
    print("preconditions declared by PB-1@1.3 that N17 fails:", check_preconditions(pb, est) or "none (that is the bug)")
elif mode == "probe":
    print("v5.4 lint with the assumption probe (P5) over the month-15 registry")
    for b in [PB1("1.3", False), PB2("1.1", False), PB3("0.9", False), PB4()]:
        for rule, where, msg in lint_playbook(b):
            print(f"  {rule} {where:8} {msg}")
    print("fixed versions: PB-1@1.4, PB-2@1.2, PB-3@0.9.1 declare gateway, object_store and fhir")
elif mode == "match":
    r = Registry()
    for b in [PB1("1.4", True), PB2("1.2", True), PB3("0.9.1", True), PB4()]:
        r.add(b)
    for est_id, wf in [("N17", "claims-intake"), ("N15", "claims-intake"), ("N13", "correspondence"),
                       ("N20", "referral-intake")]:
        print(f"{est_id} ({wf}, gateway={ESTATE[est_id]['gateway']}):")
        for key, status, unmet in r.match(ESTATE[est_id], wf):
            why = "; ".join(f"{s} needs {f} in {{{', '.join(a)}}}, has {h}" for s, f, a, h in unmet)
            print(f"  {key:11} {status:7} {why}")
    est = dict(ESTATE["N17"], gateway="fieldkit-direct")
    print("N17 after PB-4 writes the route record (gateway=fieldkit-direct):")
    for key, status, unmet in r.match(est, "claims-intake"):
        print(f"  {key:11} {status}")
