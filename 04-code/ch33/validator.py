"""Listing 33.8: the validator's 14 questions, answered by evidence, by translation or by a stated boundary."""
from world import M, REQUEST

one = {t: 0 for t in (M.EVIDENCE_ANSWER, M.TRANSLATION, M.BOUNDARY)}
comp = dict(one)
for qid, asked, t1, q in REQUEST:
    one[t1] += 1; comp[q.answer_type] += 1
print("one-model framing (day 74):  " + "  ".join(f"{k} {v}" for k, v in one.items()))
print("component framing (day 146): " + "  ".join(f"{k} {v}" for k, v in comp.items()))
print()
for qid, asked, t1, q in REQUEST:
    move = "" if t1 == q.answer_type else f"   ({t1} -> {q.answer_type})"
    print(f"{qid} {asked:<56} {q.answer_type:<11}{move}")
    print(f"     {q.answer}" + (f"; compensating: {q.compensating}" if q.compensating else ""))
probs = [p for *_, q in REQUEST for p in q.problems()]
print()
print(f"lint: {len(probs)} problems")
