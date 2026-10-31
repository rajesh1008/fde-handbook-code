"""Figure 29.1: the 41 defects of days 106 to 140 by category, and the three Caldwell's API and UI tests caught (Listing 29.1)."""
from _common import S, save, js
d = js("why_not_enough")
rows = d["rows"]
roles = {1: "system", 2: "model", 3: "data", 4: "evidence", 5: "approval"}
fig, ax = S.figure(height=3.9)
names = list(rows)
for i, n in enumerate(names):
    f, layer, api = rows[n]
    ax.barh(i, f, height=0.6, color=S.TINT[roles[layer]], edgecolor=S.ROLE[roles[layer]], hatch=S.HATCH[roles[layer]])
    if api:
        ax.barh(i, api, height=0.6, color=S.ROLE["blocker"])
    S.label(ax, f + 0.2, i, f"{f} found, L{layer}" + (f"; API/UI caught {api}" if api else "; API/UI caught 0"), va="center", fs=9)
short = ["rule or function bug", "one document class", "unsupported answer", "contract or wiring", "multi-step scenario", "drift or live-only"]
ax.set_yticks(range(len(names)), short, fontsize=9)
ax.invert_yaxis(); ax.set_xlim(0, 16); ax.set_xlabel("defects, days 106 to 140")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 1, data="04-code/ch29/output/why_not_enough.json")
