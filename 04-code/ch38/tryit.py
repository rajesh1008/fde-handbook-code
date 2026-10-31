"""Try It Yourself. a: shift the pass-3 day and watch evidence expire. b: change one answer after approval and
see which check catches it. c: try to accept a high residual risk."""
import sys
import _paths  # noqa: F401
from fieldkit.security import evidence_check, Answer
import world as W
from residual import REGISTER, Residual

part = sys.argv[1] if len(sys.argv) > 1 else "a"
A3 = W.answers(3)
if part == "a":
    for day in (129, 143, 144, 158, 188, 190, 218, 250):
        v = evidence_check(A3, W.EVIDENCE, day, W.SCOPE)
        bad = [x.qid for x in v if not x.passed]
        print(f"pass held on day {day}: {41 - len(bad):>2} of 41 pass" + (f"; failing {', '.join(bad)}" if bad else ""))
elif part == "b":
    A2 = W.answers(2)
    fp = {a.qid: W.fingerprint(a, W.EVIDENCE) for a in A2}
    cases = [("words", "SQ-07", dict(text="Per Greystone's schedule; drafts kept 30 days after closure.")),
             ("claim", "SQ-21", dict(claim="measured")),
             ("evidence", "SQ-23", dict(evidence=("EV-16",))),
             ("whitespace", "SQ-29", dict(text=next(a.text for a in A2 if a.qid == "SQ-29") + " "))]
    for kind, q, kw in cases:
        a = next(x for x in A3 if x.qid == q)
        b = Answer(q, a.theme, a.question, kw.get("text", a.text), kw.get("evidence", a.evidence), kw.get("claim", a.claim),
                   a.design_changing)
        ok = evidence_check([b], W.EVIDENCE, 129, W.SCOPE)[0].passed
        print(f"{kind:<10} {q}: evidence check {'passes' if ok else 'fails'}; fingerprint "
              f"{'unchanged' if W.fingerprint(b, W.EVIDENCE) == fp[q] else 'CHANGED -> reread'}")
elif part == "c":
    r = REGISTER[0]
    for res in [(2, 3), (3, 3), (3, 4), (4, 4)]:
        t = Residual(r.id, r.finding, r.risk, r.inherent, res, r.controls, r.accepted_by, r.vendor_owner, r.review_day,
                     r.triggers, r.signed_day)
        print(f"RR-01 with residual {res[0]}x{res[1]}={res[0] * res[1]:>2}: {'; '.join(t.lint()) or 'acceptable'}")
