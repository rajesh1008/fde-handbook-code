"""Figure 25.7: when claims-core rejects a write: the first build guessed and resubmitted; the executor holds."""
import re
from _common import S, save, blank, text
g = int(re.search(r"guessed cause code: (\d+)", text("day109_retry")).group(1))
fig, ax = S.figure(height=4.2)
blank(ax, (0, 10), (0, 6))
S.box(ax, 3.4, 4.8, 3.2, 0.9, "V-118 rejects", role="system", fs=10.5)
S.box(ax, 0.2, 2.6, 4.0, 1.0, "first build: guess\na cause, resubmit", role="blocker", fs=10)
S.box(ax, 5.8, 2.6, 4.0, 1.0, "executor: hold,\nintent is final", role="approval", fs=10)
S.arrow(ax, 4.2, 4.8, 2.2, 3.6); S.arrow(ax, 5.8, 4.8, 7.8, 3.6)
S.box(ax, 0.2, 0.5, 4.0, 1.0, f"{g} claims with a\nguessed code", role="blocker", fs=10)
S.box(ax, 5.8, 0.5, 4.0, 1.0, "adjuster asks\nthe claimant", role="evidence", fs=10)
S.arrow(ax, 2.2, 2.6, 2.2, 1.5); S.arrow(ax, 7.8, 2.6, 7.8, 1.5)
save(fig, 7, kind="diagram", data="04-code/ch25/output/day109_retry.txt")
