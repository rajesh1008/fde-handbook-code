"""Figure 12.10: Signature 7, fieldkit after Chapter 12 (v1.5). Shared template signatures/signature7.py; the state
is registered as STATES['ch12'] here. The new module, bid.py, is drawn in the emphasis stroke."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "signatures"))
import signature7
prev = signature7.STATES["ch01"]
mods = [(n, "", r, None) for n, d, r, _ in prev["modules"]] + [
    ("engagement.py", "", "evidence", None), ("deployment.py", "", "approval", None),
    ("discovery.py", "", "data", None), ("questionbank.py", "", "data", None),
    ("scoping.py", "", "evidence", None), ("autonomy.py", "", "model", None),
    ("integration.py", "", "cost", None), ("bid.py", "commitments", "evidence", "new")]
signature7.STATES.setdefault("ch12", dict(version="v1.5", modules=mods, imports=prev["imports"],
                                         labs=[("Ch 12 lab", "extract_run.py")],
                                         future=[("v1.6", "Ch 13"), ("v2", "Part III"), ("v3+", "Parts IV–VI")]))
signature7.render("ch12", "fig12-10", __file__)
