"""Tests for the Chapter 4 lab. Run: python -m pytest -q test_ch04.py"""
import pytest
from deployment import Checklist, Proof, is_person
from checklists import demo_as_sold, caldwell, caldwell_projected, greystone_sales_demo, REQUIRED
from promise_rewrite import GRAHAM, REWRITTEN, lint, Claim
from oversight import simulate, profile, SYSTEMS, wilson_lower


def test_twenty_five_proofs_five_per_dimension():
    assert len(REQUIRED) == 25
    c = caldwell(10)
    assert {d: sum(p.dimension == d for p in c.proofs.values()) for d in
            ("capability", "workflow", "controls", "ownership", "reconstructability")} == dict.fromkeys(
        ("capability", "workflow", "controls", "ownership", "reconstructability"), 5)


def test_demo_as_sold_is_demo_only():
    v = demo_as_sold().assess(2)
    assert v.label == "DEMO ONLY" and v.gated == 0


def test_no_owner_fools_naive_but_not_gated():
    good, bad = caldwell_projected().assess(140), caldwell_projected(no_owner=True).assess(140)
    assert good.label == "READY"
    assert bad.naive == good.naive and bad.naive >= 0.8   # the naive score cannot see it
    assert bad.label == "NOT READY" and len(bad.blocking) == 3


def test_owner_without_authority_blocks():
    v = greystone_sales_demo().assess(0)
    assert any("without authority" in b for b in v.blocking)
    assert any("synthetic" in b for b in v.blocking)


def test_is_person():
    assert is_person("Anne Kessler")
    for bad in ("Claims Operations", "TBD", "Model Risk Committee", "", "Northlight FDE"):
        assert not is_person(bad)


def test_vendor_measured_capability_discounted():
    c = Checklist("x", customer_people=("Anne Kessler",))
    c.add(Proof("k", "capability", "r", status="held", measured_by="Graham Lowell", on_what="demo set"))
    assert c.proofs["k"].counted(c.customer_people) == "missing"


def test_promises_rejected_rewrites_pass():
    assert all(lint(c) for c in GRAHAM)
    assert not any(lint(c) for c in REWRITTEN)
    assert lint(Claim("decide later", "decision required", owner="the steering group"))


def test_oversight_same_accuracy_different_review():
    a, b = simulate(**SYSTEMS["pipeline A"]), simulate(**SYSTEMS["pipeline B"])
    pa, pb = profile(a, 0.95), profile(b, 0.95)
    assert pa["qualifies"] and pb["qualifies"]
    assert pb["review_share"] - pa["review_share"] > 0.2
    assert profile(a, 0.99)["threshold"] is None


def test_wilson():
    assert wilson_lower(0, 0) == 0
    assert 0.9 < wilson_lower(98, 100) < 0.98
