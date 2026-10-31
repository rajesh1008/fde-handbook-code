"""Shared helpers for the Chapter 5 figures (prompt 003.1 figure rules, house style 03-figures/book.mplstyle).

Render all: cd 03-figures/src/ch05 && for f in fig05_*.py; do /workspace/books/.venv/bin/python "$f"; done
Data: every plotted number comes from the chapter lab (04-code/ch05), which imports 04-code/ch02 for the vendor rows.
Figure numbers, titles and captions live in the manuscript, never inside the image.
"""
import sys, inspect, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
for p in ("05-build/design", "04-code/fieldkit", "04-code/ch02", "04-code/ch05"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["legend.framealpha"] = 1.0
FIGSIZE = (S.WIDTH_IN, 4.0)
HOME_ROLE = {"vendor": "evidence", "integrator": "system", "lab": "model"}
HOME_NAME = {"vendor": "product vendor", "integrator": "integrator", "lab": "model lab"}


def save(fig, n, kind="plot"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig05-{n:02d}", kind=kind, source=src, data="04-code/ch05 lab", strict=True)


def blank(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
