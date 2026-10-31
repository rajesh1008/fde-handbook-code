"""Listing 44.2: the skill profile at month 7, month 11 and month 12, with single holders (fieldkit bus_factor)."""
import world as W
from practice import profile_flags
team7 = ["lead FDE", "Callum Reid", "Sofia Brennan", "Jonah Webb", "Maya Brooks", "Aisha Rahman"]
team11 = ["lead FDE", "Callum Reid", "Sofia Brennan", "Aisha Rahman"]
team12 = team11 + ["Leo Martens", "Imogen Clarke"]
print("person          " + " ".join(f"{W.SHORT[c]:>6}" for c in W.COMPETENCIES))
for p in team7 + ["Leo Martens", "Imogen Clarke"]:
    print(f"{p:<16}" + " ".join(f"{W.PROFILE[p][c]:>6}" for c in W.COMPETENCIES))
for label, team in (("month 7 (six)", team7), ("month 11 (four)", team11), ("month 12 (six)", team12)):
    print(f"\n{label}: level-3 holders per competency: " +
          ", ".join(f"{W.SHORT[c]} {sum(W.PROFILE[p][c] >= 3 for p in team)}" for c in W.COMPETENCIES))
    for f in profile_flags(team):
        print("  " + f)
