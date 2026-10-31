"""Listing 22.3: the fifteen steps as built, checked against the Chapter 9 design, with measured step executions."""
import _paths  # noqa: F401
import importlib.util, pathlib, sys
from collections import Counter
from shadow_week import week

ch09 = pathlib.Path(__file__).resolve().parents[1] / "ch09"
sys.path.insert(0, str(ch09))
spec = importlib.util.spec_from_file_location("ch09_pipelines", ch09 / "pipelines.py")
P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
from fieldkit.autonomy import classify, split, SHORT, CLASSES

SHADOW_OFF = {"N13": "off in shadow (no TMS write)", "N14": "off in shadow (no shipper message)"}


def executions(docs, res):
    """Which steps each document actually ran in the week."""
    ex = Counter()
    for d, r in zip(docs, res):
        ex["N01"] += 1
        if d["channel"] == "edi":
            ex["N02"] += 1
        if r["outcome"] == "held":
            continue
        if d["channel"] != "edi":
            ex["N03"] += 1
            if r.get("why", "").startswith("N03"):
                continue
            ex["N04"] += 1
            if d["kind"] == "bill of lading":
                ex["N05"] += 1
        if r.get("why", "").startswith("N05"):
            continue
        ex["N06"] += 1; ex["N07"] += 1
        if r.get("linked") is None:
            continue
        ex["N09"] += 1; ex["N11"] += 1
        if r["queue"] == "escalation":
            continue
        ex["N08"] += 1
        if d["kind"] == "freight invoice":
            ex["N10"] += 1
        if r["outcome"] == "exception":
            ex["N12"] += 1
        ex["N15"] += 1
    return ex


if __name__ == "__main__":
    docs, bk, res, g, store, refs, fx = week()
    ex = executions(docs, res)
    print(f"{'step':<4} {'class':<8} {'runs':>5}  name")
    for s in P.PENNANT:
        cls = classify(s)
        note = SHADOW_OFF.get(s.n, "")
        print(f"{s.n:<4} {SHORT[cls]:<8} {ex[s.n]:>5}  {s.name[:58]}" + (f"  [{note}]" if note else ""))
    sp = split(P.PENNANT)
    print("design split (Chapter 9):", ", ".join(f"{SHORT[i]} {sp[c]}" for i, c in enumerate(CLASSES)),
          f"-> {sp[CLASSES[0]] / len(P.PENNANT):.0%} of steps deterministic")
    by = Counter()
    for s in P.PENNANT:
        by[classify(s)] += ex[s.n]
    tot = sum(by.values())
    print("measured step executions in the week:", ", ".join(f"{SHORT[i]} {by[i]} ({by[i] / tot:.1%})" for i in range(len(CLASSES))), f"total {tot}")
    model = by[2] + by[3]
    print(f"model calls per document: {model / len(docs):.2f} (small {by[2]}, frontier {by[3]})")
