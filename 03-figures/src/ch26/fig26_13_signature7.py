"""Figure 26.13: Signature 7 (fieldkit after Chapter 26). Same template as Figure 25.16; evals.py (v3.3) is the
change, drawn in the emphasis stroke. The modules added in Chapters 21 to 25 share one box to stay within 7.2 in."""
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
        ("v2.6 to v3.2", "quality to actions", "data", None),
        ("evals.py", "v3.3: gold set, judges, gates", "evidence", "new")]
signature7.STATES.setdefault("ch26", dict(version="0.1.0", modules=mods,
                                          imports=[(2, 0), (2, 1), (8, 6), (8, 7), (14, 13), (17, 12)], labs=[],
                                          future=[]))
signature7.render("ch26", "fig26-13", __file__)
