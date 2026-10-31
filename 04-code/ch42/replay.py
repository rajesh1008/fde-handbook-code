"""The ninety-day replay (Chapter 42). Usage: python replay.py v0|v1
v0: the monitoring Pennant was handed at go-live: a 200-document scored sample every four weeks, read by Northlight,
    no leading signal; a fix goes through Kofi Mensah's weekly change board.
v1: fieldkit.liveops.DriftMonitor: a leading PSI on the layout-fingerprint score (daily, 7-day window) and a weekly
    200-document scored sample, both read by Dana Whitaker's team; contain first (route the layout to the clerks,
    an operational setting Dana owns), then fix and re-calibrate under her signature."""
import sys, random
import _paths  # noqa: F401
from world import CAL, day_docs, outcome, bins, THRESHOLD_V0, GO_LIVE, TOP12
from fieldkit.liveops import DriftMonitor, recalibrate
from fieldkit.synthetic import psi

mode = sys.argv[1] if len(sys.argv) > 1 else "v1"
FP = lambda docs: bins([x[5] for x in docs])
base_docs = [x for d in range(-7, 0) for x in day_docs(d)]
base_fp, base_mix = FP(base_docs), [x[0] for x in base_docs]
mon = DriftMonitor(leading_owner="Dana Whitaker", lagging_owner="Dana Whitaker", psi_alarm=0.10, match_floor=0.80)
t, fixed, route, first, events = THRESHOLD_V0, False, None, {}, []
fix_day = None
weeks, daily = [], []
for w in range(13):
    days = range(w * 7 + 1, min(w * 7 + 8, 91))
    docs, psis, mixes = [], [], []
    for d in days:
        if fix_day is not None and d == fix_day:
            fixed, route = True, None
            if mode == "v1":
                r = random.Random(77)
                pool = [x for x in sum((day_docs(k, fixed=True) for k in range(26, 33)), [])]
                sample = [(x[2], x[3]) for x in r.sample(pool, 600)]
                rec = recalibrate(sample, max_wrong_upper=0.015, owner="Dana Whitaker")
                t = rec["threshold"]
                events.append(f"day {d:>2}  fix and re-calibration: BRF-INV v2 fingerprint added; threshold "
                              f"{THRESHOLD_V0:.2f} -> {t:.2f} on {rec['of']} scored documents, {rec['proceed']} proceed, "
                              f"{rec['wrong']} wrong, upper bound {rec['wrong_upper']:.2%}; signed by {rec['owner']}")
            else:
                events.append(f"day {d:>2}  fix: BRF-INV v2 fingerprint shipped through the weekly change board "
                              f"(threshold unchanged, no signed record)")
        dd = day_docs(d, fixed=fixed)
        docs += [(d, x, route, t) for x in dd]
        win = [x for k in range(max(1, d - 6), d + 1) for x in day_docs(k, fixed=fixed)]
        p, pm = mon.leading(base_fp, FP(win)), psi(base_mix, [x[0] for x in win])
        psis.append(p); mixes.append(pm)
        oc = [outcome(x, t, route) for x in dd]
        daily.append((d, p, pm, oc.count("silent"), oc.count("matched"), len(dd)))
        if mode == "v1" and p >= mon.psi_alarm and "leading" not in first:
            first["leading"] = (d, round(p, 3))
            route = ("BRF-INV", "v2")
            fix_day = CAL["recal_signed"]
            events.append(f"day {d:>2}  leading alarm: fingerprint PSI {p:.3f} >= {mon.psi_alarm}; read by Dana "
                          f"Whitaker; contained day {d + 1}: BRF-INV v2 routed to the clerks")
    rs = random.Random(500 + w)
    sample = rs.sample(docs, 200)
    oc = [outcome(x, tt, rr) for _, x, rr, tt in sample]
    m, s = oc.count("matched"), oc.count("silent")
    last = days[-1]
    if mode == "v1":
        mon.read(last, "Dana Whitaker")
        reads = True
    else:
        reads = w in (3, 7, 11)
        if reads:
            mon.read(last, "Northlight")
    if reads and (m / 200 < 0.80 or s >= 2) and "lagging" not in first:
        first["lagging"] = (last, m, s)
        if mode == "v0" and fix_day is None:
            fix_day = last + 8                   # next change board, then Northlight's build
            events.append(f"day {last:>2}  monthly sample read by Northlight: {m}/200 matched, {s} silently wrong")
    weeks.append((w + 1, days[0], last, len(docs), max(psis), max(mixes), m if reads else None, s if reads else None,
                  sum(1 for _, x, rr, tt in docs if outcome(x, tt, rr) == "silent")))
print(f"NINETY-DAY REPLAY  Pennant production  mode {mode}  (deterministic stand-in; production day 0 = engagement day {GO_LIVE})")
for e in events:
    print(e)
if mode == "v0":
    print("(PSI columns computed in hindsight for comparison; nobody computed them in v0)")
print("week  days   docs  PSI fp  PSI mix  scored matched  silent  silent (all docs)")
for wk, a, b, n, p, pm, m, s, sa in weeks:
    sc = f"{m:>3}/200 {m/2:5.1f}%  {s:>3}" if m is not None else "   (not scored)    -"
    print(f"{wk:>4}  {a:>2}-{b:<2} {n:>5}  {p:6.3f}  {pm:6.3f}  {sc}   {sa:>5}")
tot = sum(x[8] for x in weeks)
print(f"silently wrong documents in 90 days: {tot}")
if mode == "v1":
    print(f"drift starts day {CAL['brf_change']} (BRF-INV layout v2); leading alarm day {first['leading'][0]}; "
          f"lagging alarm day {first['lagging'][0] if 'lagging' in first else 'none'}")
else:
    l = first.get("lagging")
    print(f"drift starts day {CAL['brf_change']}; first alarm day {l[0] if l else 'none'} (four-weekly sample, read by Northlight)")
ok, why = mon.running(90)
print(f"monitor running on day 90: {'yes' if ok else 'no'} ({why})")
if len(sys.argv) > 2:
    import json
    print("DAILY " + json.dumps([(d, round(p, 4), round(pm, 4), s, m, n) for d, p, pm, s, m, n in daily]))
