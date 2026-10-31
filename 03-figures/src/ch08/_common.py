"""Shared helpers for the Chapter 8 figures (prompt 003.1 figure rules, house style 03-figures/book.mplstyle).
Render all: /workspace/books/.venv/bin/python 05-build/tools/render_figures.py ch08
Data: every plotted number comes from the chapter lab (04-code/ch08) on its own deterministic fixtures.
Figure numbers, titles and captions live in the manuscript, never inside the image."""
import sys, inspect, pathlib, io, contextlib
R = pathlib.Path(__file__).resolve().parents[3]
for p in ("05-build/design", "04-code/fieldkit", "04-code/ch08", "03-figures/src/signatures"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["legend.framealpha"] = 1.0
# claim status -> palette role (fixed for the whole book; Signature 5)
STATUS_ROLE = dict(F="approval", R="system", V="blocker", P="model", D="data")

def save(fig, n, kind="plot", data="04-code/ch08 lab fixtures"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig08-{n:02d}", kind=kind, source=src, data=data, strict=True)

def quiet():
    return contextlib.redirect_stdout(io.StringIO())

def clean(ax, w=10, h=7):
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
