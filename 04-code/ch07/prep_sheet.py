"""Listing 7.3: the interview-prep generator. Lint the bank, then build the prep sheet for one audience inside a
time budget: the rapid round first, then the rest by weight (claim status of the expected answer x impact)."""
import sys
import caldwell_bank as cb
from collections import Counter

b = cb.build()
aud = sys.argv[1] if len(sys.argv) > 1 else "data owner"
mins = float(sys.argv[2]) if len(sys.argv) > 2 else 60
lint = b.lint()
print(f"LINT  {len(b.questions)} questions: {sum(1 for _,k,_ in lint if k=='error')} errors, "
      f"{sum(1 for _,k,_ in lint if k=='warning')} warnings")
for m, n in Counter(m.split(':')[0] if 'vendor' in m else 'expected answer came from a non-owner' for _, k, m in lint if k == 'warning').items():
    print(f"  warning x{n}: {m}")
asked, dropped = b.prep(aud, mins)
print(f"\nPREP SHEET  {aud}, {mins:.0f} minutes, {len(asked)} questions planned "
      f"({sum(q.minutes for q in asked):.1f} min), {len(dropped)} dropped")
for i, q in enumerate(asked, 1):
    if i <= 3 or q.qid in ("R11", "Q34", "Q14"):
        print(f"{i:2d}. {q.qid} [{q.category}] {q.text}")
        print(f"      why: {q.why}")
        print(f"      expect: {q.expected}  ({q.status}, from {q.expected_from})")
        print(f"      listen for: {'; '.join(q.edge_cases)}")
        print(f"      if different, changes: {q.changes}")
    elif i == 4:
        print("    ...")
for q in dropped:
    print(f"  dropped: {q.qid} weight {q.weight():.1f} {q.text}")
