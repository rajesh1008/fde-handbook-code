"""Figure 21.8: documents with no currency printed: guessing from the country against asking the sender."""
import re
from _common import S, save, text
t = text("ask_vs_guess")
n = int(re.search(r"no currency printed: (\d+)", t).group(1))
wrong = int(re.search(r"wrong on (\d+)", t).group(1))
ans = int(re.search(r"answered (\d+)", t).group(1)); still = int(re.search(r"still open (\d+)", t).group(1))
fig, ax = S.figure(height=3.7)
ax.barh(1, n - wrong, color=S.PAL["grey"], height=0.5); ax.barh(1, wrong, left=n - wrong, color=S.ROLE["blocker"], height=0.5)
ax.barh(0, ans, color=S.ROLE["approval"], height=0.5); ax.barh(0, still, left=ans, color=S.PAL["light"], height=0.5)
ax.text((n - wrong) / 2, 1.38, f"right {n - wrong}", ha="center", fontsize=10, color=S.PAL["ink"], weight="bold")
ax.text(n - wrong / 2, 1.38, f"wrong {wrong}", ha="center", fontsize=10, color=S.PAL["ink"])
ax.text(ans / 2, -0.4, f"answered {ans}, wrong 0", ha="center", fontsize=10, color=S.PAL["ink"], weight="bold")
ax.text(ans + still / 2, -0.4, f"open {still}", ha="center", fontsize=10, color=S.PAL["ink"])
ax.set_yticks([1, 0], ["guess from\ncountry", "ask the\nsender"]); ax.set_xlabel(f"documents (of {n})")
ax.set_ylim(-0.6, 1.6); ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch21/output/ask_vs_guess.txt")
