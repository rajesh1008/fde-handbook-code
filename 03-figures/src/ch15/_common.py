"""Shared helpers for the Chapter 15 figures (prompt 003.1 figure rules; 03-figures/style.md).
Render all: /workspace/books/.venv/bin/python 05-build/tools/render_figures.py ch15
Data: every plotted number comes from the chapter lab (04-code/ch15) or the fieldkit v2 histories.
Figure numbers and captions live in the manuscript, never inside the image."""
import sys, inspect, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
for p in ("05-build/design", "04-code/fieldkit", "04-code/ch15", "03-figures/src/signatures"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["legend.framealpha"] = 1.0
plt.rcParams["legend.fancybox"] = False


def save(fig, n, kind="plot", data="04-code/ch15 lab"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig15-{n:02d}", kind=kind, source=src, data=data, strict=True)


def blank(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
