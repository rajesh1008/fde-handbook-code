"""Figure 18.4: the Sunday rotation, naive adapter against the fieldkit adapter, Saturday to Monday noon."""
import re
from _common import S, save, text, hours
fig, ax = S.figure(height=3.9)
t = text("sunday_rotation")
naive, fk = t.split("== fieldkit adapter ==")
m = re.search(r"down from (day \d+ \w+ \d+:\d+) to (day \d+ \w+ \d+:\d+): (\d+) h (\d+) min", naive)
d0, d1 = hours(m.group(1)), hours(m.group(2))
start, end = 72 * 24, 74 * 24 + 12
rot = hours(re.search(r"rotations: (day \d+ \w+ \d+:\d+)", t).group(1))
for y, lab in ((1, "naive"), (0, "fieldkit")):
    ax.barh(y, end - start, left=start, color=S.TINT["evidence"] if "evidence" in S.TINT else S.PAL["green"], height=0.45, edgecolor=S.PAL["ink"], lw=S.LW["data"])
ax.barh(1, d1 - d0, left=d0, color=S.ROLE["blocker"], height=0.45)
ax.axvline(rot, color=S.PAL["ink"], lw=S.LW["control"], ls="--")
ax.axvline(rot + 1, color=S.PAL["slate"], lw=S.LW["data"], ls=":")
ax.text(rot + 1.5, 1.45, "rotation 02:00, grace to 03:00", fontsize=9)
sc = re.findall(r"scored (\d+), missed (\d+)", t)
ax.text(d0 + 1.5, 0.6, f"runner down {m.group(3)} h {m.group(4)} min; {sc[0][1]} missed", fontsize=10, color=S.PAL["ink"])
ax.text(start + 0.5, -0.45, f"fieldkit: {sc[1][0]} scored, {sc[1][1]} missed", fontsize=9)
ticks = [start, start + 24, start + 48, end]
ax.set_xticks(ticks); ax.set_xticklabels(["Sat 00:00\nday 72", "Sun 00:00\nday 73", "Mon 00:00\nday 74", "Mon 12:00"])
ax.set_yticks([0, 1]); ax.set_yticklabels(["fieldkit adapter", "naive adapter"])
ax.set_ylim(-0.7, 1.8); ax.set_xlim(start, end)
save(fig, 4, data="04-code/ch18/output/sunday_rotation.txt")
