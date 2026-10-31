"""Figure 20.12: Signature 7 (fieldkit after Chapter 20). Shared template signatures/signature7.py; the state is
registered as STATES['ch19'] here, so the template is not edited per chapter. New module in emphasis."""
from _common import S  # noqa: F401  (sets paths)
import signature7
signature7.STATES.setdefault("ch20", dict(
    version="0.1.0",
    modules=[("access.py", "", "evidence", None), ("readiness.py", "", "data", None),
             ("fixtures.py", "", "system", None), ("engagement.py", "", "evidence", None),
             ("deployment.py", "", "evidence", None), ("cadence.py", "", "evidence", None),
             ("escalation.py", "", "evidence", None), ("datareadiness.py", "", "data", None),
             ("histories.py", "", "system", None), ("synthetic.py", "", "data", None),
             ("deid.py", "", "blocker", None), ("shadow.py", "", "system", None),
             ("sampling.py", "", "evidence", None), ("gateway.py", "Ch 18", "system", None),
             ("connectors.py", "Ch 19", "system", None),
             ("estates.py", "ports, pins, parity", "evidence", "new")],
    imports=[(2, 0), (2, 1), (8, 6), (8, 7), (14, 13)],
    labs=[],   # 16 modules fill the 7.2 in height limit; the lab is named in the caption (open item: template)
    future=[]))
signature7.render("ch20", "fig20-12", __file__)
