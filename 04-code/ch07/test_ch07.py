import pytest, caldwell_bank as cb
from questionbank import Question as Q, Bank, acting_for_gaps, coverage
from discovery_snapshot import ITEMS

def test_session_numbers():
    r = cb.build().reconcile()
    assert r.answered == 40 and r.by_outcome["contradicted"] == 9 and len(r.design_changes) == 9
    assert r.by_status["vendor position"] == [6, 4]
    assert 57 <= r.elapsed <= 60

def test_four_part_rule():
    with pytest.raises(ValueError):
        Bank("x").add(Q("Z1", "data", "data owner", "Which field?", "", "", "vendor position", "N", (), "", 1, False, 1))

def test_coverage_and_gaps():
    assert coverage(cb.build().questions.values(), ITEMS) == []
    assert acting_for_gaps(("a", "b"), ("a",)) == ["b"]

def test_prep_budget():
    asked, dropped = cb.build().prep("data owner", 30)
    assert sum(q.minutes for q in asked) <= 30 and asked[0].rapid
