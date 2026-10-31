"""Listing 26.5: the regression gate is per customer. Caldwell's gate on two candidate changes."""
import json
from world import gold_items, candidate, CRITICAL
from fieldkit.evals import CustomerGate

items = gold_items()
w = {it.key: it.weight for it in items}
before = {it.key: it.anne_ok for it in items}
gate = CustomerGate(customer="Caldwell", owner="Anne Kessler", scorer="Kessler's adjusters",
                    document_set="gold-set-300", critical_fields=CRITICAL, max_drop_points=0.5, max_lost_critical=0)
out = {}
for name, label in (("p7", "prompt p7: Caldwell's definitions in the prompt"),
                    ("p7+alias", "prompt p7 on the gateway's newer model version")):
    after = {it.key: candidate(it, name) for it in items}
    base = before if name == "p7" else out["p7_after"]
    status, reasons, cells, wb, wa = gate.check(base, after, weight_of=w.get)
    print(f"candidate: {label}")
    for line in gate.lines:
        print(" ", line)
    print(f"  verdict: {status.upper()}{': ' + '; '.join(reasons) if reasons else ''}")
    lost = [k for k in cells["lost"] if k[1] in CRITICAL]
    strata = {}
    for it in items:
        if it.key in lost:
            strata[it.stratum] = strata.get(it.stratum, 0) + 1
    print(f"  lost critical items by stratum: {strata}\n")
    out[name] = dict(status=status, wb=wb, wa=wa, cells={c: len(v) for c, v in cells.items()}, reasons=reasons,
                     lost_by_stratum=strata)
    out[name + "_after"] = after
json.dump({k: v for k, v in out.items() if not k.endswith("_after")}, open("output/regression_gate.json", "w"),
          indent=1)
