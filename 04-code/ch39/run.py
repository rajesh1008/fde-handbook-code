"""Prints every listing Chapter 39 quotes. Usage: run.py funnel|adjudication|streams|gate|holiday|greystone"""
import sys, json
from collections import Counter
import _paths  # noqa: F401
from fieldkit.evals import wilson
import world as W, suite as U

D = W.caldwell_window()
what = sys.argv[1]
pct = lambda k, n: f"{k / n:.1%}" if n else "n/a"

if what == "funnel":
    f = U.funnel(D)
    print("Signature 14 · Caldwell shadow funnel, intake days 142 to 153 (rc-1; outputs never served)")
    rows = [("documents seen by the tap", f["seen"]), ("agent decisions (typed and routed)", f["decided"]),
            ("  proceed", f["proceed"]), ("  review", f["review"]), ("  escalate", f["escalate"]),
            ("  no decision (untyped)", f["none"]), ("human decisions (clerks keyed six fields)", f["human"]),
            ("agreements, all six fields", f["agree"]), ("disagreements", f["disagree"]),
            ("  equivalent format", f["equivalent"]), ("  human wrong, agent right", f["human_wrong"]),
            ("  agent wrong", f["agent_wrong"]), ("    loud (flagged, routed or escalated)", f["loud"]),
            ("    silent (proceed, no stream fired, or dropped)", f["silent"]),
            ("escalations (agent escalate + untyped)", f["escalations"])]
    for name, v in rows:
        base = f["decided"] if name.startswith("  ") and name.strip() in ("proceed", "review", "escalate") else f["seen"]
        print(f"{name:52} {v:6,}  {v / base:6.1%}" + ("  of decided" if base != f["seen"] else ""))
    k, n, a, lo, hi = W.agreement(D)
    print(f"agreement {a:.1%} (95% interval {lo:.1%} to {hi:.1%}); right or equivalent "
          f"{pct(f['agree'] + f['equivalent'] + f['human_wrong'], n)}; agent-wrong rate {pct(f['agent_wrong'], n)}")
    json.dump(f, open("output/funnel_caldwell.json", "w"))
elif what == "adjudication":
    print("disagreements by cause and band (adjudicated by Lena Ortiz, days 154 and 155)")
    causes = [c for c, _ in Counter(x["cause"] for x in D if x["cause"]).most_common()]
    print(f"{'cause':34} {'proceed':>8} {'review':>7} {'escal.':>7} {'none':>5} {'silent':>7}")
    for c in causes:
        g = [x for x in D if x["cause"] == c]; b = Counter(x["band"] for x in g)
        print(f"{c:34} {b['proceed']:8} {b['review']:7} {b['escalate']:7} {b['none']:5} {sum(x['silent'] for x in g):7}")
    print("\nsilent agent errors by intake day (the ones that block exit)")
    print("day   template  rotated  other  proceed-band docs")
    for d in W.DAYS:
        g = [x for x in D if x["day"] == d]
        sil = Counter(x["cause"] for x in g if x["silent"])
        print(f"{d}   {sil['broker template, date received']:8} {sil['rotated fax, no intake record']:8} "
              f"{sil['other agent error']:6} {sum(1 for x in g if x['band'] == 'proceed'):8}")
    for c, fx in U.FIX_OF.items():
        print(f"clean intake days after fix: {c} (fix day {fx}): {U.clean_days(D, c, fx)}")
    prc = [x for x in D if x["band"] == "proceed"]; sp = sum(x["silent"] for x in prc)
    lo, hi = wilson(sp, len(prc))
    print(f"silent on proceed, whole window: {sp} of {len(prc)} = {sp / len(prc):.2%} ({lo:.2%} to {hi:.2%})")
    prc = [x for x in prc if x["day"] >= W.ROUTER_V11]; sp = sum(x["silent"] for x in prc)
    lo, hi = wilson(sp, len(prc))
    print(f"silent on proceed, days 151 to 153: {sp} of {len(prc)} = {sp / len(prc):.2%} ({lo:.2%} to {hi:.2%})")
elif what == "streams":
    st = U.streams(D)
    print(f"six streams on the {st['extracted']} extracted agent errors (13 untyped faxes never reached extraction)")
    for s in W.STREAMS:
        print(f"  {s:20} caught {st['catch'][s]:3}")
    print(f"caught by at least one stream: {st['union']} of {st['extracted']} ({st['union'] / st['extracted']:.0%})")
    print(f"other agent errors: {st['other_union']} of {st['other']} caught ({st['other_union'] / st['other']:.0%})")
    print("missed by every stream, by cause: " + ", ".join(f"{c} {n}" for c, n in st["allmiss"].most_common()))
    print(f"pairwise phi between misses on other agent errors: max {st['max_phi']:.2f}, "
          f"mean {sum(p for *_, p in st['pairs']) / len(st['pairs']):.2f}")
    top = sorted(st["pairs"], key=lambda p: -abs(p[2]))[:3]
    for a, b, p in top:
        print(f"  {a} / {b}: {p:+.2f}")
elif what == "gate":
    rows, dec, since = U.gate(D)
    print("Shadow Exit · Caldwell rc-1 · rule fixed day 141, bars day 154, read day 157")
    U.print_gate(rows, dec)
    print("conditions carried into live:")
    print("  C-1 broker-template date received: review band checks every template first notice, first 10 live intake days (Lena Ortiz)")
    print("  C-2 S-4 interval: audit-live-400 over the first 10 live intake days must bring the upper bound to 1.2% or less, or the proceed band returns to shadow (Owen Pryce measures, Anne Kessler decides)")
    print("cutover: day 158, all four in-scope types; shadow tap kept on a 5% blind sample for one Exhibit E month")
    json.dump(dict(rows=rows, decision=dec, since={s: v[:2] for s, v in since.items()}), open("output/gate_caldwell.json", "w"))
elif what == "holiday":
    _, _, since = U.gate(D)
    rates = {s: k / n for s, (k, n, _) in since.items()}  # rc-1 as shipped: each stratum since its last change
    week1 = [x for x in D if x["day"] <= 146]
    H = W.holiday_week(rates)
    win = week1 + H
    ch = [(149, "rc-1h build (all strata)", tuple(W.STRATA))]
    print("FAILURE INJECTION · year-end intake mix replayed through a build that regressed on paper channels")
    print(f"{'stratum':22} {'ref mix':>8} {'holiday':>8} {'n':>5} {'agree':>7}")
    for s in W.STRATA:
        g = [x for x in H if x["stratum"] == s]; k = sum(1 for x in g if x["cause"] is None)
        print(f"{s:22} {W.REFERENCE[s]:8.0%} {len(g) / len(H):8.0%} {len(g):5} {pct(k, len(g)):>7}")
    v, daily = U.naive(win, since=149)
    print("daily agreement after the change: " + ", ".join(f"{d} {a:.1%}" for d, a in daily))
    print(f"naive rule (five consecutive intake days >= 85% since the change): {v}")
    rows, dec, since = U.gate(win, changes=ch, only=("G-1", "G-2", "G-3", "G-4"), scorecard=False)
    print("Shadow Exit checks G-1 to G-4 on the same ten days:")
    U.print_gate(rows, dec)
    k, n = sum(1 for x in H if x["cause"] is None), len(H)
    print(f"holiday week raw {k / n:.1%}; at the reference mix {W.reweighted(W.by_stratum(H)):.1%}; "
          f"fax+mail documents {sum(1 for x in H if x['stratum'] in W.REGRESSION)} of {n}")
    json.dump(dict(daily=daily, raw=k / n, rw=W.reweighted(W.by_stratum(H)),
                   mix={s: W.mix_of(H)[s] for s in W.STRATA}, ref=W.REFERENCE,
                   window_mix=W.mix_of(D)), open("output/holiday.json", "w"))
elif what == "greystone":
    G = W.greystone_window()
    print("Greystone · prior-authorization drafts in shadow, clinic days 1 to 20 (from day 131); drafts never shown")
    print("day  n   agree   class mix (no-auth/standard/portal/letter)")
    daily = []
    for d in W.G_DAYS:
        g = [x for x in G if x["day"] == d]; k = sum(x["agree"] for x in g)
        c = Counter(x["cls"] for x in g); daily.append((d, len(g), k / len(g)))
        print(f"{d:3} {len(g):3} {k / len(g):7.1%}   {'/'.join(str(c[x]) for x in W.G_CLASSES)}" + ("  holiday" if d in W.G_HOLIDAY_DAYS else ""))
    hol = [x for x in G if x["day"] in W.G_HOLIDAY_DAYS]
    print(f"holiday week (clinic days 11 to 15): {pct(sum(x['agree'] for x in hol), len(hol))} on {len(hol)} referrals")
    print(f"naive rule (a clinic week at or above 90%): {'GO' if sum(x['agree'] for x in hol) / len(hol) >= 0.90 else 'HOLD'}")
    print(f"{'class':36} {'n':>4} {'agree':>7} {'silent':>7} {'silent upper':>13}")
    per = {}
    for c in W.G_CLASSES:
        g = [x for x in G if x["cls"] == c]; k = sum(x["agree"] for x in g); sl = sum(x["silent"] for x in g)
        per[c] = (k, len(g), sl)
        print(f"{c:36} {len(g):4} {k / len(g):7.1%} {sl:7} {wilson(sl, len(g))[1]:13.1%}")
    k = sum(x["agree"] for x in G); n = len(G)
    rw = sum(W.G_REF[c] * per[c][0] / per[c][1] for c in W.G_CLASSES)
    pa = [x for x in G if x["cls"] != W.G_CLASSES[0]]; sl = sum(x["silent"] for x in pa)
    print(f"window raw {k / n:.1%} on {n}; at the reference mix {rw:.1%}")
    print(f"silent wrong drafts among prior-auth drafts: {sl} of {len(pa)} = {sl / len(pa):.1%} (upper {wilson(sl, len(pa))[1]:.1%})")
    letter = per[W.G_CLASSES[3]][1]; need = 60 - letter; per_day = W.G_REF[W.G_CLASSES[3]] * 22
    print("Shadow Exit (Greystone, bars by Michael Hart): coverage >= 60 per class: FAIL (letter n="
          f"{letter}); silent prior-auth upper <= 5%: {'pass' if wilson(sl, len(pa))[1] <= 0.05 else 'FAIL'}; "
          f"reweighted >= 80%: {'pass' if rw >= 0.80 else 'FAIL'}")
    print(f"decision: HOLD (stays in shadow); letter class needs {need} more at {per_day:.1f} a clinic day = "
          f"{-(-need // per_day):.0f} more clinic days at the normal mix")
    json.dump(dict(daily=daily, per=per, rw=rw, raw=k / n), open("output/greystone.json", "w"))
