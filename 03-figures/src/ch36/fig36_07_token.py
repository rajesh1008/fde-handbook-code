"""Figure 36.7: how long the on-behalf-of token stays valid after the coordinator signs out (F-23)."""
from _common import S, save, text
mins = {l.split(":")[0]: int(l.split("valid ")[1].split()[0]) for l in text("agency").splitlines() if "token valid" in l}
assert mins == {"v2": 60, "v3": 0}
fig, ax = S.figure(height=3.8)
for y, s in ((1, "v2"), (0, "v3")):
    ax.barh(y, 480, 0.5, left=-480, color=S.ROLE["system"])
    if mins[s]:
        ax.barh(y, mins[s], 0.5, left=0, color=S.ROLE["blocker"], hatch=S.HATCH["blocker"], edgecolor="white")
        ax.text(mins[s] + 6, y, f"{mins[s]} min after sign-out", va="center", fontsize=9.5)
    else:
        ax.text(6, y, "ends at sign-out", va="center", fontsize=9.5)
ax.axvline(0, color=S.PAL["ink"], lw=1.5); ax.text(0, 1.55, "sign-out", ha="center", fontsize=9.5)
ax.text(-240, 1.55, "coordinator session", ha="center", fontsize=9.5)
ax.set_yticks([1, 0]); ax.set_yticklabels(["v2, day 124", "v3, day 128"])
ax.set_xlim(-500, 200); ax.set_ylim(-0.5, 1.8); ax.set_xlabel("minutes relative to sign-out")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 7, data="04-code/ch36/output/agency.txt")
