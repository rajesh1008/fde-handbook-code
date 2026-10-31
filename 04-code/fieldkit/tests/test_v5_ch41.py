"""fieldkit v5 (Chapter 41): the hand-over test."""
import pytest
from fieldkit.handover import (Item, score, without, single_points, Alert, route_check, Step, Runbook,
                               lint_runbook, raci_check, path_coverage, Scenario, drill)


def items():
    return [Item("a", "runbooks", "x", "alone", ("Ana",), gate=True), Item("b", "drill", "y", "assisted", ("Ana", "Bo")),
            Item("c", "monitoring", "z", "exists"), Item("d", "training", "w", "alone", ("Bo",))]


def test_score_counts_existence_naively_and_evidence_gated():
    s = score(items())
    assert (s.naive, s.raw, s.gated, s.failing_gates) == (1.0, 0.625, 0.625, [])


def test_gate_caps_score():
    it = items(); it[0] = Item("a", "runbooks", "x", "assisted", ("Ana",), gate=True)
    s = score(it)
    assert s.raw == 0.5 and s.gated == 0.5 and s.failing_gates == ["a"]
    it[3] = Item("d", "training", "w", "alone", ("Bo",)); it[2] = Item("c", "m", "z", "alone", ("Bo",))
    assert score(it).gated == 0.6 and score(it).capped


def test_assisted_needs_a_name():
    with pytest.raises(ValueError):
        Item("e", "x", "y", "assisted")


def test_without_and_single_points():
    assert score(without(items(), "Ana")).raw == 0.375
    assert single_points(items())[0] == ("Ana", 0.25)


def test_route_check_finds_vendor_address():
    al = [Alert("A1", "m", "oncall@cw.example"), Alert("A2", "m", "alerts@northlight.example")]
    assert [a.id for a in route_check(al, {"cw.example"})] == ["A2"]


def test_runbook_lint_rules():
    al = [Alert("A1", "m", "oncall@cw.example")]
    rb = Runbook("RB", "t", "A1", "data", "shadow", "Ana", (Step("ask Northlight", "on-call"), Step("ok", "on-call", "v")))
    rules = sorted(r for r, _ in lint_runbook(rb, {"Ana"}, al))
    assert rules == ["RB2", "RB4", "RB5"]
    rb2 = Runbook("RB", "t", "A9", "data", "off", "Zed", (Step("a", "b", "v"),))
    assert sorted(r for r, _ in lint_runbook(rb2, {"Ana"}, al)) == ["RB1", "RB3", "RB6"]


def test_raci_one_customer_accountable():
    rows = [("x", "Ana", "Ana", ""), ("y", "Northlight", "Northlight", ""), ("z", "Ana", "Ana, Bo", "")]
    assert [a for a, _ in raci_check(rows, {"Ana", "Bo"})] == ["y", "z"]


def test_path_coverage():
    assert path_coverage({"on-call": [1, 2]}, {"on-call": [1, 2, 7], "owner": [1]}) == {"on-call": [7], "owner": [1]}


def test_drill_vendor_route_fails_then_passes():
    sc = Scenario("k", 180, "A1", 2, "A2", 293)
    rota = {"oncall@cw.example": ("cw on-call", 4), "a@northlight.example": ("Northlight", 0)}
    steps = [("s1", 10), ("s2", 15)]
    bad = drill(sc, [Alert("A1", "m", "a@northlight.example"), Alert("A2", "m", "oncall@cw.example")], rota, steps, {"cw.example"})
    assert bad["touches"] == 1 and not bad["passed"] and bad["detect"] == 117
    good = drill(sc, [Alert("A1", "m", "oncall@cw.example"), Alert("A2", "m", "oncall@cw.example")], rota, steps, {"cw.example"})
    assert good["passed"] and good["detect"] == 6 and good["mitigate"] == 31


def test_drill_nobody_on_rota_misses_deadline():
    sc = Scenario("p", 124, "A1", 2, deadline=210)
    r = drill(sc, [Alert("A1", "m", "q@pn.example")], {"q@pn.example": ("Pennant", None)}, [], {"pn.example"})
    assert r["detect"] is None and r["deadline_missed"] and not r["passed"]
