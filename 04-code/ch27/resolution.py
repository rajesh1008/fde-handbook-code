"""Section 27.1: what a confidence score is and is not. Resolution and ranking power on cal-600's checked half."""
import common as C
import world as W
from fieldkit.routing import auroc, resolution

_, fit, chk = C.cal()
m = C.model()
y = [i.right for i in chk]
sig = {
    "stated confidence (verbalized)": [i.verbal for i in chk],
    "value found in the source": [float(i.ev.found_in_source) for i in chk],
    "system check passed (4 fields)": [1.0 if i.ev.system_check else 0.0 for i in chk],
    "second pass agrees": [float(i.rerun) for i in chk],
    "document quality score": [i.q for i in chk],
    "correctness model, calibrated": [m.score(i) for i in chk],
}
print(f"cal-600 checked half: {len(chk) // 10} documents, {len(chk):,} fields, {C.acc(chk):.1%} right")
print()
print(f"{'signal':34s} {'distinct values':>15s} {'AUROC':>6s}")
for k, s in sig.items():
    print(f"{k:34s} {resolution(s):15d} {auroc(s, y):6.3f}")
print()
print("AUROC: the chance that a randomly chosen right field scores above a randomly chosen wrong one (0.5 = coin flip)")
v = sig["stated confidence (verbalized)"]
print("stated confidence on the checked half:")
for val in W.VERBAL:
    r = sum(1 for s, o in zip(v, y) if s == val and o); w = sum(1 for s, o in zip(v, y) if s == val and not o)
    if r + w:
        print(f"  {val:.2f}: {r + w:5,d} fields, {r / (r + w):.1%} right")
ms = sig["correctness model, calibrated"]
hist = lambda ok: [sum(1 for s, o in zip(ms, y) if o == ok and min(19, int(s * 20)) == b) for b in range(20)]
C.dump("resolution", dict(
    verbal={str(val): [sum(1 for s, o in zip(v, y) if s == val and o), sum(1 for s, o in zip(v, y) if s == val and not o)]
            for val in W.VERBAL},
    model_right=hist(True), model_wrong=hist(False),
    auroc={k: auroc(s, y) for k, s in sig.items()}))
