import _path  # noqa: F401
from inventories import pennant, caldwell, greystone

def test_pennant_day21_and_day24():
    assert round(pennant(denied=False).point_tax(), 2) == 2.10
    assert round(pennant().point_tax(), 2) == 3.00

def test_all_customers_lint_clean_after_inventory():
    for m in (pennant, caldwell, greystone):
        assert m().lint() == []

def test_unpriced_denial_fails_loudly():
    import pytest
    inv = pennant(denied=False)
    for l in inv.lines:
        if l.lid == "P-A2": l.alt = []
    with pytest.raises(ValueError):
        inv.deny("P-A2", "architect", 23)
    assert any("P-A2" in x for x in inv.lint())
