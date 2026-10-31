"""Try It Yourself. a: remove a subclass from training; b: your volume; c: a different absent class."""
import _paths  # noqa: F401
import sys
from collections import Counter
import lab
import models as M

S = lab.sets(); which = sys.argv[1] if len(sys.argv) > 1 else "a"
if which == "a":
    tr = [d for d in S["train"] if d.kind != "T2p"]
    mm = M.SmallModel().fit(tr)
    t2p = [d for d in S["anne"] if d.kind == "T2p"]
    held = sum(p.startswith("hold") for p in lab.guarded(mm, t2p))
    print(f"T2p removed from training: Anne's T2p docs answered {dict(Counter(mm.predict(t2p)))}, held by guard {held}")
    print("familiar words, unfamiliar convention: the familiarity check cannot see it; only a labeled slice can")
elif which == "b":
    from fieldkit.finetune import ServingOption, crossover, cost_per_doc
    vol = float(sys.argv[2]) if len(sys.argv) > 2 else 60000
    own = (12 * 46.0 + 10 * 95.0 + 2.10) / 3   # change these to your customer's hours and rates
    a = ServingOption("prompted", cost_per_doc(3600, 25, 3.00, 15.00))
    b = ServingOption("fine-tuned A", cost_per_doc(1350, 2, 0.20, 0.20), 0, own)
    print(f"volume {vol:,.0f}/month: prompted ${a.monthly(vol):,.0f}, fine-tuned ${b.monthly(vol):,.0f};"
          f" crossover {crossover(a, b):,.0f}")
else:
    tr = [d for d in S["train"] if d.kind != "police"]
    mm = M.SmallModel().fit(tr)
    pol = [d for d in S["anne"] if d.kind == "police"]
    g = lab.guarded(mm, pol)
    print(f"police reports removed from training: answers {dict(Counter(mm.predict(pol)))};"
          f" held by guard {sum(p.startswith('hold') for p in g)} of {len(pol)}")
