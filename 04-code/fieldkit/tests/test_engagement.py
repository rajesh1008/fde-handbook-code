import pytest

from fieldkit.engagement import LAYER, EngagementRepo


def _repo():
    r = EngagementRepo("Caldwell Mutual")
    r.note(1, "Graham Lowell", "promise", "Accuracy above 95% on Caldwell documents.", source="kickoff")
    r.note(4, "Priya Natarajan", "finding", "Ten documents processed outside the data-handling standard.")
    r.decision("D-1", "Which loss codes count as one type?", "Anne Kessler", 2, due_day=8)
    r.decision("D-2", "Who owns the gold set?", "", 2)
    r.request("aws-sandbox-account", "AWS sandbox account", "Daniel Reyes", 2, "in review",
              blocks="every build in Caldwell's estate")
    r.request("claims-core-readonly", "read-only claims-core account", "Daniel Reyes", 5)
    r.measure("E-1", "Field accuracy of the demo on Caldwell documents", "58% (58/100 fields)",
              "Anne Kessler", "10 documents, one week's intake", 2, kind="stand-in",
              location="deleted day 4")
    return r


def test_layer_is_v0():
    assert LAYER == "v0"


def test_lint_finds_unverifiable_promise_and_ownerless_decision():
    problems = _repo().lint(today=5)
    assert any(p.startswith("PROMISE-NO-VERIFIER") for p in problems)
    assert any(p.startswith("DECISION-NO-OWNER D-2") for p in problems)
    assert not any(p.startswith("DECISION-OVERDUE") for p in problems)
    assert any(p.startswith("DECISION-OVERDUE D-1") for p in _repo().lint(today=9))


def test_status_headline_counts_blockers_and_findings():
    s = _repo().status(today=5)
    assert "customer data on any rung: none; 1 blocker; 1 open finding." in s
    assert "58% (58/100 fields)" in s and "scorer Anne Kessler" in s
    assert "aws-sandbox-account" in s and "open 3 days" in s


def test_audit_flags_numbers_without_evidence():
    v = _repo().audit([("Demo validated on Caldwell documents.", None),
                       ("Field accuracy 58% on ten documents.", "E-1"),
                       ("Kickoff held with four Caldwell leaders.", None),
                       ("Accuracy 91%.", "E-9")])
    assert v[0].startswith("UNSUPPORTED")
    assert v[1].startswith("CITES E-1")
    assert v[2].startswith("UNSUPPORTED")  # a count is a number too
    assert v[3].startswith("NO-SUCH-EVIDENCE")


def test_save_and_load_round_trip(tmp_path):
    r = _repo()
    r.decide("D-1", 6, "AUTO-COMP covers theft and animal strikes.")
    r.save(tmp_path)
    r.write_status(tmp_path, 6)
    back = EngagementRepo.load(tmp_path)
    assert back.customer == "Caldwell Mutual"
    assert len(back.notes) == 2 and len(back.requests) == 2
    assert back.decisions[0].status == "decided" and back.decisions[0].age(9) == 4
    assert (tmp_path / "status" / "day006.md").exists()


def test_bad_kinds_are_refused():
    r = EngagementRepo("x")
    with pytest.raises(ValueError):
        r.note(1, "a", "rumour", "b")
    with pytest.raises(ValueError):
        r.measure("E", "c", "v", "m", "1 doc", 1, kind="vibes")
