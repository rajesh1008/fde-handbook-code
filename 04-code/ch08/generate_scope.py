"""Generate Caldwell's signed scoping document (v1.0, day 28) with claim-status strips. Deterministic stand-in."""
from caldwell_scope import signed
from scoping import STATUS

doc = signed()
inside, total = doc.coverage()
print(f"SCOPING DOCUMENT  {doc.customer}  {doc.version}  day {doc.day}")
print(f"signed: " + "; ".join(f"{n} ({r})" for n, r in doc.signatories))
print("\n1 SCOPE  document types x decisions" + f"   strip {doc.strip('scope')}")
for t in doc.doc_types:
    print(f"  {t.key}  {t.name:<30}{t.volume:>6,}/mo  decides {' '.join(t.decisions)}")
print(f"  in scope {inside:,} of {total:,} documents a month ({inside / total:.1%})")
print("  never decides: " + ", ".join(doc.never))
print("\n2 SUCCESS CRITERIA" + f"   strip {doc.strip('criteria')}")
for c in doc.criteria:
    print(f"  {c.key}  {c.threshold:<11}{c.scorer:<17}{c.statement}")
print("\n3 VOLUMES, LATENCY, COST" + f"   strip {doc.strip('volumes')}")
for c in [c for c in doc.claims if c.section == "volumes" and c.status != "D"]:
    print(f"  [{c.status}] {c.text}" + (f"  ({c.basis})" if c.basis else ""))
print("\n4 OUT OF SCOPE" + f"   strip {doc.strip('out of scope')}")
for e in doc.exclusions:
    print(f"  {e.item:<34}{e.volume:>5,}/mo  -> {e.route}" + (f"  [{e.revisit}]" if e.revisit else ""))
print("\n5 OPEN DECISIONS" + f"   strip {doc.strip('register')}")
for d in doc.register:
    print(f"  {d.key}  {d.owner:<16} due day {d.due_day}\n        {d.question}")
n = doc.counts()
print("\nclaims: " + "  ".join(f"{k} {n[k]}" for k in "FRVPD") + f"  total {sum(n.values())}")
print("lint findings: " + str(len(doc.lint())))
print("evaluation suite criteria exported: " + str(len(doc.suite_config())))
