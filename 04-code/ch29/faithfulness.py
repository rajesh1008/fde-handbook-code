"""Listing 29.4: retrieval faithfulness on Anne's 150 questions, and the checker validated against Joan Mercer's
claim-by-claim labels on 60 answers (deterministic stand-in)."""
import json
import common as C
import world as W

qs = W.questions()
full = C.faithfulness(qs, True)
print(f"Anne's question set: {len(qs)} questions, {full['claims']} claims in answers, "
      f"{full['supported']} supported by the cited current passage -> faithfulness {full['rate']:.1%}")
by = {}
for q, t in qs:
    f = C.faithfulness([(q, t)], True)
    b = by.setdefault(t, [0, 0]); b[0] += f["claims"]; b[1] += f["supported"]
for t, (n, s) in by.items():
    print(f"  {t:22} {s:>3} of {n:>3} claims supported")
# Joan Mercer labeled every claim in 60 answers (every second answered question)
answered = [(q, t) for q, t in qs if t != "not in the documents"][::2][:60]
claims = [c for q, t in answered for c in W.answer_claims(q, t)]
uns = [c for c in claims if not c[1]]
caught = [c for c in uns if W.checker_flags(c[0], False)]
fa = [c for c in claims if c[1] and W.checker_flags(c[0], True)]
print(f"checker vs Joan Mercer on 60 answers ({len(claims)} claims): unsupported {len(uns)}, checker caught "
      f"{len(caught)}, false alarms {len(fa)} of {len(claims) - len(uns)} supported")
off = C.faithfulness(qs, False)
print(f"lifecycle filter off (mutant M07): faithfulness {off['rate']:.1%}, superseded citations {off['superseded']} "
      f"(all {W.QTYPES['version-sensitive']} version-sensitive questions)")
for kind in ("first40", "stratified40"):
    sub = C.faith_subset(kind)
    o = C.faithfulness(sub, False)
    print(f"  per-PR subset {kind:13}: {sum(t == 'version-sensitive' for _, t in sub)} version-sensitive, "
          f"superseded citations seen {o['superseded']}")
json.dump(dict(by=by, joan=dict(claims=len(claims), uns=len(uns), caught=len(caught), fa=len(fa)),
               rate=full["rate"], off=off["rate"]), open("output/faithfulness.json", "w"), indent=1)
