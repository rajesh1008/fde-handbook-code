"""Try It Yourself, Chapter 17. Usage: tryit.py a|b|c"""
import sys
import _paths  # noqa: F401
from fieldkit.environment import AuditLog, Delegation, EgressPolicy, EgressRule, RightsGate
import account

which = sys.argv[1] if len(sys.argv) > 1 else "a"
if which == "a":
    tf = account.load()
    log = AuditLog("Caldwell security operations")
    pol = account.egress_policy(tf, log)
    pol.rules.append(EgressRule("tracing", "ingest.trace-vendor.example"))
    print("lint after adding the vendor tracing endpoint:")
    for f in pol.lint():
        print(f"  {f}")
    for k in range(48):
        pol.check("ingest.trace-vendor.example", t=f"flush {k + 1}")
    print(f"allowed flushes to a vendor service: {len(log.query(action='ALLOW'))} (each one a copy Caldwell cannot delete)")
elif which == "b":
    flagged = {"CLM-7": 18 * 60 + 20}          # flagged litigated at 18:20
    can_read = lambda u, c, t: not (c in flagged and flagged[c] <= t)
    queued = [f"CLM-{i}" for i in range(1, 41)]
    for hours in (0.25, 8):
        log = AuditLog("Caldwell security operations")
        d = Delegation("twhitfield", "nl-assist", "end-of-shift summaries", ("claims:read",), 17 * 60 + 50,
                       int(17 * 60 + 50 + hours * 60))
        rel, held = RightsGate(can_read, log).release(d, queued, 19 * 60)
        reasons = sorted({r for _, r in held})
        print(f"delegation {hours:>4} h: released {len(rel)}, withheld {len(held)} {reasons}")
else:
    from env_doc import v2
    from dataclasses import replace
    doc = replace(v2, answers=[replace(a, text=a.text.split("; readers")[0]) if a.question == "logs" else a
                               for a in v2.answers])
    print(f"v2 with readers and retention removed: {len(doc.lint())} findings")
    for f in doc.lint():
        print(f"  {f}")
