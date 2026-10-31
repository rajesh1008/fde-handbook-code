"""Shared helpers for the Chapter 16 figures (prompt 003.1 figure rules; 03-figures/style.md).
Render all: /workspace/books/.venv/bin/python 05-build/tools/render_figures.py ch16
Data: every plotted number is read from the lab's own printed output, 04-code/ch16/output/*.txt, which
04-code/ch16/make_outputs.sh regenerates from the scripts. The pipeline is the labeled extractor stand-in and the
real files are the labeled stand-in sample. Figure numbers and captions live in the manuscript, never in the image."""
import sys, inspect, pathlib, re
R = pathlib.Path(__file__).resolve().parents[3]
for p in ("05-build/design", "04-code/fieldkit", "04-code/ch16", "03-figures/src/signatures"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402,F401
plt.rcParams["legend.framealpha"] = 1.0
plt.rcParams["legend.fancybox"] = False
OUT = R / "04-code/ch16/output"


def text(name):
    return (OUT / f"{name}.txt").read_text()


def save(fig, n, kind="plot", data="04-code/ch16 lab output"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig16-{n:02d}", kind=kind, source=src, data=data, strict=True)


def blank(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")


def pct(s):
    return float(s.rstrip("%"))


def field_table():
    """policy_number 93% 76% rows from failure_no_exceptions.txt -> {field: (syn, real)}."""
    rows = {}
    for m in re.finditer(r"^\s{2}(\w+)\s+(\d+)%\s+(\d+)%$", text("failure_no_exceptions"), re.M):
        rows[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return rows


def tag_table():
    rows = []
    for m in re.finditer(r"^\s{2}([A-Za-z -]+?)\s{2,}(\d+)\s+(\d+)%$", text("failure_no_exceptions"), re.M):
        rows.append((m.group(1).strip(), int(m.group(2)), int(m.group(3))))
    return rows


def psi_table():
    blocks = text("represent").split("representativeness report")[1:]
    out = []
    for b in blocks:
        out.append({m.group(1).strip(): float(m.group(2))
                    for m in re.finditer(r"^\s{2}([a-z ]+?)\s{2,}(\d+\.\d+)\s+(ok|FAIL|WARN)", b, re.M)})
    return out


def coverage_table():
    blocks = text("represent").split("representativeness report")[1:]
    out = []
    for b in blocks:
        out.append([(m.group(1).strip(), int(m.group(2)), int(m.group(3)))
                    for m in re.finditer(r"^\s{2}([A-Za-z -]+?)\s{2,}(\d+)%\s+(\d+)%\s+", b, re.M)])
    return out
