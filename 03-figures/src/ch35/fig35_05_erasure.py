"""Figure 35.5: days to erase one Pennant consignee from each store, map v1 against map v2, with the 30-day window."""
from _common import S, save, text
def parse(name):
    out = {}
    for l in text(name).splitlines()[1:]:
        p = l.split()
        if len(p) >= 5 and p[-1] in ("ok", "FAILS"):
            out[p[0]] = (float(p[-3]), p[-1] == "ok")
    return out
v1, v2 = parse("erasure_v1"), parse("erasure_v2")
stores = ["eu-shipment-records", "match-cache", "eval-set", "run-records", "run-subject-fields", "backups"]
fig, ax = S.figure(height=4.8)
for i, s in enumerate(stores):
    for off, m, lab in ((-0.2, v1, "v1"), (0.2, v2, "v2")):
        if s not in m:
            continue
        d, ok = m[s]
        w = d if ok else 60
        ax.barh(i + off, w, 0.36, color=S.ROLE["approval"] if ok else S.ROLE["blocker"])
        ax.text(w + 1, i + off, f"{lab}: {d:g} d" if ok else f"{lab}: never", va="center", fontsize=9)
ax.axvline(30, color=S.PAL["ink"], lw=0.75, ls="--"); ax.text(30.5, -0.9, "30-day window", fontsize=9)
ax.set_yticks(range(len(stores))); ax.set_yticklabels(stores); ax.invert_yaxis()
ax.set_xlim(0, 75); ax.set_xlabel("days until the subject is gone"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch35/output/erasure_v1.txt, erasure_v2.txt")
