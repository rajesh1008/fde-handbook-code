"""Score the discovery exercise from its event log. Usage: python discovery.py c214|c231"""
import sys
import _paths  # noqa: F401
import world as W
from fieldkit.hiring import discovery_score, ANCHORS

r = discovery_score(W.TRANSCRIPTS[sys.argv[1]], W.FACTS)
print(f"candidate {sys.argv[1]}: facts surfaced {r['facts']} of {r['of']}, exceptions {r['exceptions']} of {r['of_exc']}")
print(f"first solution statement at minute {r['first_solution']}, questions before it {r['questions_before']}, confirm-backs {r['confirms']}")
print(f"anchor {r['anchor']}: {ANCHORS['discovery'][r['anchor']]}")
missed = [f for f in W.FACTS if f not in {e[2] for e in W.TRANSCRIPTS[sys.argv[1]] if e[2]}]
print("missed: " + " ".join(missed) + f"  (exceptions missed: {' '.join(f for f in missed if W.FACTS[f]) or 'none'})")
