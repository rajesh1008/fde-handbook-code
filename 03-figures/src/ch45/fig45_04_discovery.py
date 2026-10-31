"""Figure 45.4: facts surfaced by minute in the discovery exercise, with the first solution statement marked."""
import sys
from _common import S, save, R
sys.path.insert(0, str(R / "04-code/ch45"))
import world as W
from _common import text
assert "facts surfaced 3 of 11" in text("discovery_c214") and "facts surfaced 10 of 11" in text("discovery_c231")
fig, ax = S.figure(height=4.2)
for cid, role, lab in (("c231", "approval", "candidate 231: 10 of 11 facts"), ("c214", "blocker", "candidate 214: 3 of 11 facts")):
    seen, xs, ys = set(), [0], [0]
    for m, k, f in W.TRANSCRIPTS[cid]:
        if f and k in ("question", "confirm"):
            seen.add(f)
        xs.append(m); ys.append(len(seen))
    xs.append(60); ys.append(len(seen))
    ax.step(xs, ys, where="post", color=S.ROLE[role], lw=S.LW["emphasis"], label=lab)
    fs = min(m for m, k, _ in W.TRANSCRIPTS[cid] if k == "solution")
    ax.axvline(fs, color=S.ROLE[role], ls="--", lw=S.LW["data"])
    ax.text(fs + 0.8, 10.6 if cid == "c231" else 6.2, f"first solution\nminute {fs}", fontsize=9.5, color=S.PAL["ink"])
ax.set_xlim(0, 60); ax.set_ylim(0, 12); ax.set_xlabel("minute of the 60-minute exercise"); ax.set_ylabel("hidden facts surfaced (of 11)")
ax.legend(fontsize=9.5, loc="center right"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 4, data="04-code/ch45/output/discovery_c214.txt, discovery_c231.txt; 04-code/ch45/world.py")
