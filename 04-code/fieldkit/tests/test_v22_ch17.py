"""Tests for fieldkit.environment (Chapter 17, fieldkit v2.2)."""
from fieldkit.environment import (AuditLog, Answer, Delegation, EgressPolicy, EgressRule, EnvironmentDoc, KeyRecord,
                                  RightsGate, choose_tenancy, find_secrets, key_findings, tenancy_gaps)


def test_tenancy_choice_and_gaps():
    assert choose_tenancy(["keys"]) == "vendor-dedicated"
    assert choose_tenancy(["network", "identity", "keys", "logs"]) == "customer-account"
    assert choose_tenancy(["change", "incident", "network"]) == "customer-operated"
    assert tenancy_gaps("vendor-shared", ["logs", "keys"]) == ["keys", "logs"]


def test_audit_log_chain_detects_edit():
    log = AuditLog("Caldwell")
    for i in range(5):
        log.append(t=i, kind="egress", action="DENY")
    assert log.verify() == []
    log.records[2]["action"] = "ALLOW"
    assert log.verify() == [3]


def test_egress_default_deny_and_logged():
    log = AuditLog("Caldwell")
    p = EgressPolicy("nl-shadow", [EgressRule("gateway", "gateway.preprod.caldwell.internal", owner="P. Natarajan",
                                              reason="model calls")], log)
    assert p.check("gateway.preprod.caldwell.internal")
    assert not p.check("api.model-provider.example")
    assert [r["action"] for r in log.records] == ["ALLOW", "DENY"]
    assert log.query(action="DENY")[0]["rule"] == "default-deny"


def test_egress_lint():
    p = EgressPolicy("x", [EgressRule("all", "*"), EgressRule("ok", "a.b.c", owner="o", reason="r")])
    out = p.lint()
    assert "rule all: no customer owner" in out and any("wildcard destination" in o for o in out)
    assert not [o for o in out if o.startswith("rule ok")]


def test_rights_gate_rechecks_and_expires():
    log = AuditLog("Caldwell")
    gate = RightsGate(lambda u, r, t: r != "CLM-2", log)
    d = Delegation("twhitfield", "nl-assist", "cross-unit search", ("claims:read",), 600, 615)
    rel, held = gate.release(d, ["CLM-1", "CLM-2"], 605)
    assert rel == ["CLM-1"] and held == [("CLM-2", "user may not read")]
    rel, held = gate.release(d, ["CLM-1"], 620)
    assert rel == [] and held[0][1] == "delegation expired"
    assert len(log.query(kind="rights-recheck")) == 2


def test_find_secrets_ignores_references():
    text = '"GATEWAY_KEY": "nlgw_live_8f2c41d09a7be3356c1f"\n"valueFrom": "arn:aws:secretsmanager:us-east-1:1:secret:gw"'
    assert find_secrets(text, "task.json") == [("task.json", 1, "literal key or token")]


def test_key_findings():
    keys = [KeyRecord("data key", "Caldwell", "Caldwell", "KMS", 365, "runner"),
            KeyRecord("trace token", "Northlight", "Northlight", "env var", None, "tracing")]
    out = key_findings(keys, "Caldwell")
    assert len(out) == 3 and all(o.startswith("trace token") for o in out)


def test_environment_doc_lint():
    good = [Answer(q, p, "in us-east-1, readers: two named, 90 days", "arn:aws:iam::111122223333:role/x", "Caldwell")
            for q in ("where", "identity", "logs") for p in ("production", "pre-production")]
    assert EnvironmentDoc("Caldwell", "Northlight", good).lint() == []
    bad = EnvironmentDoc("Caldwell", "Northlight", [Answer("logs", "production", "provider retention",
                                                           "northlight-observability", "Northlight")])
    out = bad.lint()
    assert "where / production: not answered" in out
    assert "logs / production: evidence lives with the vendor" in out
    assert "logs / production: no named readers and retention" in out
