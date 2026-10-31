"""Chapter 35: which regime applies to which customer, the lint over each map, and retention by customer."""
import _paths  # noqa: F401
from fieldkit.privacy import generate, lint
from world import CALDWELL, greystone_config, pennant

MAPS = {
    "Greystone": ({"HIPAA"}, generate(greystone_config(125)), "Greystone",
                  "HIPAA covered entity; Northlight business associate; provider subcontractor BA [VERIFY]"),
    "Caldwell": ({"STATE"}, CALDWELL, "Caldwell",
                 "state insurance privacy and data security law, GLBA; CPPA ADMT for California policyholders [VERIFY]"),
    "Pennant": ({"GDPR"}, pennant(fixed=False), "Pennant",
                "GDPR for EU consignees; Northlight processor under Art. 28 [VERIFY]"),
}
print("Regimes and lint by customer, as of 31 Oct 2026")
for name, (reg, hops, owner, why) in MAPS.items():
    found = lint(hops, reg, owner=owner)
    personal = sum(h.personal for h in hops)
    print(f"\n{name}: {why}")
    print(f"  hops {len(hops)}   holding personal data {personal}   findings {len(found)}")
    for f in found:
        print(f)

print("\nRetention for prompts, traces and records (days; 0 = not stored)")
print("  customer    model provider  gateway/traces  cache  run records  eval set")
rows = {"Greystone": generate(greystone_config(125)), "Caldwell": CALDWELL, "Pennant": pennant(fixed=True)}
for name, hops in rows.items():
    d = {h.name: h.retention_days for h in hops}
    tr = d.get("gateway-diagnostics", d.get("gateway-logs"))
    print(f"  {name:<11} {d.get('model-endpoint', '-')!s:>14}  {tr!s:>14}  {d.get('match-cache', '-')!s:>5}  "
          f"{d.get('run-records')!s:>11}  {d.get('eval-set', '-')!s:>8}")
