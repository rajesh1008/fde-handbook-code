"""Figure 5.4: Northlight's vendor playbook scored in each home; the integrator column is the failure injection."""
from _common import S, save, plt
from matplotlib.patches import Rectangle
from homes import HOMES
from playbook import VENDOR_PLAYBOOK, run

V = {"OK": "approval", "BENT": "data", "BREAKS": "blocker", "INVERTS": "cost"}
keys = ["vendor", "lab", "integrator"]
fits = {k: run(VENDOR_PLAYBOOK, HOMES[k]) for k in keys}
fig, ax = plt.subplots(figsize=(S.WIDTH_IN, 5.2))
n = len(VENDOR_PLAYBOOK)
for j, k in enumerate(keys):
    for i, f in enumerate(fits[k]):
        role = V[f.verdict]
        fill = S.TINT[role] if f.verdict == "OK" else S.TINT[role]
        ax.add_patch(Rectangle((j, i), 1, 1, facecolor=fill, edgecolor="white", lw=2,
                               hatch=S.HATCH[role]))
        ax.text(j + 0.5, i + 0.5, f.verdict, ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
ax.add_patch(Rectangle((2, 0), 1, n, fill=False, edgecolor=S.ROLE["blocker"], lw=2.5))
ax.set_xlim(0, 3); ax.set_ylim(n, 0)
ax.set_xticks([0.5, 1.5, 2.5]); ax.set_xticklabels(["product vendor", "model lab", "integrator\n(failure injection)"], fontsize=9.5)
ax.xaxis.tick_top()
ax.set_yticks([i + 0.5 for i in range(n)]); ax.set_yticklabels([p.key for p in VENDOR_PLAYBOOK], fontsize=9.5)
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
save(fig, 4)
