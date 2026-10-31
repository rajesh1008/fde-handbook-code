"""The complete evidence set for the forty-one questions, as Sam Oakley read it at the third pass (day 129)."""
from collections import Counter
import _paths  # noqa: F401
from fieldkit.security import link_check, evidence_check, reuse, expiring
import world as W

day = W.PASS_DAYS[3]
A3 = W.answers(3)
m = evidence_check(W.morning(), W.EVIDENCE, day, W.SCOPE)
print(f"day {day} 08:00: evidence check {sum(v.passed for v in m)} of 41; failing: "
      + "; ".join(f"{v.qid} ({', '.join(v.reasons)})" for v in m if not v.passed))
print("day 129 09:10: egress test rerun by Callum Reid, EV-31 issued; SQ-02 and SQ-24 now cite EV-31")
links = link_check(A3)
ev = evidence_check(A3, W.EVIDENCE, day, W.SCOPE)
print(f"day {day}: {len(A3)} answers; link check {sum(v.passed for v in links)} of {len(A3)}; "
      f"evidence check {sum(v.passed for v in ev)} of {len(A3)}")
for p in (1, 2, 3):
    c = Counter(a.claim for a in W.answers(p))
    print(f"claims at pass {p}: " + ", ".join(f"{k} {c.get(k, 0)}" for k in ("measured", "configured", "documented", "assumed")))
cited = sorted({e for a in A3 for e in a.evidence})
print(f"evidence items cited: {len(cited)} of {len(W.EVIDENCE)} in the register; "
      f"uncited: {', '.join(sorted(set(W.EVIDENCE) - set(cited)))}")
r = reuse(A3)
print("most reused: " + ", ".join(f"{e} {n}" for e, n in r.most_common(6)))
owners = Counter(W.EVIDENCE[e].owner for e in cited)
print("evidence owners: " + ", ".join(f"{o} {n}" for o, n in owners.most_common()))
print(f"expiring within 120 days of day {day}:")
for exp, eid, title, qs in expiring(W.EVIDENCE, A3, day, 120):
    print(f"  day {exp:>3} {eid} {title[:52]:<52} -> {', '.join(qs)}")
print("by theme (questions, design-changing, measured at pass 3):")
for t in dict.fromkeys(a.theme for a in A3):
    g = [a for a in A3 if a.theme == t]
    print(f"  {t:<26} {len(g):>2} {sum(a.design_changing for a in g):>2} {sum(a.claim == 'measured' for a in g):>2}")
