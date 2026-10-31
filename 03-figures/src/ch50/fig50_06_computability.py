"""Figure 50.6: which monitoring metrics the bank could compute without the vendor, at each submission."""
from _common import S, save, text, blank
s1, s2 = text("committee_s1"), text("committee_s2")
assert "runs as svc-northlight-eval" in s1 and s2.count("computable by the bank") == 4
fig, ax = S.figure(height=3.9); blank(ax, (0, 10), (0, 5.4))
S.label(ax, 3.6, 5.0, "submission one", fs=10, ha="center", weight="bold")
S.label(ax, 7.6, 5.0, "submission two", fs=10, ha="center", weight="bold")
rows = [("M1 agreement", "vendor code and identity", "blocker"), ("M2 gate blocks", "not defined", None),
        ("M3 canary set", "not defined", None), ("M4 retrieval recall", "not defined", None)]
for i, (m, a, r) in enumerate(rows):
    y = 3.9 - i * 1.15
    S.label(ax, 0.0, y + 0.4, m, fs=9.5, va="center")
    if r:
        S.box(ax, 2.2, y, 2.8, 0.8, a, role=r, fs=9.5, lw=S.LW["emphasis"])
    else:
        ax.add_patch(__import__("matplotlib").patches.Rectangle((2.2, y), 2.8, 0.8, fill=False, ec=S.PAL["grey"], lw=S.LW["data"], ls="--"))
        S.label(ax, 3.6, y + 0.4, a, fs=9.5, ha="center", va="center")
    S.box(ax, 6.2, y, 2.8, 0.8, "bank computes", role="approval", fs=9.5)
save(fig, 6, kind="diagram", data="04-code/ch50/output/committee_s1.txt, committee_s2.txt")
