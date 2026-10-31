"""Figure 50.7: release one's boundary in production; two operations allowed, three refused by name."""
from _common import S, save, text, blank
rows = [l.split() for l in text("boundary").split("release two")[0].splitlines() if l.startswith("  production ")]
fig, ax = S.figure(height=4.2); blank(ax, (0, 10), (0, 7.6))
for i, r in enumerate(rows):
    op, verdict = r[1], r[2].rstrip(":"); y = 6.0 - i * 1.25; ok = verdict == "allowed"
    S.label(ax, 0.0, y + 0.35, op, fs=9.5, va="center", family="monospace")
    S.box(ax, 4.6, y, 1.7, 0.7, "allowed" if ok else "refused", role="approval" if ok else "blocker", fs=9.5,
          lw=S.LW["control"] if ok else S.LW["emphasis"])
    who = "Okafor" if "Okafor" in " ".join(r) else ""
    who = "Okafor, Marsh" if "Okafor and Helen Marsh" in " ".join(r) else ("Marsh" if "Helen Marsh:" in " ".join(r) else who)
    S.label(ax, 6.6, y + 0.35, who, fs=9.5, va="center")
S.label(ax, 6.6, 7.35, "signed or refused by", fs=9.5, weight="bold")
save(fig, 7, kind="diagram", data="04-code/ch50/output/boundary.txt")
