"""Listing 29.9: the first month of the gate, days 141 to 170 (deterministic stand-in commit log; timings and
costs from the stand-in model)."""
import json
import common as C
import world as W
from fieldkit.pyramid import select_layers

KIND_PATHS = {"code": "intake/route.py", "rule": "rules/v118.yaml", "prompt": "prompts/extract.txt",
              "model": "models/pins.yaml", "retrieval": "retrieval/config.yaml", "threshold": "router/thresholds.yaml",
              "dependency": "requirements.txt", "gold": "gold/refresh.csv", "infra": "infra/ci.yaml", "docs": "docs/runbook.md"}
MIX = [("code", 0.40), ("docs", 0.13), ("rule", 0.10), ("prompt", 0.09), ("infra", 0.08), ("dependency", 0.07),
       ("retrieval", 0.05), ("threshold", 0.04), ("gold", 0.02), ("model", 0.02)]


def kind_of(i):
    r, a = W.u("pr", i, "kind"), 0.0
    for k, s in MIX:
        a += s
        if r < a:
            return k
    return "code"


prs = []
for i in range(41):
    num = 200 + i
    day = 141 + int(i * 30 / 41)
    k = {212: "prompt", 231: "dependency"}.get(num, kind_of(i))
    prs.append(dict(num=num, day=day, kind=k, commits=3 + int(W.u("pr", i, "c") * 5)))
commits = sum(p["commits"] for p in prs)
runs = {1: 0, 2: 0, 3: 0, 4: 0}; dollars = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}; secs = {1: [], 2: [], 3: [], 4: []}
for p in prs:
    _, layers = select_layers([KIND_PATHS[p["kind"]]], C.PATH_RULES)
    p["layers"] = layers
    for c in range(p["commits"]):
        runs[1] += 1
        secs[1].append(3.2 + 0.014 * 412 + 4 * W.u(p["num"], c, "jit"))
    if 2 in layers:
        runs[2] += 1; s = C.chk_extractor(C.BASE); f = C.chk_faith(C.BASE)
        secs[2].append(s[2] + f[2]); dollars[2] += s[3] + f[3]
weekly = [145, 152, 159, 166]
merges = [p for p in prs if p["num"] not in (212, 231)]
for _ in merges:
    runs[3] += 1; r = C.chk_integration(C.BASE); secs[3].append(r[2]); dollars[3] += r[3]
for _ in weekly:
    runs[4] += 1; r = C.chk_system(C.BASE); secs[4].append(r[2]); dollars[4] += r[3]
med = lambda xs: sorted(xs)[len(xs) // 2]
print(f"days 141 to 170: {len(prs)} pull requests, {commits} commits, {len(merges)} merged, 2 blocked")
print(f"{'layer':16} {'runs':>5} {'median':>9} {'cost/run':>9} {'month':>9}")
names = {1: "L1 unit", 2: "L2 component", 3: "L3 integration", 4: "L4 system"}
out = {}
for n in (1, 2, 3, 4):
    m = med(secs[n]); cpr = dollars[n] / max(1, runs[n])
    unit = f"{m:.0f} s" if m < 120 else f"{m / 60:.0f} min"
    print(f"{names[n]:16} {runs[n]:>5} {unit:>9} {cpr:>9.2f} {dollars[n]:>9.2f}")
    out[n] = dict(runs=runs[n], median=m, cost=cpr, total=dollars[n])
print(f"{'L5 operational':16} {'daily':>5} {'':>9} {'':>9} {30 * (10 * W.doc_cost() + 0.9):>9.2f}")
print("blocked: PR #212 day 146 at L2 (mail date received); PR #231 day 153 at L1 (date library)")
print(f"PRs that ran L2: {runs[2]} of {len(prs)}; docs-only PRs that ran nothing: {sum(not p['layers'] for p in prs)}")
json.dump(dict(out=out, l1=secs[1], prs=len(prs), commits=commits), open("output/month.json", "w"), indent=1)
