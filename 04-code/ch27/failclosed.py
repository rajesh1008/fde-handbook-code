"""Sections 27.5 and 27.6: fail closed, and evidence is not probability (audit-400)."""
from collections import Counter
import common as C
import world as W
from fieldkit.routing import gate

aud = W.make("audit-400", 400)
m, th = C.model(), C.thresholds()
print("evidence gates on audit-400 fields (checked before any score is read):")
print(f"{'reason':22s} {'fields':>6s} {'documents':>9s} {'score >= proceed':>16s} {'of those wrong':>14s}")
rows = {}
for reason in ("budget exhausted", "conflicting sources", "no evidence"):
    its = [i for i in aud if gate(i.ev) == reason]
    hi = [i for i in its if m.score(i) >= th.proceed]
    rows[reason] = [len(its), len({i.doc for i in its}), len(hi), sum(not i.right for i in hi)]
    print(f"{reason:22s} {len(its):6d} {len({i.doc for i in its}):9d} {len(hi):16d} {sum(not i.right for i in hi):14d}")
print()
with_g = [f for d in C.route(aud) for f in d["fields"]]
no_g = [f for d in C.route(aud, gates=False) for f in d["fields"]]
esc = lambda F: sum(1 for f in F if f["band"] == "proceed" and not f["item"].right)
print("the same router with the evidence folded into the score only (gates off):")
print(f"  wrong fields that proceed unreviewed: gates on {esc(with_g)}, gates off {esc(no_g)}")
print(f"  post-review error: gates on {sum(not f['final'] for f in with_g) / len(with_g):.2%}, "
      f"gates off {sum(not f['final'] for f in no_g) / len(no_g):.2%}")
ex = next(i for i in aud if gate(i.ev) == "conflicting sources" and m.score(i) >= th.proceed)
print()
print("one field, as the review screen shows it:")
print(f"  {ex.doc} {ex.field}: calibrated score {m.score(ex):.3f} (proceed band), first notice and attached email"
      f" disagree -> escalate, reason 'conflicting sources'; value {'right' if ex.right else 'wrong'} on audit")
C.dump("failclosed", dict(rows=rows, escaped_on=esc(with_g), escaped_off=esc(no_g)))
