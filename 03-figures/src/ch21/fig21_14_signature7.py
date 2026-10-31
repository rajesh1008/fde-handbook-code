"""Figure 21.14: Signature 7 (fieldkit after Chapter 21). Shared template signatures/signature7.py; the state is
registered as STATES['ch21'] here. Chapter 20 filled the 7.2 in height at 16 modules, so the two v2.6 modules share
one row; the lab is named in the caption."""
from _common import S  # noqa: F401  (sets paths)
import signature7
signature7.STATES.setdefault("ch21", dict(
    version="0.1.0",
    modules=[("access.py", "", "evidence", None), ("readiness.py", "", "data", None),
             ("fixtures.py", "", "system", None), ("engagement.py", "", "evidence", None),
             ("deployment.py", "", "evidence", None), ("cadence.py", "", "evidence", None),
             ("escalation.py", "", "evidence", None), ("datareadiness.py", "", "data", None),
             ("histories.py", "", "system", None), ("synthetic.py", "", "data", None),
             ("deid.py", "", "blocker", None), ("shadow.py", "", "system", None),
             ("sampling.py", "", "evidence", None), ("gateway.py", "Ch 18", "system", None),
             ("connectors.py", "Ch 19", "system", None), ("estates.py", "Ch 20", "evidence", None),
             ("quality/lineage", "v2.6: scorer, chain", "data", "new")],
    imports=[(2, 0), (2, 1), (8, 6), (8, 7), (14, 13)],
    labs=[],
    future=[]))
signature7.render("ch21", "fig21-14", __file__)
