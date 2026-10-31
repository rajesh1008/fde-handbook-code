"""fieldkit v3.4 (Chapter 27): the confidence router."""
import pytest
from fieldkit.routing import (wilson, ece, resolution, auroc, Isotonic, choose_proceed, choose_floor, Evidence, gate,
                              Thresholds, route_field, route_document, AnswerCheck, post_review_error, DriftMonitor,
                              ThresholdRecord, PROCEED, REVIEW, ESCALATE)

TH = Thresholds(proceed=0.95, floor=0.41, target=0.98, lower_bound=0.989, checked_n=2000)
OK = Evidence(True, True, True, True)


def test_wilson_and_ece():
    lo, hi = wilson(98, 100)
    assert lo < 0.98 < hi and round(lo, 3) == 0.930
    assert ece([0.0, 1.0] * 50, [False, True] * 50) == 0.0
    assert ece([0.99] * 100, [True] * 50 + [False] * 50) > 0.4


def test_resolution_and_auroc():
    assert resolution([0.95, 0.99, 0.95]) == 2
    assert auroc([0.9, 0.8, 0.2, 0.1], [True, True, False, False]) == 1.0
    assert auroc([0.5] * 4, [True, False, True, False]) == 0.5


def test_isotonic_is_monotone():
    iso = Isotonic().fit([0.1, 0.2, 0.3, 0.4, 0.5, 0.6], [1, 0, 0, 1, 1, 1])
    ys = [iso.predict(x / 10) for x in range(11)]
    assert ys == sorted(ys)


def test_choose_proceed_meets_lower_bound():
    s = [i / 1000 for i in range(1000)]
    o = [x > 0.3 for x in s]
    t, lb, n = choose_proceed(s, o, 0.98, 100, grid=[x / 100 for x in range(50, 100)])
    assert lb >= 0.98 and n >= 100


def test_gate_order_and_fail_closed():
    assert gate(Evidence(False, False, False, False)) == "budget exhausted"
    assert gate(Evidence(False, None, False, True)) == "conflicting sources"
    assert gate(Evidence(False, None, None, True)) == "no evidence"
    assert gate(Evidence(False, True, None, True)) is None      # a passing system check is evidence
    assert gate(OK) is None


def test_route_field_bands():
    assert route_field(0.99, OK, TH).band == PROCEED
    assert route_field(0.80, OK, TH).band == REVIEW
    r = route_field(0.30, OK, TH)
    assert r.band == ESCALATE and not r.show_recommendation
    assert route_field(0.99, Evidence(True, False, None, True), TH).band == REVIEW
    assert route_field(0.99, Evidence(True, None, False, True), TH).band == ESCALATE


def test_route_document_reasons():
    p, rv, lo = route_field(0.99, OK, TH), route_field(0.8, OK, TH), route_field(0.1, OK, TH)
    assert route_document([p] * 10)[0] == PROCEED
    assert route_document([p] * 9 + [rv])[0] == REVIEW
    assert route_document([p] * 6 + [lo] * 4, max_blank=3) == (ESCALATE, "too many fields below floor")
    assert route_document([p] * 6 + [lo] * 4, max_blank=4)[0] == REVIEW


def test_answer_check():
    a = AnswerCheck()
    passages = ["Water loss: the supply line cause code stays blank until the desk adjuster inspects."]
    assert a.check([], passages, ["water"]) == "not in the documents"
    assert a.check(["no such sentence"], passages, ["water"]) == "not in the documents"
    assert a.route(["the supply line cause code stays blank"], passages, ["supply", "cause", "adjuster"])[0] == PROCEED
    assert a.route(["the supply line cause code stays blank"], passages, ["pet", "sublimit", "water"])[0] == ESCALATE


def test_post_review_error_and_drift():
    rate, lo, hi = post_review_error([True] * 3964 + [False] * 36)
    assert rate == 0.009 and lo < rate < hi
    m = DriftMonitor()
    assert m.check(27, 845)[0] and not m.check(8, 981)[0]
    assert m.psi([0.9] * 100, [0.9] * 100) < 0.01


def test_threshold_record_refuses_gaps():
    r = ThresholdRecord(0.95, 0.41, "98%", "cal-600", "odd half", 0.989, "62/30/8", "0.9%", "Anne Kessler",
                        ("Anne Kessler", "Daniel Reyes"), 132, "weekly audit")
    assert r.missing() == []
    assert set(ThresholdRecord(0.95, 0.41, "98%", "", "", 0.98, "", "", "", (), 120, "").missing()) >= {"owner", "signed_by"}
