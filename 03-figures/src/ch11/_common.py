"""Shared helpers for the Chapter 11 figures. Render all: 05-build/tools/render_figures.py ch11
Data: every plotted number comes from the chapter lab (04-code/ch11), imported at render time. Plan durations
there are labeled stand-in estimates. Figure numbers and captions live in the manuscript."""
import sys, inspect, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(R / "05-build/design")); sys.path.insert(0, str(R / "03-figures/src/signatures"))
sys.path.insert(0, str(R / "04-code/ch11")); sys.path.append(str(R / "04-code/fieldkit"))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["legend.framealpha"] = 1.0
INK = S.PAL["ink"]


def save(fig, n, kind="plot"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig11-{n:02d}", kind=kind, source=src, data="04-code/ch11 lab", strict=True)


def blank(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
