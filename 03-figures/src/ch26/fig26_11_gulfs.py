"""Figure 26.11: the three gulfs, as they showed up in Caldwell's numbers (Listing 26.1 and Try It b)."""
import re
from _common import S, save, text, blank
t = text("vendor_vs_customer")
d = [float(x) for x in re.findall(r"\(([-\d.]+) points\)", t)]
tb = text("tryit_b")
st = dict((s.strip(), float(v)) for s, v in re.findall(r"^\s+(first notice, \w+|[a-z ]+?)\s+([\d.]+)%", tb, re.M))
fig, ax = S.figure(height=4.0)
blank(ax, (0, 10), (0, 6))
S.box(ax, 0.2, 3.3, 3.0, 2.3, f"comprehension\n\nmix we never read\n{d[0]:+.1f} points", role="data")
S.box(ax, 3.5, 3.3, 3.0, 2.3, f"specification\n\njudge and definitions\n{d[1] + d[2]:+.1f} points", role="blocker")
S.box(ax, 6.8, 3.3, 3.0, 2.3, f"generalization\n\nfax and mail\n{st['first notice, mail']:.0f}% vs "
      f"{st['first notice, email']:.0f}% email", role="system")
S.box(ax, 2.0, 0.4, 6.0, 1.3, "fix in this order: read, define, then tune", role="approval")
S.arrow(ax, 1.7, 3.3, 3.2, 1.7); S.arrow(ax, 5.0, 3.3, 5.0, 1.7); S.arrow(ax, 8.3, 3.3, 6.8, 1.7)
save(fig, 11, kind="diagram", data="04-code/ch26/output/vendor_vs_customer.txt, tryit_b.txt")
