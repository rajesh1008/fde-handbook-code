"""Figure 7.7: Ruth Calloway's hour on day 24. Questions answered and design-changing answers by minute."""
from _common import S, plt, save, quiet
with quiet():
    import caldwell_bank as cb
b = cb.build(); qs = b.for_audience("data owner")
t, x, n, ch, xs, cs = 0.0, [0], [0], [0], [], []
for q in qs:
    a = b.answers[q.qid]; t += a.elapsed_min
    x.append(t); n.append(n[-1] + 1); ch.append(ch[-1] + (a.outcome == "contradicted"))
    if a.outcome == "contradicted": xs.append(t); cs.append(ch[-1])
fig, ax = S.figure(3.8)
ax.step(x, n, where="post", color=S.ROLE["system"], lw=S.LW["control"], label="answered")
ax.step(x, ch, where="post", color=S.ROLE["blocker"], lw=S.LW["emphasis"], label="changed the design")
ax.plot(xs, cs, "o", color=S.ROLE["blocker"], ms=4)
ax.axvline(12.6, color=S.PAL["slate"], ls=":", lw=S.LW["data"]); ax.text(13.2, 35, "rapid round ends", fontsize=9)
ax.set_xlabel("minutes into the session"); ax.set_ylabel("questions"); ax.set_xlim(0, 60); ax.set_ylim(0, 42)
ax.legend(fontsize=9, frameon=False, loc="center right")
save(fig, 7)
