"""fieldkit v4.5 (Chapter 37): gate tracker and accountable executive's pack."""
from fieldkit.gates import (Criterion, Measurement, GateRecord, Tracker, Artifact, pack, ResidualRisk,
                            residual_lint, wilson, PACK)

C = Criterion("S-1", "field accuracy", 0.80, per="document class", owner="Anne Kessler")


def rec(ms, signer="Anne Kessler", day=157, conditions=()):
    return GateRecord("Shadow Exit", entry=[("Build Complete passed", "BC")], criteria=[C], measurements=ms,
                      signer=signer, decided=day, conditions=list(conditions))


def test_aggregate_pass_hides_a_failing_class():
    ms = [Measurement("S-1", 1689, 2010), Measurement("S-1", 372, 500, scope="fax")]
    r = rec(ms)
    assert r.status(per_class=False) == "passed"
    assert r.status(per_class=True) == "blocked"
    assert [l.verdict for l in r.evaluate()] == ["met", "below"]


def test_interval_spanning_bar_is_not_shown():
    r = rec([Measurement("S-1", 1689, 2010), Measurement("S-1", 389, 490, scope="mail")])
    assert r.evaluate()[1].verdict == "not shown"


def test_non_customer_evidence_is_refused():
    r = rec([Measurement("S-1", 93, 100, kind="model confidence")])
    assert r.evaluate()[0].verdict == "refused" and r.status() == "blocked"


def test_later_gate_is_held_until_earlier_passes():
    t = Tracker("Caldwell")
    t.add(GateRecord("Architecture Review", entry=[("x", "y")], signer="Priya Natarajan", decided=67))
    t.add(GateRecord("Model-Risk Approval", entry=[("x", "y")], signer="Catherine Doyle", decided=153))
    assert t.held_back() == ["Model-Risk Approval"]


def test_condition_needs_person_and_day():
    r = rec([Measurement("S-1", 1689, 2010)], conditions=[("fax always-review", "the claims team", None)])
    assert r.status().startswith("blocked: condition")


def test_pack_downgrades_unreferenced_artifacts_and_digest_is_stable():
    arts = [Artifact("decision record", "OD-4", "Catherine Doyle", 132, "present"),
            Artifact("lineage", "", "", None, "present")]
    p, q = pack(arts), pack(arts)
    assert p["digest"] == q["digest"] and len(p["rows"]) == len(PACK)
    assert p["counts"] == {"present": 1, "partial": 1, "missing": 6} and not p["complete"]


def test_residual_risk_needs_owner_day_review_and_control():
    assert len(residual_lint([ResidualRisk("fax below bar")])) == 3
    assert residual_lint([ResidualRisk("x", "Anne Kessler", 157, 190, "always-review")]) == []
    lo, hi = wilson(372, 500)
    assert hi < 0.80 < wilson(389, 490)[1]


def test_exclusion_and_written_acceptance_need_a_person_and_a_day():
    ms = [Measurement("S-1", 1689, 2010), Measurement("S-1", 372, 500, scope="fax"),
          Measurement("S-1", 389, 490, scope="mail")]
    r = rec(ms)
    r.excluded = [("S-1", "fax", "Anne Kessler", 157)]
    r.accepted = [("S-1", "mail", "claims leadership", 157)]
    assert r.status() == "blocked"
    r.accepted = [("S-1", "mail", "Anne Kessler", 157)]
    assert r.status() == "passed" and [l.verdict for l in r.evaluate()] == ["met", "excluded", "accepted"]
