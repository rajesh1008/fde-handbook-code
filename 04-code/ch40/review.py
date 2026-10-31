"""Daniel Reyes's architects review the pack design, day 184: questions and how each closed."""
from collections import Counter
Q = [
    ("Q1", "Can Caldwell produce a pack with no Northlight person or credential?", "condition", "A2: demonstrate under cw-mrm-monitor"),
    ("Q2", "Where is the chain head anchored, and who can rewrite it?", "condition", "A1: daily head to Caldwell's log account, object lock"),
    ("Q3", "What proves the prompt text sent is the text named?", "evidence", "sent_sha checked at the gateway; mismatch blocks the call"),
    ("Q4", "What happens when the provider changes the model behind the pin?", "evidence", "M5 pin age; weekly fixed-input fingerprint in P3"),
    ("Q5", "Does the pack copy claim data out of claims-core?", "evidence", "fields only, by reference to the claim file; CA-07 retention"),
    ("Q6", "How long does a pack stay reconstructable?", "evidence", "run records 2,555 days; traces 30 days are not relied on"),
    ("Q7", "What about the decisions made before day 180?", "evidence", "backfill from parameter-store history, marked reconstructed"),
    ("Q8", "Can an adjuster's override be told from an acceptance?", "evidence", "review record outcome; claims-core audit table cross-check"),
    ("Q9", "Is a re-run of the model part of the proof?", "evidence", "no; replay of recorded inputs and outputs, rerun is advisory"),
    ("Q10", "Who is told when a pack fails to build?", "evidence", "P1 below 100% pages Caldwell model risk and the FDE"),
    ("Q11", "Can the parameter store still be edited by hand?", "evidence", "console write removed; deploy check refuses an override"),
    ("Q12", "Should the pack also cover the claims-core rules engine?", "out of scope", "FNOL-2 rules are Caldwell's system of record"),
]
print("ARCHITECTS' REVIEW, DAY 184 (Priya Natarajan and three of Daniel Reyes's architects)")
for q, text, outcome, how in Q:
    print(f"  {q:<4} {outcome:<13} {text}  [{how}]")
c = Counter(o for _, _, o, _ in Q)
print(f"  answered by evidence {c['evidence']}, conditions {c['condition']}, out of scope {c['out of scope']}; decision: approved with conditions A1, A2 (due day 195, met day 193)")
