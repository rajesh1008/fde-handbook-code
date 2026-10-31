"""Figure 17.14: Signature 7 (fieldkit after Chapter 17). Shared template signatures/signature7.py; state
registered as STATES['ch17'] here. New module in emphasis."""
from _common import S  # noqa: F401  (sets paths)
import signature7
signature7.STATES.setdefault("ch17", dict(
    version="0.1.0",
    modules=[("access.py", "", "evidence", None), ("readiness.py", "", "data", None),
             ("fixtures.py", "", "system", None), ("engagement.py", "", "evidence", None),
             ("deployment.py", "", "evidence", None), ("cadence.py", "", "evidence", None),
             ("escalation.py", "", "evidence", None), ("datareadiness.py", "", "data", None),
             ("histories.py", "", "system", None), ("synthetic.py", "", "data", None),
             ("deid.py", "", "blocker", None), ("shadow.py", "", "system", None),
             ("sampling.py", "", "evidence", None), ("environment.py", "egress, identity, logs", "approval", "new")],
    imports=[(2, 0), (2, 1), (8, 6), (8, 7)],
    labs=[("Ch 17 lab", "day64_deploy.py")],
    future=[]))
signature7.render("ch17", "fig17-14", __file__)
