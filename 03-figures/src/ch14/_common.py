"""Shared helpers for the Chapter 14 figures (prompt 003.1 figure rules, house style 03-figures/book.mplstyle).

Render all: cd 03-figures/src/ch14 && for f in fig14_*.py; do /workspace/books/.venv/bin/python "$f"; done
Data: every plotted number comes from the chapter lab (04-code/ch14). Figure numbers and captions live in the
manuscript, never inside the image.
"""
import sys, inspect, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
for p in ("05-build/design", "04-code/fieldkit", "04-code/ch14"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["legend.framealpha"] = 1.0
CLASS_ROLE = ["system", "approval", "data", "model"]   # deterministic, rules, small model, frontier


def save(fig, n, kind="plot"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig14-{n:02d}", kind=kind, source=src, data="04-code/ch14 lab", strict=True)


def blank(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
