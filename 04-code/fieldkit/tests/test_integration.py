import pytest
from fieldkit.integration import Inventory, Line

def inv():
    i = Inventory("T", (90, 100, 120), day=1)
    i.add(Line("A", "formats", "edi", "map", 40, 50, 70, "reconstructed from supplied artifact", "timed spike"),
          Line("B", "access", "api", "pull", 8, 10, 14, "vendor position", "vendor docs", owner="architect",
               alt=[Line("B1", "access", "csv", "nightly csv", 40, 50, 70, "direct customer fact", "csv export")]))
    return i

def test_point_and_exposure():
    i = inv(); assert i.total() == 60 and abs(i.point_tax() - 0.6) < 1e-9 and i.exposure() == 40

def test_deny_replaces_line():
    d = inv().deny("B", "architect", 3); assert d.total() == 100 and not d.unconfirmed()

def test_lint_refuses_unpriced_material_assumption():
    i = Inventory("T", (1, 1, 1)).add(Line("X", "gateways", "gw", "g", 5, 10, 20, "vendor position", "docs"))
    assert len(i.lint()) == 2  # no owner, no priced alternative
    with pytest.raises(ValueError): i.deny("X", "architect", 2)

def test_simulation_is_seeded_and_ordered():
    a, b = inv().simulate(n=2000), inv().simulate(n=2000)
    assert a.tax.p50 == b.tax.p50 and a.hours.p10 <= a.hours.p50 <= a.hours.p90

def test_bad_line_refused():
    with pytest.raises(ValueError): Inventory("T", (1, 1, 1)).add(Line("Z", "formats", "s", "w", 5, 3, 9, "direct customer fact", ""))
