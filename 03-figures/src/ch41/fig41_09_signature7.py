"""Figure 41.9: Signature 7 (fieldkit after Chapter 41). handover.py (v5) is the change; v2.6 to v4.5 stay grouped.
Layout identical to Figure 35.9. Versions v4.4 and v4.5 follow the Blueprint [CHECK ch36, ch37]."""
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
        ("v2.6 to v4.5", "quality to red team", "data", None),
        ("handover.py", "v5: hand-over test", "approval", "new")]
signature7.STATES.setdefault("ch41", dict(version="0.1.0", modules=mods,
                                          imports=[(2, 0), (2, 1), (8, 6), (8, 7), (10, 17), (14, 13)], labs=[],
                                          future=[]))
signature7.render("ch41", "fig41-09", __file__)
