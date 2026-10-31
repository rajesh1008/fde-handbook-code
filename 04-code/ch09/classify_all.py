"""Listing 9.1: run the decision tree over the three customers' pipelines and print the split."""
import _path  # noqa: F401
from fieldkit.autonomy import CLASSES, SHORT, split, share, no_model_share, table
from pipelines import CUSTOMERS, CALDWELL

print("CALDWELL MUTUAL  claims intake, 12 steps")
print(table(CALDWELL))
print()
print(f"{'customer':<18} {'steps':>5} {'det':>4} {'rules':>5} {'small':>5} {'front':>5} {'det %':>6} {'no model %':>10}")
tot = {c: 0 for c in CLASSES}; n = 0
for name, steps in CUSTOMERS.items():
    sp = split(steps); n += len(steps)
    for c in CLASSES: tot[c] += sp[c]
    print(f"{name:<18} {len(steps):>5} " + " ".join(f"{sp[c]:>{w}}" for c, w in zip(CLASSES, (4, 5, 5, 5)))
          + f" {share(steps):>6.0%} {no_model_share(steps):>10.0%}")
print(f"{'all three':<18} {n:>5} " + " ".join(f"{tot[c]:>{w}}" for c, w in zip(CLASSES, (4, 5, 5, 5)))
      + f" {tot[CLASSES[0]]/n:>6.0%} {(tot[CLASSES[0]]+tot[CLASSES[1]])/n:>10.0%}")
