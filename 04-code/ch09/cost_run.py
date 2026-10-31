"""Listing 9.6: cost and latency per document by class, Caldwell's eleven paths weighted by monthly volume,
against the demo architecture. STAND-IN prices and latencies (see costs.py); no provider was called."""
import random
import _path  # noqa: F401
from fieldkit.autonomy import split, CLASSES
import costs as K
from intake_paths import walk_paths
from pipelines import GREYSTONE, PENNANT

KIND = {"P03": "email", "P06": "email", "P11": "email", "P08": "structured"}
rng = random.Random(9)
vol = 0; new_tot = demo_tot = 0.0; by_class = {k: 0.0 for k in ("det", "rules", "small", "frontier", "platform")}
lat_new, lat_demo, lat_cls = [], [], {k: [] for k in ("det", "rules", "small", "frontier")}
print(f"{'path':<5}{'docs/mo':>8}{'demo $/doc':>11}{'pipeline $/doc':>15}{'fall':>6}")
for row, steps, c, refusal in walk_paths():
    kind = KIND.get(row[0], "scan")
    by, new = K.pipeline_cost(c, kind)
    _, demo = K.demo_cost(kind)
    v = row[2]; vol += v; new_tot += v * new; demo_tot += v * demo
    for k in by: by_class[k] += v * by[k]
    print(f"{row[0]:<5}{v:>8,}{demo:>11.4f}{new:>15.4f}{1 - new / demo:>6.0%}")
    for _ in range(max(1, v // 100)):           # one latency draw per hundred documents
        lb, lt = K.pipeline_latency(c, rng); lat_new.append(lt)
        for k in lb:
            if lb[k]: lat_cls[k].append(lb[k])
        lat_demo.append(K.demo_latency(rng)[1])
print(f"weighted: demo {demo_tot / vol:.4f}  pipeline {new_tot / vol:.4f}  per document; fall {1 - new_tot / demo_tot:.1%}")
print(f"monthly at {vol:,} documents: demo ${demo_tot:,.0f}  pipeline ${new_tot:,.0f}")
print("pipeline cost by class per document: " + "  ".join(f"{k} {v / vol:.4f}" for k, v in by_class.items()))
print(f"frontier share of pipeline cost: {by_class['frontier'] / new_tot:.0%}")
print("latency per document, seconds   p50    p95")
print(f"  demo agent                  {K.pct(lat_demo, .5):6.1f} {K.pct(lat_demo, .95):6.1f}")
print(f"  deterministic-first         {K.pct(lat_new, .5):6.1f} {K.pct(lat_new, .95):6.1f}")
for k, xs in lat_cls.items():
    print(f"    of which {k:<8}         {K.pct(xs, .5):6.2f} {K.pct(xs, .95):6.2f}")
print("other customers, one typical document:")
for name, steps, kind in (("Greystone Health", GREYSTONE, "email"), ("Pennant Logistics", PENNANT, "scan")):
    sp = split(steps); c = [sp[k] for k in CLASSES]
    _, new = K.pipeline_cost(c, kind); _, demo = K.demo_cost(kind)
    print(f"  {name:<18} classes {c}  demo {demo:.4f}  pipeline {new:.4f}  fall {1 - new / demo:.0%}")
