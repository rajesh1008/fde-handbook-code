"""Figure 15.1 (Stage 0 sample): Caldwell Mutual's access requests on day 47, grouped by ladder rung.
Data: 04-code/fieldkit fixtures (caldwell_tracker); nothing typed by hand. Rev 003.1 figure rules; 03-figures/style.md."""
import sys, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
for p in ("05-build/design", "04-code/fieldkit"):
    sys.path.insert(0, str(R / p))
import fde_style as S  # noqa: E402
S.use()
from matplotlib.patches import Patch  # noqa: E402
from fieldkit import LADDER  # noqa: E402
from fieldkit.fixtures import caldwell_tracker  # noqa: E402

TODAY = 47
t = caldwell_tracker()
fig, ax = S.figure(height=4.6)
y, ticks, labels = 0.0, [], []
for rung in reversed(LADDER):                       # live at the bottom, synthetic at the top
    reqs = sorted((r for r in t.requests.values() if r.rung == rung), key=lambda r: -(r.requested_day or 999))
    for r in reqs:
        ticks.append(y); labels.append(r.key)
        if r.requested_day is None:
            ax.text(1, y, "not yet requested", va="center", fontsize=9.5, color=S.PAL["ink"], style="italic")
        else:
            granted = r.status == "granted"
            end = r.granted_day if granted else TODAY
            role = "approval" if granted else "blocker"
            ax.barh(y, max(end - r.requested_day, 0.6), left=r.requested_day, height=0.6,
                    color=S.ROLE[role] if granted else S.TINT["blocker"], hatch="" if granted else S.HATCH["blocker"],
                    edgecolor=S.ROLE[role], linewidth=S.LW["data"])
            ax.text(end + 0.8, y, f"{end - r.requested_day} d" if end > r.requested_day else "asked today", va="center", fontsize=9.5, color=S.PAL["ink"])
        y += 1
    ax.text(79, y - 0.55, rung, ha="right", va="center", fontsize=9.5, weight="bold", color=S.PAL["ink"])
    ax.axhline(y - 0.5, color=S.PAL["light"], lw=S.LW["data"])
    y += 0.4
ax.set_yticks(ticks); ax.set_yticklabels(labels, family="monospace", fontsize=9.5)
ax.axvline(TODAY, color=S.ROLE["data"], lw=S.LW["emphasis"])
ax.text(TODAY - 0.8, y - 0.2, "day 47: real files arrive", ha="right", va="center", fontsize=9.5, color=S.PAL["ink"])
ax.set_xlim(0, 80); ax.set_ylim(-0.6, y + 0.3); ax.set_xlabel("engagement day")
ax.legend(handles=[Patch(facecolor=S.ROLE["approval"], edgecolor=S.ROLE["approval"], label="granted"),
                   Patch(facecolor=S.TINT["blocker"], hatch=S.HATCH["blocker"], edgecolor=S.ROLE["blocker"], label="waiting")],
          loc="center right", bbox_to_anchor=(1.0, 0.765), frameon=False)
S.save(fig, "fig15-01", kind="plot", source=__file__, data="04-code/fieldkit/fieldkit/fixtures.py (caldwell_tracker)")
