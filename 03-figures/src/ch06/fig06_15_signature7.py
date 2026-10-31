"""Figure 6.15: Signature 7, fieldkit after Chapter 6. Same template as fig01-06 and fig03-01; the only change,
the discovery module (v1), is drawn in the emphasis stroke. The state is registered as STATES['ch06'] at render
time, so the shared template is not edited per chapter.

Render (from the book root): /workspace/books/.venv/bin/python 05-build/tools/render_figures.py ch06
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "signatures"))
import signature7

prev = signature7.STATES["ch01"]
mods = [(n, d, r, None) for n, d, r, _ in prev["modules"]] + [("engagement.py", "", "evidence", None),
                                                              ("deployment.py", "", "approval", None),
                                                              ("discovery.py", "notes and coverage", "data", "new")]
signature7.STATES.setdefault("ch06", dict(
    version=prev["version"], modules=mods, imports=prev["imports"],
    labs=[("Ch 6 lab", "run_coverage.py")],
    future=[("v1.1", "Ch 7"), ("v2", "Part III"), ("v3+", "Parts IV–VI")],
))
signature7.render("ch06", "fig06-15", __file__)
