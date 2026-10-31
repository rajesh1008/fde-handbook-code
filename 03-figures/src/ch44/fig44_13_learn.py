"""Figure 44.13: skills by half-life and how often Northlight's engagements used them."""
from _common import S, save, text
import re
rows = [re.match(r"(.+?)\s+([\d.]+)y\s+(\d+)%\s+([\d.]+)", l) for l in text("learn").splitlines()[1:12]]
fig, ax = S.figure(height=4.4)
short = {"structured discovery interviewing": "discovery", "writing for a sponsor": "writing", "SQL and data modeling": "SQL",
         "identity and access patterns": "identity", "evaluation design with domain experts": "evaluation design",
         "one regulated domain in depth": "a regulated domain", "answering a security questionnaire": "security review",
         "cloud infrastructure as code": "infra as code", "one agent framework's API": "a framework API",
         "one model's quirks": "model quirks", "prompt phrasing tricks": "prompt tricks"}
pos = {"discovery": (11, 1.04), "writing": (21, 0.965), "evaluation design": (3.2, 1.035), "SQL": (21, 0.88),
       "identity": (5.6, 0.91), "security review": (6.5, 0.78), "a regulated domain": (13, 0.48), "infra as code": (4.3, 0.51),
       "a framework API": (1.1, 0.385), "model quirks": (0.56, 0.69), "prompt tricks": (0.56, 0.585)}
for m in rows:
    n, hl, used, v = m.group(1), float(m.group(2)), int(m.group(3)) / 100, float(m.group(4))
    r = "approval" if v >= 0.5 else ("data" if v >= 0.2 else "blocker")
    ax.scatter([hl], [used], s=60, color=S.ROLE[r], zorder=3)
    ax.text(*pos[short[n]], short[n], fontsize=9)
ax.set_xscale("log"); ax.set_xlim(0.35, 60)
ax.set_xticks([0.5, 1, 2, 5, 10, 20]); ax.set_xticklabels(["0.5", "1", "2", "5", "10", "20"]); ax.minorticks_off(); ax.set_ylim(0.3, 1.1)
ax.set_xlabel("half-life, years (log scale; estimate)"); ax.set_ylabel("share of engagement task codes using it")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 13, data="04-code/ch44/output/learn.txt")
