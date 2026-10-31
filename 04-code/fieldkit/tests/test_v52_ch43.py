"""fieldkit v5.2 (Chapter 43): service.py unit tests."""
from fieldkit.handover import Item, Step, Runbook, score
from fieldkit.service import (aged, Path, two_year, summary, takeover_hours, exit_lint, exit_drill, price_retainer,
                              EXIT_BASE)


def _items(n=4, gate_first=True):
    return [Item(f"I{k}", "d", "t", "alone", ("Ann",), gate=(gate_first and k == 0)) for k in range(n)]


def test_aged_thresholds():
    i = _items(1)[0]
    assert aged(i, 179).status == "alone" and aged(i, 180).status == "assisted" and aged(i, 365).status == "exists"
    assert aged(aged(i, 180), 180).status == "exists" and aged(i, 400).by == ()


def test_practice_keeps_credit_and_absence_decays_it():
    kept = two_year(Path("kept", practice={"*": 90}), _items(), months=12)
    lost = two_year(Path("lost"), _items(), months=13)
    assert kept[-1].readiness == 1.0 and lost[5].readiness == 0.5 and lost[5].capped is False
    assert lost[-1].readiness == 0.0 and lost[-1].takeover_hours == EXIT_BASE + 4 * 36


def test_gate_decay_caps():
    rows = two_year(Path("p", practice={"I1": 30, "I2": 30, "I3": 30}), _items(), months=7)
    assert rows[5].capped and rows[5].readiness == 0.6


def test_events_and_costs():
    p = Path("p", fee=(1000, 500), vendor_hours=(4, 2), customer_hours=10, customer_fixed=100, ramp=(5,),
             practice={"*": 90}, events=((2, "lost", "I3"), (3, "alone", "I3", ("Bo",)), (4, "leave", "Bo")),
             renewal=0.5)
    r = two_year(p, _items(), months=24, vendor_rate=150, customer_rate=100)
    assert r[0].customer_cost == 1000 + 1500 + 100 and r[1].customer_cost == 1000 + 1000 + 100
    assert r[1].readiness == 0.75 and r[2].readiness == 1.0 and r[3].readiness == 0.75
    s = summary(p, r)
    assert s[1]["revenue"] == 12000 and s[2]["cost"] == 3600 and s["weighted_gp"] == 12000 - 7200 + round(0.5 * (6000 - 3600))
    assert r[0].vendor_margin == 0.4


def test_takeover_counts_vendor_steps():
    assert takeover_hours(_items(), vendor_only_steps=2) == EXIT_BASE + 40


RB = Runbook("RB", "t", "A1", "data", "off", "Ann", (
    Step("read ops.vendor.example", "vendor on-call", "ok"),
    Step("copy to gs://cust-bucket/x and check vault:cust/key", "Ann", "ok"),
    Step("open dash.unknown.example", "Ann", "ok")), exit_via="shadow")
OWN = {"ops.vendor.example": "Vendor", "gs://cust-bucket": "customer", "vault:cust/key": "customer"}


def test_exit_lint_by_owner_not_by_name():
    f = exit_lint(RB, OWN)
    assert [(x.step, x.owner) for x in f] == [(1, "Vendor"), (3, "unregistered")]


def test_exit_drill_blocks_and_workarounds():
    d = exit_drill(RB, OWN, "Ann", (5, 5, 5), start=0, deadline=60)
    assert d["blocked_at"] == 1 and not d["passed"]
    d = exit_drill(RB, OWN, "Ann", (5, 5, 5), {"ops.vendor.example": ("own logs", 10),
                                               "dash.unknown.example": ("own dash", 10)}, start=0, deadline=60)
    assert d["passed"] and d["end"] == 35


def test_retainer():
    r = price_retainer(10, round_to=50)
    assert (r.fee, r.hourly, r.overage) == (3750.0, 375.0, 468.75)
    assert r.margin(10) == 0.6 and r.margin(5) == 0.8 and r.margin(20, carried=10) < 0.25
