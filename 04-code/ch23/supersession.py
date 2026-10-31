"""Section 23.3: freshness and supersession. Failure injection 2: a superseded policy wording retrieved for a live claim."""
import _paths  # noqa: F401
import caldwell_docs as C
from fieldkit.retrieval import context_header

TODAY = 20260515   # stand-in calendar date for engagement day 104
ix, recs, acl, versions = C.build(day=88)
tom = C.PEOPLE["tom"]
live = "water loss supply line cause code blank desk adjuster before field inspection"
print("live claim CLM-2026-118342 (shadow, day 104): supply line, cause code blank, review screen asks the manual")
print(f"query: {live!r}")
print("\n-- before: library ingested as exported, every file treated as current")
for i, (p, s) in enumerate(ix.search(live, tom, k=3, lifecycle=False), 1):
    print(f"  {i}. {p.doc_id:12s} effective {p.effective_from}  {p.text[:92]}...")
print("  drafted note: 'cause code may stay blank until field inspection' -> contradicts V-118; Tom Whitfield flagged it")

multi = sorted(d for d, n in versions.items() if n > 1) + ["CM-WL-07"]
qs = [q for q in C.questions(recs) if q.category == "version-sensitive"]
def stale_above(**kw):
    n = draft = 0
    for q in qs + [C.Question("LIVE", live, "version-sensitive", ("CM-WL-07-v3-p00",))]:
        hits = ix.search(q.text, tom, k=10, **kw)
        gold_rank = next((i for i, (p, _) in enumerate(hits) if p.pid in q.gold), 99)
        base = q.gold[0].rsplit("-v", 1)[0]
        gdoc = q.gold[0].rsplit("-p", 1)[0]
        older = [i for i, (p, _) in enumerate(hits) if p.doc_id.startswith(base + "-v") and p.doc_id != gdoc
                 and p.state != "draft" and not p.pid.startswith("CM-WL-07-v4") and i < gold_rank]
        drafts = [i for i, (p, _) in enumerate(hits) if p.pid.startswith("CM-WL-07-v4") and i < gold_rank]
        n += bool(older); draft += bool(drafts)
    return n, draft, len(qs) + 1
print(f"\n{len(multi)} documents have more than one version in the folder; {len(qs)} of Anne's questions are version-sensitive (+1 live)")
print(f"{'treatment':44s} {'older version above current':>27s} {'draft above current':>19s}")
rows = [("as exported (no lifecycle)", dict(lifecycle=False)),
        ("newest effective date boosted (recency 1.0)", dict(lifecycle=False, recency=1.0))]
for label, kw in rows:
    a, d, n = stale_above(**kw); print(f"{label:44s} {a:>21d} of {n} {d:>13d} of {n}")
reg = C.lifecycle_register(versions)
C.apply_register(ix, reg)
a, d, n = stale_above()
print(f"{'lifecycle register, filtered before ranking':44s} {a:>21d} of {n} {d:>13d} of {n}")
print(f"\nregister signed by Joan Mercer day 106: {sum(1 for x in reg if x[1] == 'superseded')} files superseded, "
      f"{sum(1 for x in reg if x[1] == 'draft')} draft")
print("\n-- after: same query, same day")
for i, (p, s) in enumerate(ix.search(live, tom, k=3), 1):
    print(f"  {i}. {context_header(p, TODAY)[:100]}")
print("\n-- a reopened 2023 claim asks what applied on its handling date (as_of 2023-08-15)")
p, _ = ix.search(live, tom, k=1, as_of=20230815)[0]
print(f"  {context_header(p, TODAY)}")
