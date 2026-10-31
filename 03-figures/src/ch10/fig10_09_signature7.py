"""Figure 10.9: Signature 7, fieldkit after Chapter 10 (v1.4). Shared template signatures/signature7.py; the state
is registered as STATES['ch10'] here. The new module, integration.py, is drawn in the emphasis stroke."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "signatures"))
import signature7
prev = signature7.STATES["ch01"]
mods = [(n, "", r, None) for n, d, r, _ in prev["modules"]] + [
    ("engagement.py", "", "evidence", None), ("deployment.py", "", "approval", None),
    ("discovery.py", "", "data", None), ("questionbank.py", "", "data", None),
    ("scoping.py", "", "evidence", None), ("autonomy.py", "", "model", None),
    ("integration.py", "tax estimator", "cost", "new")]
signature7.STATES.setdefault("ch10", dict(version="v1.4", modules=mods, imports=prev["imports"],
                                         labs=[("Ch 10 lab", "estimate_all.py")],
                                         future=[("v1.5", "Ch 12"), ("v2", "Part III"), ("v3+", "Parts IV–VI")]))
signature7.render("ch10", "fig10-09", __file__)
