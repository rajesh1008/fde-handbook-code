"""The proposal that became a fact: trace SD-15 back to its origin, then repair it (deterministic stand-in)."""
from caldwell_scope import draft_v03
from scoping import STATUS, RANK, Claim, Evidence, Source

doc = draft_v03()
sd = next(c for c in doc.claims if c.key == "SD-15")
print("TRACE  SD-15 back to its origin")
for c in doc.chain(sd):
    ev = "evidence event: none" if c.evidence is None else f"evidence: {c.evidence.who}, day {c.evidence.day}"
    print(f"  day {c.source.day:>3}  {c.key:<6}{STATUS[c.status]:<32}{c.source.artifact:<22}{c.source.who}")
    print(f"           \"{c.text}\"  ({ev})")
o = doc.origin(sd)
print(f"origin: {o.key}, {STATUS[o.status]}, {o.source.who} ({o.source.party}), day {o.source.day}")
print(f"status written in v0.3: {STATUS[sd.status]} (rank {RANK[sd.status]}); "
      f"status it may carry: {STATUS[o.status]} (rank {RANK[o.status]})")
print()
# repair, day 26: the FDE asks the person who would own the requirement, in front of the deal sheet
ask = Evidence("Anne Kessler", 26, "scope working session",
               "Nothing goes to the claims core unreviewed until I have seen the curve on our documents.")
fixed = Claim("OD-4", "Auto-route threshold: who sets it, and on what evidence", "D",
              Source("Northlight FDE", "vendor", "scope v0.4", 26), "criteria", owner="Anne Kessler", due_day=90,
              evidence=ask)            # a new claim with its own origin; the old chain is kept as a note
fixed_note = "supersedes SR-03 (week-2 status report corrected the same day); origin DS-07, vendor position"
doc.claims = [fixed]
doc.register.append(__import__("caldwell_scope").register()[3])   # OD-4
print("REPAIR  day 26, asked in the scope working session")
print(f"  Anne Kessler: \"{ask.words}\"")
print(f"  SD-15 rewritten as {fixed.key}: {STATUS[fixed.status]}, owner {fixed.owner}, due day {fixed.due_day}")
print(f"  lineage note: {fixed_note}")
print(f"  findings on the rewritten claim: {len([f for f in doc.lint() if f[0] == fixed.key])}")
