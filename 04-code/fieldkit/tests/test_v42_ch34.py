"""fieldkit v4.2: procurement, legal and the contract (Chapter 34)."""
from fieldkit.contract import (Clause, trigger_findings, extract, lint, Dependency, Decision, CostLine, year_one_margin,
                               renewal_weighted_two_year, binom_sf, wilson_upper, design_service_level,
                               point_rule, zero_tolerance_breach, services_net)

ACC = Clause("A", "Northlight warrants that the System will be 98% accurate, as determined by Acme. "
                  "For each calendar month in which it is not, Northlight shall credit 50% of the monthly fee.")
GOOD = Clause("B", "Northlight warrants that the post-review document error, scored by Acme's adjusters on a "
                   "sample of 400 documents each calendar month, will not reach 2.25%. For each month in breach "
                   "Northlight shall credit 5% of the monthly subscription fee.")


def test_extract_attaches_credit_and_finds_customer_obligations():
    cs, cust, none = extract([ACC, Clause("C", "Acme shall pay within 60 days."), Clause("D", "Law of Utopia.")])
    assert [c.cid for c in cs] == ["A.1"] and cs[0].kind == "service level" and cs[0].metric == "accuracy"
    assert cust == [("C", "Acme shall pay within 60 days.")] and none == ["D"]


def test_unmeasurable_and_unilateral_but_naive_passes():
    cs, _, _ = extract([ACC])
    assert lint(cs, naive=True)[0].findings == []
    kinds = [f[0] for f in lint(cs)[0].findings]
    assert kinds == ["UNMEASURABLE", "UNILATERAL MEASURE"]


def test_measurable_clause_is_clean():
    cs, _, _ = extract([GOOD])
    c = lint(cs)[0]
    assert c.params["sample"] == 400 and c.params["scorer"].startswith("Acme") and c.findings == []
    assert c.remedy == "credit 5% monthly fee"


def test_dependency_unless_excluded_and_decisions():
    a = Clause("E", "Northlight shall make the System available 99.9% of the time, measured at the console, "
                    "in each calendar month, including the gateway.")
    b = Clause("F", "Northlight shall make the System available 99.5% of the time, measured at the service "
                    "boundary, in each calendar month, excluding gateway outages.")
    dep = [Dependency("gateway", "Acme architecture")]
    dec = [Decision("R2", "monitoring report", "customer produces it", "CONFLICT")]
    ca, _, _ = extract([a, b, Clause("G", "Northlight shall deliver a monthly monitoring report.")])
    out = lint(ca, dependencies=dep, decisions=dec)
    assert ("UNCONTROLLED INPUT" in [f[0] for f in out[0].findings])
    assert all(f[0] != "UNCONTROLLED INPUT" for f in out[1].findings)
    assert out[2].findings[0][0] == "CONFLICT"


def test_margin_and_renewal_weighting():
    m, rev, cost = year_one_margin({"s": 100.0}, [CostLine("a", "a", 108.0, "estimated")])
    assert round(m, 2) == -0.08 and rev == 100 and cost == 108
    assert renewal_weighted_two_year(-8, 50, 0.8) == 32


def test_binomial_and_wilson():
    assert abs(binom_sf(1, 10, 0.1) - (1 - 0.9 ** 10)) < 1e-12
    assert binom_sf(0, 5, 0.3) == 1.0 and binom_sf(6, 5, 0.3) == 0.0
    assert 0.0254 < wilson_upper(4, 400) < 0.0255


def test_design_beats_point_rule():
    sl = design_service_level("x", "error", "s", 0.01, 0.03)
    assert sl.p_breach(0.01) <= 0.05 and sl.p_breach(0.03) >= 0.80
    pr = point_rule("x", "error", "s", 0.01, 0.03, 400, 0.01)
    assert pr.p_breach(0.01) > 0.3


def test_zero_tolerance_and_services_net():
    assert abs(zero_tolerance_breach(0.01, 60) - (1 - 0.99 ** 60)) < 1e-12
    assert services_net(1000, 150, "fixed", fee=200000) == 50000
    assert services_net(2000, 150, "tm", bill_rate=260, cap=450000) == 150000


def test_triggers_and_no_cap():
    out = trigger_findings([("G1", "Acme will accept the System when it performs to Acme's satisfaction."),
                            ("G2", "Acme will accept the System when it meets the criteria in Exhibit A."),
                            ("G3", "Acme will accept it per Exhibit A, or ten business days after certification.")])
    assert [o[1] for o in out] == ["UNDEFINED TRIGGER", "NO DEEMED ACCEPTANCE"]
    cs, _, _ = extract([Clause("L", "Northlight shall indemnify Acme for any harm arising from the System.")])
    assert lint(cs)[0].findings == [("UNCAPPED", "no cap stated")]
