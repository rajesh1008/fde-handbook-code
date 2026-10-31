"""Data flows the reviewer can verify: lint the declared inventory, then reconcile it with what was observed."""
import _paths  # noqa: F401
from fieldkit.security import reconcile_flows
from world import FLOWS, OBSERVED

phi = sum(f.data == "phi" for f in FLOWS)
cross = [f for f in FLOWS if f.boundary]
print(f"declared flows: {len(FLOWS)} ({phi} carry patient data); crossing a trust boundary: {len(cross)}")
for f in cross:
    print(f"  {f.id} {f.source} -> {f.dest}: {f.boundary}; control: {f.control}; verify: {f.verify}")
problems = [p for f in FLOWS for p in f.lint()]
print(f"inventory lint: {len(problems)} problems")
r = reconcile_flows(FLOWS, OBSERVED)
print(f"observed in flow logs and diagnostic settings, day 102: {len(set(OBSERVED))} pairs")
print(f"  matched {r['matched']}; undeclared {len(r['undeclared'])}; declared but not seen {len(r['unseen'])}")
for s, d in r["undeclared"]:
    print(f"  undeclared: {s} -> {d}")
for i in r["unseen"]:
    print(f"  not seen: {i} (audit log -> Greystone SIEM; export not yet configured)")
