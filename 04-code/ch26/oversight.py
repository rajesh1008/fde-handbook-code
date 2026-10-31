"""Listing 26.6: Caldwell's oversight profile on Anne's gold set (the Chapter 4 profile, now on real scoring).
Threshold chosen on one half of the documents, checked on the other; Wilson lower bound on the checked half."""
import json
from world import gold_items, candidate
from fieldkit.evals import wilson

items = gold_items()
half = lambda it: int(it.doc[1:]) % 2
out = {}
for name in ("p6", "p7"):
    ok = (lambda it: it.anne_ok) if name == "p6" else (lambda it: candidate(it, "p7"))
    A = [it for it in items if half(it) == 0]
    B = [it for it in items if half(it) == 1]
    print(f"{'baseline p6' if name == 'p6' else 'candidate p7'}: target  threshold  auto share  "
          f"accuracy (checked half)  Wilson low  review share")
    rows = []
    for target in (0.95, 0.98):
        chosen = None
        for t in [x / 100 for x in range(50, 100)]:
            auto = [it for it in A if it.conf >= t]
            if len(auto) >= 30 and sum(ok(it) for it in auto) / len(auto) >= target:
                chosen = t
                break
        if chosen is None:
            print(f"   {target:.0%}   not reachable on this half")
            continue
        auto = [it for it in B if it.conf >= chosen]
        k = sum(ok(it) for it in auto)
        lo, _ = wilson(k, len(auto))
        share = len(auto) / len(B)
        print(f"   {target:.0%}     {chosen:.2f}       {share:5.1%}          {k / len(auto):5.1%}             "
              f"{lo:5.1%}      {1 - share:5.1%}")
        rows.append(dict(target=target, t=chosen, auto=share, accB=k / len(auto), lo=lo))
    curve = []
    for t in [x / 100 for x in range(50, 100, 2)]:
        auto = [it for it in B if it.conf >= t]
        if auto:
            curve.append((t, len(auto) / len(B), sum(ok(it) for it in auto) / len(auto)))
    out[name] = dict(rows=rows, curve=curve)
json.dump(out, open("output/oversight.json", "w"), indent=1)
