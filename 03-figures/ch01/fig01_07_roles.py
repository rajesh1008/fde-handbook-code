"""Figure 1.7: the FDE against three adjacent roles, on five questions."""
from _common import S, save, tbox
import matplotlib.pyplot as plt
cols = ["forward deployed\nengineer", "sales\nengineer", "consultant", "support\nengineer"]
rowsq = ["when does the work start?", "who owns the result?", "writes production\ncode in the\ncustomer's estate?",
         "measured on", "what is left behind"]
cells = [["after signature, often\nbefore scope is final", "before signature", "when a statement of\nwork is signed", "when a ticket opens"],
         ["the engineer, until\nhand-over", "the account executive", "the client", "the customer"],
         ["yes, daily", "demos and\nproofs only", "sometimes; often\nadvises", "fixes and\nworkarounds"],
         ["the system running\nand provable", "technical win rate", "billable delivery against\nthe statement of work", "time to resolve"],
         ["a running system, evidence\nand a runbook", "a won deal", "a report or a\nhanded-over build", "a closed ticket"]]
fig, ax = plt.subplots(figsize=(10, 5.6)); ax.set_xlim(0, 10.5); ax.set_ylim(0, 6.3); ax.axis("off")
cw, rh, x0 = 1.98, 1.0, 2.5
for j, c in enumerate(cols):
    role = "approval" if j == 0 else "evidence"
    tbox(ax, x0 + j * cw + 0.05, 5.25, cw - 0.1, 0.85, c, role=role, fs=9, fill_alpha=0.25 if j == 0 else 0.1)
for i, rq in enumerate(rowsq):
    y = 4.2 - i * rh
    ax.text(0.05, y + 0.45, rq, fontsize=8.5, va="center", weight="bold", color=S.PAL["ink"])
    for j in range(4):
        ax.add_patch(plt.Rectangle((x0 + j * cw + 0.05, y + 0.05), cw - 0.1, rh - 0.1, facecolor=S.PAL["mist"] if j else "#DCEFE0",
                                   edgecolor="white"))
        ax.text(x0 + j * cw + cw / 2, y + 0.5, cells[i][j], ha="center", va="center", fontsize=7.6, color=S.PAL["ink"])
save(fig, 7)
