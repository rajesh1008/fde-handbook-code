"""An instruction change: Joan Mercer's day-146 ruling makes repair-estimate supplements 'none'."""
import _paths  # noqa: F401
import lab
import models as M
import world as W

S = lab.sets(); test = W.supplements(80)
pool = [d for d in S["train"] if d.kind == "T4s"] + W.supplements(200, seed=3005)
anne_new = [d.truth if d.kind != "T4s" else "none" for d in S["anne"]]
M.NEW_RULE["active"] = True
fr = M.frontier(test); fa = M.frontier(S["anne"])
M.NEW_RULE["active"] = False
print("c06-p4: one line added to the prompt (supplement on an existing claim = none), same day, $0 training")
print(f"  supplement test set (80): {sum(p == 'none' for p in fr)} filed as none;"
      f" Anne's set under the new rule: {sum(p == t for p, t in zip(fa, anne_new))}/900")
print("c06-ft: retrain with k relabeled supplement examples (history supplements relabeled first)")
print(f"{'k':>5}  {'supplements filed none':>23}  {'Anne new rule':>14}")
hist_supp = {d.id for d in S["train"] if d.kind == "T4s"}
for k in (0, 25, 50, 100, 200):
    chosen = {d.id for d in pool[:k]}
    train = [d for d in S["train"]]
    labels = ["none" if d.id in chosen else d.label for d in train]
    extra = [d for d in pool[:k] if d.id not in hist_supp]
    mm = M.SmallModel().fit(train + extra, labels + ["none"] * len(extra))
    p = mm.predict(test)
    pa = lab.guarded(mm, S["anne"])
    print(f"{k:>5}  {sum(x == 'none' for x in p):>17} / 80  {sum(lab.right(a, t) for a, t in zip(pa, anne_new)):>10} / 900")
print("each retrain: about 41 minutes and $2.10 of compute, then revalidation on Anne's set before it can ship")
