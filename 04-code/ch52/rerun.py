"""Listings 52.1 and 52.2: rerun Caldwell's evaluation suite on one and two generations after the pin."""
import _paths  # noqa: F401
from fieldkit.evals import four_cells
from fieldkit.pyramid import caught_at, LAYER_NAMES, MergeGate
import world as W, suite as S

print("Caldwell evaluation suite, gold-set-300 test split (201 documents x 10 fields = 2,010 fields)")
print(f"{'version':<15}{'weighted':>9}{'raw':>8}{'gained':>8}{'lost':>6}{'lost crit':>10}{'$/doc':>9}{'p95 s':>7}")
base = W.scored(W.PIN)
for v in W.VERSIONS:
    s = W.scored(v)
    w = sum(W.WEIGHT[k[1]] * ok for k, ok in s.items()) / sum(W.WEIGHT[k[1]] for k in s)
    raw = sum(s.values()) / len(s)
    gained = sum(s[k] and not base[k] for k in s); lost = sum(base[k] and not s[k] for k in s)
    lc = sum(base[k] and not s[k] for k in s if k[1] in W.CRITICAL)
    print(f"{v:<15}{w:>9.1%}{raw:>8.1%}{gained:>8}{lost:>6}{lc:>10}{W.COST[v]:>9.4f}{W.P95[v]:>7}")
det = sum(W.scored(W.N2)[k] == base[k] for k in base if k[1] in W.DETERMINISTIC)
print(f"deterministic fields unchanged across versions: {det} of {201 * len(W.DETERMINISTIC)}")
print()
pyr = S.pyramid()
gate = MergeGate(owner="Anne Kessler")
for v in (W.N1, W.N2):
    res = pyr.run({"version": v}, stop_on_fail=False)
    at = caught_at(res); d = gate.decide(res)
    print(f"{v}: decision {d['decision']}" + (f", caught at layer {at} ({LAYER_NAMES[at]})" if at else ""))
    for r in res:
        print(f"  L{r.layer} {r.check:<16}{r.verdict:<13}{r.detail}")
