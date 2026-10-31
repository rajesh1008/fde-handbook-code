"""Figure 30.10: what fine-tuning on Caldwell's data changes in the model-risk classification (diagram)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.0); blank(ax)
S.box(ax, 0.2, 4.5, 4.2, 1.2, "Prompted vendor model", "model", lw=S.LW["emphasis"])
S.box(ax, 5.6, 4.5, 4.2, 1.2, "Fine-tuned on\nCaldwell data", "system", lw=S.LW["emphasis"])
S.arrow(ax, 4.4, 5.1, 5.6, 5.1, weight="emphasis")
for j, t in enumerate(["third-party model use", "vendor due diligence", "use-case review"]):
    S.box(ax, 0.2, 3.1 - 1.15 * j, 4.2, 0.9, t, "evidence")
for j, t in enumerate(["full model-risk scope", "validation before production", "retrain is a model change",
                       "signed training-data record"]):
    S.box(ax, 5.6, 3.4 - 1.05 * j, 4.2, 0.85, t, "blocker")
save(fig, 10, kind="diagram", data="04-code/ch30/output/governance.txt")
