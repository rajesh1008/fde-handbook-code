"""Listing 50.5: Helen Marsh's classification test. Two readings of the same fourteen components, the diff, the
risk tier inside full scope and the validation plan size. Uses fieldkit.modelrisk unchanged."""
import _paths  # noqa: F401
from fieldkit import modelrisk as M
import world as W


def run(components=W.COMPONENTS):
    a = M.classify_all(W.NORTHLIGHT_READING, components)
    b = M.classify_all(W.HARBOURLINE_READING, components)
    return a, b


if __name__ == "__main__":
    a, b = run()
    by = {c.cid: c for c in W.COMPONENTS}
    print(f"{'id':<4} {'component':<38} {'Northlight day 22':<26} {'Harbourline E-23 reading':<26} tier")
    for x, y in zip(a, b):
        print(f"{x.cid:<4} {by[x.cid].name:<38} {x.outcome:<26} {y.outcome:<26} {W.tier(by[x.cid], y)}")
    for name, cl in (("Northlight day 22", a), ("Harbourline E-23 reading", b)):
        n = M.counts(cl)
        print(f"{name}: " + ", ".join(f"{k} {v}" for k, v in n.items() if v) + f"; plan items {len(M.plan_for(cl))}; "
              f"register {M.register_digest(cl)}")
    d = M.diff(a, b)
    print(f"changed by the bank's reading: {len(d)} components: " + ", ".join(x[0] for x in d))
    tiers = [W.tier(by[y.cid], y) for y in b]
    print(f"full scope tiers: high {tiers.count('high')}, medium {tiers.count('medium')}; agreed day {W.DAYS['classification_agreed']}, Helen Marsh")
