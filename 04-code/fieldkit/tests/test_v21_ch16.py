"""fieldkit v2.1 (Chapter 16): representativeness, de-identification, shadow tap, stratified sampling."""
import random
from fieldkit.synthetic import psi, coverage, classifier_auc, RepresentativenessReport, GapLine
from fieldkit.deid import scrub_patterns, known_value_scan, scrub_known, k_anonymity, linkage_attack, shift_days
from fieldkit.shadow import ShadowTap, make_canary, scan_stores
from fieldkit.sampling import allocate, Manifest


def test_psi_zero_for_same_and_large_for_disjoint():
    assert psi(["a", "b"] * 50, ["a", "b"] * 50) < 1e-9
    assert psi(["a"] * 100, ["b"] * 100) > 0.25


def test_coverage_flags_missing_exception():
    rows = coverage([[]] * 100, [["faded scan"]] * 20 + [[]] * 80)
    assert rows[0][3] == "MISSING"


def test_classifier_separates_different_sets_and_not_same():
    rng = random.Random(1)
    a = [{"x": rng.choice("ab")} for _ in range(200)]
    b = [{"x": rng.choice("ab")} for _ in range(200)]
    c = [{"x": "c"} for _ in range(200)]
    assert classifier_auc(a, b) < 0.65
    assert classifier_auc(a, c) > 0.95


def test_report_and_gap_line_stop_rule():
    r = RepresentativenessReport([{"k": "a"}] * 50, [{"k": "b"}] * 50, [[]] * 50, [["x"]] * 50).run()
    assert r.verdict.startswith("NOT")
    g = GapLine({"all": (0.94, 0.71, 2000), "ok": (0.80, 0.78, 500)}, verdict="REPRESENTATIVE: regression use")
    uses = {row[0]: row[5] for row in g.rows()}
    assert uses == {"all": "plumbing only", "ok": "regression ok"}


def test_known_value_scan_catches_ocr_bent_policy_and_names():
    text = "INS: CALDWELL MUTUAL NP1b5562\nThanks, Maria"
    hits = known_value_scan(scrub_patterns(text), {"policy": "HP165562", "claimant_name": "Maria Morales"})
    assert {h[0] for h in hits} == {"policy", "claimant_name"}
    assert known_value_scan(scrub_known(text, {"policy": "HP165562", "claimant_name": "Maria Morales"}),
                            {"policy": "HP165562", "claimant_name": "Maria Morales"}) == []


def test_k_anonymity_and_linkage():
    rel = [{"d": "1", "t": "x"}, {"d": "1", "t": "x"}, {"d": "2", "t": "y"}]
    assert k_anonymity(rel, ["d", "t"])[0] == 1
    pub = [{"d": "2", "t": "y", "identity": "P"}]
    assert linkage_attack(rel, pub, ["d", "t"]) == [(2, "P")]
    assert shift_days("c1", "s") == shift_days("c1", "s")


def test_shadow_canary_scan(tmp_path):
    c = make_canary(random.Random(2))
    for debug, expect in ((True, True), (False, False)):
        d = tmp_path / str(debug)
        tap = ShadowTap("k", str(d), debug_log=debug)
        tap.observe("D1", f"claimant {c['claimant_name']}", {"a": 1}, {"a": 1}, {"f": "x"})
        assert bool(scan_stores(str(d), [c["claimant_name"]])) is expect


def test_allocate_floor_total_and_manifest():
    plan = allocate({"big": 9000, "small": 100}, 300, floor=20)
    assert sum(a for a, _ in plan.values()) == 300 and plan["small"][0] == 20
    m = Manifest("m", "a", "b", "loc", "never")
    m.add("f1", "s", "text")
    assert m.verify({"f1": "text"}) == [] and m.verify({"f1": "text "}) == ["f1"]
