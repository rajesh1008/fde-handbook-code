"""Shared helpers for the Chapter 43 figures (prompt 003.1 figure rules; 03-figures/style.md).
Render all: /workspace/books/.venv/bin/python 05-build/tools/render_figures.py ch43
Data: every plotted number is read from the lab's printed output, 04-code/ch43/output/*.txt, which
04-code/ch43/make_outputs.sh regenerates. Pennant and Caldwell data are the lab's deterministic stand-in.
Figure numbers and captions live in the manuscript, never in the image."""
import sys, inspect, pathlib, re  # noqa: F401
R = pathlib.Path(__file__).resolve().parents[3]
for p in ("05-build/design", "04-code/fieldkit", "04-code/ch43", "03-figures/src/signatures"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402,F401
plt.rcParams["legend.framealpha"] = 1.0
plt.rcParams["legend.fancybox"] = False
OUT = R / "04-code/ch43/output"


def text(name):
    return (OUT / f"{name}.txt").read_text()


def save(fig, n, kind="plot", data="04-code/ch43 lab output"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig43-{n:02d}", kind=kind, source=src, data=data, strict=True)


def blank(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")


def nums(s):
    return [float(x.replace(",", "")) for x in re.findall(r"-?[\d,]*\d(?:\.\d+)?", s)]


def dct(line):
    import ast
    return ast.literal_eval(line[line.index("{"):])



def nums(s):
    return [float(x.replace(",", "")) for x in re.findall(r"-?[\d,]*\d(?:\.\d+)?", s)]


def weeks(name):
    rows = []
    for l in text(name).splitlines():
        m = re.match(r"\s+(\d+)\s+(\d+)-(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(.*)$", l)
        if m:
            rest = m.group(7)
            sc = re.match(r"\s*(\d+)/200\s+([\d.]+)%\s+(\d+)\s+(\d+)", rest)
            rows.append(dict(week=int(m.group(1)), psi=float(m.group(5)), mix=float(m.group(6)),
                             matched=float(sc.group(2)) if sc else None,
                             silent_all=int(sc.group(4)) if sc else int(rest.split()[-1])))
    return rows


def months(which):
    import json
    return json.loads(text(f"model_{which}").split("MONTHS ", 1)[1])


PATH_STYLE = {"hand-over": ("approval", "-", "hand-over"), "hybrid": ("system", "--", "hybrid"),
              "managed-v0": ("blocker", ":", "managed v0"), "managed": ("model", "-", "managed")}


def endlabels(ax, ends, gap, x=24.4):
    """ends: list of (y, label). Joins labels at equal y and spreads the rest at least `gap` apart."""
    groups = {}
    for y, lab in ends:
        groups.setdefault(round(y, 6), []).append(lab)
    pts = sorted((y, ", ".join(l)) for y, l in groups.items())
    placed = []
    for y, lab in pts:
        if placed and y - placed[-1][0] < gap:
            y = placed[-1][0] + gap
        placed.append((y, lab))
    for y, lab in placed:
        ax.text(x, y, lab, fontsize=9, va="center")
