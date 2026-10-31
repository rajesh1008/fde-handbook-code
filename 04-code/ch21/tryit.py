"""Try It Yourself, Chapter 21: a) move the legibility gate, b) score by mean instead of minimum,
c) edit a source after extraction and watch verify() catch it."""
import sys
import _paths  # noqa: F401

if __name__ == "__main__":
    v = sys.argv[1] if len(sys.argv) > 1 else "a"
    if v == "a":
        import importlib, pennant, checks, scorer
        for t in (0.55, 0.60, 0.65, 0.70, 0.75):
            importlib.reload(pennant); importlib.reload(checks); importlib.reload(scorer)
            checks.LEGIBLE_AT = t   # move the gate, not the truth
            docs, ver, wo, wi, aw, ret = scorer.run()
            held = sum(x.decision != "accept" for x in ver)
            print(f"legibility gate {t:.2f}: held {held / len(ver):.1%} (clean held {sum(1 for d, x in zip(docs, ver) if x.decision != 'accept' and not d['_truth'])}), exceptions {sum(wi.values())} vs {sum(wo.values())} "
                  f"({(sum(wi.values()) - sum(wo.values())) / sum(wo.values()):+.0%}), awaiting sender {aw}")
    elif v == "b":
        from pennant import feed
        from checks import scorer as mk
        docs = feed(); s = mk()
        vs = s.run(docs)
        for cut in (0.80, 0.90):
            passed = [(d, x) for d, x in zip(docs, vs) if x.mean >= cut]
            bad = sum(1 for d, x in passed if d["_truth"])
            print(f"mean score >= {cut:.2f}: passes {len(passed)}, of which defective {bad}")
        print(f"minimum (hard gates): passes {sum(x.decision == 'accept' for x in vs)}, of which defective "
              f"{sum(1 for d, x in zip(docs, vs) if x.decision == 'accept' and d['_truth'])}")
    else:
        import lineage_break as lb
        from fieldkit.lineage import LineageStore, RefTables
        refs = RefTables(); st = LineageStore(refs)
        rel = lb.build(st, refs.register("fx_rates", lb.FX[66], "day 66", "treasury"))
        edited = dict(lb.SOURCES_NOW, **{"mail/2026/hls-inv-77310.pdf": "0b7e11aa4c02"})
        print("source re-saved by a mailbox rule after extraction:")
        for p in st.verify(rel, sources=edited, recompute=lb.recompute):
            print("  " + p)
        gone = {k: v for k, v in lb.SOURCES_NOW.items() if "mail/" not in k}
        print("source aged out of the 30-day mailbox:")
        for p in st.verify(rel, sources=gone):
            print("  " + p)
