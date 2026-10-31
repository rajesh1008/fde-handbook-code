"""Figure 43.9: Signature 7 (fieldkit after Chapter 43). service.py (v5.2) is the change; v2.6 to v5.1 are grouped.
Layout identical to Figure 42.10."""
from _common import S  # noqa: F401  (sets paths)
import signature7
mods = [("access.py", "", "evidence", None), ("readiness.py", "", "data", None),
        ("fixtures.py", "", "system", None), ("engagement.py", "", "evidence", None),
        ("deployment.py", "", "evidence", None), ("cadence.py", "", "evidence", None),
        ("escalation.py", "", "evidence", None), ("datareadiness.py", "", "data", None),
        ("histories.py", "", "system", None), ("synthetic.py", "", "data", None),
        ("deid.py", "", "blocker", None), ("shadow.py", "", "system", None),
        ("sampling.py", "", "evidence", None), ("gateway.py", "Ch 18", "system", None),
        ("connectors.py", "Ch 19", "system", None), ("estates.py", "Ch 20", "evidence", None),
        ("v2.6 to v5.1", "quality to live ops", "data", None),
        ("service.py", "v5.2: the year after", "cost", "new")]
signature7.STATES.setdefault("ch43", dict(version="0.1.0", modules=mods,
                                          imports=[(2, 0), (2, 1), (8, 6), (8, 7), (10, 16), (14, 13)], labs=[],
                                          future=[]))
signature7.render("ch43", "fig43-09", __file__)
