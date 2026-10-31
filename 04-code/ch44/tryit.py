"""Try It Yourself variations a, b, c (Chapter 44)."""
import sys
import world as W
from practice import decide, load_series, red_months
v = sys.argv[1] if len(sys.argv) > 1 else "a"
if v == "a":
    w = dict(W.WEIGHTS, build=0.35, discovery=0.05, communication=0.06)
    s = W.CANDIDATES["C-3"]
    print(f"a) build weight 0.35, discovery 0.05, communication 0.06 (sum {sum(w.values()):.2f})")
    print("   C-3 weighted, no floors:", decide(s, weights=w, floors={}))
    print("   C-3 weighted, floors kept:", decide(s, weights=w))
elif v == "b":
    print("b) drop E1 (discovery role-play) to save 45 minutes")
    ex = {k: v2 for k, v2 in W.EXERCISES.items() if not k.startswith("E1")}
    for c in ("C-1", "C-3", "C-4"):
        print(f"   {c}:", decide(W.CANDIDATES[c], exercises=ex))
elif v == "c":
    print("c) Pennant overnight rota depth 2 instead of 3 (Maya Brooks, policy on)")
    for depth in (1, 2, 3):
        s = load_series("Maya Brooks", policy=True, rota_depth=depth)
        print(f"   depth {depth}: peak {max(x for x in s if x is not None):.2f}; red months {red_months(s)}")
