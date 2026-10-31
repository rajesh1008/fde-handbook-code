"""Try It Yourself, Chapter 33: python tryit.py a|b|c (deterministic; no model calls)."""
import sys
from dataclasses import replace
from world import M, DESIGNS, CALDWELL, HARBOURLINE, METRICS_V2, VENDOR_IDS, I

v = sys.argv[1] if len(sys.argv) > 1 else "a"
if v == "a":
    print("Try 1: route on the model's stated confidence instead of a fitted router (router v0 style).")
    comps = [replace(c, trained_on_customer_data=False, kind="prompted") if c.cid == "RT" else c for c in DESIGNS[153]]
    for name, cs in (("fitted router", DESIGNS[153]), ("stated confidence", comps)):
        cl = M.classify_all(CALDWELL, cs)
        rt = next(k for k in cl if k.cid == "RT")
        print(f"  {name:<18} RT -> {rt.outcome:<26} plan items {len(M.plan_for(cl))}")
    print("  Chapter 27: stated confidence put 14.8% errors in the proceed band (152 of 1,029); post-review error with the fitted router 0.9%")
    print("  (audit-400). One fewer validation item is not worth that.")
elif v == "b":
    print("Try 2: let Northlight's annotators label the weekly audit sample for M1.")
    m1 = METRICS_V2[0]
    m1b = replace(m1, inputs=(m1.inputs[0], I("weekly audit labels", "Northlight", "Northlight annotation team"),
                              m1.inputs[2]))
    for m in (m1, m1b):
        b = m.blockers("Caldwell", VENDOR_IDS)
        print(f"  {m.mid} computable by Caldwell alone: {'yes' if not b else 'no'}" + "".join(f"\n     - {x}" for x in b))
elif v == "c":
    print("Try 3: classify Caldwell's day-153 design under a bank policy written to OSFI E-23 (stand-in reading).")
    for fw in (CALDWELL, HARBOURLINE):
        cl = M.classify_all(fw, DESIGNS[153])
        full = [k.cid for k in cl if k.outcome == M.FULL]
        print(f"  {fw.name:<24} full scope {len(full)} ({', '.join(full)}); plan items {len(M.plan_for(cl))}")
    print("  Under the bank reading no vendor model in a material use is 'registered, not validated': it is")
    print("  validated before use, so V02, V03 and V13 become findings, not boundaries.")
