"""fieldkit v3.6: pyramid runner (Chapter 29)."""
from fieldkit.pyramid import (Layer, Pyramid, MergeGate, Metric, Mutant, PASS, FAIL, INCONCLUSIVE, SKIPPED,
                              select_layers, classify_path, paired_slices, slice_verdict, binom_tail, control_run,
                              independence, EvidenceRecord, chain, verify, trace_matrix, caught_at)

RULES = [("prompts/", "prompt"), ("rules/", "rule"), ("docs/", "docs"), ("requirements", "dependency")]
LAYERS = [Layer(1, "unit", "", "", 30, 0), Layer(2, "component", "", "", 900, 20)]


def test_unknown_path_runs_code_layers():
    assert classify_path("src/x.py", RULES) == "code"
    assert select_layers(["docs/a.md"], RULES) == (["docs"], [])
    assert select_layers(["prompts/p9.txt"], RULES)[1] == [1, 2, 3]
    assert 4 in select_layers(["docs/a.md"], RULES, release=True)[1]


def test_binom_and_slice_verdict():
    assert abs(binom_tail(0, 10) - 1) < 1e-12 and abs(binom_tail(10, 10) - 2 ** -10) < 1e-15
    assert slice_verdict(100, 5, 5)[0] == PASS
    assert slice_verdict(100, 1, 12)[0] == FAIL
    assert slice_verdict(20, 0, 2)[0] == INCONCLUSIVE


def test_paired_slices_counts_and_same_keys():
    b = {("d1", "f"): True, ("d2", "f"): False}; a = {("d1", "f"): False, ("d2", "f"): True}
    s = paired_slices(b, a, lambda k: k[1])["f"]
    assert (s["gains"], s["losses"], s["n"]) == (1, 1, 2)
    try:
        paired_slices(b, {}, lambda k: k)
        assert False
    except ValueError:
        pass


def test_gate_blocks_fail_holds_inconclusive_and_fail_cannot_be_signed():
    p = Pyramid(LAYERS)
    p.add(1, "rules", lambda s: (PASS, "", 1, 0, {}))
    p.add(2, "slice", lambda s: (s, "x", 1, 1, {}))
    assert MergeGate("Anne").decide(p.run(FAIL))["decision"] == "block"
    assert MergeGate("Anne", ["slice"]).decide(p.run(FAIL))["decision"] == "block"
    assert MergeGate("Anne").decide(p.run(INCONCLUSIVE))["decision"] == "hold"
    assert MergeGate("Anne", ["slice"]).decide(p.run(INCONCLUSIVE))["decision"] == "merge"


def test_stop_on_fail_skips_later_layers():
    p = Pyramid(LAYERS).add(1, "a", lambda s: (FAIL, "", 0, 0, {})).add(2, "b", lambda s: (PASS, "", 0, 0, {}))
    r = p.run(None)
    assert r[1].verdict == SKIPPED and caught_at(r) == 1


def test_metric_regression_direction():
    assert Metric("acc", 0.9, 0.89).verdict() == FAIL
    assert Metric("cost", 1.0, 1.05, higher_is_better=False, tolerance=0.1).verdict() == PASS


def test_control_run_late_and_escaped():
    p = Pyramid(LAYERS)
    p.add(1, "l1", lambda s: (FAIL if s == "m1" else PASS, "", 0, 0, {}))
    p.add(2, "l2", lambda s: (FAIL if s in ("m1", "m2") else PASS, "", 0, 0, {}))
    ms = [Mutant("m1", "", 1, lambda s: "m1"), Mutant("m2", "", 1, lambda s: "m2"), Mutant("m3", "", 2, lambda s: "m3")]
    st = [r["status"] for r in control_run(p, "base", ms)]
    assert st == ["caught", "late", "escaped"]


def test_independence_unique_and_phi():
    r = independence({"a": {1, 2}, "b": {2, 3}, "c": {1, 2}}, [1, 2, 3, 4])
    assert r["rows"]["b"]["unique"] == 1 and r["union"] == 3 and r["missed"] == 1
    assert abs(r["phi"][("a", "c")] - 1.0) < 1e-9


def test_evidence_chain_detects_tamper():
    recs = [EvidenceRecord("R1", "rules", 1, "run1", "abc", PASS, {"n": 3}),
            EvidenceRecord("R2", "slice", 2, "run1", "abc", PASS, {})]
    chain(recs)
    assert verify(recs) is None
    recs[0].verdict = FAIL
    assert verify(recs) == 1
    tm = trace_matrix({"R1": "", "R3": ""}, recs)
    assert tm["R1"]["covered"] and not tm["R3"]["covered"]
