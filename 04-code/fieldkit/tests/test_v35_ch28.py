"""fieldkit v3.5 (Chapter 28): guardrails."""
import pytest
from fieldkit.guardrails import (RuleCard, GuardrailSuite, RuleTest, test_rules as run_rule_tests, Budget,
                                 CircuitBreaker, FleetBreaker, Statement, elicitation_report, Decision, Verdict)


def card(rid, kind="output", effect="block", **kw):
    base = dict(statement="s", kind=kind, source="session", owner="Michael Hart", stated_by="Michael Hart", day=120,
                effect=effect, route_to=kw.pop("route_to", "coordinator" if effect == "route" else ""))
    base.update(kw)
    return RuleCard(rid, **base)


def test_lint_catches_ownerless_and_unreviewed_verify():
    c = RuleCard("R1", "s", "input", "session", "", "Keisha Monroe", 121, status="VERIFY")
    p = c.lint()
    assert any("no owner" in x for x in p) and any("no review day" in x for x in p)


def test_route_needs_a_destination():
    assert any("routes to nobody" in x for x in RuleCard("R2", "s", "input", "session", "o", "o", 1, effect="route").lint())


def test_missing_check_fails_closed():
    s = GuardrailSuite([card("O-1")], {})
    d = s.run("output", {})
    assert d.effect == "block" and "fail closed" in d.failed[0].reason


def test_raising_check_fails_closed():
    s = GuardrailSuite([card("O-1")], {"O-1": lambda ctx: ctx["missing"]})
    assert s.run("output", {}).effect == "block"


def test_precedence_block_beats_route():
    d = Decision.of([Verdict("a", False, "route", route_to="clinician"), Verdict("b", False, "block")])
    assert d.effect == "block"
    d = Decision.of([Verdict("a", False, "repair"), Verdict("b", False, "route", route_to="clinician")])
    assert d.effect == "route" and d.route_to == "clinician"


def test_retired_rules_do_not_run():
    s = GuardrailSuite([card("O-1", status="retired")], {})
    assert s.run("output", {}).effect == "pass" and s.missing() == []


def test_rule_needs_both_kinds_of_case():
    s = GuardrailSuite([card("O-1"), card("O-2")], {"O-1": lambda c: (c["x"] < 3, ""), "O-2": lambda c: (True, "")})
    r = run_rule_tests(s, [RuleTest("O-1", "low", {"x": 1}, True), RuleTest("O-1", "high", {"x": 5}, False),
                           RuleTest("O-2", "any", {}, True)])
    assert r.untested == ["O-2"] and r.failures == []


def test_budget_repeat_and_steps():
    b = Budget(max_steps=5, max_repeat=2)
    assert b.charge("lookup", {"name": "A"}) is None
    assert b.charge("lookup", {"name": "A"}) is None
    assert "repeat budget" in b.charge("lookup", {"name": "A"})
    b = Budget(max_steps=2)
    b.charge(); b.charge()
    assert "step budget" in b.charge()


def test_breaker_opens_after_no_progress_and_stays_open():
    br = CircuitBreaker(threshold=3)
    assert [br.record("lookup", False) for _ in range(3)] == ["closed", "closed", "open"]
    assert br.record("lookup", True) == "open" and not br.allow("lookup")


def test_fleet_breaker_pages_above_rate():
    f = FleetBreaker(rate=0.05, min_runs=20, page="on-call")
    out = [f.record("h1", i < 1) for i in range(20)]
    assert out[-1] is None
    assert f.record("h1", True).startswith("page on-call: 2 of 21")


def test_elicitation_report_finds_dangling():
    st = [Statement("S1", 120, "michael", "Michael Hart", "t", "rule:I-04"),
          Statement("S2", 121, "desk", "Keisha Monroe", "t", "merged:I-99"),
          Statement("S3", 121, "desk", "Luis Ortega", "t", "out of scope")]
    r = elicitation_report(st, [card("I-04", kind="input")])
    assert r["dangling"] == ["S2"] and r["disposition"]["out of scope"] == 1
