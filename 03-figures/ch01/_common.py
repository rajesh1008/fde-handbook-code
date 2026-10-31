import sys, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
for p in ("05-build/design", "04-code/fieldkit", "04-code/ch01"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.apply()
HERE = pathlib.Path(__file__).resolve().parent
# verb -> (role colour, hatch) so colour never carries meaning alone
VERB_ROLE = {"discover": "data", "decide": "evidence", "access": "blocker", "build": "system",
             "pass": "approval", "hand over": "model", "internal": "cost", "travel": None}
def vstyle(v):
    r = VERB_ROLE[v]
    if r is None:
        return dict(color="#BFC7D2", hatch="oo")
    return dict(color=S.ROLE[r], hatch=S.HATCH[r] or ("" if v != "hand over" else "++"))
def save(fig, n):
    fig.savefig(HERE / f"fig01-{n:02d}.png", dpi=240)
def tbox(ax, x, y, w, h, text, role="evidence", fs=10, fill_alpha=0.16):
    """S.box with the label on a white backing so hatching never sits under text."""
    p = S.box(ax, x, y, w, h, "", role=role, fs=fs, fill_alpha=fill_alpha)
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=S.PAL["ink"],
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.92))
    return p
