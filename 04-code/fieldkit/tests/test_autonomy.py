"""Tests for fieldkit.autonomy (module version 1.3, Chapter 9)."""
import pytest
from fieldkit.autonomy import (AUTONOMY_VERSION, CLASSES, Step, TreeError, TREE, classify, no_model_share, share,
                               split, walk)


def test_version_and_classes():
    assert AUTONOMY_VERSION == "1.3"
    assert len(CLASSES) == 4


def test_first_yes_decides_and_answers_are_returned():
    s = Step("X1", "look up policy", determined=True, written_rules=True, rule_owner="A")
    assert walk(s) == (0, ("Q1 yes",))
    r = Step("X2", "route", written_rules=True, rule_owner="Head of claims")
    assert walk(r) == (1, ("Q1 no", "Q2 yes"))
    m = Step("X3", "classify loss cause", closed_output=True, check="code table")
    assert walk(m) == (2, ("Q1 no", "Q2 no", "Q3 yes"))
    f = Step("X4", "summarize")
    assert walk(f) == (3, ("Q1 no", "Q2 no", "Q3 no"))


def test_ownerless_rule_refused_then_accepted():
    with pytest.raises(TreeError, match="habits"):
        classify(Step("X5", "finance cage", written_rules=True))
    assert classify(Step("X5", "finance cage", written_rules=True, rule_owner="Finance lead")) == 1


def test_unchecked_closed_output_refused():
    with pytest.raises(TreeError, match="not closed"):
        classify(Step("X6", "doc type", closed_output=True))


def test_model_step_may_not_do_never_operations():
    for op in ("join", "arithmetic", "threshold", "identity"):
        with pytest.raises(TreeError, match="split the step"):
            classify(Step("X7", "read invoice", closed_output=True, check="schema", ops=(op,)))
    assert classify(Step("X8", "sum lines", determined=True, ops=("arithmetic",))) == 0


def test_split_and_shares():
    steps = [Step("A", "a", determined=True), Step("B", "b", written_rules=True, rule_owner="o"),
             Step("C", "c", closed_output=True, check="k"), Step("D", "d")]
    assert list(split(steps).values()) == [1, 1, 1, 1]
    assert share(steps) == 0.25 and no_model_share(steps) == 0.5


def test_tree_is_data_and_extensible():
    extra = TREE + (dict(key="Q4", ask="Is it read-only?", attr="determined", yes=0),)
    assert classify(Step("E", "e"), extra) == 3
