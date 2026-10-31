"""Listing 44.3: the same candidate pool through the old loop and the new four-exercise rubric."""
import sys
import world as W
from practice import decide, observed
print("old loop observes:", ", ".join(observed(W.OLD_LOOP)))
print("new loop observes:", ", ".join(observed(W.EXERCISES)))
print(f"\n{'cand':<5} {'old loop':<18} {'new rubric':<30} outcome")
for c, s in W.CANDIDATES.items():
    o = decide(s, W.OLD_LOOP, mode="old")
    n = decide(s)
    print(f"{c:<5} {o[0] + ' ' + str(o[1]):<18} {n[0] + ' ' + str(n[1]) + ' (' + n[2] + ')':<30} {W.OUTCOME.get(c, '')}")
print("\nfailure injection C-3 (aces the build, fails discovery):")
s = W.CANDIDATES["C-3"]
print("  scores:", " ".join(f"{W.SHORT[c]}={s[c]}" for c in W.COMPETENCIES))
print("  old loop:", decide(s, W.OLD_LOOP, mode="old"))
print("  new rubric without floors:", decide(s, floors={}))
print("  new rubric:", decide(s))
print("\nJonah Webb's month-4 packet re-read under the new rubric:")
print("  old loop:", decide(W.JONAH_M4, W.OLD_LOOP, mode="old"))
print("  new rubric:", decide(W.JONAH_M4))
offers = [c for c, s in W.CANDIDATES.items() if decide(s)[0] == "hire"]
print(f"\noffers: {len(offers)} of {len(W.CANDIDATES)} ({', '.join(offers)}); accepted: "
      f"{sum('accepted' in W.OUTCOME.get(c, '') for c in offers)}")
