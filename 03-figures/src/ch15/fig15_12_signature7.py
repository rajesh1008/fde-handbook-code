"""Figure 15.12: Signature 7 (fieldkit after Chapter 15). Shared template signatures/signature7.py; the state is
registered as STATES['ch15'] here, so the template is not edited per chapter. New and changed modules in emphasis."""
from _common import S  # noqa: F401  (sets paths)
import signature7
base = signature7.STATES["ch01"]
signature7.STATES.setdefault("ch15", dict(
    version="0.1.0",
    modules=[("access.py", "access ladder tracker", "evidence", "changed"),
             ("readiness.py", "data-readiness register", "data", None),
             ("fixtures.py", "the four customers", "system", None),
             ("engagement.py", "", "evidence", None),
             ("deployment.py", "", "evidence", None),
             ("cadence.py", "", "evidence", None),
             ("escalation.py", "escalation", "evidence", "new"),
             ("datareadiness.py", "field register", "data", "new"),
             ("histories.py", "replay", "system", "new")],
    imports=[(2, 0), (2, 1), (8, 6), (8, 7)],
    labs=[("Ch 15 lab", "escalate_day47.py")],
    future=[("v2.x", "Part III"), ("v3", "Part IV"), ("v4–v5", "Parts V–VI")]))
signature7.render("ch15", "fig15-12", __file__)
