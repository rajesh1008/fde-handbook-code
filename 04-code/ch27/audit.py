"""Section 27.7: post-review error as the number that matters. audit-400, routed review days 136 to 139,
audited field by field by Anne Kessler's team on day 140."""
from collections import Counter, defaultdict
import common as C
import world as W
from fieldkit.routing import post_review_error

aud = W.make("audit-400", 400)
R = C.route(aud)
n = len(R)
bc = Counter(d["band"] for d in R)
rc = Counter(d["reason"] for d in R)
print(f"audit-400: {n} documents, {len(aud):,} fields, routed by router v1 (thresholds signed day 132)")
for b in ("proceed", "review", "escalate"):
    print(f"  {b:8s} {bc[b]:4d} documents  {bc[b] / n:6.1%}")
print("  reasons:")
for k, v in rc.most_common():
    print(f"    {k:44s} {v:4d}")
F = [f for d in R for f in d["fields"]]
pre = sum(not f["item"].right for f in F)
rate, lo, hi = post_review_error([f["final"] for f in F])
wrong = sum(not f["final"] for f in F)
print()
print(f"fields wrong as extracted: {pre} of {len(F):,} ({pre / len(F):.1%})")
print(f"fields wrong after routing and review: {wrong} of {len(F):,}: post-review error {rate:.1%} "
      f"(95% interval {lo:.1%} to {hi:.1%})")
print(f"{'final band':12s} {'fields':>6s} {'wrong after':>11s} {'rate':>6s}")
by = defaultdict(list)
for f in F:
    k = f["band"] if f["band"] != "review" else ("review, suggested" if f["shown"] else "review, keyed")
    by[k].append(f["final"])
rows = {}
for k in ("proceed", "review, suggested", "review, keyed", "escalate"):
    v = by[k]
    rows[k] = [len(v), sum(not x for x in v)]
    print(f"{k:18s} {len(v):6,d} {sum(not x for x in v):6d} {sum(not x for x in v) / max(1, len(v)):6.1%}")
crit = sum(not f["final"] for f in F if f["item"].field in W.CRITICAL)
print(f"critical fields wrong after review: {crit}")
print()
print("by stratum (share of documents):")
st = defaultdict(Counter)
for d in R:
    st[d["stratum"]][d["band"]] += 1
strata = {}
for k in W.STRATA:
    c = st[k]; t = sum(c.values())
    strata[k] = [c["proceed"] / t, c["review"] / t, c["escalate"] / t, t]
    print(f"  {k:20s} {t:3d}  proceed {c['proceed'] / t:5.0%}  review {c['review'] / t:5.0%}  escalate {c['escalate'] / t:5.0%}")
print()
everything = [W.review_outcome(f["item"], "review", True) for f in F]
e_rate = sum(not x for x in everything) / len(everything)
print("the alternative, a person reviews every field with the suggestion shown:")
print(f"  documents a person opens: {n} of {n} (routed: {bc['review'] + bc['escalate']} of {n})")
print(f"  post-review error: {e_rate:.1%} ({sum(not x for x in everything)} fields)")
iso, t, *_ = C.v0()
print()
print(f"router v0 on the first real sample: proceed-band error 14.8% (failure_injection.txt); "
      f"router v1 after review: {rate:.1%}")
C.dump("audit", dict(bands={b: bc[b] / n for b in ("proceed", "review", "escalate")}, reasons=dict(rc),
                     post=dict(rate=rate, lo=lo, hi=hi, wrong=wrong, n=len(F), pre=pre), rows=rows, strata=strata,
                     everything=e_rate))
