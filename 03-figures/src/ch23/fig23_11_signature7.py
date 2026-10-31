"""Figure 23.11: Signature 7 (fieldkit after Chapter 23). Same template as Figure 21.14; retrieval.py (v3) is the
change, drawn in the emphasis stroke. The lab is named in the caption."""
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
        ("quality/lineage", "Ch 21", "data", None), ("retrieval.py", "v3: ACL, supersession", "system", "new")]
signature7.STATES.setdefault("ch23", dict(version="0.1.0", modules=mods,
                                          imports=[(2, 0), (2, 1), (8, 6), (8, 7), (14, 13)], labs=[], future=[]))
signature7.render("ch23", "fig23-11", __file__)
