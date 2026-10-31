"""How many labels: the learning curve on Anne's set, against the prompted arm's 796 of 900."""
import _paths  # noqa: F401
import lab
import models as M
from fieldkit.finetune import learning_crossover

S = lab.sets(); docs = S["anne"]
target = lab.n_right(M.frontier(docs), docs) / len(docs)
sizes = [100, 200, 400, 800, 1600, 3200, 4800]
accs = []
print(f"{'clerk labels':>12}  {'c06-ft (no guard)':>18}  {'with guard':>11}")
for n in sizes:
    mm = M.SmallModel().fit(S["train"][:n])
    a = lab.n_right(mm.predict(docs), docs); g = lab.n_right(lab.guarded(mm, docs), docs)
    accs.append(a / len(docs))
    print(f"{n:>12}  {lab.pct(a, len(docs)):>18}  {lab.pct(g, len(docs)):>11}")
x = learning_crossover(sizes, accs, target)
print(f"c06-p4 reference: {100*target:.1f}%; fine-tuned arm first matches it at {x} labels")
print("labels here are the clerks' existing type codes: zero new labeling hours; Anne's set is never trained on")
