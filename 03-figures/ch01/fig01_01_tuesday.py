"""Figure 1.1: the FDE's Tuesday (day 82) at Caldwell Mutual, from the lab's calendar fixture."""
import csv
from _common import S, R, vstyle, save
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
rows = [r for r in csv.DictReader(open(R / "04-code/ch01/data/week_a_caldwell_calendar.csv")) if r["day"] == "82"]
def t(s): h, m = map(int, s.split(":")); return h + m / 60
fig, ax = plt.subplots(figsize=(9, 5.2))
for i, r in enumerate(rows):
    y = len(rows) - 1 - i
    st = vstyle(r["tag"])
    ax.barh(y, t(r["end"]) - t(r["start"]), left=t(r["start"]), height=0.6, color=st["color"], hatch=st["hatch"],
            edgecolor="white", alpha=0.9)
    cust = "caldwellmutual.com" in r["attendees"]
    ax.text(t(r["end"]) + 0.12, y, f"{r['title']}" + ("  [customer]" if cust else ""), va="center", fontsize=8)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r["tag"] for r in reversed(rows)], fontsize=8.5)
ax.set_xlim(7, 23.5); ax.set_xticks(range(7, 19)); ax.set_xticklabels([f"{h}:00" for h in range(7, 19)], fontsize=8)
ax.set_xlabel("time of day (Hartford)")
cust_h = sum(t(r["end"]) - t(r["start"]) for r in rows if "caldwellmutual.com" in r["attendees"])
verbs = {r["tag"] for r in rows} - {"internal", "travel"}
words = {9: "nine", 10: "ten", 5: "five", 4: "four", 6: "six"}
ax.set_title(f"Day 82: {words.get(len(rows), len(rows))} calendar entries, {words.get(len(verbs), len(verbs))} of the six verbs, "
             f"{cust_h:g} hours with Caldwell staff", loc="left", fontsize=11)
for s in ("left",): ax.spines[s].set_visible(False)
save(fig, 1)
