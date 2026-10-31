"""Section 27.8: re-calibration after drift. Weekly proceed-band audits (120 documents each) in the shadow run;
on day 143 one broker's first-notice email template moves the date reported into the loss-date box."""
import common as C
import world as W
from fieldkit.routing import CorrectnessModel, DriftMonitor, set_thresholds, wilson

TEMPLATE = dict(stratum="first notice, email", share=0.55, wrong=0.9)
m1, th1 = C.model(), C.thresholds()
_, fit, chk = C.cal()
base = [m1.score(i) for i in chk]
mon = DriftMonitor()
rows = []


def week(day, m, th, feats, template):
    items = W.make(f"week-{day}", 120, template=template)
    R = C.route(items, m, th)
    pb = [f["item"] for d in R for f in d["fields"] if f["band"] == "proceed"]
    wrong = sum(not i.right for i in pb)
    lo, hi = wilson(wrong, len(pb))
    psi = mon.psi(base, [m.score(i) for i in items])
    trip, why = mon.check(wrong, len(pb), base, [m.score(i) for i in items])
    t2 = [i for i in items if i.tmpl2 and i.field in W.DATE_FIELDS and not i.right]
    rows.append(dict(day=day, n=len(pb), wrong=wrong, err=wrong / max(1, len(pb)), lo=lo, hi=hi, psi=psi, trip=trip))
    print(f"day {day}: {len(pb):4d} proceed fields, {wrong:3d} wrong ({wrong / len(pb):.1%}, low {lo:.1%}), "
          f"PSI {psi:.3f} -> {'RE-CALIBRATE: ' + why if trip else why}")
    if t2:
        print(f"         new-template date fields wrong: {len(t2)}, mean score {sum(m.score(i) for i in t2) / len(t2):.3f}, "
              f"in proceed band {sum(m.score(i) >= th.proceed for i in t2)}")


print(f"router v1 (signed day 132): proceed {th1.proceed:.2f}, floor {th1.floor:.2f}; promise error at most 2%")
week(134, m1, th1, None, None)
week(141, m1, th1, None, None)
week(148, m1, th1, None, TEMPLATE)
print()
rc = W.make("recal-150", 100, template=dict(TEMPLATE, share=0.75), only="first notice, email")
print("day 150: 100 documents from the broker scored by Tom Whitfield; the intake header's form version becomes a")
print("feature for the two date fields; model refitted on cal-600 plus the new documents, thresholds re-checked")
fit2 = fit + [i for i in rc if int(i.doc[-4:]) % 2 == 0]
chk2 = chk + [i for i in rc if int(i.doc[-4:]) % 2 == 1]
m2 = CorrectnessModel(lambda it: it.features(v2=True)).fit(fit2, [i.right for i in fit2])
th2 = set_thresholds([m2.score(i) for i in fit2], [i.right for i in fit2], [m2.score(i) for i in chk2],
                     [i.right for i in chk2])
print(f"  router v1.1: proceed {th2.proceed:.2f}, floor {th2.floor:.2f}, lower bound {th2.lower_bound:.1%} "
      f"on {th2.checked_n:,} fields; signed by Anne Kessler, day 151")
week(155, m2, th2, None, TEMPLATE)
C.dump("drift", dict(rows=rows, promise=0.02))
