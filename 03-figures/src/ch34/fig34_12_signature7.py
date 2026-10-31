"""Figure 34.12: Signature 7 (fieldkit after Chapter 34). contract.py (v4.2) is the change; layout identical to
Figure 33.11. Versions v3.6 to v4.0 follow the Blueprint [CHECK ch29-ch32]."""
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
        ("v2.6 to v4.1", "quality to model risk", "data", None),
        ("contract.py", "v4.2: commitments as data", "cost", "new")]
signature7.STATES.setdefault("ch34", dict(version="0.1.0", modules=mods,
                                          imports=[(2, 0), (2, 1), (8, 6), (8, 7), (14, 13)], labs=[],
                                          future=[]))
signature7.render("ch34", "fig34-12", __file__)
