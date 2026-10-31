"""Figure 36.8: twenty report items, one disposition each."""
from _common import S, save, text
line = next(l for l in text("triage").splitlines() if l.startswith("dispositions:"))
d = {k.rsplit(" ", 1)[0]: int(k.rsplit(" ", 1)[1]) for k in line.split(": ", 1)[1].split(", ")}
assert sum(d.values()) == 20 and d["new finding"] == 11
order = [("new finding", "blocker"), ("merged", "system"), ("duplicate", "evidence"), ("routed", "data"),
         ("out of scope", "cost"), ("by design", "approval")]
fig, ax = S.figure(height=4.0)
y = list(range(len(order)))[::-1]
for yi, (k, r) in zip(y, order):
    ax.barh(yi, d[k], 0.6, color=S.ROLE[r]); ax.text(d[k] + 0.2, yi, str(d[k]), va="center", fontsize=9.5)
labels = {"new finding": "new finding (F-13 to F-23)", "merged": "merged into F-09", "duplicate": "duplicate",
          "routed": "routed to clinical safety", "out of scope": "out of scope", "by design": "by design (I-06)"}
ax.set_yticks(y); ax.set_yticklabels([labels[k] for k, _ in order])
ax.set_xlabel("report items, day 127 triage"); ax.set_xlim(0, 12.5)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch36/output/triage.txt")
