"""Listing 29.6: pull request #212 (day 146), extractor prompt p9. The aggregate rises; one document class falls.
Which layer catches it? Deterministic stand-in; scored as Anne Kessler's adjusters scored gold-set-300 test."""
import json
import common as C
import world as W
from fieldkit.pyramid import select_layers

paths = ["prompts/extract_p9.txt", "prompts/examples/email_03.json"]
kinds, layers = select_layers(paths, C.PATH_RULES)
print(f"PR #212 'extractor prompt p9: three email examples, date received from the letter'")
print(f"  changed: {paths} -> kinds {kinds}, layers {layers}")
p = C.build()
sysc = dict(C.BASE, prompt="p9")
res = p.run(sysc, layers=layers)
for r in res:
    print(f"  L{r.layer} {r.check:24} {r.verdict.upper():12} {r.detail}")
d = C.gate_owner().decide(res)
print(f"  gate: {d['decision'].upper()}, caught at layer {d['caught_at']}")
ext = next(r for r in res if r.check == "extractor slices").metrics
b, a = ext["before"], ext["after"]
st, reasons, cells, wb, wa = C.aggregate_gate(b, a)
print(f"\nwhat the Chapter 26 aggregate gate alone says: {st.upper()} {reasons}")
print("  " + ", ".join(f"{k} {len(v)}" for k, v in cells.items()))
print(f"\nbefore/after on gold-set-300 test (201 documents, 2,010 fields), by document class")
print(f"{'class':22} {'fields':>6} {'p8.3':>7} {'p9':>7} {'gained':>6} {'lost':>5}  verdict")
rows = {}
for r in ext["rows"]:
    if r["kind"] == "stratum":
        print(f"{r['slice']:22} {r['n']:>6} {r['before'] / r['n']:>7.1%} {r['after'] / r['n']:>7.1%} {r['gains']:>6} "
              f"{r['losses']:>5}  {r['verdict']}")
        rows[r["slice"]] = [r["n"], r["before"], r["after"], r["gains"], r["losses"], r["verdict"]]
print(f"{'all classes':22} {len(b):>6} {wb:>7.1%} {wa:>7.1%} {len(cells['gained']):>6} {len(cells['lost']):>5}")
worst = [r for r in ext["rows"] if r["kind"] == "stratum x field" and r["verdict"] == "fail"]
for r in worst:
    print(f"slice {r['slice'][0]} x {r['slice'][1]}: {r['before']} of {r['n']} -> {r['after']} of {r['n']}, "
          f"sign test p = {r['p']:.1e}")
json.dump(dict(rows=rows, agg=[wb, wa], worst=[[*r["slice"], r["n"], r["before"], r["after"]] for r in worst]),
          open("output/failure_injection.json", "w"), indent=1)
