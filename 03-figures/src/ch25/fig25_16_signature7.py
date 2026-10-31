"""Figure 25.16: Signature 7 (fieldkit after Chapter 25). Same template as Figure 23.11; actions.py (v3.2) is the
change, drawn in the emphasis stroke. The four modules added in Chapters 21 to 24 (quality, lineage,
retrieval, surface) share one box so the figure stays within the 7.2 in height, as Chapter 21 did. [CHECK ch24]"""
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
        ("v2.6 to v3.1", "quality to surface", "data", None),
        ("actions.py", "v3.2: boundaries, records", "approval", "new")]
signature7.STATES.setdefault("ch25", dict(version="0.1.0", modules=mods,
                                          imports=[(2, 0), (2, 1), (8, 6), (8, 7), (14, 13), (17, 14)], labs=[],
                                          future=[]))
signature7.render("ch25", "fig25-16", __file__)
