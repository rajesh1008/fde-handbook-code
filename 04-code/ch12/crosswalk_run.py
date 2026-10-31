"""Platform-standards crosswalk: draft v0.6 (week 3) and v1.0 (week 6)."""
import _path  # noqa: F401
from fieldkit.bid import crosswalk
from harbourline import standards

for draft in ("v0.6", "v1.0"):
    counts, problems = crosswalk(standards(draft))
    print(f"crosswalk {draft}: {sum(counts.values())} standards")
    for o, n in counts.items():
        print(f"  {o:<27} {n:>3}")
    print(f"  problems: {len(problems)}")
    for k, code, msg in problems:
        print(f"    {k} {code}: {msg}")
dev = [s for s in standards() if s.outcome == "deviation requested"]
print("deviations requested in v1.0, each with a named approver at Harbourline:")
for s in dev:
    print(f"  {s.key} ({s.approver}): {s.text} Proposal: {s.evidence}.")
