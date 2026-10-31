"""Section 23.2: access control inherited from the source. Failure injection 1: permissions applied after ranking or not at all."""
import _paths  # noqa: F401
import random
import caldwell_docs as C
from fieldkit.retrieval import Index, Audience, evaluate

recs, acl, versions = C.library()
restricted = {p["pid"] for p in recs if p["acl"] != ["claims-all"]}
print(f"source: {len(recs):,} passages, {len(restricted)} restricted ({len(restricted) / len(recs):.1%}): "
      "claims-siu, claims-litigation, claims-employee, claims-mgmt")

# 1. the first export: SIU files whose permission sits on the folder, not the file, arrive with an empty ACL
r = random.Random(7); first = []
for p in recs:
    q = dict(p)
    if q["acl"] == ["claims-siu"] and r.random() < 0.2:
        q["acl"] = []
    first.append(q)
ix0 = Index(embed=C.embed); ix0.ingest(first, day=87)
print(f"day 87 first export: ingested {len(ix0.passages):,}, refused {len(ix0.refused)} "
      f"(reason: {ix0.refused[0][1]}; permission inherited from the folder, not expanded in the export)")

ix, _, _, _ = C.build(day=88)
C.apply_register(ix, C.lifecycle_register(versions))
qs = C.questions(recs)
tom = C.PEOPLE["tom"]
log_r = random.Random(11)
cur = [p for p in recs if p["latest"] and p["details"]]
log = [f"{p['topic']} {p['details'][0][0]} {p['details'][1][0]}" for p in log_r.sample(cur, 300)]
queries = [q.text for q in qs] + log
print(f"day 88 rebuilt with folder ACLs expanded: ingested {len(ix.passages):,}, refused {len(ix.refused)}")
print(f"test: {len(queries)} searches as tom.whitfield (claims-all only): Anne's 150 questions + 300 from the shadow log")
print()
print(f"{'mode':34s} {'searches leaking':>16s} {'restricted shown':>16s} {'short lists':>11s} {'empty':>5s}")
res = {}
for mode, label in (("none", "no permission filter"), ("post", "filter after ranking (top 10)"), ("pre", "filter before ranking")):
    leak = shown = short = empty = 0
    for q in queries:
        hits = ix.search(q, tom, k=10, acl=mode)
        bad = sum(p.pid in restricted for p, _ in hits)
        leak += bad > 0; shown += bad; short += len(hits) < 10; empty += len(hits) == 0
    res[mode] = (leak, shown, short, empty)
    print(f"{label:34s} {leak:16d} {shown:16d} {short:11d} {empty:5d}")
print()
for mode, label in (("post", "filter after ranking"), ("pre", "filter before ranking")):
    e = evaluate(ix, qs, C.who_for, k=10, acl=mode)
    print(f"recall at ten, Anne's set, askers' own permissions, {label}: {e['recall']:.2f}")
print()
siu = C.PEOPLE["siu"]
both = Audience((tom, siu))
q = "siu referral prior loss history late notice"
for who, label in ((siu, "SIU investigator alone"), (both, "shared review: Tom + SIU investigator")):
    hits = ix.search(q, who, k=10)
    print(f"{label:38s}: {sum(p.pid in restricted for p, _ in hits)} restricted of {len(hits)} returned")
