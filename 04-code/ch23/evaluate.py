"""Section 23.4: measuring retrieval with the customer's questions (Anne Kessler's 150) against the vendor's synthetic set."""
import _paths  # noqa: F401
import caldwell_docs as C
from fieldkit.retrieval import evaluate

ix, recs, acl, versions = C.build(day=88)
C.apply_register(ix, C.lifecycle_register(versions))
anne = C.questions(recs); synth = C.questions(recs, synthetic=True)
ans = [q for q in anne if q.gold]
print(f"Anne's set: {len(anne)} questions, {len(ans)} answerable, {len(anne) - len(ans)} not in the documents; "
      "three adjuster teams, gold marked by two adjusters, ties settled by Anne")
print()
print(f"{'retriever':38s} {'synthetic set':>13s} {'Anne @10':>9s} {'Anne @5':>8s} {'MRR':>5s}")
rows = [("lexical (BM25)", dict(mode="lexical")), ("vector (gateway embedding stand-in)", dict(mode="vector")),
        ("hybrid, plain fusion", dict(mode="hybrid", identifiers=False)), ("hybrid + identifier routing", dict(mode="hybrid"))]
for label, kw in rows:
    s = evaluate(ix, synth, C.who_for, k=10, **kw); a = evaluate(ix, anne, C.who_for, k=10, **kw)
    a5 = evaluate(ix, anne, C.who_for, k=5, **kw)
    print(f"{label:38s} {s['recall']:13.2f} {a['recall']:9.2f} {a5['recall']:8.2f} {a['mrr']:5.2f}")
    last = a
print()
print("by category, hybrid + identifier routing, recall at ten:")
for c, (n, r) in last["by_category"].items():
    print(f"  {c:22s} n={n:3d}  {r:.2f}")
missed = sorted(q for q, r in last["per"].items() if r < 1)
print(f"questions with a gold passage missing from the top ten: {len(missed)}")
bm = lambda q: max(ix._bm25(q.text, ix.passages).values(), default=0.0)
na = [bm(q) for q in anne if not q.gold]; sc = sorted(bm(q) for q in ans)
line = sc[len(sc) // 20]
print(f"not in the documents: {len(na)} questions all returned ten passages; top lexical score below the "
      f"answerable 5th percentile ({line:.1f}) for {sum(x < line for x in na)} of {len(na)}")
print("\nexample, A001:", anne[0].text)
