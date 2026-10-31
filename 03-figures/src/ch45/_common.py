"""Shared helpers for the Chapter 45 figures (prompt 003.1 figure rules; 03-figures/style.md).
Render all: /workspace/books/.venv/bin/python 05-build/tools/render_figures.py ch45
Data: every plotted number is read from the lab's printed output, 04-code/ch45/output/*.txt, which
04-code/ch45/make_outputs.sh regenerates. Hiring data are the lab's deterministic stand-in.
Figure numbers and captions live in the manuscript, never in the image."""
import sys, inspect, pathlib, re  # noqa: F401
R = pathlib.Path(__file__).resolve().parents[3]
for p in ("05-build/design", "04-code/fieldkit", "04-code/ch45", "03-figures/src/signatures"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402,F401
plt.rcParams["legend.framealpha"] = 1.0
plt.rcParams["legend.fancybox"] = False
OUT = R / "04-code/ch45/output"


def text(name):
    return (OUT / f"{name}.txt").read_text()


def save(fig, n, kind="plot", data="04-code/ch45 lab output"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig45-{n:02d}", kind=kind, source=src, data=data, strict=True)


def blank(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")


def nums(s):
    return [float(x.replace(",", "")) for x in re.findall(r"-?[\d,]*\d(?:\.\d+)?", s)]


def dct(line):
    import ast
    return ast.literal_eval(line[line.index("{"):])


COMPS = ("discovery", "decomposition", "build", "judgment", "communication")


def coverage(name):
    rows = []
    for l in text(name).splitlines():
        p = l.split()
        if len(p) >= 7 and re.match(r"^[A-Z]\d$", p[0]) and p[6].isdigit() and p[1] in (".", "obs", "self"):
            rows.append((p[0], p[1:6], int(p[6]), "take-home" in l))
    return rows


def heat(ax, rows):
    import numpy as np
    from matplotlib.colors import ListedColormap
    val = {".": 0, "self": 1, "obs": 2}
    m = np.array([[val[c] for c in r[1]] for r in rows])
    cm = ListedColormap(["#FFFFFF", S.TINT["data"], S.TINT["approval"]])
    ax.imshow(m, cmap=cm, vmin=0, vmax=2, aspect="auto")
    for i, r in enumerate(rows):
        for j, c in enumerate(r[1]):
            if c != ".":
                ax.text(j, i, "observed" if c == "obs" else "self-report", ha="center", va="center", fontsize=9,
                        color=S.PAL["ink"], fontweight="bold" if c == "obs" else "normal",
                        bbox=dict(fc="white", ec="none", pad=1.0))
    ax.set_xticks(range(5)); ax.set_xticklabels([c if c != "decomposition" else "decompo-\nsition" for c in COMPS], fontsize=9.5)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([f"{r[0]}  {r[2]} min" for r in rows], fontsize=9.5)
    ax.set_xticks([x - 0.5 for x in range(1, 5)], minor=True); ax.set_yticks([y - 0.5 for y in range(1, len(rows))], minor=True)
    ax.grid(which="minor", color=S.PAL["ink"], lw=0.5); ax.tick_params(which="both", length=0)
    ax.xaxis.tick_top()
