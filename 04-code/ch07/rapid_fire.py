"""Listing 7.5: the sixty-second rapid-fire round. Twelve questions, each answerable with yes, no, a number or a
name. Any answer that takes longer than a minute is a deep question in disguise and is moved out of the round."""
import caldwell_bank as cb

b = cb.build()
rapid = [q for q in b.for_audience("data owner") if q.rapid]
t = 0.0
for q in rapid:
    a = b.answers[q.qid]; t += a.elapsed_min
    flag = "  -> over a minute: becomes a deep question next time" if a.elapsed_min > 1.0 else ""
    print(f"{q.qid} {a.elapsed_min*60:4.0f}s {a.outcome:12s} {q.text}{flag}")
print(f"\nround: {len(rapid)} questions in {t:.1f} minutes; contradicted {sum(b.answers[q.qid].outcome=='contradicted' for q in rapid)}")
