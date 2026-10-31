"""Figure 32.4: what each check passes: link check, evidence check, review."""
import re
from _common import S, save, text
link = int(re.search(r"link check .*?: (\d+) of", text("pack_check")).group(1))
ev = int(re.search(r"evidence check on day \d+ .*?: (\d+) of", text("pack_check")).group(1))
rv = int(re.search(r"(\d+) passed, \d+ findings", text("review")).group(1))
labels = ["link check, day 100", "evidence check, day 100", "architecture review, day 103"]
roles = ["evidence", "system", "approval"]
fig, ax = S.figure(height=3.8)
for i, (v, r) in enumerate(zip([link, ev, rv], roles)):
    ax.barh(i, v, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r], lw=1.5)
    ax.text(v + 0.5, i, f"{v} of 41", va="center", fontsize=10)
ax.set_yticks(range(3)); ax.set_yticklabels(labels); ax.invert_yaxis(); ax.set_xlim(0, 48)
ax.set_xlabel("answers passing"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 4, data="04-code/ch32/output/pack_check.txt, review.txt")
