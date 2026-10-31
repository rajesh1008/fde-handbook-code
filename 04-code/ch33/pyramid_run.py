"""Listing 33.10: the chapter lab through the Chapter 29 pyramid runner; which layer caught the injection."""
from world import M, DESIGNS, CALDWELL, VENDOR_IDS
from pack import build
from fieldkit.pyramid import Layer, Pyramid, caught_at, PASS, FAIL

SIGNED_R3 = M.register_digest(M.classify_all(CALDWELL, DESIGNS[153]))


def lint(s):
    p = s["pack"].lint()
    return (FAIL if p else PASS), f"{len(p)} lint problems", 0.1, 0.0, {}


def register(s):
    d = M.register_digest(s["pack"].classes)
    return (PASS if d == SIGNED_R3 else FAIL), f"register {d} vs signed {SIGNED_R3}", 0.2, 0.0, {}


def computable(s):
    bad = [m.mid for m, b in M.computability(s["pack"].metrics, "Caldwell", VENDOR_IDS) if b]
    return (FAIL if bad else PASS), ("needs Northlight: " + ", ".join(bad)) if bad else "all computable", 1.4, 0.0, {}


def numbers(s):
    keys = {(e.key, e.cid) for e in s["pack"].evidence}
    ok = ("outcomes", "RT") in keys and ("outcomes", "EX") in keys
    return (PASS if ok else FAIL), "pack numbers trace to suite outputs", 3.0, 0.0, {}


L = [Layer(1, "unit", "pack schema", "every change", 1, 0), Layer(2, "component", "classification", "every change", 5, 0),
     Layer(3, "integration", "environment facts", "every change", 30, 0),
     Layer(4, "system", "suite outputs", "nightly", 600, 0)]
py = Pyramid(L).add(1, "pack lint", lint).add(2, "register matches signed r3", register) \
    .add(3, "metrics computable by Caldwell", computable).add(4, "evidence traces to suite", numbers)
for v in ("v1", "v2"):
    res = py.run({"pack": build(v)})
    print(f"pack {v}:")
    for r in res:
        print(f"  layer {r.layer} {r.check:<34} {r.verdict:<8} {r.detail}")
    c = caught_at(res)
    print(f"  caught at layer: {c if c else 'none (all layers pass)'}")
