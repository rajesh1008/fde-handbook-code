"""Try It Yourself, Chapter 43. Usage: python tryit.py a|b|c"""
import sys
from dataclasses import replace
import world as W
from fieldkit.handover import Step, Runbook
from fieldkit.service import two_year, summary, exit_lint


def a():
    """Stretch Pennant's retention drills from every 90 days to every 200 and watch the capability go."""
    base = W.PENNANT_PATHS["managed"]
    for period in (90, 180, 200, 365):
        pr = {k: (period if v == 90 else v) for k, v in W.RETENTION.items()}
        rows = two_year(replace(base, practice=pr), W.items(W.PENNANT0))
        low = min(r.readiness for r in rows)
        capped = sum(r.capped for r in rows)
        print(f"drills every {period:>3} days: lowest readiness {low:.3f}, months capped at 0.60: {capped:>2} of 24, "
              f"peak takeover hours {max(r.takeover_hours for r in rows)}")

def b():
    """Rollover capped at one month's band instead of unlimited."""
    r = W.RET12
    for cap in (None, 12, 0):
        bank = 0.0
        for used in (5, 4, 6, 33):
            carried = bank
            mg = r.margin(used, carried=carried)
            bank = max(0.0, bank + r.band - used)
            if cap is not None:
                bank = min(bank, cap)
        label = "unlimited rollover" if cap is None else ("no rollover" if cap == 0 else f"rollover capped at {cap} h")
        print(f"{label:<26} month 4 (33 h used, {carried:.0f} h carried): margin {mg*100:.1f}%")


def c():
    """Add a dashboard nobody registered to a clean v1 runbook."""
    rb = W.RB_V1[1]
    extra = Step("check the latency panel on grafana.nl-tools.example", "Northlight on-call (night)", "panel green")
    rb2 = Runbook(rb.id, rb.title, rb.trigger, rb.failure_class, rb.mode, rb.owner, rb.steps + (extra,), rb.exit_via)
    print(f"{rb.id} v1: {len(exit_lint(rb, W.OWNERS))} exit findings")
    for f in exit_lint(rb2, W.OWNERS):
        print(f"{rb.id} v1 plus one step: {f}")
    print("registering the host as Northlight's or Pennant's is a decision someone signs; the lint will not guess")


if __name__ == "__main__":
    {"a": a, "b": b, "c": c}[sys.argv[1] if len(sys.argv) > 1 else "a"]()
