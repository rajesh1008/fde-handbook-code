"""Try It Yourself. a: record the model by alias, not by pin. b: wait six months and rebuild v0 packs.
c: edit one recorded decision after the fact and watch the chain head."""
import random, sys
import _paths  # noqa: F401
import world as W, pack as P
from fieldkit.lineage import digest
part = sys.argv[1] if len(sys.argv) > 1 else "a"
recs = W.records(W.FIX, W.FIX + 2)
if part == "a":
    s = random.Random(3).sample(recs, 40)
    for r in s:
        r["model"] = "provider-default (alias)"
    st = [P.build(r, W.FIX + 3)[0] for r in s]
    bad = sum(x["prompt and model"] == "inferred" for x in st)
    print(f"a: model recorded by alias in 40 of 40 packs -> prompt and model element 'inferred' in {bad}; packs complete {sum(P.complete(x) for x in st)} of 40")
elif part == "b":
    v0 = [r for r in W.records(W.LIVE, W.DISPUTE - 1)]
    s = random.Random(40).sample(v0, 40)
    for asof in (177, 200, 340):
        c = [P.build(r, asof)[0]["prompt and model"] for r in s]
        print(f"b: as of day {asof}: contradicted {c.count('contradicted')}, inferred {c.count('inferred')} of 40")
else:
    s = recs[:200]
    packs = [[r["id"], P.build(r, W.FIX + 3)[0], r["fields_digest"]] for r in s]
    head = P.chain_head(packs)
    s[117]["fields"]["loss_location"] = "edited after the fact"
    packs2 = [[r["id"], P.build(r, W.FIX + 3)[0], r["fields_digest"]] for r in s]
    st = packs2[117][1]["decision"]
    print(f"c: anchored head {head}; recomputed head {P.chain_head(packs2)}; decision element of {s[117]['id']}: {st}")
