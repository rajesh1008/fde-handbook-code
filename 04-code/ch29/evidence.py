"""Listing 29.10: the first month's test evidence, chained, traced to requirements, and tampered with once."""
import json
import common as C
from fieldkit.pyramid import EvidenceRecord, chain, verify, trace_matrix

REQ = {}
src = [("release boundary (Ch 25)", 12, "integration replay"), ("customer gate (Ch 26)", 8, "extractor slices"),
       ("router (Ch 27)", 10, "rule regression"), ("customer rules (Ch 28)", 9, "rule regression"),
       ("Caldwell QE (Owen Pryce)", 7, "scenario simulator")]
check_of = {}
for name, n, chk in src:
    for i in range(n):
        rid = f"R-{len(REQ) + 1:02d}"
        REQ[rid] = name; check_of[rid] = chk
uncovered_by_design = {"R-44": "adjuster sees why a field was routed (UI)", "R-45": "evidence pack readable by audit",
                       "R-46": "rollback drill each quarter"}
recs = []
for day in range(141, 171):
    for rid, chk in check_of.items():
        if rid in uncovered_by_design:
            continue
        if chk == "scenario simulator" and day not in (145, 152, 159, 166):
            continue
        if chk in ("rule regression", "integration replay", "extractor slices") and day % 3:
            continue
        recs.append(EvidenceRecord(rid, chk, {"rule regression": 1, "extractor slices": 2, "integration replay": 3,
                                              "scenario simulator": 4}[chk], f"run-{day}", f"c{day:04x}", "pass", {}))
head = chain(recs)
tm = trace_matrix(REQ, recs)
unc = [r for r, v in tm.items() if not v["covered"]]
print(f"requirements {len(REQ)}, evidence records {len(recs)}, chain head {head[:12]}")
print(f"verify: {'intact' if verify(recs) is None else 'broken'}")
print(f"uncovered requirements: {len(unc)}")
for r in unc:
    print(f"  {r} {uncovered_by_design[r]}")
recs[200].verdict = "fail"
print(f"after editing record 200's verdict: chain breaks at record {verify(recs)}")
json.dump(dict(req=len(REQ), recs=len(recs), unc=len(unc)), open("output/evidence.json", "w"), indent=1)
