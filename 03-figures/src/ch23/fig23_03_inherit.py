"""Figure 23.3: ACL inherited at ingest and applied before ranking; the empty ACL is refused (acl_inherit.txt)."""
from _common import S, save, blank, text, nums
t = text("acl_inherit"); refused = int(nums(t.splitlines()[1].split("refused")[1])[0])
fig, ax = S.figure(height=3.9); blank(ax, (0, 10), (0, 6))
S.box(ax, 0.2, 3.6, 2.2, 1.3, "source file\nACL: claims-siu", role="data", fs=9.5)
S.box(ax, 2.9, 3.6, 2.2, 1.3, "ingest copies\nthe ACL", role="system", fs=9.5)
S.box(ax, 5.6, 3.6, 2.0, 1.3, "permission\nfilter", role="evidence", fs=9.5)
S.box(ax, 8.0, 3.6, 1.8, 1.3, "rank\ntop ten", role="model", fs=9.5)
S.box(ax, 2.9, 0.8, 2.2, 1.3, f"empty ACL:\nrefused ({refused})", role="blocker", fs=9.5)
S.arrow(ax, 2.4, 4.25, 2.9, 4.25); S.arrow(ax, 5.1, 4.25, 5.6, 4.25); S.arrow(ax, 7.6, 4.25, 8.0, 4.25)
S.arrow(ax, 4.0, 3.6, 4.0, 2.1)
S.label(ax, 7.3, 1.45, "filter first, then rank", fs=10)
save(fig, 3, kind="diagram", data="04-code/ch23/output/acl_inherit.txt")
