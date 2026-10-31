"""Listing 28.3: replay the sandbox week and the injected referral through v1 and v2 of the suite."""
import _paths  # noqa: F401
from collections import Counter
from pipeline import suite, run, queued
from world import sandbox_week, injected, make_draft
import random

refs, drafts, actions, faults = sandbox_week()
inj = injected()
inj_draft = make_draft(inj, random.Random(5))
inj_acts = [dict(op="queue.write", target="coordinator_queue", identity="svc-greystone-sandbox-read",
                 intent="GR-INJ-01:draft", args=dict(mrn=inj["mrn"]))]
print(f"sandbox week: {len(refs)} referrals, {sum(r['red_flag'] for r in refs)} red flags, {len(drafts)} drafts in the Ch25 run")
print(f"refused calls proposed: {sum(1 for a in actions.values() for x in a if x['op'] != 'queue.write')}")
for v in ("v1", "v2"):
    s = suite(v)
    res = {r["id"]: run(s, r, drafts.get(r["id"]), actions.get(r["id"])) for r in refs}
    disp = Counter(x["disp"] for x in res.values())
    fired = Counter(f for x in res.values() for f in set(x["fired"]))
    denied = Counter(f for x in res.values() for f in x["denied"])
    print(f"\nsuite {v} on the sandbox week")
    for k, n in sorted(disp.items(), key=lambda x: -x[1]):
        print(f"  {k:<28} {n:>4}")
    print(f"  reached the queue           {sum(queued(x) for x in res.values()):>4}")
    print(f"  refused calls denied        {sum(denied.values()):>4}  ({', '.join(f'{k} {n}' for k, n in sorted(denied.items()))})")
    print("  rules that fired: " + ", ".join(f"{k} {n}" for k, n in sorted(fired.items())))
    caught = {}
    for name, ids in faults.items():
        caught[name] = sum(1 for i in ids if res[i]["fired"])
    print("  seeded faults caught: " + "; ".join(f"{k} {caught[k]}/{len(v_)}" for k, v_ in faults.items()))
    r = run(s, inj, inj_draft, inj_acts)
    print(f"  injected GR-INJ-01 (internal medicine, F10.239): {r['disp']}  fired {r['fired'] or 'none'}")
# cost and latency per layer (stand-in prices and latencies; the deployment's numbers come from its gateway logs)
print("\ncost and latency per layer, per referral (stand-in)")
layers = [("input, deterministic (11)", 0.0, 2), ("input, model-assisted (1)", 0.00034, 310),
          ("output, deterministic (22)", 0.0, 3), ("output, model-assisted (4)", 0.00136, 340),
          ("action, deterministic (14)", 0.0, 1), ("budget, deterministic (8)", 0.0, 1)]
for name, cost, ms in layers:
    print(f"  {name:<30} ${cost:.5f}  {ms:>4} ms")
total = sum(c for _, c, _ in layers)
print(f"  {'all guardrails':<30} ${total:.5f}  {2 + 310 + 3 + 340 + 1 + 1:>4} ms serial, {2 + 3 + 1 + 1 + 340:>4} ms with the model checks in parallel")
print(f"  {'the draft itself (Ch20)':<30} $0.26730  9800 ms")
print(f"  guardrails share of cost: {total / (total + 0.2673):.2%}")
