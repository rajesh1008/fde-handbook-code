"""fieldkit.scoping (book layer v1.2, Chapter 8): the behaviors the chapter depends on."""
from fieldkit.scoping import (Claim, Criterion, DocType, Evidence, Exclusion, OpenDecision, ScopeDoc, Source,
                              RANK)


def crit(key, scorer="Anne Kessler", threshold=">= 98%", metric="fields correct", method="suite: field_score"):
    return Criterion(key, "Fields sent without review are right", metric, scorer, "gold set", 500,
                     "fields sent without review", threshold, method, ("review share",))


def doc(criteria=(), claims=(), lineage=None, register=()):
    return ScopeDoc("Caldwell Mutual", 28, "v1.0", [DocType("T1", "first notice", ("K1",), 6000)],
                    {"K1": "classify"}, ["coverage"], list(criteria),
                    [Exclusion("attorney letters", "legal deadlines", "legal mail coordinator", 230)],
                    list(register), list(claims), lineage or {})


def test_criterion_without_measurement_or_person_is_not_exported():
    d = doc([crit("C-01"), crit("C-02", metric="", method=""), crit("C-03", scorer="claims operations")])
    codes = {(k, c) for k, c, _ in d.lint()}
    assert ("C-02", "NO MEASUREMENT") in codes and ("C-03", "NO SCORER") in codes
    assert [c["key"] for c in d.suite_config()] == ["C-01"]


def test_fact_needs_a_person_and_number_needs_basis():
    c = Claim("Z", "Intake takes 16 minutes a document", "F", Source("Caldwell Mutual", "customer", "x", 1))
    codes = [code for code, _ in doc().claim_problems(c)]
    assert "FACT WITHOUT A PERSON" in codes and "NUMBER WITHOUT BASIS" in codes


def test_rise_without_evidence_is_flagged_and_with_evidence_is_not():
    origin = Claim("G-0", "Fax receipt time starts the clock", "V", Source("Northlight FDE", "vendor", "bank", 12))
    bare = Claim("G-a", "Fax receipt time starts the clock", "F", Source("Michael Hart", "customer", "draft", 18),
                 derived_from="G-0")
    assert any(c == "UPGRADED BY REPETITION" for _, c, _ in doc(claims=[bare], lineage={"G-0": origin}).lint())
    ok = Claim("G-a", "Fax receipt time starts the clock", "F", Source("Michael Hart", "customer", "draft", 18),
               derived_from="G-0", evidence=Evidence("Michael Hart", 18, "scope session", "yes, the fax time"))
    assert not any(c == "UPGRADED BY REPETITION" for _, c, _ in doc(claims=[ok], lineage={"G-0": origin}).lint())
    assert RANK["F"] > RANK["R"] > RANK["V"] == RANK["P"] > RANK["D"]


def test_open_decision_needs_owner_and_day():
    od = OpenDecision("OD-9", "Who sets the threshold?", "claims leadership", 20, None, "")
    codes = [c for c, _ in od.problems()]
    assert codes == ["NO OWNER", "NO DUE DAY", "NO IMPACT"]


def test_coverage_counts_in_scope_plus_excluded():
    assert doc().coverage() == (6000, 6230)
