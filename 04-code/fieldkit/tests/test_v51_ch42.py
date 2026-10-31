"""fieldkit v5.1 (Chapter 42): liveops."""
from fieldkit.liveops import (DriftMonitor, recalibrate, PageRoute, Incident, deprecation_plan, upgrade_gate,
                              OwnershipMap, live_stable, hhmm)


def test_drift_monitor_needs_a_customer_reader():
    m = DriftMonitor("Dana Whitaker", "Dana Whitaker")
    assert m.leading(["a"] * 50 + ["b"] * 50, ["a"] * 50 + ["b"] * 50) < 0.01
    assert m.leading(["a"] * 90 + ["b"] * 10, ["a"] * 10 + ["b"] * 90) > 0.25
    m.read(10, "Northlight")
    assert m.running(12)[0] is False
    m.read(12, "Dana Whitaker")
    assert m.running(15)[0] is True and m.running(30)[0] is False


def test_recalibrate_respects_the_line_and_needs_a_signature():
    sample = [(0.95, True)] * 500 + [(0.75, True)] * 40 + [(0.75, False)] * 10 + [(0.6, False)] * 50
    r = recalibrate(sample, max_wrong_upper=0.015, owner="Dana Whitaker")
    assert r["threshold"] is not None and r["threshold"] > 0.75 and r["signed"] is False
    assert recalibrate([(0.9, False)] * 20, 0.01, "x")["threshold"] is None


def test_page_route_lint():
    bad = PageRoute("oncall@northlight.example", "fde", "Jenna Ruiz", approver_is_role=False).lint()
    assert len(bad) == 2
    assert PageRoute("pennant-platform-oncall", "fde", "own-operations").lint() == []


def test_incident_metrics():
    i = Incident("x")
    for m, k in ((124, "start"), (130, "detect"), (134, "ack"), (184, "mitigate")):
        i.log(m, k, k)
    assert i.metrics() == dict(ttd=6, tta=4, ttm=60) and hhmm(130) == "02:10"


def test_deprecation_in_a_freeze():
    p = deprecation_plan(41, 62, [(45, 75)], evidence_days=7)
    assert p["freeze_exception"] and p["earliest_ready"] == 48 and p["slack_days"] == 13
    q = deprecation_plan(41, 62, [(45, 75)], evidence_days=7, read_day=52)
    assert q["slack_days"] == 2
    assert not deprecation_plan(20, 41, [(45, 75)], 7)["freeze_exception"]


def test_upgrade_gate():
    dims = {"suite": (89.3, 87.2, 85.0, True), "latency": (4.1, 3.8, 6.0, False)}
    assert upgrade_gate(dims, 15)[0] == "HOLD"
    assert upgrade_gate(dims, 15, signoff="Dana Whitaker", accepted={"latency": "Kofi Mensah"})[0] == "PROMOTE"
    assert upgrade_gate({"suite": (80.0, 87.2, 85.0, True)}, 0)[0] == "ROLLBACK"


def test_ownership_rule_and_its_blind_spot():
    m = OwnershipMap()
    m.add("own-exec", "J"); m.add("own-operations", "J", deputy="R"); m.add("own-override", "J", deputy="R")
    m.add("provider account", "J")
    assert m.two_of_five() == []
    assert len(m.single_points()) == 2
    m.leave("J")
    assert m.orphans() == ["own-exec", "provider account"]
    m.add("own-exec", "J"); m.add("own-gold-set", "J"); m.add("own-model-risk", "J")
    m.departed.clear()
    assert m.two_of_five()


def test_live_stable_refuses_vendor_measurement():
    v, _ = live_stable([("a", True, "e", "Dana Whitaker"), ("b", True, "e", "Northlight")])
    assert v == "NOT YET"
    assert live_stable([("a", True, "e", "Dana Whitaker")])[0] == "LIVE STABLE"
