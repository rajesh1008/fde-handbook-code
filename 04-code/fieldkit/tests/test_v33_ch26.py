import pytest
from fieldkit.evals import (gold_value_ready, GoldValuePolicy, percent_agreement, cohen_kappa, calibration_report,
                            Adjudicator, JudgeValidation, corrected_rate, corrected_interval, flip_rate, four_cells,
                            CustomerGate, wilson)

def test_fourteen_day_rule():
    assert not gold_value_ready(13) and gold_value_ready(14)
    ready, held = GoldValuePolicy().split([3, 20, 14], lambda a: a)
    assert ready == [20, 14] and held == [3]

def test_kappa_perfect_chance_and_opposite():
    assert cohen_kappa([1, 0, 1, 0], [1, 0, 1, 0]) == 1.0
    assert cohen_kappa([1, 1, 0, 0], [1, 0, 1, 0]) == 0.0
    assert cohen_kappa([1, 0], [0, 1]) < 0
    with pytest.raises(ValueError):
        percent_agreement([1], [1, 0])

def test_calibration_lines_depend_on_field_kind():
    a = {"date": [1, 1, 0, 1, 0, 1, 1, 0], "location": [1, 1, 0, 1, 0, 1, 1, 0]}
    b = {"date": [1, 1, 0, 1, 1, 1, 1, 0], "location": [1, 1, 0, 1, 1, 1, 1, 0]}
    r = calibration_report(a, b, exact_fields={"date"})
    assert r["date"][1] == 0.8 and r["location"][1] == 0.6
    assert r["date"][2] is False and r["location"][2] is True

def test_adjudication_needs_named_owner_reason_and_closure():
    with pytest.raises(ValueError):
        Adjudicator("claims team")
    adj = Adjudicator("Anne Kessler")
    a = {("G1", "loss_type"): "WTR-PLUMB", ("G1", "loss_date"): "2026-03-02"}
    b = {("G1", "loss_type"): "WTR-WEATHER", ("G1", "loss_date"): "2026-03-02"}
    ds = adj.compare(a, b)
    assert len(ds) == 1
    with pytest.raises(RuntimeError):
        adj.gold(a)
    with pytest.raises(ValueError):
        adj.decide(ds[0], "WTR-PLUMB", "because")
    adj.decide(ds[0], "WTR-PLUMB", "rubric gap")
    assert adj.gold(a)[("G1", "loss_type")] == "WTR-PLUMB" and adj.reason_counts()["rubric gap"] == 1

def test_judge_validation_catches_a_lenient_judge():
    expert = [True] * 70 + [False] * 30
    lenient = [True] * 70 + [True] * 25 + [False] * 5
    ok, reasons = JudgeValidation(lenient, expert).verdict()
    assert not ok and "TNR" in reasons[0]
    good = [True] * 68 + [False] * 2 + [False] * 27 + [True] * 3
    v = JudgeValidation(good, expert)
    assert v.verdict()[0] and round(v.tpr, 2) == 0.97 and v.tnr == 0.9

def test_corrected_rate_and_interval():
    assert corrected_rate(0.95, 1.0, 0.0 + 0.5) == pytest.approx(0.9)
    with pytest.raises(ValueError):
        corrected_rate(0.5, 0.5, 0.5)
    expert = [True] * 70 + [False] * 30
    judge = [True] * 66 + [False] * 4 + [False] * 24 + [True] * 6
    p, lo, hi = corrected_interval(judge * 2, judge, expert, reps=300)
    assert lo <= p <= hi and abs(p - 0.70) < 0.02

def test_flip_rate_and_wilson():
    assert flip_rate([[True, True, False], [True, False, False]]) == pytest.approx(1 / 3)
    lo, hi = wilson(98, 100)
    assert 0.92 < lo < 0.98 < hi

def test_four_cells_and_customer_gate_blocks_lost_critical():
    before = {("D1", "policy_number"): True, ("D1", "loss_type"): False, ("D2", "policy_number"): True,
              ("D2", "loss_type"): False}
    after = {("D1", "policy_number"): False, ("D1", "loss_type"): True, ("D2", "policy_number"): True,
             ("D2", "loss_type"): True}
    c = four_cells(before, after)
    assert len(c["lost"]) == 1 and len(c["gained"]) == 2
    gate = CustomerGate("Caldwell", "Anne Kessler", "adjusters", "gold-set-300", ("policy_number",))
    status, reasons, *_ = gate.check(before, after)
    assert status == "owner review" and "policy_number" in reasons[0]
    assert gate.check(before, after, signed_off=[("D1", "policy_number")])[0] == "pass"
    worse = dict(before); worse[("D2", "policy_number")] = False
    assert gate.check(before, worse)[0] == "block"
    gate2 = CustomerGate("Caldwell", "Anne Kessler", "adjusters", "gold-set-300", ("claimant_name",))
    assert gate2.check(before, after)[0] == "pass"

def test_repeat_runs_count_against_validity():
    expert = [True] * 70 + [False] * 30
    good = [True] * 68 + [False] * 2 + [False] * 27 + [True] * 3
    v = JudgeValidation(good, expert)
    shaky = [good, [not x if i % 10 == 0 else x for i, x in enumerate(good)]]
    assert v.verdict_with_repeats([good, good])[0] and not v.verdict_with_repeats(shaky)[0]
