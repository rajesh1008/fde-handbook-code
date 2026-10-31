import subprocess, sys, pathlib
import _paths  # noqa: F401
from fieldkit.security import evidence_check, link_check, review, reconcile_flows
from world import ANSWERS, EVIDENCE, SCOPE, FLOWS, OBSERVED, THREATS, findings, stacks, SETTLED

HERE = pathlib.Path(__file__).parent


def test_counts_match_canon():
    assert len(ANSWERS) == 41 and sum(a.design_changing for a in ANSWERS) == 23
    assert len(SETTLED) == 23 and sum(d <= 40 for d in SETTLED) == 11


def test_failure_injection_link_check_passes_everything():
    assert all(v.passed for v in link_check(ANSWERS))
    assert sum(v.passed for v in evidence_check(ANSWERS, EVIDENCE, 100, SCOPE)) == 34


def test_review_result():
    r = review(evidence_check(ANSWERS, EVIDENCE, 103, SCOPE), findings())
    assert (r["passed"], r["findings"]) == (29, 12)


def test_flows_and_threats():
    r = reconcile_flows(FLOWS, OBSERVED)
    assert len(r["undeclared"]) == 1 and r["unseen"] == ["D12"]
    assert THREATS.stride_only() == 17 and len(THREATS.threats) == 22


def test_greystone_blocks_and_scripts_run():
    s = {x.customer: x for x in stacks()}
    assert "security" in s["Greystone"].blocking() and not s["Caldwell"].lint()
    for name in ("pack_check", "review", "remediation"):
        subprocess.run([sys.executable, str(HERE / f"{name}.py")], check=True, capture_output=True)


def test_answer_cards_v2_pass_on_pilot_day():
    import answer_cards as ac
    from fieldkit.security import evidence_check
    v1 = evidence_check([ac.V1[q] for q in ac.IDS], ac.REG, 100, ac.SCOPE)
    v2 = evidence_check([ac.V2[q] for q in ac.IDS], ac.REG, 131, ac.SCOPE)
    assert [x.passed for x in v2] == [True, True, True]
    assert not all(x.passed for x in v1)
