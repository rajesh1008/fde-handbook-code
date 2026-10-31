from fieldkit.bid import (Question, Standard, Clarification, triage, crosswalk, extract, lint, five_moves,
                          safety_net, to_register, LAYER)
from fieldkit.cadence import Register


def test_layer():
    assert LAYER == "v1.5"


def test_triage_flags_joint_question_sent_to_sales():
    qs = [Question("Q1", "H", "Uptime and credits", ("operations", "terms"), "sales"),
          Question("Q2", "B", "Price", ("price",), "sales")]
    counts, _, mis = triage(qs)
    assert counts == {"engineering": 0, "joint": 1, "sales": 1} and [m[0] for m in mis] == ["Q1"]


def test_crosswalk_refuses_vendor_say_so_and_unnamed_approver():
    s = [Standard("A", "logging", "SIEM retention", "comply", "product supports export", "V", True),
         Standard("B", "change", "change board", "deviation requested", "x", "V", True, "the change board")]
    codes = [p[1] for p in crosswalk(s)[1]]
    assert codes == ["COMPLY ON VENDOR SAY-SO", "DEVIATION WITHOUT APPROVER"]


def test_estate_claim_needs_customer_source_and_contradiction_blocks():
    claims = extract({"A": "Acme's gateway supports streaming [F: Jane Doe, conference]. "
                           "Acme's store keeps versions [V]. We will reply within 20 seconds [V]."}, "Acme")
    k = Clarification("CL-1", "stream?", "No.", ("gateway",), ("stream",), False)
    codes = {(c, code) for c, _, code, _ in lint(claims, [k])}
    assert ("BC-01", "CONTRADICTED") in codes and ("BC-02", "ESTATE CLAIM WITH VENDOR STATUS") in codes
    assert ("BC-03", "AT RISK") in codes and ("BC-01", "ORAL FACT") in codes


def test_conditional_is_not_checked():
    claims = extract({"A": "If streaming arrives in the gateway, we will adopt it [P]."})
    k = Clarification("CL-1", "stream?", "No.", ("gateway",), ("stream",), False)
    assert lint(claims, [k]) == []


def test_decision_needs_person_and_day():
    claims = extract({"A": "The model will be chosen by the bank [D: model risk, soon]."})
    assert lint(claims)[0][2] == "DECISION WITHOUT OWNER OR DUE DAY"


def test_five_moves_and_safety_net_and_register():
    p, secs = five_moves(dict(position="Yes.", evidence="6 users.", example="One queue.",
                              boundary="It does not edit memos.", proof="Line 4 of the crosswalk."))
    assert p == [] and secs > 0
    claims = extract({"A": "We will reply within 20 seconds [V]. The owner will be named later [D: Jane Doe, day 9]."})
    page = safety_net("Acme", claims, [], ["no date"], "Reads and drafts only.")
    assert len(page) <= 60
    reg = Register("Acme")
    moved = to_register(claims, reg, {"A": "Laura Finch"}, {"A": 30})
    assert [r.owner for r in moved] == ["Laura Finch", "Jane Doe"]
