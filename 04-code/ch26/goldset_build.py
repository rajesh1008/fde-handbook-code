"""Listing 26.2: building gold-set-300 with Anne Kessler's adjusters: the draw, the 14-day rule, the hours."""
import json
from collections import Counter
from world import gold_docs, PLAN, POP, u
from fieldkit.evals import GoldValuePolicy

docs = gold_docs()
print("gold-set-300: drawn by Natarajan (claims system query), plan signed by Kessler on day 59")
for s in sorted(PLAN, key=lambda s: -POP[s]):
    print(f"  {s:<22} drawn {PLAN[s][0]:3d}  weight {PLAN[s][1]:.2f}")
split = Counter(d[3] for d in docs)
print(f"  split: {split['dev']} development (rubric and judge tuning), {split['test']} held out (reported numbers)")

# coded values (policy number, cause-of-loss code) are checked against the claims record; Chapter 7's rule
ready, held = GoldValuePolicy(14).split(docs, lambda d: d[4])
changed = [(d[0], f) for d in held for f in ("policy_number", "loss_type") if u(d[0], f, "late-fix") < .099]
print(f"\n14-day rule on the claims record behind each document (age at labeling, days 66 to 83)")
print(f"  ready at labeling: {len(ready)}   held until the record is 14 days old: {len(held)}")
print(f"  coded values that changed while held: {len(changed)} of {2 * len(held)} "
      f"({len(changed) / (2 * len(held)):.1%}); each would have been a wrong gold value")

# expert time: minutes are the stand-in plan Kessler approved; the booked column is the lab's count of the work
MIN_LABEL, MIN_ADJ = 6, 4
calib = 40
overlap = sum(1 for d in docs if int(d[0][1:]) % 5 == 0)
dis = json.load(open("output/annotation.json"))["disagreements"] if __import__("os").path.exists(
    "output/annotation.json") else 0
rows = [("calibration, two rounds (40 docs, 3 people)", "all three", calib * 2 * 3 * MIN_LABEL),
        ("labeling, one adjuster per document (300)", "Whitfield, Ortiz", 300 * MIN_LABEL),
        ("second label on every fifth document (60)", "the other adjuster", overlap * MIN_LABEL),
        (f"adjudication of {dis} disagreements", "Kessler", dis * MIN_ADJ),
        ("two rubric meetings (60 min, 3 people)", "all three", 2 * 60 * 3)]
print("\nexpert hours (stand-in plan: 6 min to score one document's ten fields, 4 min to adjudicate one)")
tot = 0
for name, who, m in rows:
    tot += m
    print(f"  {name:<46} {who:<22} {m / 60:5.1f} h")
print(f"  {'total':<46} {'':<22} {tot / 60:5.1f} h  over three weeks, about {tot / 60 / 3 / 3:.1f} h per person per week")
json.dump(dict(ready=len(ready), held=len(held), changed=len(changed), rows=[(n, m / 60) for n, _, m in rows],
               split=dict(split)), open("output/goldset_build.json", "w"), indent=1)
