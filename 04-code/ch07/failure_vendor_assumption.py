"""Listing 7.2: the failure injection. Design v0 was written on day 20 from the bank's expected answers, as if
every expected answer were a fact. Six of them were vendor positions. Run the date-received check v0 was built
around against synthetic records shaped like Caldwell's, then hold v0 against what Ruth Calloway said on day 24."""
from collections import Counter
import caldwell_bank as cb
from caldwell_records import first_notices

b = cb.build()
v0 = [q for q in cb.DATA_OWNER]
print("DESIGN v0 (day 20): built on 40 expected answers, statuses not checked")
print(f"  expected answers that were vendor positions: {sum(q.status == 'vendor position' for q in v0)}")
recs = first_notices()
wrong = [r for r in recs if r["received_at"] != r["notice_received_dt"]]
print(f"\nCHECK  date received = received_at (R11 expected answer), {len(recs)} synthetic first notices")
print(f"  ingest date differs from notice_received_dt: {len(wrong)} of {len(recs)} ({100*len(wrong)/len(recs):.0f}%)")
by = Counter(r["path"] for r in recs); bad = Counter(r["path"] for r in wrong)
late = [((r["received_at"] - r["notice_received_dt"]).days) for r in wrong]
for p in sorted(by, key=lambda p: -bad[p] / by[p]):
    if bad[p]:
        print(f"    {p}  {bad[p]:3d} of {by[p]:3d} wrong")
print(f"  worst lag: {max(late)} days; documents whose clock would start late by 3+ days: {sum(d >= 3 for d in late)}")
print("\nDAY 24  Ruth Calloway, claims data manager, answers the same 40 questions")
r = b.reconcile()
for status, (asked, contra) in sorted(r.by_status.items(), key=lambda kv: -kv[1][1] / kv[1][0]):
    print(f"  {status:38s} {contra} of {asked:2d} contradicted ({100*contra/asked:.0f}%)")
vp = [(q, a) for q, a in r.design_changes if q.status == "vendor position"]
print("\nv0 design elements built on a contradicted vendor position:")
for q, a in vp:
    print(f"  {q.qid}  {q.changes}: expected '{q.expected}'")
    print(f"       Ruth: {a.text}")
