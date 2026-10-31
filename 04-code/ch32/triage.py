"""What the questionnaire asks: themes, design-changing items and the evidence each theme needs."""
from collections import Counter, defaultdict
import _paths  # noqa: F401
from world import ANSWERS, EVIDENCE, SIZES

rows = defaultdict(lambda: [0, 0, Counter(), Counter()])
for a in ANSWERS:
    r = rows[a.theme]; r[0] += 1; r[1] += a.design_changing; r[3][a.claim] += 1
    for e in a.evidence:
        r[2][EVIDENCE[e].kind] += 1
print(f"{'theme':<28}{'asked':>6}{'design':>8}  evidence kinds cited")
order = sorted(rows, key=lambda t: -rows[t][0])
for t in order:
    n, d, k, c = rows[t]
    print(f"{t:<28}{n:>6}{d:>8}  " + ", ".join(f"{x} {m}" for x, m in k.most_common(3)))
print(f"{'total':<28}{len(ANSWERS):>6}{sum(a.design_changing for a in ANSWERS):>8}")
claims = Counter(a.claim for a in ANSWERS)
print("claims: " + ", ".join(f"{k} {claims[k]}" for k in ("measured", "configured", "documented", "assumed")))
print()
print("questionnaire size at three customers (asked, applicable, design-changing)")
for name, asked, app, d in SIZES:
    print(f"  {name:<10}{asked:>5}{app:>6}{d:>5}   applicable {100 * app / asked:.0f}%")
