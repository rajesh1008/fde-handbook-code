import world as W
from practice import decide, calibration, evaluate_plan, PLANS, load_series, red_months, ladder_check, runway, headcount, profile_flags


def test_weights_sum_to_one():
    assert abs(sum(W.WEIGHTS.values()) - 1.0) < 1e-9


def test_failure_injection_old_loop_hires_c3():
    assert decide(W.CANDIDATES["C-3"], W.OLD_LOOP, mode="old")[0] == "hire"


def test_floor_blocks_c3_even_above_bar():
    d = decide(W.CANDIDATES["C-3"])
    assert d[0] == "no hire" and d[1] >= W.BAR and "discovery" in d[2]


def test_unobserved_is_not_a_pass():
    assert decide(W.JONAH_M4)[0] == "no decision"


def test_anchors_raise_agreement():
    assert calibration(W.RATINGS_AFTER)["mean_kappa"] >= 0.6 > calibration(W.RATINGS_BEFORE)["mean_kappa"]


def test_pods_cover_more_needs_than_solo():
    solo = evaluate_plan("s", PLANS["solo (one FDE per customer)"])
    pods = evaluate_plan("p", PLANS["pods + shared evaluation lead"])
    assert pods["met"] == pods["needed"] > solo["met"]


def test_hannah_red_before_leaving_and_policy_clears():
    assert red_months(load_series("Maya Brooks"))[0] < 11
    assert red_months(load_series("Maya Brooks", policy=True)) == []


def test_activity_is_not_evidence():
    assert not ladder_check(W.PACKETS["packet P-3 (for Senior FDE, failure injection)"], "Senior FDE")["ready"]
    assert ladder_check(W.PACKETS["Sofia Brennan (for Senior FDE, month 12)"], "Senior FDE")["ready"]


def test_single_client_runway_dips():
    c = runway(W.SCENARIOS["one client at 90%, ends month 6 (failure injection)"])
    assert min(c[7:13]) < max(c[:7])


def test_headcount_and_flags():
    assert [n for _m, n, _o in headcount()][-1] == 6
    assert any("evaluation" in f for f in profile_flags(["lead FDE", "Callum Reid", "Sofia Brennan", "Aisha Rahman", "Leo Martens", "Imogen Clarke"]))
