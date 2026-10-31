"""Shared helpers for the Chapter 6 figures (prompt 003.1 figure rules, house style 03-figures/book.mplstyle).

Render all: /workspace/books/.venv/bin/python 05-build/tools/render_figures.py ch06
Data: every plotted number comes from the chapter lab (04-code/ch06), a labeled deterministic stand-in.
Figure numbers, titles and captions live in the manuscript, never inside the image.
"""
import sys, inspect, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
for p in ("05-build/design", "04-code/ch06"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["legend.framealpha"] = 1.0
H = 4.0
SHORT = {"P01": "mail", "P02": "main fax", "P03": "shared mailbox", "P04": "agent portal", "P05": "closed fax number",
         "P06": "adjuster email", "P07": "phone, then mail", "P08": "nightly file", "P09": "finance cage",
         "P10": "legal", "P11": "repair email"}


def save(fig, n, kind="plot"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig06-{n:02d}", kind=kind, source=src, data="04-code/ch06 lab", strict=True)


def blank(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")


def doc_role(documented):
    return "system" if documented else "data"
