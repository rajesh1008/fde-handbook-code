import _paths  # noqa: F401
from linter import lint, RULES
from world import STORIES, INJECTED, AUDIT
from catalog import CATALOG


def test_catalog_has_fifteen_pairs():
    assert [p.rule for p in CATALOG] == [f"R{i:02d}" for i in range(1, 16)]


def test_v1_flags_every_story():
    for m in STORIES:
        assert RULES[int(m["rule"][1:]) - 1](m, True)[0] == "FLAG", m["id"]


def test_failure_injection_passes_v0_fails_v1():
    r = RULES[1]
    assert r(INJECTED, False)[0] == "PASS"
    assert r(INJECTED, True)[0] == "FLAG"


def test_pennant_day28_sponsor_only():
    assert RULES[1](STORIES[1], False)[0] == "PASS"
    assert "4 of 5 roles" in RULES[1](STORIES[1], True)[1]


def test_aggregate_rule_uses_interval():
    s, d = RULES[6](STORIES[6])
    assert s == "FLAG" and "84.0%" in d and "74.4%" in d


def test_audit_no_open_flags():
    for m in AUDIT.values():
        assert all(s != "FLAG" for _, s, _ in lint(m)), m["id"]
    st = {r: s for r, s, _ in lint(AUDIT["Pennant"])}
    assert st["R02"] == "WARN" and st["R03"] == "DEV"
