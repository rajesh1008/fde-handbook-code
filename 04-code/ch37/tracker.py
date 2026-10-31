"""Run the gate tracker on Caldwell's records. Usage: tracker.py aggregate|perclass|terms|evidence|order"""
import sys
import _paths  # noqa: F401
from fieldkit.gates import wilson
import world

mode = sys.argv[1] if len(sys.argv) > 1 else "terms"


def show(rec, per_class=True):
    print(f"{rec.gate}  signer {rec.signer or '-'}  decided day {rec.decided}")
    for l in rec.evaluate(per_class):
        print(f"  {l.key:4} {l.scope:22} {l.verdict:10} {l.detail}")
    for text, owner, due in rec.conditions:
        print(f"  condition: {text} ({owner}, day {due})")
    print(f"  status: {rec.status(per_class)}")


if mode in ("aggregate", "perclass", "terms"):
    t = world.caldwell(mode)
    print(f"GATE TRACKER  Caldwell Mutual  mode {mode}  (deterministic stand-in; numbers from Ch31 lab output)")
    show(t.records["Shadow Exit"], per_class=(mode != "aggregate"))
elif mode == "evidence":
    t = world.caldwell("aggregate")
    sx = t.records["Shadow Exit"]
    sx.measurements = sx.measurements + world.DRAFT_EXTRAS
    print("DRAFT PACKET, day 156: every item offered against a Shadow Exit criterion, by kind")
    for m in world.DRAFT_EXTRAS:
        c = next(c for c in sx.criteria if c.key == m.key)
        from fieldkit.gates import judge
        l = judge(c, m)
        print(f"  {m.key:4} {m.kind:21} {m.on:32} {l.verdict:8} {l.detail}")
    print("customer measurements offered:", sum(m.kind == "customer measurement" for m in sx.measurements),
          "| refused:", sum(judge(next(c for c in sx.criteria if c.key == m.key), m).verdict == "refused"
                            for m in sx.measurements))
elif mode == "order":
    for label, m in (("day 156, aggregate packet", "perclass"), ("day 157, exit terms signed", "terms")):
        t = world.caldwell(m)
        print(f"EFFECTIVE GATES  Caldwell Mutual  {label}")
        for g, st, day, note in t.effective():
            print(f"  {g:20} {st:24} {('day ' + str(day)) if day else '':8} {note}")
    t = world.caldwell("perclass")
    from fieldkit.gates import GateRecord
    t.add(GateRecord("Live Stable", entry=[("live monitoring will catch fax errors", "proposal, day 156")],
                     signer="Daniel Reyes", decided=158))
    print("PROPOSAL  let live monitoring stand in for the fax class")
    for g, st, day, note in t.effective():
        if g in ("Shadow Exit", "Live Stable"):
            print(f"  {g:20} {st:24} {note}")
