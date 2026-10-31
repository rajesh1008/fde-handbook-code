"""Listing 33.9: the review decision, its conditions, and gate status per customer."""
from world import M, TIMELINE

print("Caldwell model-risk review, engagement days")
for d, t in TIMELINE:
    print(f"  day {d:>3}  {t}")
print()
cits = [0] * 58 + [1, 1]   # Tom Whitfield's day-146 audit of 60 summaries: wrong citations per summary
print(f"citation audit (Tom Whitfield, day 146): 60 summaries, 0 uncited statements, "
      f"{sum(cits)} wrong citations (superseded manual section)")
print()
conds = [M.Condition("R1", "C06 stays on c06-p4 until c06-ft1 completes its own full validation", "Callum Reid", 190,
                     "Owen Pritchard signs the ten plan items for C06-ft1"),
         M.Condition("R2", "the first monthly monitoring report is produced by Caldwell's team with no Northlight "
                     "involvement", "Anne Kessler", 190, "report M1 to M6 run as Caldwell identities and read by Anne")]
print("decision, day 153: passed with two conditions (Catherine Doyle, Head of Model Risk)")
for c in conds:
    print(f"  {c.cid} {c.text}; owner {c.owner}; due day {c.due_day}; status {c.status(153)}")
    print(f"     closes when: {c.closes_when}")
