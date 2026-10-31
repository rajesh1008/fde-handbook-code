"""fieldkit v3.7: fine-tune evaluation suite (Chapter 30)."""
from fieldkit.finetune import (wilson, mcnemar_exact, paired_compare, per_class, familiarity, GuardRule,
                               AbsentClassGuard, cost_per_doc, ServingOption, crossover, learning_crossover,
                               TrainingDataRecord, risk_class, SwitchGate)


def test_wilson_and_mcnemar():
    lo, hi = wilson(838, 900)
    assert 0.91 < lo < 0.931 < hi < 0.95
    assert mcnemar_exact(0, 0) == 1.0
    assert abs(mcnemar_exact(5, 5) - 1.0) < 1e-12
    assert mcnemar_exact(60, 20) < 0.001


def test_paired_compare_cells_and_verdict():
    t = ["a"] * 10
    pa = ["a"] * 9 + ["b"]
    pb = ["a"] * 5 + ["b"] * 5
    c = paired_compare(pa, pb, t)
    assert (c.both_right, c.a_only, c.b_only, c.both_wrong) == (5, 4, 0, 1)
    assert c.right_a == 9 and c.right_b == 5
    assert c.verdict() == "no detectable difference"   # four discordant pairs prove nothing
    try:
        paired_compare(pa, pb[:-1], t)
        assert False
    except ValueError:
        pass


def test_per_class_by_key():
    r = per_class(["x", "y", "x"], ["x", "x", "x"], key=["k1", "k2", "k2"])
    assert r == {"k1": (1, 1), "k2": (1, 2)}


def test_guard_rule_first_then_familiarity():
    vocab = {"a", "b", "c"}
    g = AbsentClassGuard(vocab, 0.9, [GuardRule("registry", lambda t: "firm1" in t, "legal", "coordinator")])
    assert g.check(["a", "b", "c"]) is None
    assert g.check(["a", "b", "firm1"]).route == "legal"
    h = g.check(["a", "z"])
    assert h.reason == "unfamiliar" and abs(h.familiarity - 0.5) < 1e-12
    assert familiarity([], vocab) == 0.0
    try:
        AbsentClassGuard(vocab, 1.0)
        assert False
    except ValueError:
        pass


def test_costs_and_crossover():
    f = cost_per_doc(3600, 25, 3.0, 15.0)
    s = cost_per_doc(1350, 2, 0.20, 0.20)
    assert abs(f - 0.011175) < 1e-9 and 40 < f / s < 42
    a = ServingOption("frontier", f)
    b = ServingOption("ft", s, ownership_monthly=501.0)
    v = crossover(a, b)
    assert 45000 < v < 47000
    assert abs(a.monthly(v) - b.monthly(v)) < 1e-6
    assert crossover(ServingOption("x", 0.1), ServingOption("y", 0.1, 5)) is None
    assert crossover(ServingOption("x", 0.2, 10), ServingOption("y", 0.1)) is None
    assert learning_crossover([100, 200, 400], [0.8, 0.9, 0.95], 0.884) == 200
    assert learning_crossover([100], [0.5], 0.9) is None


def test_training_record_and_risk_and_gate():
    r = TrainingDataRecord(dataset="history-6000", data_owner="Ruth Calloway", label_owner="Anne Kessler")
    assert "purpose" in r.missing() and "signature of data_owner" in r.missing() and not r.ok()
    full = TrainingDataRecord(*["x"] * 11, signed_by=["x"], signed_day=138)
    assert full.ok()
    assert risk_class(False, False).startswith("outside")
    assert risk_class(False, True).startswith("third-party")
    assert risk_class(True, True).startswith("model developed")
    g = SwitchGate(["paired", "validation"])
    assert g.check({"paired": True}) == (False, ["validation"])
    assert g.check({"paired": True, "validation": True}) == (True, [])
