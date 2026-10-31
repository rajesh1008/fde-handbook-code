"""fieldkit v4.1: model risk and the customer's governance (Chapter 33)."""
import pytest
from fieldkit.modelrisk import (Component, Rule, Framework, classify_all, counts, diff, register_digest, plan_for,
                                Evidence, Pack, Input, Metric, computability, repeat_agreement, wilson_lower,
                                ValidatorQuestion, Condition, FULL, REGISTERED, TOOL, NOT_MODEL, OUTSIDE, PLAN)

POLICY = Framework("p", (Rule({"quantitative": False}, NOT_MODEL, "code"),
                         Rule({"trained_on_customer_data": True, "core_decision": True}, FULL, "trained"),
                         Rule({"core_decision": True}, REGISTERED, "vendor use"),
                         Rule({}, TOOL, "tool")))
CODE = Component("A", "parser", "code", False, False, True)
VEND = Component("B", "prompted", "prompted", True, False, True, True, ("prompt",))
FIT = Component("C", "router", "fitted", True, True, True)
JUDGE = Component("D", "judge", "judge", True, False, False, True)


def test_rules_in_order_and_outcomes():
    cl = classify_all(POLICY, [CODE, VEND, FIT, JUDGE])
    assert [k.outcome for k in cl] == [NOT_MODEL, REGISTERED, FULL, TOOL]
    assert counts(cl) == {FULL: 1, REGISTERED: 1, TOOL: 1, NOT_MODEL: 1}
    assert len(plan_for(cl)) == sum(len(PLAN[o]) for o in (NOT_MODEL, REGISTERED, FULL, TOOL))


def test_no_matching_rule_raises():
    with pytest.raises(ValueError):
        Framework("x", (Rule({"quantitative": False}, NOT_MODEL, ""),)).classify(VEND)


def test_diff_and_digest_follow_design_changes():
    a = classify_all(POLICY, [CODE, VEND])
    b = classify_all(POLICY, [CODE, VEND, FIT])
    assert diff(a, b) == [("C", "absent", FULL)]
    assert register_digest(a) != register_digest(b)
    assert register_digest(a) == register_digest(classify_all(POLICY, [CODE, VEND]))


def test_pack_lint_finds_gaps_scorerless_evidence_and_unmonitored_components():
    cl = classify_all(POLICY, [CODE, VEND])
    p = Pack("X", "v1", cl, [Evidence("change_control", "*", "pins", "", "ledger", "s")])
    probs = p.lint()
    assert any("names no scorer" in x for x in probs)
    assert any(x == "no monitoring metric covers B" for x in probs)
    assert ("B", "outcomes") in p.gaps() and ("A", "change_control") not in p.gaps()


def test_computability_flags_vendor_inputs_and_identities():
    m = Metric("M1", "m", "t", "owner", ("B",), (Input("labels", "Cust", "s3"), Input("job", "Cust", "ci", "vendor-id")))
    n = Metric("M2", "m", "t", "owner", ("B",), (Input("labels", "Vendor", "vendor account"),))
    res = dict((x.mid, b) for x, b in computability([m, n], "Cust", ("vendor-id",)))
    assert len(res["M1"]) == 1 and "identity the vendor operates" in res["M1"][0]
    assert "owned by Vendor" in res["M2"][0]


def test_repeat_agreement_and_wilson():
    assert repeat_agreement(["a", "a", "b", "a"]) == (0.75, "a")
    assert abs(wilson_lower(27, 845) - 0.022) < 0.001
    assert wilson_lower(0, 0) == 0.0


def test_boundary_needs_compensating_control_and_conditions_age():
    assert ValidatorQuestion("V1", "q", "boundary", "no").problems()
    assert not ValidatorQuestion("V1", "q", "boundary", "no", "pin").problems()
    assert ValidatorQuestion("V1", "q", "guess", "x").problems()
    c = Condition("R1", "t", "o", 190, "w")
    assert c.status(153) == "open" and c.status(191) == "overdue" and c.status(200, met=True) == "met"
    assert OUTSIDE not in PLAN or PLAN[OUTSIDE] == ()
