"""fieldkit v4.3 (Chapter 35): data map generation, privacy lint, PII scan, erasure trace."""
from fieldkit.privacy import Hop, generate, lint, digest, pii_scan, erasure_trace, minimum_necessary, diff

CFG = {"components": [
    {"name": "drafting", "holder": "Northlight", "data": ["PHI"], "location": "gh-tenant", "basis": "BAA",
     "stores": [{"name": "app-log", "kind": "log", "body": False, "retention_days": 30},
                {"name": "provider-store", "holder": "Provider", "kind": "log", "retention_days": 30}]}]}


def test_generate_emits_component_and_store_hops():
    hops = generate(CFG)
    assert [h.name for h in hops] == ["drafting", "app-log", "provider-store"]
    assert hops[1].data == ("META",) and hops[0].retention_days == 0


def test_hipaa_flags_store_without_baa_and_unsigned_log():
    rules = sorted(f.rule for f in lint(generate(CFG), {"HIPAA"}, owner="Greystone"))
    assert rules == ["H1", "H2"]


def test_gdpr_transfer_and_erasure():
    h = Hop("audit", "Northlight", ("EU-PI",), "us", 365, "DPA", "store", deletable=False, region_ok=False)
    assert sorted(f.rule for f in lint([h], {"GDPR"}, owner="Pennant")) == ["G1", "G3"]
    assert erasure_trace([h])[0][1] == "cannot erase"


def test_digest_stable_and_sensitive():
    a, b = generate(CFG), generate(CFG)
    assert digest(a) == digest(b)
    b[2].retention_days = 0
    assert digest(a) != digest(b)
    assert [h.name for h in diff(a[:1], a)] == ["app-log", "provider-store"]


def test_scan_known_values_catch_names_patterns_miss():
    rep = pii_scan(["referral for Ellen Thorpe re knee pain", "MRN 1234567 follow-up", "nothing here"],
                   known=[{"p0_name": "Ellen Thorpe"}])
    assert rep.hit_entries == 2 and rep.pattern_only == 1
    assert "Ellen" not in "".join(rep.examples)


def test_minimum_necessary():
    extra, share = minimum_necessary(["a", "b", "c", "d"], ["a", "b"])
    assert extra == ["c", "d"] and share == 0.5
