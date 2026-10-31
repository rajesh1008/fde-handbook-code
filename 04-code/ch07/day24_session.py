"""Listing 7.6: the record of the hour. Reconcile Ruth Calloway's 40 answers against the bank's expected answers."""
import caldwell_bank as cb

b = cb.build(); r = b.reconcile()
print(f"SESSION  {cb.WHO}, data owner, day {cb.DAY}: {r.answered} of {len(b.for_audience('data owner'))} answered "
      f"in {r.elapsed:.0f} minutes")
for k in ("confirmed", "refined", "redirected", "contradicted"):
    print(f"  {k:13s} {r.by_outcome.get(k, 0):2d}")
print(f"  edge cases listed {r.edge_cases_listed}, heard in the answers {r.edge_cases_seen} (each becomes a test case)")
print(f"\nDESIGN CHANGES ({len(r.design_changes)})")
for q, a in r.design_changes:
    print(f"  {q.qid}  {cb.DESIGN[q.qid]}")
print("\nFOLLOW-UPS (answered by naming another owner)")
for q, a in r.follow_ups:
    print(f"  {q.qid} -> {a.redirect_to}: {q.text}")
print(f"\nANSWERS FROM SOMEONE WHO DOES NOT OWN THEM: {len(r.wrong_person)}")
