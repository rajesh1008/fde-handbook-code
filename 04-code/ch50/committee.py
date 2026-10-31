"""Listings 50.6 and 50.8: the model-risk pack at submission one (day 118, returned day 126) and submission two
(day 152, approved day 158). Pack lint, metric computability, validator questions, the gate records and the
mutation run behind the numeric-gate criterion. Uses fieldkit.modelrisk and fieldkit.gates unchanged."""
import sys
import _paths  # noqa: F401
from fieldkit import modelrisk as M
from fieldkit import gates as G
import world as W, classify, memo, shadowrun

CLASSES = classify.run()[1]
FULL = [k.cid for k in CLASSES if k.outcome == M.FULL]
REG = [k.cid for k in CLASSES if k.outcome == M.REGISTERED]
CODE = [k.cid for k in CLASSES if k.outcome == M.NOT_MODEL]
VENDOR = FULL + REG
E = M.Evidence


def evidence(sub):
    ev = [E("purpose", "*", "reads and drafts the financial analysis and risk factors of a commercial credit memo",
            "Helen Marsh", "use statement", "pack s1 sec 1")]
    for c in FULL:
        ev += [E("conceptual_soundness", c, "design: deterministic first, model last", "Helen Marsh", "design review", "pack sec 2"),
               E("development_data", c, "no training on bank data; prompts built on synthetic packages", "Northlight", "day 4 grant", "pack sec 3")]
    for c in VENDOR:
        ev += [E("outcomes", c, "agreement 172/200 on Northlight-scored memos" if sub == 1 else
                 "agreement 546/600 on credit review scoring", "Northlight" if sub == 1 else "Harbourline credit review",
                 "200 synthetic memos" if sub == 1 else "600 shadow memos", "pack sec 4"),
               E("limits", c, "no recommendation; quarantined statements get no draft", "Helen Marsh", "boundary", "Schedule D")]
    for c in REG:
        ev += [E("vendor_due_diligence", c, "third-party risk file", "Harbourline third-party risk", "provider", "TPR file"),
               E("design_review", c, "supporting use only", "Helen Marsh", "design", "pack sec 2"),
               E("sensitivity", c, "retrieval recall by policy chapter", "Northlight", "policy set", "pack sec 5"),
               E("stability", c, "repeat retrieval identical 20 of 20", "Northlight", "50 queries", "pack sec 5")]
    for c in VENDOR:
        ev.append(E("monitoring", c, "monthly metric", "Helen Marsh", "metric set", "pack sec 7"))
    for c in CODE:
        ev.append(E("change_control", c, "release pipeline, two-person review", "Martin Shaw", "pipeline", "CAB record"))
    if sub == 2:
        for c in FULL:
            ev += [E("benchmark", c, "challenger: the officer's own memo, 600 shadow memos", "Harbourline credit review", "shadow", "SE record"),
                   E("sensitivity", c, "agreement and silent misses per standard and per format", "Harbourline credit review", "600 memos", "pack sec 5"),
                   E("stability", c, STABILITY.get(c, "numbers identical across 20 runs (computed by code)"), "Helen Marsh", "20 runs x 50 packages", "pack sec 5")]
        for c in VENDOR:
            ev.append(E("change_control", c, "version pinned at the bank gateway; 90 days' notice; revalidation trigger; "
                        "fallback: drafting off, spread continues", "Helen Marsh", "Schedule D clause 6", "contract"))
    return ev


def _runs(n_same, n=1000):
    return ["a"] * n_same + ["b"] * (n - n_same)


STABILITY = {c: f"modal agreement {M.repeat_agreement(_runs(k))[0]:.1%} over 1,000 repeat runs"
             for c, k in (("H03", 996), ("H05", 991), ("H08", 988))}


def metrics(sub):
    hl, nl = "Harbourline Bank", "Northlight"
    if sub == 1:
        code = M.Input("evaluation suite code", nl, "Northlight repository", "svc-northlight-eval")
        return [M.Metric("M1", "agreement with credit review", ">= 90% monthly", "Helen Marsh", ("H10", "H11"),
                         (M.Input("credit review scores", hl, "credit review store"), code))]
    code = M.Input("evaluation suite code", hl, "Harbourline repository (transferred day 140)", "svc-hl-mrm-val")
    lin = M.Input("lineage store", hl, "Harbourline cloud, Canada")
    return [M.Metric("M1", "agreement with credit review, 90 memos a month", "breach at 15", "Helen Marsh", ("H10", "H11"),
                     (M.Input("credit review scores", hl, "credit review store"), code)),
            M.Metric("M2", "numeric gate blocks per 100 drafts", "<= 3", "Helen Marsh", ("H03", "H05", "H08"), (lin, code)),
            M.Metric("M3", "canary set agreement after any provider change", "= previous release", "Helen Marsh",
                     ("H03", "H05", "H08", "H10", "H11", "H12"), (M.Input("canary packages", hl, "validation store"), code)),
            M.Metric("M4", "retrieval recall on policy questions", ">= 95%", "Helen Marsh", ("H09",), (lin, code))]


QUESTIONS = {
    1: [M.ValidatorQuestion("V1", "Which components are models under our policy", "evidence", "Listing 50.5: five full scope"),
        M.ValidatorQuestion("V2", "What is the challenger", "translation", "the officer's own memo, once shadow runs"),
        M.ValidatorQuestion("V3", "What happens when the provider withdraws the model version", "boundary",
                            "the provider controls its schedule")],
    2: [M.ValidatorQuestion("V1", "Which components are models under our policy", "evidence", "Listing 50.5: five full scope"),
        M.ValidatorQuestion("V2", "What is the challenger", "evidence", "546 of 600 against the officer's own memo"),
        M.ValidatorQuestion("V3", "What happens when the provider withdraws the model version", "boundary",
                            "the provider controls its schedule",
                            "pinned at the gateway, 90 days' notice, revalidation trigger, drafting off as fallback")],
}


def mutation_run(n=40):
    """The numeric-gate criterion: 40 synthetic statements, three injections each, plus the clean drafts."""
    caught = clean_ok = 0
    for i in range(n):
        f = {k: (round(v * (0.85 + 0.01 * ((i * 7) % 31))), p) for k, (v, p) in W.STATEMENT["fields"].items()}
        f["total_assets"] = (f["total_liabilities"][0] + f["equity"][0], 2)
        st = dict(W.STATEMENT, fields=f, uri=f"hl-docs://synthetic/{i:03d}.pdf")
        for inj in (None, "model_ratio", "model_calc", "unlabeled"):
            s2, e2, c2 = memo.spread(st)
            claims = memo.draft(s2, e2, c2, inject=inj)
            cl, rel = memo.release(s2, claims)
            p = memo.numeric_gate(s2, claims) + memo.currency_lint(claims) + memo.lineage_check(s2, cl, rel, {st["uri"]: st["sha256"]})
            if inj is None:
                clean_ok += not p
            else:
                caught += bool(p)
    return caught, 3 * n, clean_ok, n


def tracker(asof):
    t = G.Tracker(W.CUSTOMER)
    agree = G.Criterion("agreement", "draft agrees with the officer's memo", 0.90, per="accounting standard", owner="Helen Marsh")
    t.add(G.GateRecord("Architecture Review", [("surface in the suite, brain in the governed cloud", "AR record")],
                       signer="Martin Shaw", decided=W.DAYS["architecture"]))
    t.add(G.GateRecord("Build Complete", [("lab and evaluation suite green", "BC record")], signer="David Okafor",
                       decided=W.DAYS["build_complete"]))
    if asof < W.DAYS["shadow_exit"]:
        t.add(G.GateRecord("Shadow Exit", [("shadow started day 120", "SE plan")], [agree], []))
        sub = 1
    else:
        recs = shadowrun.records(); f = shadowrun.funnel(recs)
        ms = [G.Measurement("agreement", f["agree"], f["human"], "all", measured_by="Harbourline credit review", on="600 memos", day=149)]
        ms += [G.Measurement("agreement", k, n, s, measured_by="Harbourline credit review", on="600 memos", day=149)
               for s, k, n, *_ in shadowrun.by_standard(recs)]
        t.add(G.GateRecord("Shadow Exit", [("600 memos scored", "SE record")], [agree], ms, "David Okafor", W.DAYS["shadow_exit"],
                           conditions=[("score every US GAAP memo in the first 90 live days", "Helen Marsh", 261)],
                           accepted=[("agreement", "US GAAP", "Helen Marsh", W.DAYS["shadow_exit"])]))
        sub = 2
    pack = M.Pack(W.CUSTOMER, f"s{sub}", CLASSES, evidence(sub), metrics(sub))
    have = pack.items() - len(pack.gaps())
    plan = G.Criterion("plan", "every plan item evidenced", 1.0, outcome=False, owner="Helen Marsh")
    gate = G.Criterion("gate", "numeric gate catches injected drafts", 0.99, outcome=False, owner="Helen Marsh")
    caught, n, _, _ = mutation_run() if sub == 2 else (0, 0, 0, 0)
    ms = [G.Measurement("plan", have, pack.items(), kind="log", measured_by="Helen Marsh", on="pack lint")]
    if sub == 1:
        ms.append(G.Measurement("agreement", 172, 200, kind="component test", measured_by="Northlight", on="200 synthetic memos"))
        t.add(G.GateRecord("Model-Risk Approval", [("pack s1", "submission day 118")], [plan, agree], ms))
    else:
        ms.append(G.Measurement("gate", caught, n, kind="component test", measured_by="Helen Marsh", on="120 injected drafts"))
        t.add(G.GateRecord("Model-Risk Approval", [("pack s2", "submission day 152")], [plan, gate], ms, "Helen Marsh",
                           W.DAYS["model_risk"], conditions=[
                               ("revalidate full-scope components within 30 days of a provider version change", "Helen Marsh", 261),
                               ("writes need a separate submission (release two)", "David Okafor", 171)]))
    return t, pack


if __name__ == "__main__":
    sub = int(sys.argv[1])
    asof = W.DAYS["returned"] if sub == 1 else W.DAYS["model_risk"]
    t, pack = tracker(asof)
    lint = pack.lint()
    print(f"submission {sub} (day {W.DAYS['submission_1'] if sub == 1 else W.DAYS['submission_2']}): plan items "
          f"{pack.items()}, evidenced {pack.items() - len(pack.gaps())}, lint findings {len(lint)}")
    groups = {}
    for l in lint:
        key = l.split(" for ")[0] if l.startswith("missing") else "no monitoring metric"
        groups.setdefault(key, []).append(l.split()[-1])
    for k, v in groups.items():
        print(f"  {k:<28} {len(v):>2}  {', '.join(v)}")
    for m, b in M.computability(pack.metrics, "Harbourline Bank", ("svc-northlight-eval",)):
        print(f"  metric {m.mid} {m.name}: " + ("computable by the bank" if not b else "; ".join(b)))
    for q in QUESTIONS[sub]:
        print(f"  {q.qid} [{q.answer_type}] {q.asked}: " + ("; ".join(q.problems()) or (q.compensating or q.answer)))
    if sub == 2:
        c, n, ok, m = mutation_run()
        print(f"  mutation run: {c}/{n} injected drafts caught; {ok}/{m} clean drafts passed")
    for line in t.records["Model-Risk Approval"].evaluate():
        print(f"  Model-Risk Approval {line.key:<10} {line.scope:<8} {line.verdict:<10} {line.detail}")
    if "Shadow Exit" in t.records:
        for line in t.records["Shadow Exit"].evaluate():
            print(f"  Shadow Exit {line.key:<10} {line.scope:<8} {line.verdict:<10} {line.detail}")
    print("gate stack:")
    for g, st, day, note in t.effective():
        print(f"  {g:<20} {st:<24} {'' if day is None else 'day ' + str(day):<8} {note}")
