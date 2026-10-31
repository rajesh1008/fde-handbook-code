"""Figure 33.11: Signature 7 (fieldkit after Chapter 33). modelrisk.py (v4.1) is the change; modules from
Chapters 21 to 32 share one box to stay within 7.2 in. Versions v3.6 to v4.0 follow the Blueprint [CHECK ch29-ch32]."""
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
        ("v2.6 to v4.0", "quality to gate stack", "data", None),
        ("modelrisk.py", "v4.1: classification as data", "approval", "new")]
signature7.STATES.setdefault("ch33", dict(version="0.1.0", modules=mods,
                                          imports=[(2, 0), (2, 1), (8, 6), (8, 7), (14, 13), (17, 12)], labs=[],
                                          future=[]))
signature7.render("ch33", "fig33-11", __file__)
