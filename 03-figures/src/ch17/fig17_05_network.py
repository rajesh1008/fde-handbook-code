"""Figure 17.5: the team account's network: no route out, four named endpoints, every decision logged."""
from _common import S, save, blank
fig, ax = S.figure(height=4.6)
blank(ax, (0, 10), (0, 7))
S.box(ax, 0.1, 0.2, 6.6, 6.0, "", role="system", lw=S.LW["control"])
S.label(ax, 0.3, 5.75, "VPC 10.42.0.0/24, private subnets only", fs=10, weight="bold")
S.box(ax, 0.5, 2.6, 2.2, 1.3, "shadow\nrunner", role="system", lw=S.LW["emphasis"])
for i, (lab, role) in enumerate((("gateway endpoint", "blocker"), ("secrets endpoint", "data"),
                                 ("logs endpoint", "evidence"), ("S3, one bucket", "data"))):
    y = 4.6 - i * 1.25
    S.box(ax, 3.7, y, 2.7, 0.9, lab, role=role, fs=9.5); S.arrow(ax, 2.7, 3.25, 3.7, y + 0.45, weight="data")
S.box(ax, 7.3, 4.6, 2.6, 1.3, "internet\nno gateway, no NAT", role="blocker", ls="--")
S.box(ax, 7.3, 1.0, 2.6, 1.6, "Caldwell\negress log", role="evidence")
S.arrow(ax, 6.7, 1.8, 7.3, 1.8, weight="data")
save(fig, 5, kind="diagram", data="04-code/ch17/terraform/main.tf.json")
