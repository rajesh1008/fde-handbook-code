"""The absent-class guard: familiarity plus the legal mail coordinator's registry rule."""
import _paths  # noqa: F401
from collections import Counter
import numpy as np
import lab
from fieldkit.finetune import familiarity

S = lab.sets(); m = lab.ft1(); vocab = set(m.vocab)
print(f"familiarity = share of a document's words seen in training; hold below {lab.THRESHOLD}")
for name, docs in (("history test split", S["test"]), ("Anne's set, in scope", [d for d in S["anne"] if d.truth != "none"]),
                   ("Anne's set, out of scope", [d for d in S["anne"] if d.truth == "none"]), ("legal-60", S["legal"])):
    f = np.array([familiarity(d.tokens, vocab) for d in docs])
    print(f"  {name:<26} n={len(docs):<5} min {f.min():.3f}  p5 {np.percentile(f, 5):.3f}  median {np.median(f):.3f}"
          f"  below threshold {int((f < lab.THRESHOLD).sum())}")
import json
groups = {"Anne's set, in scope": [d for d in S["anne"] if d.truth != "none"],
          "Anne's set, out of scope": [d for d in S["anne"] if d.truth == "none"], "legal-60": S["legal"]}
json.dump({"threshold": lab.THRESHOLD, "groups": {k: [round(familiarity(d.tokens, vocab), 4) for d in v]
           for k, v in groups.items()}}, open("output/familiarity.json", "w"))
g = lab.guard(m)
print()
for name, docs in (("Anne's set", S["anne"]), ("legal-60", S["legal"]), ("history test split", S["test"])):
    holds = [(d, g.check(d.tokens)) for d in docs]
    c = Counter((d.kind, x.reason) for d, x in holds if x)
    before, after = lab.n_right(m.predict(docs), docs), lab.n_right(lab.guarded(m, docs), docs)
    print(f"{name:<20} held {sum(c.values()):>3} {dict(c)}")
    print(f"{'':<20} right (true class): c06-ft1 {before}/{len(docs)} -> with guard {after}/{len(docs)}")
