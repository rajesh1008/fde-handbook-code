"""Listing 22.1: run Pennant's shadow week through the pipeline and score it the way the reconciliation team does."""
import _paths  # noqa: F401
import sys
from collections import Counter
from week import feed, fx_registry
from pipeline import run, grade

def week(version="pennant-qs-1.0", link_mode="first key", **kw):
    docs, bk = feed()
    refs, fx = fx_registry()
    res, store = run(docs, bk, refs, fx, version=version, link_mode=link_mode, **kw)
    return docs, bk, res, grade(docs, bk, res), store, refs, fx

if __name__ == "__main__":
    v = sys.argv[1] if len(sys.argv) > 1 else "v1"
    args = ("pennant-qs-1.0", "first key") if v == "v1" else ("pennant-qs-1.1", "two keys")
    docs, bk, res, g, store, refs, fx = week(*args)
    n = len(docs)
    print(f"shadow week days 124-130, {n} documents (deterministic stand-in); scorer {args[0]}, linkage: {args[1]}")
    print(f"fx table {fx} (owner {refs.meta(fx)['owner']}, as of {refs.meta(fx)['as_of']})")
    ch = Counter(d["channel"] for d in docs)
    print("by channel:", ", ".join(f"{c} {ch[c]}" for c in ("edi", "scan", "photo")))
    print("by day:    ", ", ".join(f"{dd} {sum(1 for d in docs if d['day'] == dd)}" for dd in range(124, 131)))
    oc = Counter(r["outcome"] for r in res)
    print("system outcome:", ", ".join(f"{k} {oc[k]}" for k in ("matched", "exception", "held", "person")))
    gc = Counter(g)
    for k in ("matched", "exception confirmed", "false exception", "held, confirmed", "held, not needed", "to a person", "silently wrong"):
        print(f"  {k:<20} {gc[k]:>5}  {gc[k] / n:6.1%}")
    print(f"matched as scored by the reconciliation team: {gc['matched']} of {n} = {gc['matched'] / n:.1%}")
    for c in ("edi", "scan", "photo"):
        idx = [i for i, d in enumerate(docs) if d["channel"] == c]
        m = sum(g[i] == "matched" for i in idx); w = sum(g[i] == "silently wrong" for i in idx)
        print(f"  {c:<6} {len(idx):>5} docs  matched {m / len(idx):6.1%}  silently wrong {w}")
    wrong = [(d, r) for d, r, gg in zip(docs, res, g) if gg == "silently wrong"]
    for d, r in wrong:
        print(f"  wrong: {d['doc_id']} {d['channel']} {d['kind']}, {r['why']} -> PN-{48000 + r['linked']}, truth PN-{48000 + d['_ship']}; truth tags {sorted(d['_truth']) or d.get('_disc') or 'misread'}")
