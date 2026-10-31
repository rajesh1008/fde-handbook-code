"""Try It Yourself, Chapter 50. a: a correct ratio rounded to one decimal. b: a component's use reclassified.
c: Shadow Exit judged on the 400-memo sample the bid offered."""
import sys
import _paths  # noqa: F401
from fieldkit import modelrisk as M
from fieldkit import gates as G
import memo, world as W, classify, shadowrun

part = sys.argv[1]
if part == "a":
    store, ext, calc = memo.spread()
    for mode in (None, "round"):
        claims = memo.draft(store, ext, calc, inject=mode)
        g, c, lin = memo.check(store, claims)
        print(f"{'correct draft' if mode is None else 'rounded to 1.3x'}: claim 2 = {claims[1][0]!r}")
        print("  gate: " + ("; ".join(g) or "pass") + " | lineage: " + ("; ".join(lin) or "holds"))
    print("question: is a blocked 1.3x a false alarm or a policy? Harbourline's definition table sets two decimals.")
elif part == "b":
    import dataclasses
    a = classify.run()[1]
    comps = [dataclasses.replace(c, core_decision=False) if c.cid == "H10" else c for c in W.COMPONENTS]
    b = classify.run(comps)[1]
    print("H10 risk-factor summary marked supporting use (core_decision False)")
    print("  changed:", M.diff(a, b), "plan items", len(M.plan_for(a)), "->", len(M.plan_for(b)))
    print("  who may make that change: Helen Marsh, in writing, with the reason; the FDE may only propose it")
elif part == "c":
    agree = G.Criterion("agreement", "draft agrees with the officer's memo", 0.90, per="accounting standard")
    for total in (400, 600):
        recs = shadowrun.records(scale=total / 600); f = shadowrun.funnel(recs)
        ms = [G.Measurement("agreement", f["agree"], f["human"], measured_by="Harbourline credit review")]
        ms += [G.Measurement("agreement", k, n, s, measured_by="Harbourline credit review") for s, k, n, *_ in shadowrun.by_standard(recs)]
        r = G.GateRecord("Shadow Exit", [("shadow", "SE")], [agree], ms, "David Okafor", 150)
        print(f"{total} memos: status {r.status()}")
        for l in r.evaluate():
            print(f"  {l.scope:<8} {l.verdict:<10} {l.detail}")
