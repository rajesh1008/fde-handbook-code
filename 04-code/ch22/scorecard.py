"""Listing 22.5: the scorecard the reconciliation team signs, with three definitions of matched and the lineage check."""
import _paths  # noqa: F401
from collections import Counter
from shadow_week import week
from pipeline import recompute

if __name__ == "__main__":
    docs, bk, res, g, store, refs, fx = week()
    n = len(docs)
    linked = sum(1 for r in res if r.get("linked") is not None)
    untouched = sum(1 for r in res if r["outcome"] == "matched")
    team = sum(1 for x in g if x == "matched")
    print(f"three definitions of matched on the same {n} documents")
    print(f"  linked to a booking (the build team's first draft)   {linked:>5}  {linked / n:.1%}")
    print(f"  closed with no person touching it (operations)       {untouched:>5}  {untouched / n:.1%}")
    print(f"  right booking, every rule agrees, team confirms      {team:>5}  {team / n:.1%}   <- signed definition")
    print()
    print(f"{'channel':<7} {'docs':>5} {'matched':>8} {'excepted':>9} {'held':>6} {'person':>7} {'wrong':>6}")
    rows = {}
    for c in ("edi", "scan", "photo", "all"):
        idx = [i for i, d in enumerate(docs) if c == "all" or d["channel"] == c]
        k = Counter(g[i] for i in idx)
        m = k["matched"] / len(idx)
        e = (k["exception confirmed"] + k["false exception"]) / len(idx)
        h = (k["held, confirmed"] + k["held, not needed"]) / len(idx)
        p = k["to a person"] / len(idx)
        rows[c] = (len(idx), m, e, h, p, k["silently wrong"])
        print(f"{c:<7} {len(idx):>5} {m:>8.1%} {e:>9.1%} {h:>6.1%} {p:>7.1%} {k['silently wrong']:>6}")
    k = Counter(g)
    print(f"exceptions the team confirmed {k['exception confirmed']} of {k['exception confirmed'] + k['false exception']}; "
          f"holds the team confirmed {k['held, confirmed']} of {k['held, confirmed'] + k['held, not needed']}")
    claims = [r["claim"] for r in res if r.get("claim")]
    probs = [p for c in claims for p in store.verify(c, recompute=recompute)]
    print(f"lineage: {len(claims)} claims, {len(store.nodes)} nodes, {store.size_bytes() / 1024:,.0f} KB for the week; verify problems {len(probs)}")
    eur = next(r for d, r in zip(docs, res) if r.get("claim") and d.get("currency") == "EUR" and r["outcome"] == "matched" and d["kind"] == "freight invoice")
    print(f"chain for {eur['doc_id']}:")
    for line in store.explain(eur["claim"]):
        print("  " + line)
