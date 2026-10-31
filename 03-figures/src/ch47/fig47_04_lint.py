"""Figure 47.4: engagement lint findings by rule across all twenty engagements, month 15 and month 18."""
from _common import S, save, text
import re
def counts(n):
    return {m.group(1): int(m.group(2)) for m in re.finditer(r"^  (E\d)\s+(\d+)", text(n), re.M)}
a, b = counts("lint_m15"), counts("lint_m18")
rules = list(a)
fig, ax = S.figure(height=3.8)
x = range(len(rules))
ax.bar([i - 0.2 for i in x], [a[r] for r in rules], 0.4, color=S.ROLE["blocker"], hatch="\\\\", ec="white", label="month 15: 17 findings")
ax.bar([i + 0.2 for i in x], [b[r] for r in rules], 0.4, color=S.ROLE["system"], ec="white", label="month 18: 0 findings")
ax.set_xticks(list(x)); ax.set_xticklabels(rules); ax.set_ylabel("findings"); ax.set_ylim(0, 5)
ax.legend(loc="upper right", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 4, data="04-code/ch47/output/lint_m15.txt, lint_m18.txt")
