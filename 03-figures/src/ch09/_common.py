"""Shared helpers for the Chapter 9 figures. Render all: 05-build/tools/render_figures.py ch09
Data: every plotted number comes from the chapter lab (04-code/ch09), run at render time. Prices, latencies and
model error rates there are labeled stand-ins. Figure numbers and captions live in the manuscript."""
import sys, inspect, pathlib, random
R = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(R / "05-build/design")); sys.path.insert(0, str(R / "03-figures/src/signatures"))
sys.path.insert(0, str(R / "04-code/ch09")); sys.path.append(str(R / "04-code/fieldkit"))
import fde_style as S  # noqa: E402
S.use()
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["legend.framealpha"] = 1.0
CLASS_ROLE = ["system", "approval", "data", "model"]
CLASS_NAME = ["deterministic", "rules + guardrails", "small model", "frontier model"]
KIND = {"P03": "email", "P06": "email", "P11": "email", "P08": "structured"}


def save(fig, n, kind="plot"):
    src = inspect.stack()[1].filename
    return S.save(fig, f"fig09-{n:02d}", kind=kind, source=src, data="04-code/ch09 lab", strict=True)


def blank(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")


def handles(roles=CLASS_ROLE):
    return [plt.Rectangle((0, 0), 1, 1, fc=S.ROLE[r], hatch=S.HATCH[r], ec="white") for r in roles]


def weighted():
    """Volume-weighted cost per document and by class, from the lab (same arithmetic as cost_run.py)."""
    import costs as K
    from intake_paths import walk_paths
    vol = new = demo = 0; by = {}
    for row, _, c, _ in walk_paths():
        k = KIND.get(row[0], "scan"); b, n = K.pipeline_cost(c, k); v = row[2]
        vol += v; new += v * n; demo += v * K.demo_cost(k)[1]
        for key, val in b.items(): by[key] = by.get(key, 0) + v * val
    return demo / vol, new / vol, {k: v / vol for k, v in by.items()}
