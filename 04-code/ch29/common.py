"""Shared pieces of the Chapter 29 lab: the system configuration a run sees, the checks of the five layers, and the
pyramid that wires them. Deterministic stand-in; see world.py."""
import time
import _paths  # noqa: F401
import world as W
from fieldkit.pyramid import (Layer, Pyramid, MergeGate, Metric, PASS, FAIL, INCONCLUSIVE, paired_slices,
                              slice_verdict)
from fieldkit.evals import CustomerGate

LAYERS = [Layer(1, "unit", "every rule and pure function: one case that passes, one that must fail", "every commit", 30, 0.0),
          Layer(2, "component", "every model-backed component on every slice of the customer's set", "every pull request that changes behavior", 900, 20.0),
          Layer(3, "integration", "every external contract and every gateway failure mode, replayed", "every merge to main, nightly", 600, 1.0),
          Layer(4, "system", "every scenario template end to end, live through the gateway", "weekly and before any release", 3600, 150.0),
          Layer(5, "operational", "the live stream: canaries, judge check, drift replay", "continuous, reviewed weekly", 0, 12.0)]
PATH_RULES = [("prompts/", "prompt"), ("rules/", "rule"), ("router/thresholds", "threshold"), ("retrieval/", "retrieval"),
              ("models/pins", "model"), ("gold/", "gold"), ("requirements", "dependency"), ("infra/", "infra"),
              ("docs/", "docs")]

BASE = dict(prompt="p8.3", datelib=3.9, router_floor=0.47, failclosed=True, acl_filter=True, lifecycle_filter=True,
            v118_map_ok=True, retry_inside_intent=True, rotation_handled=True, breaker_steps=12, judge_fp_rate=0.12,
            drift_window_days=7, faith_subset="stratified40", judge_rule="40 docs, TNR >= 0.80")


def gate_owner():
    return MergeGate("Anne Kessler (item sign-off in the change ticket)")


# ------------------------------------------------------------------------------------------------ layer one
def rules_run(sysc):
    fails = {}
    for c in W.rule_cases():
        ok = True
        if c["dated"]:
            ok = W.parse_date(c["date"], sysc["datelib"]) == W.parse_date(c["date"], 3.9) and \
                W.parse_date(c["date"], 3.9)[1] == c["m"]
        fam = c["family"]
        if fam == "V-118 cause code" and not sysc["v118_map_ok"] and c["i"] % 4 == 0:
            ok = False
        if fam == "permission filter" and not sysc["acl_filter"] and c["i"] % 2 == 0:
            ok = False
        if fam == "router gates" and (not sysc["failclosed"] or sysc["router_floor"] < 0.47) and c["i"] % 3 == 0:
            ok = False
        if not ok:
            fails[fam] = fails.get(fam, 0) + 1
    return fails


def chk_rules(sysc):
    t0 = time.perf_counter(); fails = rules_run(sysc); real = time.perf_counter() - t0
    n = sum(W.FAMILIES.values()); bad = sum(fails.values())
    modeled = 3.2 + 0.014 * n
    return (FAIL if bad else PASS, f"{n - bad} of {n} rule cases pass" + (f"; failing {fails}" if bad else ""),
            modeled, 0.0, dict(n=n, failing=bad, by=fails, real_seconds=real))


# ------------------------------------------------------------------------------------------------ layer two
def slice_table(before, after, margin=0.02, alpha=0.05):
    rows = []
    for key, fn in (("stratum", lambda k: W.STRATUM[k[0]]), ("stratum x field", lambda k: (W.STRATUM[k[0]], k[1]))):
        for s, c in sorted(paired_slices(before, after, fn).items(), key=lambda kv: str(kv[0])):
            v, p = slice_verdict(c["n"], c["gains"], c["losses"], margin, alpha)
            rows.append(dict(kind=key, slice=s, verdict=v, p=p, **c))
    return rows


def chk_extractor(sysc, margin=0.02, alpha=0.05):
    before, after = W.extract("p8.3"), W.extract(sysc["prompt"])
    if sysc["prompt"] == "p8.3" and sysc.get("drop_mail_date"):
        after = {k: (v and not (W.STRATUM[k[0]] == "first notice, mail" and k[1] == "date_received"))
                 for k, v in after.items()}
    agg = Metric("aggregate field accuracy", sum(before.values()) / len(before), sum(after.values()) / len(after))
    rows = slice_table(before, after, margin, alpha)
    bad = [r for r in rows if r["verdict"] != PASS]
    v = FAIL if (agg.verdict() == FAIL or any(r["verdict"] == FAIL for r in bad)) else (INCONCLUSIVE if bad else PASS)
    detail = f"aggregate {agg.before:.1%} -> {agg.after:.1%}; slices not passing: " + \
        (", ".join(f"{r['slice']} {r['verdict']}" for r in bad) if bad else "none")
    n = len(W.gold_test())
    sec = n * 2 * W.CALL_SECONDS / W.CONCURRENCY + 60
    return v, detail, sec, n * W.doc_cost(), dict(agg=(agg.before, agg.after), rows=rows, before=before, after=after)


def faith_subset(kind):
    qs = W.questions()
    if kind == "first40":
        return qs[:40]
    by = {}
    for q in qs:
        by.setdefault(q[1], []).append(q)
    want = {"procedure": 14, "form or code": 8, "version-sensitive": 8, "cross-document": 6, "not in the documents": 4}
    return [q for t, n in want.items() for q in by[t][:n]]


def faithfulness(qs, lifecycle):
    claims = [c for q, t in qs for c in W.answer_claims(q, t, lifecycle)]
    sup = sum(c[1] for c in claims); sv = sum(c[2] for c in claims)
    return dict(claims=len(claims), supported=sup, rate=sup / max(1, len(claims)), superseded=sv)


def chk_faith(sysc, full=False):
    qs = W.questions() if full else faith_subset(sysc["faith_subset"])
    b = faithfulness(qs, True); a = faithfulness(qs, sysc["lifecycle_filter"])
    m = Metric("faithfulness", b["rate"], a["rate"], tolerance=0.005)
    bad = m.verdict() == FAIL or a["superseded"] > 0
    return (FAIL if bad else PASS, f"{len(qs)} questions, faithfulness {a['rate']:.1%}, superseded citations "
            f"{a['superseded']}", 20 + len(qs) * 4 / W.CONCURRENCY * 2, len(qs) * W.q_cost(), dict(before=b, after=a))


# ---------------------------------------------------------------------------------------------- layer three
INTEGRATION = [("claims-core contract", 22), ("gateway 429 then success", 8), ("key rotation mid-run", 6),
               ("mailroom duplicate delivery", 10), ("claims-core timeout, compensation", 8), ("log and identity", 10)]


def chk_integration(sysc):
    fails = {}
    if not sysc["retry_inside_intent"]:
        fails["gateway 429 then success"] = 8
    if not sysc["rotation_handled"]:
        fails["key rotation mid-run"] = 6
    n = sum(k for _, k in INTEGRATION); bad = sum(fails.values())
    return (FAIL if bad else PASS, f"{n - bad} of {n} replayed integration cases pass" + (f"; failing {fails}" if bad else ""),
            150 + 0.5 * n, 0.03 * n / 4, dict(n=n, by=fails))


# ----------------------------------------------------------------------------------------------- layer four
TEMPLATES = 40
PER_TEMPLATE = 30
RUNAWAY_TEMPLATES = (12, 27, 33)      # claims-core returns the same error forever


def scenario_ids():
    return [(t, v) for t in range(1, TEMPLATES + 1) for v in range(PER_TEMPLATE)]


def scenario_outcome(t, v, sysc, oracle_fixed=False, broken_fixed=False):
    """Returns 'pass' or the reason it fails, as triage later classifies it."""
    if not broken_fixed and t == 31 and v % 15 == 0:
        return "broken scenario"          # stub returns a claim status claims-core does not have
    if not oracle_fixed and (t, v) in ((4, 7), (9, 21), (16, 3), (22, 18), (38, 11)):
        return "oracle defect"            # expected value in the case is wrong
    if t == 7 and v % 5 == 0:
        return "agent defect: two letters in one envelope become one claim"
    if t == 14 and v % 6 == 1:
        return "agent defect: police report reference lost when pages arrive out of order"
    if t == 19 and v % 10 == 3:
        return "agent defect: duplicate fax during key rotation opens a second claim"
    if t == 25 and v % 10 == 5:
        return "agent defect: handwritten loss date on page two ignored"
    if t == 29 and v % 10 == 8:
        return "agent defect: loss location taken from the broker's letterhead"
    if t == 36 and v % 15 == 2:
        return "agent defect: claimant name truncated at 40 characters"
    if t in RUNAWAY_TEMPLATES and v % 3 == 0 and sysc["breaker_steps"] > 12:
        return "agent defect: loop exceeds step budget"
    return "pass"


def chk_system(sysc, baseline=None):
    out = {s: scenario_outcome(*s, sysc, oracle_fixed=True, broken_fixed=True) for s in scenario_ids()}
    base = baseline or {s: scenario_outcome(*s, BASE, oracle_fixed=True, broken_fixed=True) for s in scenario_ids()}
    new = [s for s in out if out[s] != "pass" and base[s] == "pass"]
    docs = len(out) * 1.6
    sec = docs * 2 * W.CALL_SECONDS / 16 + 600
    fa = chk_faith(sysc, full=True)
    bad = bool(new) or fa[0] == FAIL
    return (FAIL if bad else PASS, f"{len(out)} scenarios, {sum(v != 'pass' for v in out.values())} failing, "
            f"{len(new)} new against the accepted baseline; full question set: {fa[1]}", sec, docs * W.doc_cost() + 201 * W.doc_cost() + 150 * W.q_cost(),
            dict(new=len(new), out=out))


# ----------------------------------------------------------------------------------------------- layer five
def judge_check(sysc, rule=None):
    rule = rule or sysc["judge_rule"]
    if rule.startswith("20"):
        F = 9; fp = round(sysc["judge_fp_rate"] * F)
        bad = fp > 3
        return bad, f"20 docs: {fp} false passes of {F} expert fails (suspect above 3)"
    F = 19; fp = round(sysc["judge_fp_rate"] * F); tnr = (F - fp) / F
    return tnr < 0.80, f"40 docs: TNR {tnr:.2f} on {F} expert fails (suspect below 0.80)"


def chk_operational(sysc):
    bad_j, dj = judge_check(sysc)
    psi = 0.31 if sysc["drift_window_days"] <= 7 else 0.31 * 7 / sysc["drift_window_days"]
    drift_ok = psi >= 0.2                # the replayed day-143 template change must trip it
    canary = 10
    bad = bad_j or not drift_ok
    return (FAIL if bad else PASS, f"canaries {canary} of {canary}; judge check {dj}; drift replay PSI {psi:.2f} "
            f"({'trips' if drift_ok else 'does not trip'} at 0.20)", 0, 10 * W.doc_cost() + 0.9, dict(psi=psi))


def build():
    p = Pyramid(LAYERS)
    p.add(1, "rule regression", chk_rules)
    p.add(2, "extractor slices", chk_extractor)
    p.add(2, "retrieval faithfulness", chk_faith)
    p.add(3, "integration replay", chk_integration)
    p.add(4, "scenario simulator", chk_system)
    p.add(5, "operational checks", chk_operational)
    return p


def aggregate_gate(before, after):
    g = CustomerGate("Caldwell Mutual", "Anne Kessler", "Anne Kessler's adjusters", "gold-set-300 test (201)",
                     W.CRITICAL)
    return g.check(before, after)
