"""Try It Yourself. Usage: python tryit.py a|b|c"""
import sys, dataclasses
import _paths  # noqa: F401
import world as W
from fieldkit.hiring import Loop, Round, Probe, lint_loop, five_moves, MOVES, calibrate

p = sys.argv[1]
if p == "a":  # replace the discovery exercise with a second coding round
    rounds = [r if r.id != "D1" else Round("D1", "second coding round", 60, (Probe("build"), Probe("decomposition")))
              for r in W.LOOP_V1.rounds]
    f = lint_loop(Loop("v1 with D1 swapped for coding", rounds))
    print("\n".join(f"{x.code} {x.text}" for x in f) or "no findings"); print(f"findings: {len(f)}")
elif p == "b":  # take the boundary and proof sentences out of the strong answer
    a = W.ANSWERS["strong"].rsplit(" That stops", 1)[0]
    m = five_moves(a)
    print("  ".join(f"{k} {'yes' if m[k] else 'NO'}" for k in MOVES) + f"  -> {sum(m.values())} of 5")
elif p == "c":  # Sofia scores discovery one point high in every session
    r = [(w, s, c, min(4, v + 1) if (w == "Sofia Brennan" and c == "discovery") else v) for w, s, c, v in W.calibration("after")]
    for who, (off, exact, n) in calibrate([x for x in r if x[2] == "discovery"]).items():
        print(f"discovery only: {who:<14} offset {off:+.2f} equal to median {exact:.0%}{'  DRIFT' if abs(off) >= 0.5 else ''}")
