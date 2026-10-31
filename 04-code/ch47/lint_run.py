"""Listings 47.2 and 47.3: the engagement linter over all twenty manifests at month 15 and month 18."""
import sys, collections, _paths  # noqa: F401
from fieldkit.playbooks import Registry, lint_engagement, RULES
from world import PB1, PB2, PB3, PB4, manifests, name
month = int(sys.argv[1])
r = Registry()
if month == 15:
    for b in [PB1("1.1", False), PB1("1.3", False), PB2("1.1", False), PB3("0.9", False), PB4()]:
        r.add(b, probe=False)
    r.deprecate("PB-1@1.1", reason="gold set of 120 replaced by 300", migrate_by=14)
else:
    for b in [PB1("1.3", False), PB1("1.4", True), PB2("1.2", True), PB3("0.9.1", True), PB4()]:
        r.add(b, probe=b.version != "1.3")
    r.deprecate("PB-1@1.3", reason="undeclared gateway step", migrate_by=17)
F = []
for m in manifests(month):
    F += lint_engagement(m, r, month=month)
    r.adoptions[m["id"]] = m["playbook"]
by_rule = collections.Counter(f[0] for f in F)
engs = sorted({f[1] for f in F})
print(f"engagement lint, month {month}: {len(F)} findings at {len(engs)} of 20 engagements")
for rule in RULES:
    print(f"  {rule} {by_rule.get(rule, 0):>2}  {RULES[rule]}")
print("findings:")
for rule, e, msg in F:
    print(f"  {rule} {name(e):11} {msg}")
if not F:
    print("  none")
devs = [(m["id"], d) for m in manifests(month) for d in m["deviations"]]
print(f"registered deviations: {len(devs)} (" + "; ".join(f"{name(e)} {d['what']} review month {d['review_by']}" for e, d in devs) + ")")
