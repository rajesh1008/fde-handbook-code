"""Listing 28.4: the red team's 140 attacks and 60 benign twins against v2, v3 and a keyword guard."""
import _paths  # noqa: F401
from collections import Counter, defaultdict
from fieldkit.guardrails import FleetBreaker
from pipeline import suite, run, queued
from attacks import attacks, twins, CATS, keyword_guard, escaped

A, T = attacks(), twins()
print(f"red-team set: {len(A)} attacks in {len(CATS)} categories, {len(T)} benign twins")
rows = {}
for name, s, pre in [("v2", suite("v2"), None), ("v3", suite("v3"), None), ("keyword guard + v2", suite("v2"), keyword_guard)]:
    esc = defaultdict(int)
    stopped_by = Counter()
    for a in A:
        res = run(s, a["ref"], a["draft"], a["actions"], a["stop"], pre)
        if escaped(a, res):
            esc[a["cat"]] += 1
        else:
            for f in set(res["fired"]):
                stopped_by[f] += 1
    over = [t for t in T if not queued(run(s, t["ref"], t["draft"], t["actions"], t["stop"], pre))]
    rows[name] = (esc, over, stopped_by)
    print(f"\n{name}: escapes {sum(esc.values())} of {len(A)}; benign twins refused or routed {len(over)} of {len(T)}")
    for c in CATS:
        print(f"  {c:<30} escapes {esc[c]:>2} / 20")
    print("  rules that stopped attacks: " + ", ".join(f"{k} {n}" for k, n in sorted(stopped_by.items())))
    words = Counter(t["word"] for t in over)
    print("  twins refused or routed by word: " + (", ".join(f"{w} {n}" for w, n in sorted(words.items())) or "none"))
# fleet breaker during the loop-induction hour (day 127, 10:00 to 11:00): 20 attacks among 46 ordinary replays
fb = FleetBreaker(rate=0.05, min_runs=20, page="Northlight on-call (managed-service run desk notified)")
seq = [False] * 46
for i in range(20):
    seq.insert(3 + i * 3, True)
first = None
for n, tripped in enumerate(seq, 1):
    msg = fb.record("day 127 10:00-11:00", tripped)
    if msg and first is None:
        first = (n, msg)
print(f"\nfleet breaker, loop-induction hour: {sum(seq)} of {len(seq)} runs tripped; first page at run {first[0]}: {first[1]}")
