"""Pack completeness, the monitor Caldwell runs as cw-mrm-monitor. Daily share of decisions whose pack holds, by status
of the weakest element. Before the backfill (as of day 180) and after it (as of day 215)."""
import _paths  # noqa: F401
import world as W, pack as P

recs = W.records(W.LIVE, W.END)
RANK = ["verified", "reconstructed", "inferred", "contradicted", "unverifiable"]


def weakest(st):
    vals = [v for v in st.values() if v != "n/a"]
    return max(vals, key=RANK.index)


for asof, hist, title in ((W.FIX, False, "AS OF DAY 180, BEFORE BACKFILL (v0 rules)"), (W.END, True, "AS OF DAY 215, AFTER BACKFILL")):
    print(f"P1 PACK COMPLETENESS {title}")
    for d in range(W.LIVE, min(asof, W.END) + 1):
        day = [r for r in recs if r["day"] == d]
        c = {k: 0 for k in RANK}
        for r in day:
            c[weakest(P.build(r, asof, hist)[0])] += 1
        print(f"  day {d}: " + " ".join(f"{k} {c[k]}" for k in RANK) + f"  complete {100 * (c['verified'] + c['reconstructed']) / len(day):.1f}%")
    print()
print("MONITORS CALDWELL RUNS WITHOUT NORTHLIGHT (cw-mrm-monitor)")
for m in ("M1 proceed-band error, weekly audit sample", "M2 router score drift (PSI)", "M3 field and type accuracy, 30-day refresh",
          "M4 v2 citation audit, 30 summaries a month (Tom Whitfield)", "M5 pin age and provider deprecation dates",
          "M6 judge validity, 20 documents a week", "P1 pack completeness, daily", "P2 chain head anchored in Caldwell's log account, daily",
          "P3 reconstruction rehearsal, 40 decisions, weekly"):
    print("  " + m)
