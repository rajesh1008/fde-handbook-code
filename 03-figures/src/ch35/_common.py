"""Shared helpers for the Chapter 35 figures (prompt 003.1 figure rules; 03-figures/style.md).
Render all: /workspace/books/.venv/bin/python 05-build/tools/render_figures.py ch35
Data: every plotted number is read from the lab's printed output, 04-code/ch35/output/*.txt, which
04-code/ch35/make_outputs.sh regenerates. Greystone data are the lab's deterministic stand-in.
Figure numbers and captions live in the manuscript, never in the image."""
import sys, inspect, pathlib, re  # noqa: F401
R = pathlib.Path(__file__).resolve().parents[3]
for p in ("05-build/design", "04-code/fieldkit", "04-code/ch35", "03-figures/src/signatures"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402,F401
plt.rcParams["legend.framealpha"] = 1.0
plt.rcParams["legend.fancybox"] = False
OUT = R / "04-code/ch35/output"


def text(name):
    return (OUT / f"{name}.txt").read_text()


def save(fig, n, kind="plot", data="04-code/ch35 lab output"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig35-{n:02d}", kind=kind, source=src, data=data, strict=True)


def blank(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")


def nums(s):
    return [float(x.replace(",", "")) for x in re.findall(r"-?[\d,]*\d(?:\.\d+)?", s)]


def dct(line):
    import ast
    return ast.literal_eval(line[line.index("{"):])

