"""Figure 3.1: Signature 7, second state (fieldkit after Chapter 3). Hand-laid SVG from the shared template
03-figures/src/signatures/signature7.py, same layout, scale and palette as its Chapter 1 appearance (fig01-06); the only change, the
engagement module (v0), is drawn in the emphasis stroke. The state is defined here and registered as
STATES['ch03'] at render time, so the shared template is not edited per chapter.

Render (from the book root): /workspace/books/.venv/bin/python 05-build/tools/render_figures.py ch03
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "signatures"))
import signature7

prev = signature7.STATES["ch01"]
signature7.STATES.setdefault("ch03", dict(
    version=prev["version"],
    modules=[(n, d, r, None) for n, d, r, _ in prev["modules"]]
            + [("engagement.py", "", "evidence", "new")],
    imports=prev["imports"],
    labs=[("Ch 1 lab", "weeklog.py"), ("Ch 3 lab", "caldwell_week.py"), ("Ch 15 lab", "day47_status.py")],
    future=[f for f in prev["future"] if f[0] != "v0"],
))
signature7.render("ch03", "fig03-01", __file__)
