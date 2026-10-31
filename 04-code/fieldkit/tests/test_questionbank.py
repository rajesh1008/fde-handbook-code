import pytest
from fieldkit.questionbank import Question as Q, Answer, Bank, acting_for_gaps, coverage

def q(qid, aud="data owner", status="vendor position", rapid=False, minutes=1.0, serves=()):
    return Q(qid, "data", aud, "Which field holds the date received?", "decides the extraction target",
             "received_at", status, "Northlight", ("fax header",), "date rule", 2, rapid, minutes, serves)

def test_question_without_expected_answer_is_refused():
    with pytest.raises(ValueError):
        Bank("x").add(Q("Z1", "data", "data owner", "Which field?", "", "", "vendor position", "N", (), "", 1, False, 1))

def test_prep_never_exceeds_budget_and_rapid_first():
    b = Bank("x")
    for i in range(12):
        b.add(q(f"Q{i}", rapid=(i < 3), minutes=1.0 if i < 3 else 4.0))
    asked, dropped = b.prep("data owner", 15)
    assert sum(x.minutes for x in asked) <= 15 and asked[0].rapid and dropped

def test_acting_for_gaps_and_coverage():
    assert acting_for_gaps(("read", "search by name"), ("read",)) == ["search by name"]
    assert coverage([q("Q1", serves=("P01",))], ["P01", "P02"]) == ["P02"]

def test_wrong_role_set_aside_and_redirect_names_owner():
    b = Bank("x"); b.add(q("Q1")); b.add(q("Q2"))
    b.record(Answer("Q1", 18, "platform lead", "platform", "confirmed", "yes"))
    b.record(Answer("Q2", 24, "data owner", "data owner", "contradicted", "no", 2.0))
    r = b.reconcile()
    assert len(r.wrong_person) == 1 and len(r.design_changes) == 1
    with pytest.raises(ValueError):
        b.record(Answer("Q2", 24, "data owner", "data owner", "redirected", "not me"))
