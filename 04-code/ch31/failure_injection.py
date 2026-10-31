"""Listing 31.3: the rotated fax, seen in shadow, then injected into the pyramid (deterministic stand-in)."""
import _paths  # noqa: F401
from fieldkit.pyramid import caught_at, MergeGate, LAYER_NAMES
from agent import Doc, Release, Gateway, run, pyramid
from world import shadow, FIX_DAY

docs = shadow()
rot = [d for d in docs if d["rotated"]]
pre = [d for d in rot if d["day"] < FIX_DAY]
post = [d for d in rot if d["day"] >= FIX_DAY]
print(f"shadow days 142 to 149: {len(pre)} faxes arrived rotated; {sum(d['kind'] == 'first notice' for d in pre)} were "
      f"first notices, {sum(d['kind'] == 'repair estimate' for d in pre)} repair estimates")
old, gw = Release(orientation=False, legibility_gate=False), Gateway()
print("\nwhat the pre-fix build did with the first three (C01 and C06 only):")
for d in pre[:3]:
    tr, out = run(Doc(d["id"], d["day"], "fax", "T1", "IK-" + d["id"], rotated=90, narrative=False,
                      truth=dict(date_received=f"day {d['day']}", policy_number="synthetic")), old, gw)
    print(f"  {d['id']}  {tr[0][3]}  | {tr[1][3]}  | {tr[2][2]}")


def missed(system):
    if system["release"].orientation:
        g, n = Gateway(), 0
        for d in post:
            _, out = run(Doc(d["id"], d["day"], "fax", "T1", "IK-" + d["id"], rotated=180, narrative=False,
                             truth=dict(date_received="x", policy_number="x")), system["release"], g)
            n += out["kind"] == "none"
        return n
    return sum(d["kind"] == "first notice" for d in pre)


P = pyramid(missed)
runs = [("A  pre-fix build, suite as it was on day 142", dict(release=old, rotated_slice=False), False),
        ("B  pre-fix build, rotated-fax slice injected", dict(release=old, rotated_slice=True), True),
        ("C  orientation detection + CW-I-01, slice kept", dict(release=Release(), rotated_slice=True), True)]
for name, system, stop in runs:
    res = P.run(system, stop_on_fail=stop)
    gate = MergeGate("Anne Kessler").decide(res)
    print(f"\nrun {name}")
    for r in res:
        print(f"  L{r.layer} {LAYER_NAMES[r.layer]:<12}{r.verdict:<9}{r.check}: {r.detail}")
    c = caught_at(res)
    print(f"  caught at: {'L%d %s' % (c, LAYER_NAMES[c]) if c else 'nothing'}; gate: {gate['decision']}")
print(f"\nafter the merge on day {FIX_DAY}: {len(post)} rotated faxes on days 150 to 153, "
      f"{missed(dict(release=Release()))} typed none")
