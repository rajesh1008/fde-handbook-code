"""Figure 12.6: spoken seconds per move in the strong and weak answers to the console question (five_moves_run.py)."""
from _common import S, plt, save, handles, hbar
import runpy, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(str(S.ROOT / "04-code/ch12/five_moves_run.py"))
from fieldkit.bid import MOVES
roles = ["system", "evidence", "model", "blocker", "approval"]
fig, ax = S.figure(3.7)
for y, key in ((1, "strong"), (0, "weak")):
    left = 0
    for m, r in zip(MOVES, roles):
        sec = len(g[key].get(m, "").split()) * 60 / 150
        if sec:
            hbar(ax, y, left, sec, r, h=0.5); left += sec
    S.label(ax, left + 0.8, y, f"{left:.0f} s", fs=10, va="center")
ax.set_yticks([0, 1]); ax.set_yticklabels(["weak", "strong"])
ax.set_xlabel("seconds spoken at 150 words a minute"); ax.set_xlim(0, 60); ax.set_ylim(-0.6, 2.3)
ax.legend(handles(roles), list(MOVES), loc="upper center", ncol=5, fontsize=9)
save(fig, 6)
