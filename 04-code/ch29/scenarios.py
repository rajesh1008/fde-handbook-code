"""Listing 29.5: the golden-set schema check and the first weekly scenario run (day 145), triaged."""
import json
import common as C
import world as W

REQUIRED = ("case_id", "layer", "stratum", "source_refs", "expected", "critical_fields", "rubric_version",
            "labeled_by", "adjudicated_by", "ready_after_day", "provenance", "contract_version")
recs = []
for d, s in W.gold_test():
    recs.append(dict(case_id=d, layer=2, stratum=s, source_refs=[d + ".pdf"], expected="10 fields", critical_fields=W.CRITICAL,
                     rubric_version="R3", labeled_by="adjuster", adjudicated_by="Anne Kessler", ready_after_day=94,
                     provenance="claims-core", contract_version="n/a"))
for q, t in W.questions():
    r = dict(case_id=q, layer=2, stratum=t, source_refs=["claims manual"], expected="answer + citation", critical_fields=(),
             rubric_version="F1", labeled_by="Joan Mercer", adjudicated_by="Anne Kessler", ready_after_day=60,
             provenance="question set", contract_version="n/a")
    if t == "cross-document" and int(q[3:]) % 3 == 0:
        r.pop("rubric_version")
    recs.append(r)
for t, v in C.scenario_ids():
    r = dict(case_id=f"SC-{t:02d}-{v:02d}", layer=4, stratum="scenario", source_refs=["template"], expected="end state",
             critical_fields=W.CRITICAL, rubric_version="S1", labeled_by="Callum Reid", adjudicated_by="Tom Whitfield",
             ready_after_day=140, provenance="template", contract_version="claims-core 7.2")
    if t == 31:
        r["contract_version"] = "claims-core 6.x"
    recs.append(r)
missing = {}
stale = 0
for r in recs:
    for k in REQUIRED:
        if k not in r:
            missing[k] = missing.get(k, 0) + 1
    if r.get("contract_version") == "claims-core 6.x":
        stale += 1
print(f"golden-set records: {len(recs)} (201 documents, 150 questions, {len(C.scenario_ids())} scenarios)")
print(f"  schema: missing fields {missing}; stale contract version {stale} (template 31)")
out = {s: C.scenario_outcome(*s, C.BASE) for s in C.scenario_ids()}
fails = {s: o for s, o in out.items() if o != "pass"}
tri = {}
for o in fails.values():
    k = o.split(":")[0]
    tri[k] = tri.get(k, 0) + 1
causes = sorted({o.split(": ", 1)[1] for o in fails.values() if o.startswith("agent")})
print(f"weekly L4 run, day 145: {len(out)} scenarios, {len(fails)} failing")
for k, n in tri.items():
    print(f"  {k:16} {n:>3}")
print(f"  agent defects come from {len(causes)} root causes:")
for c in causes:
    print(f"    - {c}")
print(f"  not the agent's fault: {tri.get('oracle defect', 0) + tri.get('broken scenario', 0)} of {len(fails)} "
      f"({(tri.get('oracle defect', 0) + tri.get('broken scenario', 0)) / len(fails):.0%})")
mr = [(t, v) for t, v in C.scenario_ids() if t in (2, 5, 11)]
print(f"metamorphic relations (rotate scan, reorder pages, duplicate delivery): {len(mr)} paired cases, "
      f"{sum(out[s] != 'pass' for s in mr)} violations")
json.dump(dict(tri=tri, n=len(out), causes=len(causes), missing=missing), open("output/scenarios.json", "w"), indent=1)
