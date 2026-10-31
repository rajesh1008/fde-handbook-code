"""Figure 25.12: compensation through the customer's own procedure; anything a person touched goes to a person."""
import re
from _common import S, save, blank, text
t = text("compensate")
dup, comp, routed = map(int, re.search(r"duplicates (\d+)\s+compensated (\d+)\s+routed to the claims data team (\d+)", t).groups())
g = int(re.search(r"guessed cause code (\d+)", t).group(1))
fig, ax = S.figure(height=4.4)
blank(ax, (0, 10), (0, 6.4))
S.box(ax, 0.2, 4.9, 4.3, 1.0, f"{dup} duplicates\nfound by key and business key", role="evidence", fs=10)
S.box(ax, 5.5, 4.9, 4.3, 1.0, f"{g} guessed\ncause codes", role="blocker", fs=10)
S.box(ax, 1.0, 2.9, 2.7, 0.9, "touched by\na reviewer?", role="evidence", fs=10)
S.arrow(ax, 2.35, 4.9, 2.35, 3.8)
S.box(ax, 0.0, 0.6, 2.4, 1.2, f"no: VOID-DUP\n{comp} voided", role="approval", fs=10)
S.box(ax, 2.7, 0.6, 2.4, 1.2, f"yes: claims\ndata team {routed}", role="data", fs=10)
S.arrow(ax, 1.8, 2.9, 1.2, 1.8); S.arrow(ax, 2.9, 2.9, 3.9, 1.8)
S.box(ax, 5.9, 0.6, 3.6, 1.2, f"senior adjuster {g}\nnot voided, not edited", role="data", fs=10)
S.arrow(ax, 7.65, 4.9, 7.65, 1.8)
save(fig, 12, kind="diagram", data="04-code/ch25/output/compensate.txt")
