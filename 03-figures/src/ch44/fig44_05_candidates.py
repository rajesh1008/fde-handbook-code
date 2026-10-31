"""Figure 44.5: each candidate's old-loop mean against the new weighted score, with the decision under each."""
from _common import S, save, text
import re
rows = [l for l in text("rubric").splitlines() if re.match(r"C-\d", l)]
fig, ax = S.figure(height=4.2)
for i, l in enumerate(rows):
    c = l.split()[0]
    om = float(re.search(r"(?:no hire|hire) ([\d.]+)", l[5:24]).group(1)); oh = l[5:24].strip().startswith("hire")
    nm = float(re.search(r"(?:no hire|hire) ([\d.]+)", l[24:]).group(1)); nh = l[24:].strip().startswith("hire")
    ax.plot([i, i], [om, nm], color=S.PAL["ink"], lw=0.75)
    ax.scatter([i - 0.0], [om], s=70, marker="s", color=S.ROLE["data"] if oh else "white", ec=S.ROLE["data"], lw=1.5, zorder=3)
    ax.scatter([i], [nm], s=80, marker="o", color=S.ROLE["approval"] if nh else "white", ec=S.ROLE["approval"], lw=1.5, zorder=3)
    if "floor:" in l:
        ax.text(i + 0.12, nm - 0.22, l.split("floor: ")[1].split()[0] + " floor", fontsize=9)
ax.axhline(2.75, color=S.ROLE["approval"], lw=0.75, ls="--"); ax.text(7.4, 2.62, "new bar 2.75", fontsize=9, ha="right")
ax.axhline(3.0, color=S.ROLE["data"], lw=0.75, ls=":"); ax.text(-0.3, 3.07, "old bar 3.0", fontsize=9)
ax.scatter([], [], marker="s", color=S.ROLE["data"], label="old loop (filled = hire)")
ax.scatter([], [], marker="o", color=S.ROLE["approval"], label="new rubric (filled = hire)")
ax.set_xticks(range(len(rows))); ax.set_xticklabels([l.split()[0] for l in rows]); ax.set_ylim(1.4, 4.6)
ax.set_ylabel("score (1 to 4)"); ax.legend(loc="upper right", fontsize=9, ncol=2); ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch44/output/rubric.txt")
