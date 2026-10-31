"""Listing 29.8: six verification streams on the wrong fields of gold-set-300 test (prompt p8.3), before and after
the second pass moved to a different model pin. Deterministic stand-in; wrong means Anne's adjusters said so."""
import json
import world as W
from fieldkit.pyramid import independence

ex = W.extract("p8.3")
wrong = [k for k, ok in ex.items() if not ok]


def catches(same_model):
    c = {s: set() for s in ("schema and type", "business rules", "system of record", "source grounding",
                            "second extraction", "cross-document")}
    for k in wrong:
        d, f = k; s = W.STRATUM[d]; poor = s in ("first notice, fax", "first notice, mail")
        if W.u(k, "schema") < (0.22 if f in ("policy_number", "loss_date", "date_received", "police_report_ref") else 0.04):
            c["schema and type"].add(k)
        if W.u(k, "rules") < (0.30 if f in ("loss_date", "date_received", "loss_type") else 0.06):
            c["business rules"].add(k)
        if f in W.SYSTEM_CHECKED and W.u(k, "sor") < 0.80:
            c["system of record"].add(k)
        g = W.u(k, "ground") < (0.40 if poor else 0.60)
        if g:
            c["source grounding"].add(k)
        if same_model:
            if (g and W.u(k, "sp") < 0.85) or W.u(k, "sp2") < 0.08:
                c["second extraction"].add(k)
        elif W.u(k, "sp3") < 0.55:
            c["second extraction"].add(k)
        if f in W.TWO_SOURCE_FIELDS and W.u(k, "xdoc") < 0.45:
            c["cross-document"].add(k)
    return c


res = {}
for label, same in (("day 140, second pass on the extractor's model", True), ("day 148, second pass on a different pin", False)):
    r = independence(catches(same), wrong)
    res[label] = r
    print(f"{label}: {r['n']} wrong fields")
    for s, v in r["rows"].items():
        print(f"  {s:20} caught {v['caught']:>3}  only this stream {v['unique']:>3}")
    print(f"  any stream {r['union']} of {r['n']} ({r['union'] / r['n']:.0%}); missed by all six {r['missed']}")
    ph = r["phi"][("source grounding", "second extraction")]
    print(f"  correlation of misses, grounding vs second extraction: phi {ph:.2f}")
best = max(res[label]["rows"].values(), key=lambda v: v["caught"])["caught"]
print(f"best single stream catches {best}; removing 'second extraction' after day 148 loses "
      f"{res[label]['rows']['second extraction']['unique']} catches no other stream makes")
json.dump({k: dict(rows=v["rows"], union=v["union"], n=v["n"], missed=v["missed"],
                   phi=v["phi"][("source grounding", "second extraction")]) for k, v in res.items()},
          open("output/streams.json", "w"), indent=1)
