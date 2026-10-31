"""Section 23.2: the source changed and the index did not. Day 90, 14:00 Eastern: Caldwell legal moved the preservation
notice templates (12 correspondence files) from claims-all to claims-litigation. Exposure by ACL sync cadence."""
import _paths  # noqa: F401
import random
import caldwell_docs as C
from fieldkit.retrieval import acl_drift

ix, recs, acl, versions = C.build(day=88)
C.apply_register(ix, C.lifecycle_register(versions))
moved = sorted({p.doc_id for p in ix.passages.values() if p.doc_id.startswith("CM-C10-") and p.state == "current"})[:12]
source = dict(acl); source.update({d: ["claims-litigation"] for d in moved})
drift = acl_drift(ix, source)
print(f"moved files: {len(moved)} ({moved[0]} .. {moved[-1]}); drift check finds {len(drift)} files, "
      f"{sum(1 for _, k in drift if k == 'broader')} broader in the index than in the source")
# shadow log: 103 review-screen searches a day, adjusters without claims-litigation
r = random.Random(90); cur = [p for p in recs if p["latest"] and p["details"]]
corr = [p for p in cur if p["topic"] == "correspondence"]
log = []
for i in range(7 * 103):
    p = r.choice(corr) if r.random() < 0.06 else r.choice(cur)
    log.append((14 + i * 24 * 7 / (7 * 103), f"{p['topic']} {p['details'][0][0]} {p['details'][1][0]}"))
tom = C.PEOPLE["tom"]
exposed_at = [h for h, q in log if any(p.doc_id in moved for p, _ in ix.search(q, tom, k=10))]
cadences = [("weekly batch (next run day 95 02:00)", 108), ("nightly 02:00", 12), ("hourly", 1), ("ACL checked at query time", 0)]
print(f"searches in the seven days after the move: {len(log)}; would show a moved file to a non-litigation user: {len(exposed_at)}")
print()
print(f"{'ACL sync cadence':38s} {'exposure hours':>14s} {'searches exposed':>16s}")
for name, hours in cadences:
    n = sum(1 for h in exposed_at if h < 14 + hours)
    print(f"{name:38s} {hours:14d} {n:16d}")
changed = ix.sync_acl(source, day=90)
print()
print(f"nightly sync applied day 91 02:00: {len(changed)} files changed; drift after sync: {len(acl_drift(ix, source))}")
