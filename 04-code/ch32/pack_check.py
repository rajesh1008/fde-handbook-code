"""Failure injection first: the pack that 'had evidence for every answer' on day 100."""
from collections import Counter
import _paths  # noqa: F401
from fieldkit.security import link_check, evidence_check
from world import ANSWERS, EVIDENCE, SCOPE, PACK_DAY

print(f"Questionnaire pack v1, Greystone, day {PACK_DAY}: {len(ANSWERS)} answers, {len(EVIDENCE)} evidence items")
naive = link_check(ANSWERS)
print(f"link check (does every answer cite evidence?): {sum(v.passed for v in naive)} of {len(naive)} -> pack sent")
print()
print("day 101, Sam Oakley's analyst checks dates only:")
for a in ANSWERS:
    for e in a.evidence:
        ev = EVIDENCE[e]
        if ev.expires_day <= 101:
            print(f"  {a.qid}  {e} issued day {ev.issued_day}, valid {ev.valid_days} days, expired day {ev.expires_day}")
print()
v = evidence_check(ANSWERS, EVIDENCE, PACK_DAY, SCOPE)
print(f"evidence check on day {PACK_DAY} (register, date, scope, owner, claim): {sum(x.passed for x in v)} of {len(v)} pass")
for x in v:
    if not x.passed:
        print(f"  {x.qid}  " + "; ".join(x.reasons))
kinds = Counter()
for x in v:
    for r in x.reasons:
        kinds["expired" if "expired" in r else "describes another deployment" if "describes" in r
              else "owner not a person" if "owner" in r else "claim assumed" if "assumed" in r else r] += 1
print("by reason: " + ", ".join(f"{k} {n}" for k, n in kinds.most_common()))
