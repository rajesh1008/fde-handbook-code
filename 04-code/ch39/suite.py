"""The shadow evaluation suite: funnel (Signature 14), adjudication, streams, and the Shadow Exit rule.
Deterministic stand-in. Every function takes plain document dicts from world.py."""
import math
from collections import Counter
import _paths  # noqa: F401
from fieldkit.evals import wilson
import world as W

SCORECARD = [  # Chapter 31, Anne Kessler's bars written day 154; results from rc-1 on day 156
    ("S-1", "field accuracy, gold-heldout", "80%", "84.0% (82.4% to 85.6%)", "pass"),
    ("S-2", "critical fields", "80%", "83.9%", "pass"),
    ("S-3", "agreement with keyed claims", "85%", "88.0% (86.7% to 89.2%)", "pass"),
    ("S-4", "post-review error, audit-shadow-400", "1.2% or less", "1.10%, upper bound 1.47%", "condition"),
    ("S-5", "first notices with no intake record", "0", "0 since day 150", "see G-5"),
    ("S-6", "retention and erasure drill", "pass", "pass", "pass"),
    ("S-7", "model spend per routed document", "$0.05 or less", "$0.0338", "pass")]
SIGNERS = [("Anne Kessler", "business owner, signs the gate"), ("Priya Natarajan", "system owner, cutover"),
           ("Owen Pryce", "quality engineering, measurement")]
FIX_OF = {"rotated fax, no intake record": W.ORIENTATION_FIX, "broker template, date received": W.TEMPLATE_FIX}


def funnel(docs):
    n = len(docs); band = Counter(x["band"] for x in docs)
    agree = sum(1 for x in docs if x["cause"] is None)
    cause = Counter(x["cause"] for x in docs if x["cause"])
    wrong = [x for x in docs if x["wrong"]]
    silent = sum(1 for x in wrong if x["silent"])
    return dict(seen=n, decided=n - band["none"], proceed=band["proceed"], review=band["review"],
                escalate=band["escalate"], none=band["none"], human=n, agree=agree, disagree=n - agree,
                equivalent=cause["equivalent format"], human_wrong=cause["clerk keying error, agent right"],
                agent_wrong=len(wrong), loud=len(wrong) - silent, silent=silent,
                escalations=band["escalate"] + band["none"])


def phi(a, b):
    n11 = sum(1 for x, y in zip(a, b) if x and y); n10 = sum(1 for x, y in zip(a, b) if x and not y)
    n01 = sum(1 for x, y in zip(a, b) if y and not x); n00 = len(a) - n11 - n10 - n01
    den = math.sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00))
    return (n11 * n00 - n10 * n01) / den if den else 0.0


def streams(docs):
    ext = [x for x in docs if x["wrong"] and x["band"] != "none"]
    other = [x for x in ext if x["cause"] == "other agent error"]
    catch = {s: sum(1 for x in ext if s in x["streams"]) for s in W.STREAMS}
    union = sum(1 for x in ext if x["streams"])
    miss = {s: [s not in x["streams"] for x in other] for s in W.STREAMS}
    pairs = [(a, b, phi(miss[a], miss[b])) for i, a in enumerate(W.STREAMS) for b in W.STREAMS[i + 1:]]
    allmiss = Counter(x["cause"] for x in ext if not x["streams"])
    return dict(extracted=len(ext), catch=catch, union=union, other=len(other),
                other_union=sum(1 for x in other if x["streams"]), pairs=pairs,
                max_phi=max(p for _, _, p in pairs), allmiss=allmiss)


def last_change(stratum, changes):
    ds = [d for d, _, touched in changes if stratum in touched or touched == "all"]
    return max(ds) if ds else None


def clean_days(docs, cause, fix):
    days = sorted({x["day"] for x in docs})
    seen = [d for d in days if d >= fix and any(x["day"] == d and x["cause"] == cause for x in docs)]
    return 0 if seen else sum(1 for d in days if d >= fix)


def gate(docs, *, changes=W.CHANGES, min_days=10, coverage=60, tvd_max=0.10, bar=0.85, clean=4,
         silent_upper=0.03, phi_max=0.30, routing_change=W.ROUTER_V11, only=None, scorecard=True):
    days = sorted({x["day"] for x in docs}); weeks = sorted({d // 7 for d in days})
    rows = []
    def add(code, name, measured, need, verdict):
        if only is None or code in only:
            rows.append((code, name, measured, need, verdict))
    add("G-1", "window length", f"{len(days)} intake days, {len(weeks)} calendar weeks, {len(changes)} logged changes",
        f">= {min_days} days, >= 2 weeks", "pass" if len(days) >= min_days and len(weeks) >= 2 else "FAIL")
    since = {}
    for s in W.STRATA:
        lc = last_change(s, changes)
        g = [x for x in docs if x["stratum"] == s and (lc is None or x["day"] >= lc)]
        since[s] = (sum(1 for x in g if x["cause"] is None), len(g), lc)
    low = min(W.STRATA, key=lambda s: since[s][1])
    add("G-2", "coverage per stratum since its last change", f"lowest: {low} n={since[low][1]}",
        f">= {coverage} each", "pass" if since[low][1] >= coverage else "FAIL")
    k, n, raw, lo, hi = W.agreement(docs)
    mixd = W.tvd(W.mix_of(docs), W.REFERENCE)
    rw = W.reweighted({s: since[s][:2] for s in W.STRATA})
    add("G-3", "agreement at the reference mix", f"raw {raw:.1%}, mix distance {mixd:.2f}, reweighted {rw:.1%}",
        f">= {bar:.0%} reweighted", "pass" if rw >= bar else "FAIL")
    last5 = [x for x in docs if x["day"] in days[-5:]]
    l5 = W.agreement(last5)[2]
    add("G-4", "stability, last five intake days", f"{l5:.1%} vs window {lo:.1%} to {hi:.1%}",
        "inside the window interval", "pass" if lo <= l5 <= hi else "FAIL")
    prc = [x for x in docs if x.get("band") == "proceed" and x["day"] >= routing_change]
    sp = sum(1 for x in prc if x["silent"]); up = wilson(sp, len(prc))[1]
    conds = []
    worst = "pass"
    for cause, fix in FIX_OF.items():
        if any(x["cause"] == cause and x["silent"] for x in docs):
            cd = clean_days(docs, cause, fix)
            if cd < clean:
                conds.append(f"{cause}: {cd} clean days after day {fix} fix")
                worst = "condition"
    if up > silent_upper:
        worst = "FAIL"
    add("G-5", "silent errors", f"proceed since day {routing_change}: {sp} of {len(prc)}, upper {up:.2%}; "
        + ("; ".join(conds) if conds else "every fixed cause clean"), f"upper <= {silent_upper:.0%}; {clean} clean days", worst)
    if "band" in docs[0] and any(x["streams"] for x in docs):
        st = streams(docs)
        add("G-6", "six streams ran before output", f"{st['union']} of {st['extracted']} caught, max phi {st['max_phi']:.2f}",
            f"max phi <= {phi_max}", "pass" if st["max_phi"] <= phi_max else "FAIL")
    if scorecard:
        add("G-7", "scorecard S-1 to S-7", "S-4 upper bound 1.47% above the 1.2% bar; others pass", "all bars", "condition")
        add("G-8", "signatures", ", ".join(p for p, _ in SIGNERS), "named owners", "pass")
    verdicts = [r[4] for r in rows]
    decision = "HOLD" if "FAIL" in verdicts else ("GO WITH CONDITIONS" if "condition" in verdicts else "GO")
    return rows, decision, since


def naive(docs, bar=0.85, run=5, since=None):
    days = sorted({x["day"] for x in docs if since is None or x["day"] >= since})
    daily = [(d, W.agreement([x for x in docs if x["day"] == d])[2]) for d in days]
    streak = 0
    for d, a in daily:
        streak = streak + 1 if a >= bar else 0
        if streak >= run:
            return "GO", daily
    return "HOLD", daily


def print_gate(rows, decision):
    print(f"{'check':5} {'what':42} {'verdict':10} measured  |  needed")
    for code, name, m, need, v in rows:
        print(f"{code:5} {name:42} {v:10} {m}  |  {need}")
    print(f"decision: {decision}")
