"""fieldkit v5.4 (Chapter 47, Section 47.8): engagement linter and playbook registry.

What it protects: recurrence counted by shape, versioned playbooks matched to a customer estate before work
starts, and rule-based linters for playbooks (P1 to P5) and engagement manifests (E1 to E8).
"""
import pytest

from fieldkit.playbooks import (
    FieldReport, Playbook, Registry, Step, check_preconditions, classify, classify_by_name, continuity,
    evidence_score, implied_capabilities, lint_engagement, lint_playbook, loop_metrics, rank_reports, recurrence,
)


def pb(pid="PB-1", version="1.0", gateway=("apim",)):
    """A clean two-step playbook: S2 needs the customer's model gateway to be one of `gateway`."""
    return Playbook(pid, version, "claims intake", "N01", "platform team", "claims", [
        Step("S1", "Load the sample documents", owner="FDE", test="sample loads"),
        Step("S2", "Route model calls through the gateway", owner="FDE", test="gateway smoke test",
             requires={"gateway": set(gateway)}),
    ])


def registry():
    r = Registry()
    r.add(pb())
    return r


def manifest(**kw):
    m = dict(id="N05", playbook="PB-1@1.0", adapter="fieldkit.gateway", eval_suite="evals/claims",
             gold_owner="anne@customer.example", phase="handed over", customer_domain="customer.example",
             alert_routes=["oncall@customer.example"], deviations=[], fieldkit_layer=54, needs_layer=54,
             secrets_owner="customer")
    m.update(kw)
    return m


def test_classify_by_shape_not_name():
    assert classify(20, 17) == "bespoke" and classify_by_name(20) == "platform"
    assert classify(20, 3) == "platform" and classify(4, 2) == "playbook"


def test_recurrence_counts_engagements_once():
    rows = recurrence([("N01", "connector", "rest", 5), ("N01", "connector", "rest", 3),
                       ("N02", "connector", "sftp", 7)])
    assert rows[0]["n"] == 2 and rows[0]["variants"] == 2 and rows[0]["hours"] == 15


def test_form_lint_passes_undeclared_capability_probe_catches_it():
    b = Playbook("PB-2", "1.0", "referral", "N03", "platform team", "referral", [
        Step("S1", "Call the model through the gateway", owner="FDE", test="smoke test")])
    assert lint_playbook(b, probe=False) == []
    assert [f[0] for f in lint_playbook(b)] == ["P5"]


def test_lint_form_rules():
    b = Playbook("PB-3", "v1", "draft", "N04", "", "any", [Step("S1", "Write the runbook")], maturity="live")
    rules = sorted({f[0] for f in lint_playbook(b)})
    assert rules == ["P1", "P2", "P3", "P4"]


def test_implied_capabilities_word_boundaries():
    assert implied_capabilities("Store the key in the vault behind SSO") == ["sso", "vault"]
    assert implied_capabilities("Vaulted ceilings and a gatewayless lobby") == []


def test_preconditions_and_match():
    assert check_preconditions(pb(), dict(gateway="none")) == [("S2", "gateway", ["apim"], "none")]
    r = registry()
    assert r.match(dict(gateway="apim"), "claims") == [("PB-1@1.0", "ready", [])]
    assert r.match(dict(gateway="none"), "claims")[0][1] == "blocked"


def test_registry_refuses_failing_playbook_and_tracks_versions():
    r = Registry()
    with pytest.raises(ValueError):
        r.add(Playbook("PB-9", "1.0", "x", "N01", "", "any", [Step("S1", "do it", owner="FDE", test="t")]))
    r.add(pb("PB-9", "1.9"))
    r.add(pb("PB-9", "1.10"))
    assert r.latest("PB-9").version == "1.10"
    r.deprecate("PB-9@1.10", reason="gateway step wrong", migrate_by=6)
    assert r.latest("PB-9").version == "1.9"
    r.adopt("N05", "PB-9@1.9")
    assert r.on("PB-9@1.9") == ["N05"]


def test_engagement_lint_clean_and_each_rule():
    r = registry()
    assert lint_engagement(manifest(), r, month=5) == []
    cases = {
        "E1": dict(playbook="PB-404@1.0"),
        "E3": dict(adapter="vendor-sdk"),
        "E4": dict(gold_owner=""),
        "E5": dict(alert_routes=["oncall@vendor.example"]),
        "E6": dict(deviations=[dict(what="adapter", reason="", owner="", review_by=9)]),
        "E7": dict(fieldkit_layer=53),
        "E8": dict(secrets_owner="vendor"),
    }
    for rule, change in cases.items():
        assert rule in [f[0] for f in lint_engagement(manifest(**change), r, month=5)], rule
    r.deprecate("PB-1@1.0", reason="replaced", migrate_by=4)
    assert [f[0] for f in lint_engagement(manifest(), r, month=5)] == ["E2"]


def test_registered_deviation_suppresses_e1_and_e3():
    r = registry()
    devs = [dict(what="playbook", reason="first of its kind", owner="Laura Finch", review_by=6),
            dict(what="adapter", reason="customer gateway not yet live", owner="Laura Finch", review_by=6)]
    m = manifest(playbook=None, adapter="direct", deviations=devs)
    assert lint_engagement(m, r, month=5) == []
    assert {f[0] for f in lint_engagement(m, r, month=7)} == {"E6"}


def test_evidence_beats_votes_and_needs_artifact():
    loud = FieldReport("FR-1", "custom dashboard", "N02", ["N02"], [30], votes=9, acv_usd=900_000)
    quiet = FieldReport("FR-2", "document quality gate", "N03", ["N03", "N05", "N08", "N11"], [30, 40, 40, 60],
                        votes=1, artifact="04-code/ch47/quality_gate.py")
    assert evidence_score(loud) == 0 and evidence_score(quiet) == 160
    assert rank_reports([loud, quiet])[0].rid == "FR-2"
    assert rank_reports([loud, quiet], by="votes")[0].rid == "FR-1"


def test_loop_metrics_and_continuity():
    m = loop_metrics([
        dict(first_month=0, shipped_month=10, adopted=["N01"], hours_before=50, hours_after=10),
        dict(first_month=2, shipped_month=16, adopted=["N01", "N02"], hours_before=30, hours_after=4),
    ])
    assert m == dict(features=2, median_lead_months=12.0, adopting_engagements=2, hours_saved=92)
    c = continuity([("Caldwell", 13, "Priya", "Sam", 10, 30), ("Caldwell", 16, "Sam", "Ana", 5, 30)])
    assert c["Caldwell"]["changes"] == 2 and len(c["Caldwell"]["bad"]) == 1
