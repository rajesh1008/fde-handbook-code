"""Try It Yourself: a, two-key linkage on its own; b, the N05 date floor; c, the R3 tolerance."""
import _paths  # noqa: F401
import sys
from collections import Counter
import pipeline
from shadow_week import week


def show(label, g, n=2100):
    k = Counter(g)
    print(f"  {label:<34} matched {k['matched'] / n:6.1%}  person {k['to a person']:>3}  exceptions {k['exception confirmed'] + k['false exception']:>3}"
          f" (false {k['false exception']:>2})  wrong {k['silently wrong']}")


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "a"
    if t == "a":
        print("a: which fix closes the thumb hole? (same week, same documents)")
        for ver, mode in (("pennant-qs-1.0", "first key"), ("pennant-qs-1.0", "two keys"), ("pennant-qs-1.1", "first key"), ("pennant-qs-1.1", "two keys")):
            show(f"{ver}, {mode}", week(ver, mode, lineage=False)[3])
    elif t == "b":
        print("b: lower the N05 handwritten-date floor")
        for f in (0.95, 0.90, 0.80, 0.70):
            show(f"date floor {f:.2f}", week(date_floor=f, lineage=False)[3])
    else:
        print("c: tighten or loosen the R3 tolerance (USD 1.00 or this share of the contract)")
        for p in (0.0, 0.005, 0.02, 0.05):
            pipeline.R3_PCT = p
            show(f"R3 {p:.1%}", week(lineage=False)[3])
