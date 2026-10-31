"""Figure 4.7 (Signature 2): the demo-deployment gap. One row per dimension; what a demo proves against what a
deployment must prove. Later chapters re-draw it with draw(emphasis=<dimension>): only the 2.5 pt stroke moves."""
from _common import S, save, title, blank, DIMS

ROWS = {
    "capability": ("vendor's documents", "customer's mix,\nexpert-scored"),
    "workflow": ("one happy path", "every intake path"),
    "controls": ("vendor keys", "customer's controls"),
    "ownership": ("a believer", "named owners\nwith authority"),
    "reconstructability": ("a recording", "traceable outputs"),
}


def draw(emphasis=None):
    fig, ax = blank(5.2)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10.4)
    S.label(ax, 4.55, 9.75, "a demo proves", fs=11, ha="center", weight="bold")
    S.label(ax, 8.05, 9.75, "a deployment proves", fs=11, ha="center", weight="bold")
    for i, d in enumerate(DIMS):
        y = 7.75 - i * 1.85
        demo, dep = ROWS[d]
        S.label(ax, 2.85, y + 0.7, d, fs=10, ha="right", va="center")
        S.box(ax, 3.05, y, 3.0, 1.4, demo, role="model", fs=10, ls="--", lw=S.LW["data"])
        S.arrow(ax, 6.1, y + 0.7, 6.5, y + 0.7, weight="data")
        S.box(ax, 6.55, y, 3.0, 1.4, dep, role="approval", fs=10,
              lw=S.LW["emphasis"] if d == emphasis else S.LW["control"])
    return fig, ax


if __name__ == "__main__":
    fig, ax = draw()
    title(ax, "Signature 2: the demo-deployment gap")
    save(fig, 7, kind="diagram", data="none (concept diagram; the thesis in Section 4.2)")
