"""The second customer: Caldwell Mutual's first ninety days (Chapter 42). Usage: python caldwell.py
Live on engagement day 158 (production day 0). Routing at go-live 62.3% draft / 29.8% review / 8.0% decline-to-
draft (Chapter 27). On production day 24 two large brokers switch to a new medical-bill template; the routing mix
moves before any quality number does. The drift method that worked at Pennant (PSI on a fingerprint score) finds
nothing here, because the change is in the content, not the layout. Exhibit E (Chapter 34): post-review document
errors, breach at 7 or more in the 310 sampled each month, scored by Anne Kessler's team."""
import random
import _paths  # noqa: F401
from fieldkit.synthetic import psi
from fieldkit.evals import wilson


def week(w):
    r = random.Random(4200 + w)
    n = 1400
    shift = w >= 4                                    # production day 24 falls in week 4 (days 22-28)
    p_draft, p_review = (0.623, 0.298) if not shift else (0.57, 0.34)
    routes, fp = [], []
    for _ in range(n):
        u = r.random()
        routes.append("draft" if u < p_draft else "review" if u < p_draft + p_review else "decline")
        fp.append(f"b{min(19, int(min(0.99, r.gauss(0.94, 0.02)) / 0.05))}")
    return routes, fp


base_r, base_fp = week(0)
print("CALDWELL  first ninety days  production day 0 = engagement day 158  (deterministic stand-in)")
print("week  draft   review  decline  PSI routing  PSI fingerprint")
first = None
for w in range(1, 7):
    rt, fp = week(w)
    sh = {k: rt.count(k) / len(rt) for k in ("draft", "review", "decline")}
    pr, pf = psi(base_r, rt), psi(base_fp, fp)
    flag = "  <- routing alarm (>= 0.01 on a three-way mix)" if pr >= 0.01 and first is None else ""
    if flag:
        first = w
    print(f"{w:>4}  {sh['draft']:6.1%}  {sh['review']:6.1%}  {sh['decline']:6.1%}   {pr:9.4f}   {pf:9.4f}{flag}")
print(f"routing alarm in week {first}; fingerprint PSI flat: the template changed content, not layout")
for n, wrong, day in ((200, 3, 27), (600, 4, 30)):
    lo, hi = wilson(wrong, n)
    verdict = "inconclusive: the sample cannot show the line" if hi > 0.025 else "threshold kept"
    print(f"re-check day {day}: {n - wrong}/{n} drafted claims correct; wrong-rate upper bound {hi:.2%} "
          f"(line 2.5%): {verdict}")
print("re-check signed by Anne Kessler, day 30")
print("Exhibit E (post-review document errors in 310 sampled; breach at 7 or more):")
for month, errs in (("month 1", 2), ("month 2", 4), ("month 3", 3)):
    print(f"  {month}: {errs} errors  {'BREACH' if errs >= 7 else 'within'}  scored by Anne Kessler's team")
print("Live Stable: engagement day 248 (production day 90), hand-over readiness 0.90 (Chapter 41)")
