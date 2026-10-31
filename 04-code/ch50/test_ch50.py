"""Chapter 50 lab tests: the numbers the chapter quotes."""
import _paths  # noqa: F401
import memo, classify, committee, shadowrun, boundary, gateway, execpack, world as W
from fieldkit import modelrisk as M
from fieldkit.gates import pack


def test_formats_and_standards():
    assert len(W.FORMATS) == 12 and len(W.STANDARDS) == 3 and sum(W.PACKAGES.values()) == 638


def test_spread_ratios():
    store, ext, calc = memo.spread()
    v = {r: store.nodes[c].attrs["value"] for r, c in calc.items()}
    assert v == {"dscr": 1.27, "debt_to_ebitda": 3.2, "current_ratio": 1.52, "tnw": 11100}
    assert all(r[4] == "pass" for r in memo.covenant_lines(store, calc))


def test_crossfoot_quarantine():
    bad = dict(W.STATEMENT, fields=dict(W.STATEMENT["fields"], equity=(13040, 2)))
    assert memo.crossfoot(W.STATEMENT) == [] and memo.crossfoot(bad)


def test_injections_caught():
    for inj, where in (("model_ratio", "gate"), ("model_calc", "lineage"), ("unlabeled", "currency")):
        store, ext, calc = memo.spread()
        g, c, lin = memo.check(store, memo.draft(store, ext, calc, inject=inj))
        assert {"gate": g, "lineage": lin, "currency": c}[where]
    store, ext, calc = memo.spread()
    assert memo.check(store, memo.draft(store, ext, calc)) == ([], [], [])


def test_mutation_run():
    assert committee.mutation_run() == (120, 120, 40, 40)


def test_classification():
    a, b = classify.run()
    assert M.counts(b) == {M.FULL: 5, M.REGISTERED: 2, M.NOT_MODEL: 7} and len(M.plan_for(b)) == 75
    assert len(M.plan_for(a)) == 70 and len(M.diff(a, b)) == 5


def test_submissions():
    t1, p1 = committee.tracker(126)
    assert len(p1.lint()) == 27 and t1.records["Model-Risk Approval"].status() == "blocked"
    t2, p2 = committee.tracker(158)
    assert p2.lint() == [] and t2.records["Model-Risk Approval"].status() == "passed with conditions"
    assert [s for _, s, _, _ in t2.effective()][:4] == ["passed", "passed", "passed with conditions", "passed with conditions"]


def test_shadow():
    f = shadowrun.funnel(shadowrun.records())
    assert (f["seen"], f["human"], f["agree"], f["silent"], f["escalate"]) == (638, 600, 546, 12, 38)


def test_boundary():
    b = boundary.release_one()
    assert b.check("draft_memo", "production")[0] and not b.check("write_origination", "production")[0]


def test_gateway_and_pack():
    assert sum(bool(p) for _, p in gateway.audit(gateway.TRACES["build (day 118)"])) == 2
    assert not any(p for _, p in gateway.audit(gateway.TRACES["go-live (day 171)"]))
    assert pack(execpack.STATES[118])["counts"] == {"present": 3, "partial": 2, "missing": 3}
    assert pack(execpack.STATES[171])["counts"] == {"present": 7, "partial": 1, "missing": 0}
