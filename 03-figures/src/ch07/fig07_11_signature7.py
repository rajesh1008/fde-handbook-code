"""Figure 7.11: Signature 7, fieldkit after Chapter 7 (v1.1). Same template as fig01-06, fig03-01 and fig06-15;
the only change, the questionbank module, is drawn in the emphasis stroke. The state is registered as
STATES['ch07'] at render time, so the shared template is not edited per chapter.

Render (from the book root): /workspace/books/.venv/bin/python 05-build/tools/render_figures.py ch07
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "signatures"))
import signature7

prev = signature7.STATES["ch01"]
mods = [(n, d, r, None) for n, d, r, _ in prev["modules"]] + [("engagement.py", "", "evidence", None),
                                                              ("deployment.py", "", "approval", None),
                                                              ("discovery.py", "notes and coverage", "data", None),
                                                              ("questionbank.py", "four-part questions", "data", "new")]
signature7.STATES.setdefault("ch07", dict(
    version="v1.1", modules=mods, imports=prev["imports"],
    labs=[("Ch 7 lab", "day24_session.py")],
    future=[("v2", "Part III"), ("v3+", "Parts IV–VI")],
))
signature7.render("ch07", "fig07-11", __file__)
