"""Chapter 35 Try It Yourself. Usage: tryit.py a | b | c"""
import sys

import _paths  # noqa: F401
from fieldkit.privacy import Hop, erasure_trace, generate, lint, pii_scan
from world import greystone_config, known_values, pennant, provider_log, referrals

part = sys.argv[1] if len(sys.argv) > 1 else "a"
if part == "a":
    hops = generate(greystone_config(125))
    hops.append(Hop("support-ticket-attachments", "HelpdeskSaaS", ("PHI",), "vendor US", 365, "", "store"))
    for f in lint(hops, {"HIPAA"}, owner="Greystone"):
        print(f)
    print("a: one screenshot attached to a support ticket is a new hop; the map catches it")
elif part == "b":
    refs = referrals()
    for n in (50, 100, 200):
        p = pii_scan(provider_log(refs[:n]))
        k = pii_scan(provider_log(refs[:n]), known=known_values(refs[:n]))
        print(f"b: first {n:>3} referrals  patterns {p.hit_entries:>3} entries   patterns+known {k.hit_entries:>3} entries")
else:
    hops = pennant(fixed=True)
    hops = [h if h.name != "backups" else Hop("backups", "Northlight", ("EU-PI",), "GCP europe-west4", 35, "DPA PA-03",
                                              "backup", deletable=False) for h in hops]
    for f in lint(hops, {"GDPR"}, owner="Pennant"):
        print(f)
    print("c: longest erasure path", max(d for _, _, d, ok in erasure_trace(hops) if d is not None), "days")
