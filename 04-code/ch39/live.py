"""After the Shadow Exit: conditions C-1 and C-2, the blind 5% sample, and the first Exhibit E month.
Deterministic stand-in (ledgered): live intake days 158 to 188, 520 in-scope documents an intake day."""
import json, random
import _paths  # noqa: F401
from fieldkit.evals import wilson
from fieldkit.sampling import allocate
from fieldkit.shadow import keyed_id
import world as W, suite as U

rng = random.Random(3958)
_, _, since = U.gate(W.caldwell_window())
rate = {s: k / n for s, (k, n, _) in since.items()}
DAYS = [d for d in range(158, 189) if d % 7 not in (0, 1)]  # Saturdays and Sundays closed (days 147, 148 pattern)
pop = {s: round(W.REFERENCE[s] * 520 * len(DAYS)) for s in W.STRATA}
docs = [dict(id=f"L{i:05d}", stratum=s) for i, s in enumerate(s for s in W.STRATA for _ in range(pop[s]))]
blind = [x for x in docs if int(keyed_id(x["id"], "caldwell-blind-2026")[:2], 16) < 13]
b_agree = sum(1 for x in blind if rng.random() < rate[x["stratum"]])
sighted = [x for x in docs if x not in blind][:4000]
s_acc = sum(1 for x in sighted if (lambda a: a or rng.random() < 0.75)(rng.random() < rate[x["stratum"]]))
print(f"live month: intake days {DAYS[0]} to {DAYS[-1]} ({len(DAYS)} days), {sum(pop.values()):,} in-scope documents")
print("C-1 broker-template date received, first 10 live intake days: 47 template first notices, review band checked 47, date errors 0 -> closed day 172")
lo, hi = wilson(33, 4000)
print(f"C-2 audit-live-400 (Owen Pryce, days 158 to 167): 33 wrong of 4,000 fields = 0.83% ({lo:.2%} to {hi:.2%}) -> upper bound under 1.2%, closed day 170")
lo, hi = wilson(b_agree, len(blind))
print(f"blind sample (keyed hash, clerks key before seeing the proposal): {b_agree} of {len(blind)} agree = {b_agree / len(blind):.1%} ({lo:.1%} to {hi:.1%})")
lo, hi = wilson(s_acc, len(sighted))
print(f"sighted acceptance on 4,000 non-blind documents: {s_acc / len(sighted):.1%} ({lo:.1%} to {hi:.1%}) -> not an agreement measure")
plan = allocate(pop, 310, floor=10)
print("\nExhibit E, first scored month (sample drawn by Caldwell's job on day 191, first business day of the month)")
print(f"{'stratum':22} {'population':>10} {'sampled':>8}")
for s in W.STRATA:
    print(f"{s:22} {pop[s]:10,} {plan[s][0]:8}")
ids = [f"E{i:03d}" for i in range(310)]
err = set(random.Random(1890).sample(ids, 4))
nonerr = [i for i in ids if i not in err]
dis = [sorted(err)[0]] + random.Random(1891).sample(nonerr, 2)
v2_extra = random.Random(1892).choice([i for i in nonerr if i not in dis])
a = {i: (i in err) or i == dis[1] for i in ids}           # scorer 1, Lena Ortiz
b = {i: (i in err and i != dis[0]) or i == dis[2] for i in ids}  # scorer 2, Tom Whitfield
split = [i for i in ids if a[i] != b[i]]
anne = {i: (a[i] if a[i] == b[i] else i in err) for i in ids}      # third scorer on splits only
k = sum(anne.values())
print(f"scorers agree on {310 - len(split)} of 310; {len(split)} split items to the third scorer; rubric gold-v3")
lo, hi = wilson(k, 310)
print(f"Anne Kessler's team: {k} errors in 310 = {k / 310:.2%}, upper bound {hi:.2%}; breach line 7 -> no breach, no credit")
nl_v2 = set(err) | {v2_extra}
print(f"Northlight computation, day 192 (script pinned to rubric gold-v2): {len(nl_v2)} errors; extra item {v2_extra}: broker-template date received")
print(f"rerun on gold-v3, day 194: {len(err)} errors, same items as Anne's team: {sorted(err) == sorted(i for i in ids if anne[i])}")
print("result: match on count and on items; no dispute filed; chronic counter 0 of 6 months")
json.dump(dict(blind=(b_agree, len(blind)), sighted=(s_acc, len(sighted)), errors=k, split=len(split)), open("output/live.json", "w"))
