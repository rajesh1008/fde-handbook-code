"""Figure 24.15: Signature 7 (fieldkit after Chapter 24). Same template as Figure 23.11; surface.py (v3.1) is the change.
The 7.2 in height holds 18 modules, so gateway and connectors share one row. The lab is named in the caption."""
from _common import S  # noqa: F401  (sets paths)
import signature7
mods = [("access.py", "", "evidence", None), ("readiness.py", "", "data", None),
        ("fixtures.py", "", "system", None), ("engagement.py", "", "evidence", None),
        ("deployment.py", "", "evidence", None), ("cadence.py", "", "evidence", None),
        ("escalation.py", "", "evidence", None), ("datareadiness.py", "", "data", None),
        ("histories.py", "", "system", None), ("synthetic.py", "", "data", None),
        ("deid.py", "", "blocker", None), ("shadow.py", "", "system", None),
        ("sampling.py", "", "evidence", None), ("gateway/connectors", "Ch 18, 19", "system", None),
        ("estates.py", "Ch 20", "evidence", None), ("quality/lineage", "Ch 21", "data", None),
        ("retrieval.py", "Ch 23", "system", None), ("surface.py", "v3.1: options, broker", "system", "new")]
signature7.STATES.setdefault("ch24", dict(version="0.1.0", modules=mods,
                                          imports=[(2, 0), (2, 1), (8, 6), (8, 7)], labs=[], future=[]))
signature7.render("ch24", "fig24-14", __file__)
