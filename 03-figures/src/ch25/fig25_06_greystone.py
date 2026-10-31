"""Figure 25.6: Greystone sandbox week: what happened to 200 referrals and the refused actions the planner tried."""
import re
from _common import S, save, text
t = text("greystone_drafts")
red = int(re.search(r"red flags routed to a clinician (\d+)", t).group(1))
dr = int(re.search(r"draft_prior_auth\s+allowed\s+(\d+)", t).group(1))
den = {k: int(v) for k, v in re.findall(r"(set_urgency|submit_prior_auth|message_patient)\s+boundary\s+(\d+)", t)}
fig, ax = S.figure(height=3.7)
names = ["drafted for a\ncoordinator", "red flag to a\nclinician", "set urgency\n(denied)", "submit\n(denied)",
         "message patient\n(denied)"]
vals = [dr, red, den["set_urgency"], den["submit_prior_auth"], den["message_patient"]]
cols = [S.ROLE["approval"], S.ROLE["data"], S.ROLE["blocker"], S.ROLE["blocker"], S.ROLE["blocker"]]
y = list(range(5))[::-1]
ax.barh(y, vals, color=cols, height=0.6)
for yy, v in zip(y, vals):
    ax.text(v + 2, yy, str(v), va="center", fontsize=10, color=S.PAL["ink"])
ax.set_yticks(y, names, fontsize=9.5); ax.set_xlim(0, 215); ax.set_xlabel("referrals or calls")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch25/output/greystone_drafts.txt")
