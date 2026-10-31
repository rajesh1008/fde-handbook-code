"""Try It Yourself. a: take the observed operators out of Pennant's map. b: move the Shadow Exit bar.
c: lint the next insurer's deal sheet and playbook (Chapter 46 facts)."""
import sys
import _paths  # noqa: F401
from stakeholders import StakeholderMap
from linter import r02, r04, r07, r15
import pennant
from world import STORIES, CM


def a():
    m = pennant.DAY28
    no_clerks = StakeholderMap(m.customer, m.day, [p for p in m.people if p.key != "clerks"])
    for label, sm in (("day 28 as recorded", m), ("clerks removed", no_clerks)):
        for g in (False, True):
            s, d = r02(dict(smap=sm), g)
            print(f"{label:20} {'v1' if g else 'v0'} {s:5} {d}")


def b():
    gate = dict(STORIES[6]["gate"])
    for bar in (0.75, 0.78, 0.80, 0.84):
        gate["bar"] = bar
        s, d = r07(dict(gate=gate))
        print(f"bar {bar:.0%}: {s:5} {d}")


def c():
    m = dict(commitments=[dict(id="deal sheet: 40% faster", measurer="", documents="", computation="", interval="")],
             playbook_steps=[("PB-01", ["claims intake mailbox"]), ("PB-04", ["claims_core_doc_api"])],
             estate=["claims intake mailbox"], domain=CM)
    for rule in (r04, r15):
        print(rule.__name__.upper(), *rule(m))


if __name__ == "__main__":
    {"a": a, "b": b, "c": c}[sys.argv[1]]()
