"""Listing 33.1: the classification test as data, failure first (the system classified as one thing)."""
from world import M, DESIGNS, SYSTEM, CALDWELL, CALDWELL_V0, NORTHLIGHT_V0, REQUEST

print("FAILURE FIRST: the system classified as one thing")
o, why = CALDWELL_V0.classify(SYSTEM)
nobody = sum(1 for r in REQUEST if r[2] == M.BOUNDARY)
print(f"  day 74  {CALDWELL_V0.name:<15} SYS -> {o}: {why}")
print(f"          request: {len(REQUEST)} items, {nobody} that nobody at Caldwell or Northlight can supply")
o, why = NORTHLIGHT_V0.classify(SYSTEM)
print(f"  day 76  {NORTHLIGHT_V0.name:<15} SYS -> {o}: {why}")
nv = M.classify_all(NORTHLIGHT_V0, DESIGNS[153])
left = [k.cid for k in nv if k.outcome == M.OUTSIDE and CALDWELL.classify(
    next(c for c in DESIGNS[153] if c.cid == k.cid))[0] == M.REGISTERED]
print(f"  the same one question per component on day 153: {len(left)} vendor models in core decisions left "
      f"untested ({', '.join(left)})")
print()
print("THE COMPONENT TEST under", CALDWELL.name)
prev = None
for day in (82, 132, 153):
    cl = M.classify_all(CALDWELL, DESIGNS[day])
    n = M.counts(cl)
    print(f"  day {day:>3}: {len(cl)} components  " + "  ".join(f"{k} {v}" for k, v in n.items())
          + f"  plan items {len(M.plan_for(cl))}  register {M.register_digest(cl)}")
    if prev:
        for cid, a, b in M.diff(prev, cl):
            print(f"           changed: {cid} {a} -> {b}")
    prev = cl
print()
print("REGISTER r3 (day 153)")
for c, k in zip(DESIGNS[153], prev):
    dc = "; ".join(c.design_choices) if c.design_choices else "-"
    print(f"  {k.cid:<8} {c.kind:<10} trained={'yes' if c.trained_on_customer_data else 'no ':<3} "
          f"core={'yes' if c.core_decision else 'no ':<3} -> {k.outcome:<26} design choices: {dc}")
print()
print("SECOND CUSTOMER: the same components under", M_H := "harbourline-e23-reading", "(stand-in reading, [VERIFY])")
from world import HARBOURLINE  # noqa: E402
hb = M.classify_all(HARBOURLINE, DESIGNS[153])
print("  " + "  ".join(f"{k} {v}" for k, v in M.counts(hb).items()) + f"  plan items {len(M.plan_for(hb))}")
for cid, a, b in M.diff(prev, hb):
    print(f"  moved: {cid} {a} -> {b}")
