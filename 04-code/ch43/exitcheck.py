"""Can Pennant run the managed-service runbooks if Northlight is gone? Usage: python exitcheck.py v0|v1
Two lints over the same four runbooks: Chapter 41's runbook lint (rule RB5 flags any step that names the vendor)
and the exit lint (any step touching an asset the customer does not own). Stand-in runbooks."""
import sys
import world as W
from fieldkit.handover import lint_runbook
from fieldkit.service import exit_lint


def run(v):
    rbs = W.RB_V0 if v == "v0" else W.RB_V1
    print(f"EXIT CHECK  Pennant managed-service runbooks {v}  (deterministic stand-in)")
    steps = sum(len(r.steps) for r in rbs)
    rb5 = [f for r in rbs for f in lint_runbook(r, W.PN_PEOPLE, W.PN_ALERTS) if f[0] == "RB5"]
    other = [(r.id, f) for r in rbs for f in lint_runbook(r, W.PN_PEOPLE, W.PN_ALERTS) if f[0] != "RB5"]
    ex = [f for r in rbs for f in exit_lint(r, W.OWNERS)]
    print(f"runbooks {len(rbs)}, steps {steps}")
    print(f"Chapter 41 runbook lint, rule RB5 (step names the vendor): {len(rb5)} of {steps} steps")
    print(f"Chapter 41 runbook lint, other rules: {len(other)} findings")
    print(f"exit lint (step touches an asset Pennant does not own): {len(ex)} steps in "
          f"{len({f.runbook for f in ex})} runbooks")
    for f in ex:
        print(f"  {f}")
    print(f"takeover rebuild estimate: {len(ex)} steps x 20 h = {len(ex) * 20} h")
    return rb5, ex


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "v0")
