from fieldkit.cadence import Item, Record, Register, plan_sprint, gate_check, review, lint_status, bus_factor, GATES, LAYER

def _items():
    return [Item("A", "control", "P0", 5, "Anne Kessler", ["0 open roles"], {0: "e"}, gate="Architecture Review"),
            Item("B", "outcome", "P1", 5, "Anne Kessler", ["returns 14 fields"], {0: "e"}),
            Item("C", "speed", "P3", 5, "Anne Kessler", ["under 4 s"], {0: "e"})]

def test_layer():
    assert LAYER == "v1.6"

def test_ready_needs_owner_and_testable_criteria():
    assert Item("X", "t", "P1", 1, "team", ["be good"]).ready_problems() == [
        "no named accountable owner", "criterion 1 is not testable: 'be good'"]

def test_guard_and_gate():
    items = _items()
    assert plan_sprint(items, 10).violations == []
    p = plan_sprint(items, 10, pinned=("C", "B"))
    assert p.violations and "A" in p.violations[0]
    for i in p.selected:
        i.status = "accepted"
    assert gate_check("Architecture Review", items, 20)[0] is False

def test_review_follow_up_without_date_is_no():
    i = Item("B", "o", "P1", 3, "Anne Kessler", ["returns 3"], {0: "e"}, status="accepted with follow-up")
    assert review("s", [i], 1).outcomes["not accepted"] == [i]

def test_register_and_lint():
    r = Register("X")
    r.add(Record("D-1", "q", "Anne Kessler", 1, 5))
    r.add(Record("D-2", "q", "the vendor", 1, None, kind="scope change"))
    kinds = {k for _, k, _ in r.alerts(10)}
    assert {"OVERDUE", "NO OWNER", "NO DUE DAY", "NO IMPACT"} <= kinds
    assert lint_status("approved for production", {g: False for g in GATES})
    assert bus_factor({"x": [("Anne Kessler", "c")]})
