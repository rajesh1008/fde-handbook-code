"""Paired comparison on Anne's set and the per-kind table (where each arm loses)."""
import _paths  # noqa: F401
import lab
import models as M
from fieldkit.finetune import paired_compare, per_class

S = lab.sets(); m = lab.ft1(); docs = S["anne"]
truth = [d.truth for d in docs]
ft, ftg, fr = m.predict(docs), lab.guarded(m, docs), M.frontier(docs)
for name, a in (("c06-ft1", ft), ("c06-ft1 + guard", ftg)):
    c = paired_compare(a, fr, truth, right=lab.right)
    lo, hi = c.ci("a"); flo, fhi = c.ci("b")
    print(f"{name} vs c06-p4 on Anne's set (n={c.n})")
    print(f"  {name}: {c.right_a} right ({100*c.right_a/c.n:.1f}%, 95% CI {100*lo:.1f} to {100*hi:.1f})")
    print(f"  c06-p4:  {c.right_b} right ({100*c.right_b/c.n:.1f}%, 95% CI {100*flo:.1f} to {100*fhi:.1f})")
    print(f"  both right {c.both_right}, only {name} right {c.a_only}, only c06-p4 right {c.b_only}, both wrong {c.both_wrong}")
    print(f"  exact McNemar p = {c.p_value:.2g}: {c.verdict()}")
print()
kinds = [d.kind for d in docs]
pa, pb = per_class(ftg, truth, kinds, lab.right), per_class(fr, truth, kinds, lab.right)
label = {"T1": "T1 Caldwell form", "T2": "T2 agency form", "T2p": "T2 on Caldwell template", "T3": "T3 letter/email",
         "T4": "T4 estimate", "T4s": "T4 supplement", "medical": "none: medical", "police": "none: police/fire",
         "corr": "none: correspondence", "attorney": "none: attorney letter"}
print(f"{'kind (true class)':<28}{'n':>4}  {'ft1+guard':>9}  {'c06-p4':>7}")
for k in label:
    r1, n = pa[k]; r2, _ = pb[k]
    print(f"{label[k]:<28}{n:>4}  {100*r1/n:8.1f}%  {100*r2/n:6.1f}%")
ins = [i for i, t in enumerate(truth) if t != "none"]
print(f"in-scope documents held by the guard: {sum(ftg[i].startswith('hold') for i in ins)}")
