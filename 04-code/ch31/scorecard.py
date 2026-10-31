"""Listing 31.5: Anne Kessler's scorecard, day 156 (deterministic stand-in)."""
import _paths  # noqa: F401
from fieldkit.routing import wilson
from world import gold_scores, gold_docs, STRATA, CRITICAL, FIELDS, BUILDS

docs = dict(gold_docs())
s = {b: gold_scores(b) for b in BUILDS}
print(f"gold-heldout: {len(docs)} documents, {len(docs) * len(FIELDS):,} fields, labels by Lena Ortiz, owner Anne Kessler")
print(f"{'stratum':<22}{'docs':>5}" + "".join(f"{b:>17}" for b in BUILDS) + f"{'change':>9}")
for st in STRATA:
    ids = [d for d, t in docs.items() if t == st]
    acc = [sum(s[b][(d, f)] for d in ids for f in FIELDS) / (len(ids) * 10) for b in BUILDS]
    print(f"{st:<22}{len(ids):>5}" + "".join(f"{x:>17.1%}" for x in acc) + f"{(acc[1] - acc[0]) * 100:>+8.1f}")
for label, fl in (("all fields", FIELDS), ("critical fields", CRITICAL)):
    out = []
    for b in BUILDS:
        k = sum(s[b][(d, f)] for d in docs for f in fl); n = len(docs) * len(fl)
        out.append((k, n))
    lo, hi = wilson(*out[1])
    print(f"{label:<27}" + "".join(f"{k:>8,}/{n:,} {k / n:.1%}" for k, n in out) + f"   rc-1 interval {lo:.1%} to {hi:.1%}")
worse = [st for st in STRATA if sum(s[BUILDS[1]][(d, f)] for d, t in docs.items() if t == st for f in FIELDS)
         < sum(s[BUILDS[0]][(d, f)] for d, t in docs.items() if t == st for f in FIELDS)]
print("strata where rc-1 is worse than p7:", ", ".join(worse) or "none")
print("""
scorecard (draft bars written by Anne Kessler on day 154; the Shadow Exit gate that judges them is Chapter 39's)
  S-1 field accuracy, gold-heldout           bar 80%        rc-1 84.0%                    Anne's gate, nl-eval CI
  S-2 critical fields, gold-heldout          bar 80%        rc-1 83.9%                    Anne's gate, nl-eval CI
  S-3 agreement with keyed claims, shadow    bar 85%        88.0% (shadow_run.txt)        code vs production extract
  S-4 post-review error, audit-shadow-400    bar 1.2%       1.10% (shadow_run.txt)        Lena Ortiz adjudication
  S-5 first notices with no intake record    bar 0          9 before day 150, 0 after     Ruth Calloway reconciliation
  S-6 retention and erasure drill            bar pass       pass (memory.txt)             Priya Natarajan
  S-7 model spend per routed document        bar $0.05      see tree.txt                  gateway cost lines""")
