"""Figure 19.19: Signature 7 (fieldkit after Chapter 19). Shared template signatures/signature7.py; the state is
registered as STATES['ch19'] here, so the template is not edited per chapter. New module in emphasis."""
from _common import S  # noqa: F401  (sets paths)
import signature7
signature7.STATES.setdefault("ch19", dict(
    version="0.1.0",
    modules=[("access.py", "", "evidence", None), ("readiness.py", "", "data", None),
             ("fixtures.py", "", "system", None), ("engagement.py", "", "evidence", None),
             ("deployment.py", "", "evidence", None), ("cadence.py", "", "evidence", None),
             ("escalation.py", "", "evidence", None), ("datareadiness.py", "", "data", None),
             ("histories.py", "", "system", None), ("synthetic.py", "", "data", None),
             ("deid.py", "", "blocker", None), ("shadow.py", "", "system", None),
             ("sampling.py", "", "evidence", None), ("gateway.py", "Ch 18", "system", None),
             ("connectors.py", "file, mail, screen, outbox", "system", "new")],
    imports=[(2, 0), (2, 1), (8, 6), (8, 7), (14, 13)],
    labs=[("Ch 19 lab", "reconcile_caldwell.py")],
    future=[]))
signature7.render("ch19", "fig19-19", __file__)
