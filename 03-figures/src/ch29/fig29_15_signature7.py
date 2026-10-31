"""Figure 29.15: Signature 7 (fieldkit after Chapter 29). pyramid.py (v3.6) is the change; modules from Chapters 21
to 28 share one box to stay within 7.2 in."""
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
        ("v2.6 to v3.5", "quality to guardrails", "data", None),
        ("pyramid.py", "v3.6: pyramid runner, gate", "blocker", "new")]
signature7.STATES.setdefault("ch29", dict(version="0.1.0", modules=mods,
                                          imports=[(2, 0), (2, 1), (8, 6), (8, 7), (14, 13), (17, 12)], labs=[],
                                          future=[]))
signature7.render("ch29", "fig29-15", __file__)
