"""Pins for the Chapter 8 lab: the behaviors the chapter's text depends on."""
import caldwell_scope as cs
import calibration as cal
from scoping import Claim, Criterion, Source


def test_signed_scope_is_clean():
    doc = cs.signed()
    assert doc.lint() == []
    assert len(doc.suite_config()) == 7
    inside, total = doc.coverage()
    assert (inside, total) == (11244, 14800)


def test_criterion_without_measurement_is_refused():
    d = cs.draft_v03()
    codes = {(k, c) for k, c, _ in d.lint()}
    assert ("C-08", "NO MEASUREMENT") in codes and ("C-09", "NO THRESHOLD") in codes
    assert [c["key"] for c in d.suite_config()] == ["C-01", "C-02", "C-03"]


def test_status_never_rises_by_repetition():
    d = cs.draft_v03()
    ups = [m for k, c, m in d.lint() if c == "UPGRADED BY REPETITION"]
    assert len(ups) == 2 and d.origin(d.claims[0]).key == "DS-07"


def test_fact_needs_a_person_and_number_needs_basis():
    d = cs.signed()
    c = Claim("Z", "Intake takes 16 minutes a document", "F", Source("intake team", "customer", "x", 1))
    codes = [code for code, _ in d.claim_problems(c)]
    assert "FACT WITHOUT A PERSON" in codes and "NUMBER WITHOUT BASIS" in codes


def test_calibration_round_two():
    r2 = cal.per_field(2)
    judged = sorted(f for f, k, _ in r2 if k < 0.8)
    assert judged == ["cause_of_loss", "injury_reported", "time_of_loss"]


def test_register_alerts():
    reg = cs.signed().to_register()
    assert {k for k, c, _ in reg.alerts(37) if c == "OVERDUE"} == {"D-01", "OD-5"}
