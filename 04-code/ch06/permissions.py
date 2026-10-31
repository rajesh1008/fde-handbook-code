"""Listing 6.9: the operator's permissions as a design constraint (deterministic stand-in).

The intake automation would run under a service account with an intake clerk's permissions, because that is
the role Caldwell's access team can grant without a new review. Each step it would take is checked against
that role; a gap names who holds the permission today and how many documents a month need the step.
"""
from collections import Counter
from caldwell_discovery import watched_documents, PATHS, SPEC
from discovery import Step, permission_gaps

ROLES = {
    "intake clerk": ("read intake queues", "policy lookup by number", "create claim record"),
    "senior adjuster": ("read intake queues", "policy lookup by number", "create claim record",
                        "attach to existing claim"),
    "underwriting service desk": ("policy lookup by number", "policy search by name and address"),
    "legal mail coordinator": ("read legal mail",),
    "finance cage": ("read finance mail",),
}
STEPS = [
    Step("read the document", "P01-P08", ("read intake queues",), "intake clerk"),
    Step("find the policy from its number", "all", ("policy lookup by number",), "intake clerk"),
    Step("find the policy when the number is missing", "all", ("policy search by name and address",),
         "underwriting service desk"),
    Step("attach papers to an existing claim", "all", ("attach to existing claim",), "senior adjuster"),
    Step("read attorney letters", "P10", ("read legal mail",), "legal mail coordinator"),
    Step("read mail held by finance", "P09", ("read finance mail",), "finance cage"),
    Step("create the claim record", "all", ("create claim record",), "intake clerk"),
]
docs = watched_documents()
mix = Counter(d.exception for d in docs)
n = len(docs)
total = sum(p.volume for p in PATHS)
need = {"find the policy when the number is missing": mix["policy number missing or unreadable"] / n * total,
        "attach papers to an existing claim": mix["existing claim, not new"] / n * total,
        "read attorney letters": SPEC["P10"].volume, "read mail held by finance": SPEC["P09"].volume}
gaps = permission_gaps(STEPS, ROLES, "intake clerk")
print(f"automation runs as: intake clerk; steps checked: {len(STEPS)}; gaps: {len(gaps)}")
for s, missing, holders in gaps:
    print(f"  GAP {s.name}: needs {', '.join(missing)}; held by {', '.join(holders)}; "
          f"about {need[s.name]:,.0f} documents a month")
print(f"documents a month that need a step the service account cannot take: about {sum(need.values()):,.0f} "
      f"of {total:,} ({100 * sum(need.values()) / total:.0f}%)")
