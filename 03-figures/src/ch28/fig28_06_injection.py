"""Figure 28.6: the injected referral under v1 and v2 of rule I-04."""
import re
from _common import S, save, text, blank
t = text("replay")
v1 = re.findall(r"injected GR-INJ-01 \(.*?\): (.*?)  fired", t)
fig, ax = S.figure(height=4.2); blank(ax, (0, 10), (0, 6))
S.box(ax, 0.1, 2.4, 2.4, 1.2, "F10.239\ninternal medicine", role="data")
S.box(ax, 3.4, 4.0, 2.8, 1.2, "v1: specialty?", role="evidence")
S.box(ax, 3.4, 0.8, 2.8, 1.2, "v2: reason code?", role="evidence")
S.box(ax, 7.2, 4.0, 2.6, 1.2, v1[0], role="blocker")
S.box(ax, 7.2, 0.8, 2.6, 1.2, "coordinator", role="approval")
S.arrow(ax, 2.5, 3.2, 3.4, 4.6); S.arrow(ax, 2.5, 2.8, 3.4, 1.4)
S.arrow(ax, 6.2, 4.6, 7.2, 4.6); S.arrow(ax, 6.2, 1.4, 7.2, 1.4)
S.label(ax, 6.7, 5.0, "pass", fs=9); S.label(ax, 6.7, 1.8, "I-04", fs=9)
save(fig, 6, kind="diagram", data="04-code/ch28/output/replay.txt")
