"""Try It Yourself, Chapter 14: three exercises on the Greystone scoping run."""
from dataclasses import replace

import pipeline as pl
import projection as pj
from decision_tree import CLASSES, SHORT, classify, split, share


def a_reclassify():
    print("(a) The clinic routing rules turn out to live in two coordinators' heads, not in binders.")
    try:
        classify(replace(pl.ELECTRONIC[12], rule_owner=""))
    except ValueError as err:
        print("    tree refuses:", err)
    steps = [replace(s, written_rules=False, closed_output=True, rule_owner="") if s.n == "E13" else s
             for s in pl.ELECTRONIC]
    sp = split(steps)
    p0, p1 = pj.project(pl.ELECTRONIC), pj.project(steps)
    print("    E13 becomes", classify(steps[12]) + ";", ", ".join(f"{SHORT[c]} {sp[c]}" for c in CLASSES) + ";",
          f"deterministic {share(steps):.0%}")
    print(f"    effort {p0['effort_days']} -> {p1['effort_days']} engineer-days; build done day {p0['build_done']} -> "
          f"{p1['build_done']}; pilot day {p0['pilot']} -> {p1['pilot']} (slack {p1['slack']} days)")


def b_board():
    print("(b) The privacy board submission slips two days, past the ten-day cutoff.")
    for sub in (63, 65, 66, 67):
        p = pj.project(pl.ELECTRONIC, pj.with_(board_submission_day=sub))
        print(f"    submitted day {sub}: board day {p['board']}, data day {p['data']}, pilot day {p['pilot']}")


def c_fraction():
    print("(c) How much does day 140 depend on the assumed build fraction?")
    for f in (0.5, 0.55, 0.6, 0.65, 0.7, 0.8):
        p = pj.project(pl.ELECTRONIC, pj.with_(build_fraction=f))
        print(f"    build fraction {f:.2f}: build done day {p['build_done']}, pilot day {p['pilot']}, "
              f"critical path {p['critical']}")


if __name__ == "__main__":
    a_reclassify(); print(); b_board(); print(); c_fraction()
