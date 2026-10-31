"""Try It Yourself, Chapter 23: python tryit.py a|b|c"""
import sys
import _paths  # noqa: F401
import caldwell_docs as C
from fieldkit.retrieval import evaluate

v = sys.argv[1] if len(sys.argv) > 1 else "a"
ix, recs, acl, versions = C.build(day=88)
if v == "a":   # how much do the adjusters' own words cost? vary the share of adjuster phrasing
    C.apply_register(ix, C.lifecycle_register(versions))
    for s in (0.0, 0.2, 0.37, 0.6):
        e = evaluate(ix, C.questions(recs, slang=s), C.who_for, k=10)
        print(f"adjuster phrasing share {s:.2f}: recall at ten {e['recall']:.2f}")
elif v == "b":  # over-fetch then filter: does fetching 30 and trimming fix the post-filter short lists?
    C.apply_register(ix, C.lifecycle_register(versions)); tom = C.PEOPLE["tom"]
    qs = [q.text for q in C.questions(recs)]
    for k in (10, 30, 60):
        short = sum(len(ix.search(q, tom, k=k, acl="post")[:10]) < 10 for q in qs)
        print(f"post-filter fetching {k:2d}, keeping 10: {short} of {len(qs)} searches return fewer than ten")
    print(f"pre-filter: {sum(len(ix.search(q, tom, k=10)) < 10 for q in qs)} of {len(qs)} short")
elif v == "c":  # mark only the water-loss section and leave the other superseded files unmarked
    C.apply_register(ix, [x for x in C.lifecycle_register(versions) if x[0].startswith("CM-WL-07")])
    qs = [q for q in C.questions(recs) if q.category == "version-sensitive"]; tom = C.PEOPLE["tom"]
    bad = 0
    for q in qs:
        hits = [p for p, _ in ix.search(q.text, tom, k=10)]
        base = q.gold[0].rsplit("-v", 1)[0]
        gold_i = next((i for i, p in enumerate(hits) if p.pid in q.gold), 99)
        gdoc = q.gold[0].rsplit("-p", 1)[0]
        bad += any(p.doc_id.startswith(base + "-v") and p.doc_id != gdoc and i < gold_i for i, p in enumerate(hits))
    print(f"only CM-WL-07 marked: older version above current for {bad} of {len(qs)} version-sensitive questions")
