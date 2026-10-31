"""Listing 29.2: the five layers on the day-141 main branch (deterministic stand-in; timings and costs are the
stand-in timing model and rate card, except the measured line)."""
import json
import common as C
import world as W

p = C.build()
res = p.run(C.BASE, stop_on_fail=False)
print(f"{'layer':14} {'check':24} {'verdict':8} {'minutes':>8} {'dollars':>8}")
by = {}
for r in res:
    L = C.LAYERS[r.layer - 1]
    print(f"L{r.layer} {L.name:11} {r.check:24} {r.verdict:8} {r.seconds / 60:>8.1f} {r.dollars:>8.2f}")
    b = by.setdefault(r.layer, [0, 0]); b[0] += r.seconds; b[1] += r.dollars
print()
for L in C.LAYERS:
    s, d = by[L.n]
    print(f"L{L.n} {L.name:11} {L.frequency:40} {s / 60:6.1f} min  ${d:7.2f} per run")
real = res[0].metrics["real_seconds"]
print(f"\nmeasured on this box: layer one's 412 rule cases ran in {real * 1000:.0f} ms of pure Python;"
      f" the modeled {res[0].seconds:.0f} s adds interpreter start and test collection in Caldwell CI")
json.dump({str(k): v for k, v in by.items()}, open("output/layers.json", "w"), indent=1)
