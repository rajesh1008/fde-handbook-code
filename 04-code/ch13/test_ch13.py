from cadence_data import pennant_sprint2, caldwell_sprint2, caldwell_register, GREYSTONE_CLINIC
from fieldkit.cadence import plan_sprint, gate_check, review, lint_status, bus_factor, Item, GATES
import clinic

def test_ordering_rule_has_no_displacement():
    assert plan_sprint(pennant_sprint2(), 20).violations == []

def test_pinned_p3_displaces_p0_and_is_flagged():
    p = plan_sprint(pennant_sprint2(), 20, pinned=("P-05", "P-03"))
    assert any("P-02" in v and "P0" in v for v in p.violations)

def test_failed_gate_after_displacement():
    items = pennant_sprint2()
    p = plan_sprint(items, 20, pinned=("P-05", "P-03"))
    for i in p.selected:
        i.status = "accepted" if i.done else "not accepted"
    ok, missing = gate_check("Architecture Review", items, 46)
    assert not ok and missing[0].startswith("P-02")

def test_review_three_outcomes_and_exception():
    rv = review("s2", [i for i in caldwell_sprint2() if i.key != "C-06"], 56)
    assert [i.key for i in rv.outcomes["not accepted"]] == ["C-04"]
    assert rv.accepted_points == 18 and rv.committed == 23
    assert rv.exceptions[0][0] == "C-03"

def test_accepted_without_evidence_is_not_accepted():
    i = Item("X", "t", "P1", 1, "Anne Kessler", ["returns 3 fields"], {}, status="accepted")
    assert review("s", [i], 1).outcomes["not accepted"] == [i]

def test_status_lint():
    g = {x: False for x in GATES}
    assert lint_status("It is production-ready.", g)
    assert not lint_status("Gates passed 0 of 5.", g)

def test_register_alerts():
    kinds = {(k, kind) for k, kind, _ in caldwell_register().alerts(56)}
    assert ("D-01", "OVERDUE") in kinds and len(kinds) == 3

def test_clinic_flags_one():
    assert sum(clinic.problems(r) is not None for r in GREYSTONE_CLINIC) == 1

def test_bus_factor():
    flags = bus_factor({"a": [("Jenna Ruiz", "c")], "b": [("Jenna Ruiz", "c")], "c": [("Jenna Ruiz", "c")]})
    assert any("concentration" in f for f in flags)
