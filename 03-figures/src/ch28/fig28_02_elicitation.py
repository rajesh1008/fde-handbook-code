"""Figure 28.2: from statements to rule cards."""
import re
from _common import S, save, text, blank
t = text("elicit")
n = int(re.search(r"statements: (\d+)", t).group(1))
d = {k: int(re.search(rf"  {k}\s+(\d+)", t).group(1)) for k in ("rule", "merged", "out of scope", "contradicted")}
fs = int(re.search(r"rules from statements: (\d+)", t).group(1)); docs = int(re.search(r"documents and tables: (\d+)", t).group(1))
fig, ax = S.figure(height=4.2); blank(ax, (0, 10), (0, 6))
S.box(ax, 0.2, 2.4, 2.2, 1.2, f"{n} statements\n6 sessions", role="model")
rows = [("new rule", d["rule"], "approval", 4.6), ("merged", d["merged"], "evidence", 3.4),
        ("out of scope", d["out of scope"], "data", 2.2), ("contradicted", d["contradicted"], "blocker", 1.0)]
for lab, v, r, y in rows:
    S.box(ax, 3.4, y, 2.4, 0.9, f"{lab}: {v}", role=r)
    S.arrow(ax, 2.4, 3.0, 3.4, y + 0.45)
S.box(ax, 7.2, 3.6, 2.6, 1.2, f"60 rule cards", role="system")
S.box(ax, 7.2, 1.6, 2.6, 1.2, f"{docs} from documents", role="evidence")
S.arrow(ax, 5.8, 5.05, 7.2, 4.2); S.arrow(ax, 8.5, 2.8, 8.5, 3.6)
S.label(ax, 6.5, 5.4, f"{fs}", fs=10)
save(fig, 2, kind="diagram", data="04-code/ch28/output/elicit.txt")
