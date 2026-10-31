"""Shared helpers for the Chapter 2 figures (prompt 003.1 figure rules, house style 03-figures/book.mplstyle).

Render all: cd 03-figures/src/ch02 && for f in fig02_*.py; do /workspace/books/.venv/bin/python "$f"; done
fde_style.save() audits each figure (5.5 in width, aspect <= 3:2, text >= 9 pt, label contrast >= 4.5:1, no alpha,
no figure numbers in the image) and writes the Kindle PNG (300 ppi, sRGB, RGB), print PDF and SVG, and a manifest.
Data: every plotted number comes from the chapter lab (04-code/ch02) on its own fixtures.
Figure numbers, titles and captions live in the manuscript, never inside the image.
"""
import sys, inspect, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
for p in ("05-build/design", "04-code/fieldkit", "04-code/ch02"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["legend.framealpha"] = 1.0  # legend frame is off; keep its patch opaque (no alpha rule)
FIGSIZE = (S.WIDTH_IN, 4.0)
SHORT = {"caldwell": "Caldwell Mutual", "greystone": "Greystone Health", "pennant": "Pennant Logistics"}

def save(fig, n, kind="plot"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig02-{n:02d}", kind=kind, source=src, data="04-code/ch02 lab fixtures", strict=True)

def title(ax, t):
    """No-op: titles and captions live in the manuscript (003.1 rule 3). Kept so scripts record the claim."""
    return t
