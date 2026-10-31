"""Shared helpers for the Chapter 12 figures. Render all: 05-build/tools/render_figures.py ch12
Data: every plotted number comes from the chapter lab (04-code/ch12), run at render time. The lab is a deterministic
stand-in with a fictional bank; figure numbers and captions live in the manuscript."""
import sys, inspect, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(R / "05-build/design")); sys.path.insert(0, str(R / "03-figures/src/signatures"))
sys.path.insert(0, str(R / "04-code/ch12")); sys.path.insert(0, str(R / "04-code/fieldkit"))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["legend.framealpha"] = 1.0


def save(fig, n, kind="plot", data="04-code/ch12 lab"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig12-{n:02d}", kind=kind, source=src, data=data, strict=True)


def blank(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")


def handles(roles):
    return [plt.Rectangle((0, 0), 1, 1, fc=S.ROLE[r], hatch=S.HATCH[r], ec="white") for r in roles]


def hbar(ax, y, left, width, role, h=0.62):
    ax.barh(y, width, left=left, height=h, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white", lw=0.8)
