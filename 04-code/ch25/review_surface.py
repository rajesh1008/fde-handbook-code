"""Listing 25.8: the review surface. (1) A capacity model on the shadow week's real confidence and error
flags: escalate the least confident share, the rest pass unreviewed. (2) What the reviewer sees."""
import _paths  # noqa: F401
from fieldkit.actions import render_review
from sim import documents, FIELDS

docs = [d for day in range(111, 116) for d in documents(238, day, seed=day) if d["kind"] == "fnol"]
PER_DAY = len(docs) / 5
CAP_MIN, SEC, CATCH = 2 * 120, 75, 0.92           # two adjusters, two hours a day each; 75 s; catch at rest
ranked = sorted(docs, key=lambda d: d["conf"])
errors = sum(1 for d in docs if d["error"])
print(f"proposals {len(docs)} ({PER_DAY:.0f} a day)  with an extraction error {errors}")
print("escalate  reviewed/day  load  catch  missed errors per 1,000")
for pct in range(0, 101, 10):
    k = round(len(docs) * pct / 100)
    load = (k / 5) * SEC / 60 / CAP_MIN
    catch = CATCH if load <= 0.6 else max(0.3, CATCH - 0.35 * (load - 0.6))
    esc_err = sum(1 for d in ranked[:k] if d["error"])
    missed = (errors - esc_err) + esc_err * (1 - catch)
    print(f"{pct:>6}%  {k / 5:>11.0f}  {load:>4.2f}  {catch:>5.2f}  {1000 * missed / len(docs):>8.1f}")
mism = [d for d in docs if d["said"] != d["payload"]]
hidden = [d for d in mism if d["error"]]
print(f"description disagrees with payload: {len(mism)}  of which the description looks right and the payload "
      f"is wrong: {len(hidden)}")
d = hidden[0] if hidden else mism[0]
print(f"model says: {d['narrative']}")
print("\n".join(render_review(d["payload"], d["gold"], FIELDS)))
