"""Figure 18.11: Signature 7 (fieldkit after Chapter 18). Shared template signatures/signature7.py; the state is
registered as STATES['ch18'] here. New module in emphasis. Chapter 17 adds environment.py (v2.2)."""
from _common import S  # noqa: F401  (sets paths)
import signature7
signature7.STATES.setdefault("ch18", dict(
    version="0.1.0",
    modules=[("access.py", "", "evidence", None), ("readiness.py", "", "data", None),
             ("fixtures.py", "", "system", None), ("engagement.py", "", "evidence", None),
             ("deployment.py", "", "evidence", None), ("cadence.py", "", "evidence", None),
             ("escalation.py", "", "evidence", None), ("datareadiness.py", "", "data", None),
             ("histories.py", "", "system", None), ("synthetic.py", "", "data", None),
             ("deid.py", "", "blocker", None), ("shadow.py", "", "system", None),
             ("sampling.py", "", "evidence", None),
             ("environment.py", "", "evidence", None), ("gateway.py", "adapter, rotation", "system", "new")],
    imports=[(2, 0), (2, 1), (8, 6), (8, 7)],
    labs=[("Ch 18 lab", "sunday_rotation.py")],
    future=[]))
signature7.render("ch18", "fig18-11", __file__)
