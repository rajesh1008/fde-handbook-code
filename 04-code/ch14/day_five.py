"""Listing 14.4, failure injection: a referral path discovered on day 19 (the fifth day on site) doubles the scope.

The fax path was invisible in the EHR interface specification, in Sam Oakley's network diagram and in Michael
Hart's room. A referral coordinator named it at the read-back. This script measures what it does to the scope and
compares three responses: absorb it into release 1, absorb it and hold the date, or carve it out with an owner.
"""
import math

import pipeline as pl
import projection as pj
from decision_tree import CLASSES, SHORT, split, share

INTERFACES = dict(electronic=["EHR interface engine", "payer eligibility service", "provider directory",
                              "e-referral portal"],
                  fax=["clinic fax servers", "optical character recognition service", "patient registration",
                       "EHR order creation through the managed-service provider"])
DOC_TYPES = dict(electronic=["referral order message", "clinical notes", "payer form"],
                 fax=["fax cover and form", "handwritten referral", "scanned notes", "insurance card image"])


def owners(steps):
    return sorted({s.rule_owner for s in steps if s.rule_owner})


def profile(name, steps, ifaces, docs):
    sp = split(steps)
    return dict(name=name, steps=len(steps), det=share(steps), split=sp, interfaces=len(ifaces),
                docs=len(docs), owners=len(owners(steps)))


def fdes_to_hold(steps, i=pj.Inputs()):
    """How many FDEs keep the build off the critical path if the date must not move."""
    p = pj.project(pl.ELECTRONIC, i)
    working = (p["data"] - i.scope_day) * 5 / 7
    return math.ceil(pj.effort(steps) / (working * i.build_fraction))


def main():
    e = profile("electronic (release 1 as drafted)", pl.ELECTRONIC, INTERFACES["electronic"], DOC_TYPES["electronic"])
    both = pl.ELECTRONIC + pl.FAX
    b = profile("electronic + fax", both, INTERFACES["electronic"] + INTERFACES["fax"],
                DOC_TYPES["electronic"] + DOC_TYPES["fax"])
    vol = pl.VOLUME
    print(f"Fax share of the two-clinic count: {vol['fax']} of {vol['electronic'] + vol['fax']} = "
          f"{vol['fax'] / (vol['electronic'] + vol['fax']):.0%}")
    print()
    print(f"{'':<34}{'steps':>6}{'det':>6}{'docs':>6}{'ifaces':>8}{'owners':>8}   split")
    for r in (e, b):
        sp = ", ".join(f"{SHORT[c]} {r['split'][c]}" for c in CLASSES)
        print(f"{r['name']:<34}{r['steps']:>6}{r['det']:>6.0%}{r['docs']:>6}{r['interfaces']:>8}{r['owners']:>8}   {sp}")
    fs = split(pl.FAX)
    print(f"{'fax path alone':<34}{len(pl.FAX):>6}{share(pl.FAX):>6.0%}{'':>6}{'':>8}{'':>8}   "
          + ", ".join(f"{SHORT[c]} {fs[c]}" for c in CLASSES))
    print()
    pe, pb = pj.project(pl.ELECTRONIC), pj.project(both)
    n = fdes_to_hold(both)
    ph = pj.project(both, pj.with_(fdes=n))
    print("Response                         effort  build done  pilot  critical   T&M cost  cap headroom")
    rows = (("A absorb into release 1", pb, 2), (f"B absorb and hold the date", ph, n), ("C carve out, owner + date", pe, 2))
    for label, p, f in rows:
        print(f"{label:<32}{p['effort_days']:>7}{p['build_done']:>12}{p['pilot']:>7}  {p['critical']:<8}"
              f"{'$' + format(p['cost'], ','):>11}{'$' + format(p['headroom'], ','):>14}  ({f} FDEs)")
    print("B also assumes the fax images join the privacy board submission for day 75; on day 19 they were not in it.")
    print()
    print("Northlight's answer on day 19: C. Release 1 is the electronic path, signed today.")
    print("The fax path is an exclusion with an owner (VP ambulatory operations) and a decision due day 33:")
    print("  fund it as release 2, move outside referrals to the e-referral portal, or both.")
    print(f"Owners named by the fax steps that release 1 does not need: "
          f"{', '.join(o for o in owners(pl.FAX) if o not in owners(pl.ELECTRONIC))}")


if __name__ == "__main__":
    main()
