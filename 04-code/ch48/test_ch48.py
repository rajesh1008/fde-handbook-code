"""Pins the numbers Chapter 48 quotes. Run: pytest -q test_ch48.py"""
import _paths  # noqa: F401
import board
import clocks
import freeze
import incidents
import renewals
import turnover
import upgrades


def test_month_nine_calendar():
    from world import span
    assert span("Caldwell", 9) == (398, 427) and span("Pennant", 9) == (408, 437) and span("Greystone", 9) == (436, 465)


def test_upgrade_verdicts_differ_by_customer():
    r = upgrades.replay()
    assert r["Caldwell"]["extract-2027-01"][1] == "PROMOTE"
    assert r["Pennant"]["extract-2027-01"][1:3] == ("HOLD", "PROMOTE")
    assert r["Greystone"]["extract-2027-01"][1] == "ROLLBACK"
    assert r["Caldwell"]["extract-2027-04"][1] == "HOLD" and r["Greystone"]["extract-2027-04"][1] == "PROMOTE"
    assert upgrades.pooled("extract-2027-01")[1][0] == "HOLD"


def test_freeze_failure_and_fix():
    v0 = freeze.v0(); v1 = freeze.v1()
    assert (v0["live"], v0["exposure_days"], v0["past_policy"]) == (466, 23, 9)
    assert v1["conflict"] and v1["live"] == 446 and v1["past_policy"] == 0 and v1["exposure_hours"] == 2.5
    assert (v1["manual_referrals"], v1["manual_hours"]) == (423, 45.8)
    assert freeze.v1(emergency=False)["manual_referrals"] == 3245


def test_incident_clocks_set_before_go_live():
    hits = [k for k in clocks.CLOCKS if k[1] in clocks.INCIDENT_CLOCKS]
    assert len(hits) == 4 and not any(k[5] for k in hits)
    m = {i.name.split()[0]: i.metrics() for _, i in incidents.build()}
    assert m["INC-C-014"]["ttd"] == 50 * 60 and m["INC-P-071"]["ttm"] == 342 and m["INC-G-009"]["ttd"] == 278 * 60


def test_turnover_orphans():
    o, l = turnover.caldwell(); [o.leave(p) for p in l]
    assert o.orphans() == ["T3 run the evaluation suite"]
    o, l = turnover.pennant(True); [o.leave(p) for p in l]
    assert o.orphans() == []


def test_board_per_customer():
    q = board.quarters("Greystone")
    assert q[2]["over"] == [7] and q[2]["errors"] == 14
    assert board.quarters("Caldwell")[3]["errors"] == 11
    assert board.blended() == [97.1, 97.9, 97.6, 97.8]


def test_renewal_packs():
    ok = lambda c, d: sum(1 for r in renewals.status(c, d) if r[2] is True)
    assert ok("Caldwell", 333) == 1 and ok("Caldwell", 346) == 4 and ok("Pennant", 352) == 3
