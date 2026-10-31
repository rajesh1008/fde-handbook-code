"""The architecture review, day 103: evidence check plus the findings raised in the room."""
from collections import Counter
import _paths  # noqa: F401
from fieldkit.security import evidence_check, review, RemediationPlan
from world import ANSWERS, EVIDENCE, SCOPE, REVIEW_DAY, findings, AGENDA, PREREAD_ACCEPTED, CLEARED_IN_ROOM

v = evidence_check(ANSWERS, EVIDENCE, REVIEW_DAY, SCOPE)
fs = findings()
r = review(v, fs)
print(f"Greystone architecture review, day {REVIEW_DAY}: {r['asked']} questions, {r['passed']} passed, "
      f"{r['findings']} findings -> {r['outcome']}")
print(f"agenda ({sum(m for _, m in AGENDA)} minutes): " + ", ".join(f"{a} {m}" for a, m in AGENDA))
print(f"accepted from the pre-read: {PREREAD_ACCEPTED}; discussed in the room: {len(ANSWERS) - PREREAD_ACCEPTED} "
      f"({len(fs)} findings, {len(CLEARED_IN_ROOM)} cleared: {', '.join(CLEARED_IN_ROOM)})")
theme = {a.qid: a.theme for a in ANSWERS}
print("findings by kind:     " + ", ".join(f"{k} {n}" for k, n in Counter(f.kind for f in fs).items()))
print("findings by severity: " + ", ".join(f"{s} {Counter(f.severity for f in fs)[s]}" for s in ("high", "medium", "low")))
ct = Counter(theme[f.source] for f in fs)
print("findings by theme:    " + ", ".join(f"{t} {n}" for t, n in ct.most_common()))
print()
for f in fs:
    print(f"  {f.id} {f.source} {f.severity:<6} {f.kind:<8} {f.owner:<14} due {f.due_day}  {f.summary}")
plan = RemediationPlan(fs)
print(f"plan lint: {len(plan.lint())} problems")
