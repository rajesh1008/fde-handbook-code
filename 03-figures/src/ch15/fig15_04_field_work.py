"""Figure 15.4: which planned work each registered field supports; the key carries three pieces of work."""
from _common import S, save
from fieldkit.histories import caldwell_fields
reg = caldwell_fields()
fields = list(reg.fields["caldwell-claims-sample"].values())
work = [w for f in fields for w in f.supports]
fig, ax = S.figure(height=4.6)
for i, f in enumerate(fields):
    y = len(fields) - 1 - i
    for w in f.supports:
        x = work.index(w)
        role = "blocker" if f.name == "claim_id" else "data"
        ax.scatter([x], [y], s=70, marker="s", color=S.ROLE[role], zorder=3)
    if not f.deliver:
        ax.text(len(work) - 0.6, y, "never delivered", va="center", ha="right", fontsize=9.5, color=S.PAL["ink"], style="italic")
ax.set_yticks(range(len(fields))); ax.set_yticklabels([f.name for f in reversed(fields)], family="monospace", fontsize=9.5)
ax.set_xticks(range(len(work))); ax.set_xticklabels(work, rotation=40, ha="right", fontsize=9.5)
ax.set_xlim(-0.6, len(work) - 0.4); ax.set_ylim(-0.6, len(fields) - 0.4)
ax.grid(color=S.PAL["light"], lw=S.LW["data"]); ax.set_axisbelow(True)
save(fig, 4, data="04-code/fieldkit histories.caldwell_fields()")
