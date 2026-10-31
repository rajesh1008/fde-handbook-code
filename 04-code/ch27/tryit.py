"""Try It for Chapter 27. a: calibration set size. b: a 99% target. c: the gates switched off."""
import sys
import common as C
import world as W
from fieldkit.routing import CorrectnessModel, set_thresholds

part = sys.argv[1] if len(sys.argv) > 1 else "a"
_, fit, chk = C.cal()
aud = W.make("audit-400", 400)
share = lambda R: sum(d["band"] == "proceed" for d in R) / len(R)
post = lambda R: sum(not f["final"] for d in R for f in d["fields"]) / sum(len(d["fields"]) for d in R)
if part == "a":
    for k in (50, 100, 300):
        f = [i for i in fit if int(i.doc[-4:]) // 2 < k]
        c = [i for i in chk if int(i.doc[-4:]) // 2 < k]
        m = CorrectnessModel(lambda it: it.features()).fit(f, [i.right for i in f])
        th = set_thresholds([m.score(i) for i in f], [i.right for i in f], [m.score(i) for i in c], [i.right for i in c])
        R = C.route(aud, m, th)
        print(f"calibration set {2 * k:3d} documents: proceed {th.proceed:.3f}, lower bound {th.lower_bound:.1%} "
              f"on {th.checked_n:,} fields; audit-400 proceed {share(R):.1%}, post-review error {post(R):.2%}")
elif part == "b":
    for target in (0.98, 0.99):
        th = C.thresholds(target)
        R = C.route(aud, C.model(), th)
        print(f"target {target:.0%}: proceed threshold {th.proceed:.3f}, audit-400 proceed {share(R):.1%} of documents, "
              f"post-review error {post(R):.2%}")
else:
    for g in (True, False):
        R = C.route(aud, gates=g)
        esc = sum(1 for d in R for f in d["fields"] if f["band"] == "proceed" and not f["item"].right)
        print(f"gates {'on ' if g else 'off'}: proceed {share(R):.1%}, wrong fields proceeding unreviewed {esc}, "
              f"post-review error {post(R):.2%}")
