"""Failure injection: an answer that changed since the last review.
Sam Oakley approved 37 answers at pass 2 (day 121). Carrying those approvals forward is the naive move.
The change-aware check compares each answer's fingerprint (words, claim, evidence digests) at approval with
the answer as it stands, and reruns each answer's falsifier against what the deployment shows."""
import sys
import _paths  # noqa: F401
from fieldkit.security import evidence_check, Answer
import world as W

A2, A3 = W.answers(2), W.answers(3)
ev2 = {v.qid: v.passed for v in evidence_check(A2, W.EVIDENCE, W.PASS_DAYS[2], W.SCOPE)}
returned2 = {"SQ-09", "SQ-31", "SQ-35", "SQ-30"}
approved = {a.qid: W.fingerprint(a, W.EVIDENCE) for a in A2 if ev2[a.qid] and a.qid not in returned2}

inject = "--inject" in sys.argv
if inject:  # an engineer tidies SQ-28 on day 128 and nobody tells the reviewer
    A3 = [Answer(a.qid, a.theme, a.question, "Per the retention schedule; run records kept 2,190 days.", a.evidence,
                 a.claim, a.design_changing) if a.qid == "SQ-28" else a for a in A3]

FALSIFIERS = {  # question: (what would make the answer false, test against the observation)
    "SQ-02": ("an outbound destination the answer does not name",
              lambda o, a: o["outbound"] <= ({"model service", "observability service"} if "observability" in a.text
                                             else {"model service"})),
    "SQ-14": ("the provider keeps stored requests", lambda o, a: not o["stored_requests"]),
    "SQ-18": ("prompt attributes in exported traces", lambda o, a: not o["prompt_attrs_in_traces"]),
    "SQ-26": ("prompt text in any log or trace", lambda o, a: not o["prompt_attrs_in_traces"]),
    "SQ-03": ("full prompts kept by any trace sampler", lambda o, a: o["trace_full_sample"] == 0),
}
print(f"approved at pass 2 (day 121): {len(approved)} answers")
print(f"naive carry-forward on day 129: {len(approved)} approved + 4 re-reviewed = 41 of 41, nothing to reread"
      + ("  (the SQ-28 edit is invisible here)" if inject else ""))
now = {a.qid: a for a in A3}
text_or_claim, evidence_only = [], []
for q, fp in approved.items():
    a2 = next(x for x in A2 if x.qid == q); a3 = now[q]
    if W.fingerprint(a3, W.EVIDENCE) == fp:
        continue
    (text_or_claim if (a2.text, a2.claim) != (a3.text, a3.claim) else evidence_only).append(q)
print(f"change-aware on day 129: {len(text_or_claim) + len(evidence_only)} approved answers changed since approval")
print(f"   words or claim changed: {', '.join(text_or_claim)}")
print(f"   same words, evidence changed: {', '.join(evidence_only) or 'none'}")
print("falsifiers rerun against the deployment:")
truth = []
for q, (what, test) in FALSIFIERS.items():
    res = {d: test(W.OBSERVED[d], (A2 if d < 129 else A3)[[x.qid for x in A2].index(q)]) for d in (103, 121, 129)}
    flips = [d for d in (103, 121) if not res[d]]
    if flips and q in approved:
        truth.append(q)
    print(f"   {q} false if {what}: day 103 {'holds' if res[103] else 'FAILS'}, day 121 "
          f"{'holds' if res[121] else 'FAILS'}, day 129 {'holds' if res[129] else 'FAILS'}")
truth_only = [q for q in truth if q not in text_or_claim + evidence_only]
print(f"approved at pass 2 although the falsifier failed that day: {', '.join(truth)}")
print(f"   same words, same evidence, truth changed: {', '.join(truth_only)} (no fingerprint catches this)")
reread = sorted(set(text_or_claim + evidence_only + truth_only) | returned2)
print(f"reread list for pass 3: {len(reread)} of 41 -> {', '.join(reread)}")
